import os, json, pickle, random, asyncio, requests, subprocess, base64, sys
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

GROQ_API_KEY = os.environ['GROQ_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
CHANNEL_NAME = 'SaludMentalReal'

VOCES = ['es-MX-JorgeNeural', 'es-CO-GonzaloNeural', 'es-MX-LibertadNeural']

TEMAS = [
    'como controlar la ansiedad en momentos de crisis',
    'tecnicas de respiracion para calmar el estres inmediatamente',
    'como dormir mejor cuando la mente no para',
    'señales de que estas sufriendo burnout y como recuperarte',
    'como manejar un ataque de panico paso a paso',
    'la depresion no es tristeza lo que nadie te explica',
    'como salir de una adiccion cuando sientes que no puedes',
    'tecnicas para dejar de rumiar pensamientos negativos',
    'como hablar con alguien que esta en depresion',
    'el impacto del telefono en tu salud mental',
    'como poner limites sin sentir culpa',
    'ansiedad social como superarla poco a poco',
    'autoestima baja de donde viene y como mejorarla',
    'como manejar el duelo cuando pierdes a alguien',
    'señales de alerta de que necesitas ayuda psicologica',
    'mindfulness para principiantes en 5 minutos al dia',
    'como dejar de procrastinar cuando la ansiedad te paraliza',
    'el sindrome del impostor que es y como combatirlo',
    'como recuperarse de una ruptura sin destruirte',
    'trauma infantil como reconocerlo en tu vida adulta',
    'como ayudarte a ti mismo cuando nadie mas puede',
    'el poder del ejercicio para la salud mental',
    'como manejar la ira antes de explotar',
    'soledad emocional como enfrentarla de verdad',
    'adiccion a redes sociales como detectarla y salir',
    'como mantener la calma en situaciones de conflicto',
    'pensamientos intrusivos que son y como manejarlos',
    'como construir rutinas que protejan tu salud mental',
    'el rol del sueno en la ansiedad y la depresion',
    'como decirle no a las personas toxicas en tu vida'
]

def send_telegram(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except:
        pass

def run_ffmpeg(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'FFmpeg error: {result.stderr[-500:]}')
    return result.returncode == 0

def get_youtube():
    token_data = base64.b64decode(os.environ['TOKEN_PICKLE_B64'])
    creds = pickle.loads(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds)

def generar_guion(tema):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f'''Eres un experto en contenido viral de salud mental para YouTube en español latino. Crea contenido sobre: {tema}

Responde SOLO con este JSON sin texto adicional:
{{
  "titulo": "titulo VIRAL de maximo 70 caracteres, usa numeros o preguntas impactantes",
  "descripcion": "descripcion SEO de 400 palabras. Empieza con pregunta impactante. Usa emojis. Incluye llamada a suscribirse. Termina con 20 hashtags: #SaludMental #Ansiedad #Depresion #BienestarEmocional #PsicologiaLatina #MenteLibre #SaludMentalReal #Autoestima #Motivacion #Mindfulness #CrecimientoPersonal #PsicologiaPositiva #SuperacionPersonal #VidaSaludable #MenteClara",
  "guion": "guion narrado en español latino de 500 palabras, empatico y conversacional. Gancho impactante en primeras 5 palabras. Sin bullet points.",
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara"],
  "guion_short": "guion de 70 palabras para Short viral. Empieza con dato impactante. Termina con llamada a la accion.",
  "titulo_short": "titulo Short maximo 55 caracteres con 2 emojis"
}}'''
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user','content':prompt}],
        response_format={'type':'json_object'},
        temperature=0.9
    )
    return json.loads(resp.choices[0].message.content, strict=False)

async def generar_audio(texto, archivo, voz):
    import edge_tts
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(archivo)

async def generar_srt(texto, srt_file, voz):
    import edge_tts
    communicate = edge_tts.Communicate(texto, voz)
    words = []
    async for chunk in communicate.stream():
        if chunk['type'] == 'WordBoundary':
            words.append({
                'word': chunk['text'],
                'start': chunk['offset'] / 10000000,
                'end': (chunk['offset'] + chunk['duration']) / 10000000
            })
    if not words:
        print('SRT: no words generated')
        return False
    def fmt(s):
        h, m = int(s//3600), int((s%3600)//60)
        sec, ms = int(s%60), int((s%1)*1000)
        return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'
    grupos, grupo = [], []
    for w in words:
        grupo.append(w)
        if len(grupo) >= 4:
            grupos.append(grupo)
            grupo = []
    if grupo:
        grupos.append(grupo)
    with open(srt_file, 'w', encoding='utf-8') as f:
        for i, g in enumerate(grupos):
            f.write(f"{i+1}\n{fmt(g[0]['start'])} --> {fmt(g[-1]['end'])}\n{' '.join(x['word'] for x in g)}\n\n")
    print(f'SRT generado: {len(grupos)} grupos en {srt_file}')
    return True

def get_audio_duration(audio_file):
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', audio_file],
        capture_output=True, text=True
    )
    try:
        return float(json.loads(result.stdout)['format']['duration'])
    except:
        return 60.0

def get_video_files(carpeta):
    exts = ('.mp4', '.mov', '.avi', '.mkv', '.webm')
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(exts)]
    random.shuffle(archivos)
    return archivos

