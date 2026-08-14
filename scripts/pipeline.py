import os, json, pickle, random, asyncio, requests, subprocess, base64, sys
from groq import Groq
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

GROQ_API_KEY = os.environ['GROQ_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
CHANNEL_NAME = 'SaludMentalReal'
CHANNEL_HANDLE = '@SaludMentalReal1'

VOZ = 'es-MX-JorgeNeural'

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
    'como decirle no a las personas toxicas en tu vida',
    'por que te sientes vacio sin razon aparente',
    'como dejar de buscar aprobacion de los demas',
    'señales de que eres emocionalmente inmaduro',
    'como sanar relaciones toxicas sin drama',
    'el miedo al rechazo de donde viene y como vencerlo',
    'por que saboteas tu propio exito inconscientemente',
    'como hablar con tu mente cuando te ataca',
    'duelo emocional lo que nadie te prepara para sentir',
    'por que te cuesta tanto pedir ayuda',
    'como sobrevivir a una crisis de ansiedad nocturna'
]

COMENTARIOS_FIJOS = [
    '💬 ¿Te identificas con esto? Cuéntame en los comentarios, estoy aquí para escucharte. 👇',
    '💙 ¿Alguna vez has sentido esto? No estás solo/a. Comparte tu experiencia abajo. 👇',
    '🙏 Este video es para quien lo necesita hoy. ¿A quién se lo enviarías? Escríbelo abajo. 👇',
    '❤️ ¿Qué parte de este video te llegó más? Cuéntame, tu historia puede ayudar a otros. 👇',
    '🌱 El primer paso para sanar es hablarlo. ¿Cómo te sientes hoy? Escríbelo aquí abajo. 👇',
]

def send_telegram(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except: pass

def run_ffmpeg(cmd, label=''):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'FFmpeg [{label}] error: {result.stderr[-600:]}')
    else:
        if label: print(f'FFmpeg [{label}] OK')
    return result.returncode == 0

def get_youtube():
    token_data = base64.b64decode(os.environ['TOKEN_PICKLE_B64'])
    creds = pickle.loads(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds)

def generar_guion(tema):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f'''Eres un psicologo clinico latinoamericano que crea contenido viral en YouTube.
Tu estilo: empatico, cercano, directo, como si hablaras con un amigo que esta sufriendo.
Estructura obligatoria del guion: 
  1. GANCHO (primeras 15 palabras): dato impactante o pregunta que duela un poco
  2. VALIDACION: hazlos sentir que no estan solos, que lo que sienten es real
  3. EXPLICACION: explica el problema de forma sencilla sin terminos tecnicos
  4. SOLUCION: 3 pasos concretos y aplicables HOY
  5. CIERRE: mensaje de esperanza + invitacion a comentar

Tema: {tema}

Responde SOLO con este JSON sin texto adicional ni markdown:
{{
  "titulo": "titulo VIRAL con 2 emojis al inicio, numero o pregunta impactante, maximo 70 caracteres. Ejemplos: '😰 ¿Por qué sientes ansiedad sin razón? Esto te pasa' o '🧠 5 señales de que necesitas ayuda psicológica YA'",
  "descripcion": "descripcion de 500 palabras estructurada asi: parrafo 1 pregunta impactante que engancha, parrafo 2-4 resumen del contenido con emojis en cada parrafo, parrafo 5 invitacion a comentar y suscribirse, parrafo 6 recursos adicionales. Al final 25 hashtags virales incluyendo: #SaludMental #Ansiedad #Depresion #BienestarEmocional #PsicologiaLatina #MenteLibre #SaludMentalReal #Autoestima #Motivacion #Mindfulness #CrecimientoPersonal #TerapiaOnline #SaludMentalMexico #SaludMentalColombia #PsicologiaPositiva",
  "guion": "guion narrado de 550 palabras siguiendo la estructura de 5 partes. Conversacional, empatico, sin bullet points. Que haga sentir al oyente que alguien finalmente lo entiende.",
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara","TerapiaOnline","SaludMentalJovenes","AnsiedadSocial","ManejoDeLaAnsiedad","SaludEmocional"],
  "guion_short": "guion de 80 palabras para Short. Empieza con dato que impacte en 3 segundos. Termina con pregunta que invite a comentar. Tono urgente y empatico.",
  "titulo_short": "titulo Short con 2 emojis, maximo 50 caracteres, que genere intriga o identificacion",
  "comentario_ancla": "comentario de 2 lineas para anclar como primer comentario del canal, que invite a la gente a compartir su experiencia y sentirse en comunidad"
}}'''
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user','content':prompt}],
        response_format={'type':'json_object'},
        temperature=0.9
    )
    return json.loads(resp.choices[0].message.content, strict=False)

