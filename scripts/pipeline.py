import os, json, pickle, random, asyncio, requests, subprocess, base64
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

GROQ_API_KEY = os.environ['GROQ_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
CHANNEL_NAME = 'SaludMentalReal'

VOCES = [
    'es-ES-AlvaroNeural',
    'es-MX-JorgeNeural',
    'es-ES-XimenaNeural'
]

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

def get_youtube():
    token_data = base64.b64decode(os.environ['TOKEN_PICKLE_B64'])
    creds = pickle.loads(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds)

def generar_guion(tema):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f'''Eres un psicologo divulgador para redes sociales. Crea contenido sobre: {tema}

Responde SOLO con este JSON sin texto adicional:
{{
  "titulo": "titulo llamativo para YouTube de maximo 80 caracteres",
  "descripcion": "descripcion SEO de 300 palabras con hashtags al final",
  "guion": "guion narrado en español latino de 400 palabras, empatico y directo, sin bullet points, como si hablaras con un amigo",
  "tags": ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"],
  "guion_short": "guion corto de 60 palabras para video vertical de 30 segundos, impactante y directo",
  "titulo_short": "titulo del short de maximo 60 caracteres con emoji"
}}'''
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user','content':prompt}],
        response_format={'type':'json_object'},
        temperature=0.8
    )
    return json.loads(resp.choices[0].message.content, strict=False)

async def generar_audio_con_subtitulos(texto, audio_file, srt_file, voz):
    import edge_tts
    communicate = edge_tts.Communicate(texto, voz)
    subs = []
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk['type'] == 'audio':
            audio_chunks.append(chunk['data'])
        elif chunk['type'] == 'WordBoundary':
            subs.append({
                'word': chunk['text'],
                'start': chunk['offset'] / 10000000,
                'duration': chunk['duration'] / 10000000
            })
    with open(audio_file, 'wb') as f:
        for c in audio_chunks:
            f.write(c)
    generar_srt(subs, srt_file)

def generar_srt(subs, srt_file):
    def fmt(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = int(s % 60)
        ms = int((s % 1) * 1000)
        return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'
    lineas = []
    grupo = []
    for i, w in enumerate(subs):
        grupo.append(w)
        if len(grupo) >= 5 or i == len(subs) - 1:
            if grupo:
                inicio = grupo[0]['start']
                fin = grupo[-1]['start'] + grupo[-1]['duration']
                texto = ' '.join(g['word'] for g in grupo)
                lineas.append(f"{len(lineas)+1}\n{fmt(inicio)} --> {fmt(fin)}\n{texto}\n")
            grupo = []
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))

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

def mezclar_audio(voz, musica, salida, volumen_musica=0.12):
    subprocess.run([
        'ffmpeg', '-y', '-i', voz, '-i', musica,
        '-filter_complex',
        f'[1:a]volume={volumen_musica},aloop=loop=-1:size=2e+09[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[out]',
        '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', salida
    ], capture_output=True)

def crear_thumbnail(titulo, archivo):
    img = Image.new('RGB', (1280, 720), color=(15, 35, 70))
    draw = ImageDraw.Draw(img)
    for i in range(0, 1280, 40):
        draw.line([(i, 0), (i, 720)], fill=(20, 45, 85), width=1)
    for i in range(0, 720, 40):
        draw.line([(0, i), (1280, i)], fill=(20, 45, 85), width=1)
    draw.rectangle([40, 40, 1240, 680], outline=(0, 180, 220), width=3)
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 68)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    palabras = titulo.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        if len(linea + ' ' + p) < 22:
            linea = (linea + ' ' + p).strip()
        else:
            if linea: lineas.append(linea)
            linea = p
    if linea: lineas.append(linea)
    y = 360 - (len(lineas) * 80) // 2
    for linea in lineas:
        bbox = draw.textbbox((0, 0), linea, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((1280 - w) // 2 + 3, y + 3), linea, font=font_big, fill=(0, 0, 0))
        draw.text(((1280 - w) // 2, y), linea, font=font_big, fill=(0, 220, 255))
        y += 85
    canal = CHANNEL_NAME.upper()
    bbox2 = draw.textbbox((0, 0), canal, font=font_small)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((1280 - w2) // 2, 620), canal, font=font_small, fill=(0, 180, 220))
    img.save(archivo)

def crear_video_largo(audio_file, srt_file, videos_horizontal, output_file):
    duracion_total = get_audio_duration(audio_file)
    dur_por_clip = 12
    clips_necesarios = int(duracion_total / dur_por_clip) + 2
    clips = []
    pool = videos_horizontal * (clips_necesarios // len(videos_horizontal) + 2)
    for i in range(clips_necesarios):
        src = pool[i % len(pool)]
        clip = f'/tmp/smr_clip_{i}.mp4'
        subprocess.run([
            'ffmpeg', '-y', '-i', src,
            '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
            '-t', str(dur_por_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', clip
        ], capture_output=True)
        clips.append(clip)
    lista = '/tmp/smr_lista.txt'
    with open(lista, 'w') as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    video_mudo = '/tmp/smr_video_mudo.mp4'
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_mudo], capture_output=True)
    video_con_subs = '/tmp/smr_video_subs.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-i', video_mudo, '-vf',
        f"subtitles={srt_file}:force_style='FontName=Arial,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Bold=1,Alignment=2,MarginV=40'",
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_con_subs
    ], capture_output=True)
    subprocess.run([
        'ffmpeg', '-y', '-i', video_con_subs, '-i', audio_file,
        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_file
    ], capture_output=True)

def crear_short(audio_file, srt_file, videos_vertical, output_file):
    duracion = get_audio_duration(audio_file)
    src = random.choice(videos_vertical)
    video_mudo = '/tmp/smr_short_mudo.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-i', src,
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
        '-t', str(duracion + 2), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', video_mudo
    ], capture_output=True)
    video_con_subs = '/tmp/smr_short_subs.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-i', video_mudo, '-vf',
        f"subtitles={srt_file}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Bold=1,Alignment=2,MarginV=60'",
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_con_subs
    ], capture_output=True)
    subprocess.run([
        'ffmpeg', '-y', '-i', video_con_subs, '-i', audio_file,
        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_file
    ], capture_output=True)

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False):
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
    srt_largo = '/tmp/smr/subs_largo.srt'
    asyncio.run(generar_audio_con_subtitulos(guion, audio_voz, srt_largo, voz))

    audio_voz_short = '/tmp/smr/audio_voz_short.mp3'
    srt_short = '/tmp/smr/subs_short.srt'
    asyncio.run(generar_audio_con_subtitulos(guion_short, audio_voz_short, srt_short, voz))

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