def get_music_file():
    carpeta = 'assets/music_small'
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith('.mp3')]
    return random.choice(archivos) if archivos else None

def mezclar_audio(voz_mp3, musica, salida, vol=0.10):
    voz_wav = '/tmp/voz_temp.wav'
    run_ffmpeg(['ffmpeg', '-y', '-i', voz_mp3, '-ar', '44100', '-ac', '2', '-f', 'wav', voz_wav])
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', voz_wav, '-i', musica,
        '-filter_complex',
        f'[1:a]volume={vol},aloop=loop=-1:size=2e+09[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[out]',
        '-map', '[out]', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', salida
    ])
    if not ok:
        import shutil
        shutil.copy(voz_mp3, salida)
        print('Mezcla fallida, usando solo voz')

def crear_thumbnail(titulo, archivo):
    img = Image.new('RGB', (1280, 720), color=(10, 25, 55))
    draw = ImageDraw.Draw(img)
    for i in range(0, 1280, 35):
        draw.line([(i, 0), (i, 720)], fill=(15, 35, 70), width=1)
    for i in range(0, 720, 35):
        draw.line([(0, i), (1280, i)], fill=(15, 35, 70), width=1)
    draw.rectangle([0, 0, 8, 720], fill=(0, 200, 255))
    draw.rectangle([1272, 0, 1280, 720], fill=(0, 200, 255))
    draw.rectangle([0, 0, 1280, 8], fill=(0, 200, 255))
    draw.rectangle([0, 712, 1280, 720], fill=(0, 200, 255))
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
    except:
        font_big = ImageFont.load_default()
        font_small = font_big
    palabras = titulo.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea + ' ' + p).strip()
        bbox = draw.textbbox((0,0), test, font=font_big)
        if bbox[2] - bbox[0] < 1150:
            linea = test
        else:
            if linea: lineas.append(linea)
            linea = p
    if linea: lineas.append(linea)
    total_h = len(lineas) * 85
    y = (720 - total_h) // 2 - 30
    for ln in lineas:
        bbox = draw.textbbox((0, 0), ln, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((1280-w)//2+3, y+3), ln, font=font_big, fill=(0,0,0))
        draw.text(((1280-w)//2, y), ln, font=font_big, fill=(255,255,255))
        y += 85
    draw.rectangle([0, 650, 1280, 720], fill=(0, 150, 200))
    canal = '@SaludMentalReal'
    bbox2 = draw.textbbox((0,0), canal, font=font_small)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((1280-w2)//2, 658), canal, font=font_small, fill=(255,255,255))
    img.save(archivo, quality=95)

def agregar_subtitulos(video_in, srt_file, video_out, fontsize=18, margenv=35):
    if not os.path.exists(srt_file):
        print(f'SRT no encontrado: {srt_file}')
        return False
    style = f"FontName=Arial,FontSize={fontsize},PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Bold=1,Alignment=2,MarginV={margenv}"
    srt_escaped = srt_file.replace('\\', '/').replace(':', '\\:')
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', video_in,
        '-vf', f"subtitles='{srt_escaped}':force_style='{style}'",
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', video_out
    ])
    return ok and os.path.exists(video_out) and os.path.getsize(video_out) > 1000

def crear_video_largo(audio_file, srt_file, videos_horizontal, output_file):
    duracion_total = get_audio_duration(audio_file)
    print(f'Duracion: {duracion_total}s')
    dur_por_clip = 10
    clips_necesarios = int(duracion_total / dur_por_clip) + 3
    clips = []
    pool = videos_horizontal * (clips_necesarios // max(len(videos_horizontal), 1) + 2)
    for i in range(clips_necesarios):
        src = pool[i % len(pool)]
        clip = f'/tmp/smr_clip_{i}.mp4'
        ok = run_ffmpeg([
            'ffmpeg', '-y', '-i', src,
            '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1',
            '-t', str(dur_por_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', clip
        ])
        if ok and os.path.exists(clip) and os.path.getsize(clip) > 1000:
            clips.append(clip)
    if not clips:
        print('ERROR: No clips')
        sys.exit(1)
    lista = '/tmp/smr_lista.txt'
    with open(lista, 'w') as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    video_mudo = '/tmp/smr_video_mudo.mp4'
    run_ffmpeg(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_mudo])
    video_subs = '/tmp/smr_subs.mp4'
    ok_subs = agregar_subtitulos(video_mudo, srt_file, video_subs, fontsize=18, margenv=35)
    video_base = video_subs if ok_subs else video_mudo
    print(f'Usando video: {"con subs" if ok_subs else "sin subs"}')
    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base, '-i', audio_file,
        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_file
    ])

def crear_short(audio_file, srt_file, videos_vertical, output_file):
    duracion = get_audio_duration(audio_file)
    src = random.choice(videos_vertical)
    video_mudo = '/tmp/smr_short_mudo.mp4'
    run_ffmpeg([
        'ffmpeg', '-y', '-i', src,
        '-vf', 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2,setsar=1',
        '-t', str(int(duracion)+3), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', video_mudo
    ])
    video_subs = '/tmp/smr_short_subs.mp4'
    ok_subs = agregar_subtitulos(video_mudo, srt_file, video_subs, fontsize=16, margenv=50)
    video_base = video_subs if ok_subs else video_mudo
    print(f'Short usando: {"con subs" if ok_subs else "sin subs"}')
    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base, '-i', audio_file,
        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_file
    ])

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False):
    if not os.path.exists(video_file):
        print(f'ERROR: {video_file} no existe')
        sys.exit(1)
    if is_short and '#Shorts' not in titulo:
        titulo = titulo + ' #Shorts'
    body = {
        'snippet': {
            'title': titulo[:100],
            'description': descripcion,
            'tags': tags,
            'categoryId': '26',
            'defaultLanguage': 'es',
            'defaultAudioLanguage': 'es'
        },
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
    }
    media = MediaFileUpload(video_file, mimetype='video/mp4', resumable=True, chunksize=1024*1024*5)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = None
    while response is None:
        _, response = req.next_chunk()
    video_id = response['id']
    if thumbnail:
        try:
            youtube.thumbnails().set(videoId=video_id,
                media_body=MediaFileUpload(thumbnail, mimetype='image/jpeg')).execute()
        except:
            pass
    return video_id