async def tts_con_srt(texto, audio_file, srt_file, voz):
    import edge_tts
    communicate = edge_tts.Communicate(texto, voz)
    words = []
    audio_data = b''
    async for chunk in communicate.stream():
        if chunk['type'] == 'audio':
            audio_data += chunk['data']
        elif chunk['type'] == 'WordBoundary':
            words.append({
                'word': chunk['text'],
                'start': chunk['offset'] / 10000000,
                'end': (chunk['offset'] + chunk['duration']) / 10000000
            })
    with open(audio_file, 'wb') as f:
        f.write(audio_data)
    print(f'TTS OK: {len(audio_data)} bytes | Palabras: {len(words)}')
    if words:
        def fmt(s):
            h, m = int(s//3600), int((s%3600)//60)
            return f'{h:02d}:{m:02d}:{int(s%60):02d},{int((s%1)*1000):03d}'
        grupos, grupo = [], []
        for w in words:
            grupo.append(w)
            if len(grupo) >= 5:
                grupos.append(grupo); grupo = []
        if grupo: grupos.append(grupo)
        with open(srt_file, 'w', encoding='utf-8') as f:
            for i, g in enumerate(grupos):
                f.write(f"{i+1}\n{fmt(g[0]['start'])} --> {fmt(g[-1]['end'])}\n{' '.join(x['word'] for x in g)}\n\n")
        print(f'SRT OK: {len(grupos)} grupos -> {srt_file}')
        return True
    print('SRT: sin palabras (voz no soporta WordBoundary)')
    return False

def get_audio_duration(audio_file):
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', audio_file],
        capture_output=True, text=True)
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
    if not os.path.exists(carpeta): return None
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith('.mp3')]
    return random.choice(archivos) if archivos else None

def mezclar_audio(voz_mp3, musica, salida, vol=0.09):
    import shutil
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', voz_mp3, '-i', musica,
        '-filter_complex',
        f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];[1:a]volume={vol},aformat=sample_rates=44100:channel_layouts=stereo,aloop=loop=-1:size=2e+09[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[out]',
        '-map', '[out]', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', salida
    ], 'mezcla')
    if not ok or not os.path.exists(salida) or os.path.getsize(salida) < 1000:
        shutil.copy(voz_mp3, salida)
        print('Mezcla fallida - usando solo voz')

def crear_thumbnail(titulo, archivo):
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), color=(5, 15, 40))
    draw = ImageDraw.Draw(img)

    # Fondo con gradiente simulado
    for i in range(H):
        alpha = int(255 * (1 - i/H) * 0.3)
        r = min(255, 5 + int(i * 0.15))
        g = min(255, 15 + int(i * 0.05))
        b = min(255, 40 + int(i * 0.2))
        draw.line([(0,i),(W,i)], fill=(r,g,b))

    # Grid sutil
    for i in range(0, W, 40):
        draw.line([(i,0),(i,H)], fill=(20,50,90), width=1)
    for i in range(0, H, 40):
        draw.line([(0,i),(W,i)], fill=(20,50,90), width=1)

    # Borde superior llamativo
    draw.rectangle([0, 0, W, 6], fill=(0, 200, 255))
    draw.rectangle([0, H-6, W, H], fill=(0, 200, 255))

    # Linea izquierda decorativa
    draw.rectangle([0, 0, 6, H], fill=(0, 150, 220))

    # Caja central semitransparente
    draw.rectangle([60, 120, W-60, H-100], fill=(0, 0, 0))
    # Simular transparencia con color oscuro
    draw.rectangle([62, 122, W-62, H-102], fill=(8, 20, 55))

    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 76)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
        font_small = font_big

    # Titulo
    # Limpiar emojis para el thumbnail (PIL no los renderiza bien)
    titulo_limpio = titulo
    for emoji in ['😰','🧠','💙','❤️','🌱','🔥','⚡','💪','🙏','😔','😢','💊','🚨','⚠️','✅','🎯','💡','🧘','🌿','💚','💛','🤍','🖤','🤎','💜','🧡']:
        titulo_limpio = titulo_limpio.replace(emoji, '').strip()

    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea + ' ' + p).strip()
        try:
            bbox = draw.textbbox((0,0), test, font=font_big)
            if bbox[2] - bbox[0] < W - 160:
                linea = test
            else:
                if linea: lineas.append(linea)
                linea = p
        except:
            linea = test
    if linea: lineas.append(linea)

    total_h = len(lineas) * 88
    y = (H - total_h) // 2 - 20
    for ln in lineas:
        try:
            bbox = draw.textbbox((0,0), ln, font=font_big)
            w = bbox[2] - bbox[0]
        except:
            w = len(ln) * 40
        # Sombra
        draw.text(((W-w)//2+4, y+4), ln, font=font_big, fill=(0,0,0))
        # Texto principal blanco
        draw.text(((W-w)//2, y), ln, font=font_big, fill=(255,255,255))
        y += 88

    # Linea separadora
    draw.rectangle([100, H-95, W-100, H-91], fill=(0,200,255))

    # Footer
    canal_txt = CHANNEL_HANDLE
    try:
        bbox2 = draw.textbbox((0,0), canal_txt, font=font_med)
        w2 = bbox2[2] - bbox2[0]
    except:
        w2 = 300
    draw.text(((W-w2)//2, H-82), canal_txt, font=font_med, fill=(0,200,255))

    img.save(arquivo if False else archivo, quality=95)

def agregar_subtitulos_ffmpeg(video_in, srt_file, video_out, w, h):
    if not srt_file or not os.path.exists(srt_file):
        print('Sin SRT disponible')
        return False
    if os.path.getsize(srt_file) < 10:
        print('SRT vacio')
        return False

    fontsize = 22 if w == 1280 else 18
    margenv = 45 if w == 1280 else 60
    
    style = (f"FontName=Arial,FontSize={fontsize},"
             f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
             f"Outline=3,Shadow=1,Bold=1,Alignment=2,MarginV={margenv}")

    srt_escaped = srt_file.replace('\\', '/').replace(':', '\\:')

    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', video_in,
        '-vf', f"subtitles='{srt_escaped}':force_style='{style}'",
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
        '-crf', '23', video_out
    ], f'subtitulos_{w}x{h}')

    return ok and os.path.exists(video_out) and os.path.getsize(video_out) > 10000

def crear_video_largo(audio_file, srt_file, videos_h, output_file):
    duracion = get_audio_duration(audio_file)
    print(f'Duracion audio largo: {duracion:.1f}s')

    dur_clip = 9
    n_clips = int(duracion / dur_clip) + 4
    clips = []
    pool = videos_h * (n_clips // max(len(videos_h),1) + 3)

    for i in range(n_clips):
        src = pool[i % len(pool)]
        clip = f'/tmp/hclip_{i}.mp4'
        ok = run_ffmpeg([
            'ffmpeg', '-y', '-i', src,
            '-vf', ('scale=1280:720:force_original_aspect_ratio=decrease,'
                    'pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
                    f'zoompan=z=\'min(zoom+0.0006,1.25)\':d={dur_clip*25}:s=1280x720'),
            '-t', str(dur_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-r', '25', '-an', clip
        ], f'clip_h_{i}')
        if ok and os.path.exists(clip) and os.path.getsize(clip) > 5000:
            clips.append(clip)
            print(f'  Clip H {i+1}/{n_clips} OK')
        else:
            # Fallback sin zoom
            ok2 = run_ffmpeg([
                'ffmpeg', '-y', '-i', src,
                '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
                '-t', str(dur_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-r', '25', '-an', clip
            ], f'clip_h_{i}_fallback')
            if ok2 and os.path.exists(clip) and os.path.getsize(clip) > 5000:
                clips.append(clip)

    if not clips:
        print('ERROR: Sin clips horizontales')
        sys.exit(1)

    lista = '/tmp/lista_h.txt'
    with open(lista, 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")

    video_mudo = '/tmp/video_mudo_h.mp4'
    ok_concat = run_ffmpeg([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_mudo
    ], 'concat_h')

    if not ok_concat:
        print('ERROR concat')
        sys.exit(1)

    # Intentar agregar subtitulos
    video_subs = '/tmp/video_subs_h.mp4'
    ok_subs = agregar_subtitulos_ffmpeg(video_mudo, srt_file, video_subs, 1280, 720)
    video_base = video_subs if ok_subs else video_mudo
    print(f'Video base: {"CON subtitulos" if ok_subs else "SIN subtitulos"}')

    # Mezclar con audio
    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base, '-i', audio_file,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
        output_file
    ], 'final_h')

def crear_short(audio_file, srt_file, videos_v, output_file):
    duracion = get_audio_duration(audio_file)
    print(f'Duracion audio short: {duracion:.1f}s')

    src = random.choice(videos_v)
    clip_v = '/tmp/clip_v.mp4'
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', src,
        '-vf', ('scale=608:1080:force_original_aspect_ratio=decrease,'
                'pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
                f'zoompan=z=\'min(zoom+0.0008,1.3)\':d={int(duracion+3)*25}:s=608x1080'),
        '-t', str(int(duracion)+3), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-r', '25', '-an', clip_v
    ], 'clip_v')

    if not ok or not os.path.exists(clip_v) or os.path.getsize(clip_v) < 5000:
        run_ffmpeg([
            'ffmpeg', '-y', '-i', src,
            '-vf', 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
            '-t', str(int(duracion)+3), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-r', '25', '-an', clip_v
        ], 'clip_v_fallback')

    video_subs = '/tmp/video_subs_v.mp4'
    ok_subs = agregar_subtitulos_ffmpeg(clip_v, srt_file, video_subs, 608, 1080)
    video_base = video_subs if ok_subs else clip_v
    print(f'Short base: {"CON subtitulos" if ok_subs else "SIN subtitulos"}')

    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base, '-i', audio_file,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest',
        output_file
    ], 'final_v')

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False):
    if not os.path.exists(video_file) or os.path.getsize(video_file) < 10000:
        print(f'ERROR: {video_file} no existe o esta vacio')
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
    media = MediaFileUpload(video_file, mimetype='video/mp4', resumable=True, chunksize=5*1024*1024)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = None
    while response is None:
        _, response = req.next_chunk()
    video_id = response['id']
    if thumbnail and os.path.exists(thumbnail):
        try:
            youtube.thumbnails().set(videoId=video_id,
                media_body=MediaFileUpload(thumbnail, mimetype='image/jpeg')).execute()
            print('Thumbnail subido OK')
        except Exception as e:
            print(f'Thumbnail error: {e}')
    return video_id

def agregar_comentario(youtube, video_id, comentario):
    try:
        youtube.commentThreads().insert(
            part='snippet',
            body={
                'snippet': {
                    'videoId': video_id,
                    'topLevelComment': {
                        'snippet': {'textOriginal': comentario}
                    }
                }
            }
        ).execute()
        print('Comentario ancla agregado OK')
    except Exception as e:
        print(f'Comentario error: {e}')

def main():
    send_telegram('🧠 <b>SaludMentalReal</b> — Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)

    videos_h = get_video_files('assets/videos_h_small')
    videos_v = get_video_files('assets/videos_v_small')
    musica = get_music_file()
    print(f'Assets: {len(videos_h)} videos H | {len(videos_v)} videos V | Musica: {bool(musica)}')

    tema = random.choice(TEMAS)
    print(f'Tema: {tema}')
    datos = generar_guion(tema)

    titulo = datos['titulo']
    descripcion = datos['descripcion']
    guion = datos['guion']
    tags = datos['tags']
    titulo_short = datos['titulo_short']
    guion_short = datos['guion_short']
    comentario_ancla = datos.get('comentario_ancla', random.choice(COMENTARIOS_FIJOS))

    print(f'Titulo: {titulo}')

    # TTS + SRT
    audio_voz = '/tmp/smr/audio_voz.mp3'
    srt_largo = '/tmp/subs_largo.srt'
    asyncio.run(tts_con_srt(guion, audio_voz, srt_largo, VOZ))

    audio_voz_short = '/tmp/smr/audio_voz_short.mp3'
    srt_short = '/tmp/subs_short.srt'
    asyncio.run(tts_con_srt(guion_short, audio_voz_short, srt_short, VOZ))

    # Mezclar musica
    if musica:
        audio_largo = '/tmp/smr/audio_largo.mp3'
        mezclar_audio(audio_voz, musica, audio_largo)
        audio_short_mix = '/tmp/smr/audio_short.mp3'
        mezclar_audio(audio_voz_short, musica, audio_short_mix)
    else:
        audio_largo = audio_voz
        audio_short_mix = audio_voz_short

    # Thumbnail
    thumbnail = '/tmp/smr/thumbnail.jpg'
    crear_thumbnail(titulo, thumbnail)

    # Videos
    video_largo = '/tmp/smr/video_largo.mp4'
    crear_video_largo(audio_largo, srt_largo, videos_h, video_largo)

    video_short = '/tmp/smr/video_short.mp4'
    crear_short(audio_short_mix, srt_short, videos_v, video_short)

    # Subir a YouTube
    youtube = get_youtube()

    vid_id = subir_youtube(youtube, video_largo, titulo, descripcion, tags, thumbnail)
    agregar_comentario(youtube, vid_id, comentario_ancla)
    send_telegram(f'✅ <b>Video largo subido</b>\n{titulo}\nhttps://youtu.be/{vid_id}')

    short_id = subir_youtube(youtube, video_short, titulo_short, descripcion, tags, is_short=True)
    send_telegram(f'✅ <b>Short subido</b>\n{titulo_short}\nhttps://youtu.be/{short_id}')

    send_telegram(f'🎉 <b>SaludMentalReal</b> — Completado\nTema: {tema}')

if __name__ == '__main__':
    main()