def main():
    send_telegram('🧠 <b>SaludMentalReal</b> — Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)
    videos_h = get_video_files('assets/videos_h_small')
    videos_v = get_video_files('assets/videos_v_small')
    musica = get_music_file()
    voz = random.choice(VOCES)
    print(f'Videos H: {len(videos_h)} | V: {len(videos_v)} | Voz: {voz}')
    tema = random.choice(TEMAS)
    datos = generar_guion(tema)
    titulo = datos['titulo']
    descripcion = datos['descripcion']
    guion = datos['guion']
    tags = datos['tags']
    titulo_short = datos['titulo_short']
    guion_short = datos['guion_short']
    print(f'Titulo: {titulo} | Voz: {voz}')
    audio_voz = '/tmp/smr/audio_voz.mp3'
    asyncio.run(generar_audio(guion, audio_voz, voz))
    srt_largo = '/tmp/subs_largo.srt'
    asyncio.run(generar_srt(guion, srt_largo, voz))
    audio_voz_short = '/tmp/smr/audio_voz_short.mp3'
    asyncio.run(generar_audio(guion_short, audio_voz_short, voz))
    srt_short = '/tmp/subs_short.srt'
    asyncio.run(generar_srt(guion_short, srt_short, voz))
    if musica:
        audio_largo = '/tmp/smr/audio_largo.mp3'
        mezclar_audio(audio_voz, musica, audio_largo)
        audio_short_mix = '/tmp/smr/audio_short.mp3'
        mezclar_audio(audio_voz_short, musica, audio_short_mix)
    else:
        audio_largo = audio_voz
        audio_short_mix = audio_voz_short
    thumbnail = '/tmp/smr/thumbnail.jpg'
    crear_thumbnail(titulo, thumbnail)
    video_largo = '/tmp/smr/video_largo.mp4'
    crear_video_largo(audio_largo, srt_largo, videos_h, video_largo)
    video_short = '/tmp/smr/video_short.mp4'
    crear_short(audio_short_mix, srt_short, videos_v, video_short)
    youtube = get_youtube()
    vid_id = subir_youtube(youtube, video_largo, titulo, descripcion, tags, thumbnail)
    send_telegram(f'✅ Video largo subido\n<b>{titulo}</b>\nhttps://youtu.be/{vid_id}')
    short_id = subir_youtube(youtube, video_short, titulo_short, descripcion, tags, is_short=True)
    send_telegram(f'✅ Short subido\n<b>{titulo_short}</b>\nhttps://youtu.be/{short_id}')
    send_telegram(f'🎉 <b>SaludMentalReal</b> — Completado | Voz: {voz}')

if __name__ == '__main__':
    main()