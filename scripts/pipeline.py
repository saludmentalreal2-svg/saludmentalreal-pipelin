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
    'Estoy aqui para escucharte. Cuéntame en los comentarios: ¿te identificas con esto? No estás solo/a. 💙',
    '¿Alguna vez has sentido exactamente esto? Escríbelo abajo. Tu historia puede ayudar a alguien más. 🙏',
    'Este video es para quien lo necesita hoy. ¿A quién se lo enviarías? Etiquétalo abajo. ❤️',
    '¿Qué parte de este video te llegó más al corazón? Cuéntame, estoy leyendo todos los comentarios. 💚',
    'El primer paso para sanar es hablarlo. ¿Cómo te sientes hoy? Escríbelo aquí, sin miedo. 🌱',
]

def send_telegram(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except: pass

def run_ffmpeg(cmd, label=''):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'FFmpeg [{label}] error: {result.stderr[-400:]}')
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
  2. VALIDACION: hazlos sentir que no estan solos
  3. EXPLICACION: explica el problema sin terminos tecnicos
  4. SOLUCION: 3 pasos concretos aplicables HOY
  5. CIERRE: mensaje de esperanza + invitacion a comentar

Tema: {tema}

Responde SOLO con JSON sin markdown:
{{
  "titulo": "titulo VIRAL con 2 emojis al inicio, numero o pregunta impactante, maximo 70 caracteres",
  "descripcion": "descripcion 500 palabras: parrafo 1 pregunta engancha, parrafos 2-4 resumen con emojis, parrafo 5 invitacion comentar y suscribir, parrafo 6 recursos. Al final 25 hashtags: #SaludMental #Ansiedad #Depresion #BienestarEmocional #PsicologiaLatina #MenteLibre #SaludMentalReal #Autoestima #Motivacion #Mindfulness #CrecimientoPersonal #TerapiaOnline #SaludMentalMexico #SaludMentalColombia #PsicologiaPositiva",
  "guion": "guion 550 palabras estructura 5 partes. Conversacional empatico. Frases cortas. Maximo 15 palabras por oracion para que suene bien en audio.",
  "frases_clave": ["frase impactante 1 del video maximo 8 palabras", "frase impactante 2 maximo 8 palabras", "frase impactante 3 maximo 8 palabras", "frase impactante 4 maximo 8 palabras", "frase impactante 5 maximo 8 palabras"],
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara","TerapiaOnline","SaludMentalJovenes","AnsiedadSocial","ManejoDeLaAnsiedad","SaludEmocional"],
  "guion_short": "guion 80 palabras Short. Empieza con dato que impacte en 3 segundos. Termina con pregunta que invite a comentar.",
  "titulo_short": "titulo Short 2 emojis maximo 50 caracteres intriga o identificacion",
  "comentario_ancla": "comentario 2 lineas para anclar como primer comentario invitando comunidad"
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
        print(f'SRT OK: {len(grupos)} grupos')
        return True
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

def crear_intro(titulo, output, w=1280, h=720, duracion=3):
    img = Image.new('RGB', (w, h), color=(5, 10, 30))
    draw = ImageDraw.Draw(img)
    for i in range(h):
        r = int(5 + (i/h)*20)
        g = int(10 + (i/h)*10)
        b = int(30 + (i/h)*40)
        draw.line([(0,i),(w,i)], fill=(r,g,b))
    draw.rectangle([0, 0, w, 4], fill=(0, 200, 255))
    draw.rectangle([0, h-4, w, h], fill=(0, 200, 255))
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60 if w==1280 else 42)
        font_sub = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28 if w==1280 else 20)
    except:
        font = ImageFont.load_default()
        font_sub = font
    titulo_limpio = titulo
    for emoji in ['😰','🧠','💙','❤️','🌱','🔥','⚡','💪','🙏','😔','😢','💊','🚨','⚠️','✅','🎯','💡','🧘','🌿','💚','💛','🤍','💜','🧡','😥','😓','🤯','💔']:
        titulo_limpio = titulo_limpio.replace(emoji, '').strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea + ' ' + p).strip()
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2]-bbox[0] < w-120:
            linea = test
        else:
            if linea: lineas.append(linea)
            linea = p
    if linea: lineas.append(linea)
    total_h = len(lineas) * 75
    y = (h - total_h)//2 - 20
    for ln in lineas:
        bbox = draw.textbbox((0,0), ln, font=font)
        tw = bbox[2]-bbox[0]
        draw.text(((w-tw)//2+3, y+3), ln, font=font, fill=(0,0,0))
        draw.text(((w-tw)//2, y), ln, font=font, fill=(255,255,255))
        y += 75
    canal_txt = CHANNEL_HANDLE
    bbox2 = draw.textbbox((0,0), canal_txt, font=font_sub)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((w-tw2)//2, h-55), canal_txt, font=font_sub, fill=(0,200,255))
    img_path = output.replace('.mp4', '_intro.jpg')
    img.save(img_path, quality=95)
    run_ffmpeg([
        'ffmpeg', '-y', '-loop', '1', '-i', img_path,
        '-t', str(duracion), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-r', '25', '-an', output
    ], 'intro')

def crear_frases_overlay(frases, duracion_total, output, w=1280, h=720):
    if not frases: return None
    dur_por_frase = min(4, duracion_total / max(len(frases), 1))
    clips = []
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52 if w==1280 else 38)
        font_pequeño = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24 if w==1280 else 18)
    except:
        font = ImageFont.load_default()
        font_pequeño = font

    for i, frase in enumerate(frases):
        img = Image.new('RGB', (w, h), color=(5, 10, 30))
        draw = ImageDraw.Draw(img)
        for row in range(h):
            r = int(5 + (row/h)*25)
            g = int(10 + (row/h)*15)
            b = int(30 + (row/h)*50)
            draw.line([(0,row),(w,row)], fill=(r,g,b))
        draw.rectangle([0, 0, w, 4], fill=(0, 200, 255))
        draw.rectangle([0, h-4, w, h], fill=(0, 200, 255))
        frase_up = frase.upper()
        palabras = frase_up.split()
        lineas, linea = [], ''
        for p in palabras:
            test = (linea + ' ' + p).strip()
            bbox = draw.textbbox((0,0), test, font=font)
            if bbox[2]-bbox[0] < w-100:
                linea = test
            else:
                if linea: lineas.append(linea)
                linea = p
        if linea: lineas.append(linea)
        total_h = len(lineas) * 65
        y = (h - total_h)//2 - 10
        for ln in lineas:
            bbox = draw.textbbox((0,0), ln, font=font)
            tw = bbox[2]-bbox[0]
            draw.rectangle([(w-tw)//2-15, y-8, (w+tw)//2+15, y+58], fill=(0,0,0))
            draw.text(((w-tw)//2+2, y+2), ln, font=font, fill=(0,0,0))
            draw.text(((w-tw)//2, y), ln, font=font, fill=(0,220,255))
            y += 65
        canal_txt = CHANNEL_HANDLE
        bbox2 = draw.textbbox((0,0), canal_txt, font=font_pequeño)
        tw2 = bbox2[2]-bbox2[0]
        draw.text(((w-tw2)//2, h-40), canal_txt, font=font_pequeño, fill=(100,150,200))
        img_path = f'/tmp/frase_{i}.jpg'
        img.save(img_path, quality=90)
        clip_path = f'/tmp/frase_clip_{i}.mp4'
        run_ffmpeg([
            'ffmpeg', '-y', '-loop', '1', '-i', img_path,
            '-t', str(dur_por_frase), '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p', '-r', '25', '-an', clip_path
        ], f'frase_{i}')
        if os.path.exists(clip_path) and os.path.getsize(clip_path) > 1000:
            clips.append(clip_path)

    if not clips: return None
    lista = '/tmp/lista_frases.txt'
    with open(lista, 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    run_ffmpeg([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output
    ], 'frases_concat')
    return output if os.path.exists(output) and os.path.getsize(output) > 1000 else None

def crear_thumbnail(titulo, archivo):
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), color=(5, 10, 30))
    draw = ImageDraw.Draw(img)
    for i in range(H):
        r = int(5 + (i/H)*25)
        g = int(10 + (i/H)*10)
        b = int(30 + (i/H)*50)
        draw.line([(0,i),(W,i)], fill=(r,g,b))
    for i in range(0, W, 40):
        draw.line([(i,0),(i,H)], fill=(15,30,60), width=1)
    for i in range(0, H, 40):
        draw.line([(0,i),(W,i)], fill=(15,30,60), width=1)
    draw.rectangle([0, 0, W, 6], fill=(0, 200, 255))
    draw.rectangle([0, H-6, W, H], fill=(0, 200, 255))
    draw.rectangle([0, 0, 6, H], fill=(0, 150, 220))
    draw.rectangle([W-6, 0, W, H], fill=(0, 150, 220))
    draw.rectangle([60, 110, W-60, H-90], fill=(0, 0, 0))
    draw.rectangle([63, 113, W-63, H-93], fill=(8, 18, 50))
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 74)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
        font_small = font_big
    titulo_limpio = titulo
    for emoji in ['😰','🧠','💙','❤️','🌱','🔥','⚡','💪','🙏','😔','😢','💊','🚨','⚠️','✅','🎯','💡','🧘','🌿','💚','💛','🤍','💜','🧡','😥','😓','🤯','💔']:
        titulo_limpio = titulo_limpio.replace(emoji, '').strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea + ' ' + p).strip()
        bbox = draw.textbbox((0,0), test, font=font_big)
        if bbox[2]-bbox[0] < W-160:
            linea = test
        else:
            if linea: lineas.append(linea)
            linea = p
    if linea: lineas.append(linea)
    total_h = len(lineas) * 86
    y = (H - total_h)//2 - 25
    for ln in lineas:
        bbox = draw.textbbox((0,0), ln, font=font_big)
        tw = bbox[2]-bbox[0]
        draw.text(((W-tw)//2+4, y+4), ln, font=font_big, fill=(0,0,0))
        draw.text(((W-tw)//2, y), ln, font=font_big, fill=(255,255,255))
        y += 86
    draw.rectangle([80, H-85, W-80, H-81], fill=(0,200,255))
    canal_txt = CHANNEL_HANDLE
    bbox2 = draw.textbbox((0,0), canal_txt, font=font_med)
    tw2 = bbox2[2]-bbox2[0]
    draw.text(((W-tw2)//2, H-76), canal_txt, font=font_med, fill=(0,200,255))
    img.save(archivo, quality=95)

def crear_video_largo(audio_file, srt_file, frases, videos_h, titulo, output_file):
    duracion = get_audio_duration(audio_file)
    print(f'Duracion audio largo: {duracion:.1f}s')

    # Intro de 3 segundos
    intro_path = '/tmp/intro_largo.mp4'
    crear_intro(titulo, intro_path, 1280, 720, 3)

    # Frases overlay intercaladas
    frases_video = '/tmp/frases_video.mp4'
    frases_ok = crear_frases_overlay(frases, min(20, duracion*0.3), frases_video, 1280, 720)

    # Clips de video de fondo
    dur_clip = 9
    duracion_clips = duracion - 3
    if frases_ok: duracion_clips -= 20
    n_clips = max(3, int(duracion_clips / dur_clip) + 3)
    clips = []
    pool = videos_h * (n_clips // max(len(videos_h),1) + 3)

    for i in range(n_clips):
        src = pool[i % len(pool)]
        clip = f'/tmp/hclip_{i}.mp4'
        ok = run_ffmpeg([
            'ffmpeg', '-y', '-i', src,
            '-vf', ('scale=1280:720:force_original_aspect_ratio=decrease,'
                    'pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
                    f'zoompan=z=\'min(zoom+0.0006,1.2)\':d={dur_clip*25}:s=1280x720'),
            '-t', str(dur_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-r', '25', '-an', clip
        ], f'hclip_{i}')
        if not ok or not os.path.exists(clip) or os.path.getsize(clip) < 5000:
            run_ffmpeg([
                'ffmpeg', '-y', '-i', src,
                '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
                '-t', str(dur_clip), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-r', '25', '-an', clip
            ], f'hclip_{i}_fb')
        if os.path.exists(clip) and os.path.getsize(clip) > 5000:
            clips.append(clip)

    if not clips:
        print('ERROR: Sin clips')
        sys.exit(1)

    # Construir lista de segmentos: intro + frases + clips de video
    todos = []
    if os.path.exists(intro_path) and os.path.getsize(intro_path) > 1000:
        todos.append(intro_path)
    for c in clips[:len(clips)//2]:
        todos.append(c)
    if frases_ok and os.path.exists(frases_video) and os.path.getsize(frases_video) > 1000:
        todos.append(frases_video)
    for c in clips[len(clips)//2:]:
        todos.append(c)

    lista = '/tmp/lista_largo.txt'
    with open(lista, 'w') as f:
        for seg in todos: f.write(f"file '{seg}'\n")

    video_mudo = '/tmp/video_mudo_largo.mp4'
    run_ffmpeg([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_mudo
    ], 'concat_largo')

    # Subtitulos con drawtext desde SRT
    video_con_subs = '/tmp/video_con_texto.mp4'
    subs_ok = False
    if srt_file and os.path.exists(srt_file) and os.path.getsize(srt_file) > 10:
        srt_esc = srt_file.replace('\\', '/').replace(':', '\\:')
        style = "FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Shadow=1,Bold=1,Alignment=2,MarginV=40"
        subs_ok = run_ffmpeg([
            'ffmpeg', '-y', '-i', video_mudo,
            '-vf', f"subtitles='{srt_esc}':force_style='{style}'",
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', video_con_subs
        ], 'subtitulos')

    video_base = video_con_subs if subs_ok and os.path.exists(video_con_subs) and os.path.getsize(video_con_subs) > 10000 else video_mudo
    print(f'Video base largo: {"CON subs" if subs_ok else "SIN subs"}')

    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base, '-i', audio_file,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', output_file
    ], 'final_largo')

def crear_short(audio_file, srt_file, frases, videos_v, titulo, output_file):
    duracion = get_audio_duration(audio_file)
    print(f'Duracion audio short: {duracion:.1f}s')

    # Intro vertical 2 segundos
    intro_v = '/tmp/intro_short.mp4'
    crear_intro(titulo, intro_v, 608, 1080, 2)

    src = random.choice(videos_v)
    clip_v = '/tmp/clip_v_base.mp4'
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', src,
        '-vf', ('scale=608:1080:force_original_aspect_ratio=decrease,'
                'pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
                f'zoompan=z=\'min(zoom+0.0008,1.25)\':d={int(duracion)*25}:s=608x1080'),
        '-t', str(int(duracion)+2), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-r', '25', '-an', clip_v
    ], 'clip_v_zoom')

    if not ok or not os.path.exists(clip_v) or os.path.getsize(clip_v) < 5000:
        run_ffmpeg([
            'ffmpeg', '-y', '-i', src,
            '-vf', 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
            '-t', str(int(duracion)+2), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-r', '25', '-an', clip_v
        ], 'clip_v_fb')

    # Combinar intro + clip
    lista_v = '/tmp/lista_short.txt'
    segmentos_v = []
    if os.path.exists(intro_v) and os.path.getsize(intro_v) > 1000:
        segmentos_v.append(intro_v)
    if os.path.exists(clip_v) and os.path.getsize(clip_v) > 1000:
        segmentos_v.append(clip_v)

    video_mudo_v = '/tmp/video_mudo_short.mp4'
    if len(segmentos_v) > 1:
        with open(lista_v, 'w') as f:
            for s in segmentos_v: f.write(f"file '{s}'\n")
        run_ffmpeg([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lista_v,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_mudo_v
        ], 'concat_short')
    else:
        import shutil
        shutil.copy(clip_v, video_mudo_v)

    # Subtitulos
    video_con_subs_v = '/tmp/video_short_subs.mp4'
    subs_ok = False
    if srt_file and os.path.exists(srt_file) and os.path.getsize(srt_file) > 10:
        srt_esc = srt_file.replace('\\', '/').replace(':', '\\:')
        style = "FontName=Arial,FontSize=17,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Shadow=1,Bold=1,Alignment=2,MarginV=55"
        subs_ok = run_ffmpeg([
            'ffmpeg', '-y', '-i', video_mudo_v,
            '-vf', f"subtitles='{srt_esc}':force_style='{style}'",
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', video_con_subs_v
        ], 'subs_short')

    video_base_v = video_con_subs_v if subs_ok and os.path.exists(video_con_subs_v) and os.path.getsize(video_con_subs_v) > 10000 else video_mudo_v
    print(f'Short base: {"CON subs" if subs_ok else "SIN subs"}')

    run_ffmpeg([
        'ffmpeg', '-y', '-i', video_base_v, '-i', audio_file,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', output_file
    ], 'final_short')

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False):
    if not os.path.exists(video_file) or os.path.getsize(video_file) < 10000:
        print(f'ERROR: {video_file} invalido')
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
            print('Thumbnail OK')
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
        print('Comentario ancla OK')
    except Exception as e:
        print(f'Comentario error: {e}')

def main():
    send_telegram('🧠 <b>SaludMentalReal</b> — Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)

    videos_h = get_video_files('assets/videos_h_small')
    videos_v = get_video_files('assets/videos_v_small')
    musica = get_music_file()
    print(f'Assets: {len(videos_h)}H | {len(videos_v)}V | Musica: {bool(musica)}')

    tema = random.choice(TEMAS)
    print(f'Tema: {tema}')
    datos = generar_guion(tema)

    titulo = datos['titulo']
    descripcion = datos['descripcion']
    guion = datos['guion']
    tags = datos['tags']
    titulo_short = datos['titulo_short']
    guion_short = datos['guion_short']
    frases = datos.get('frases_clave', [])
    comentario_ancla = datos.get('comentario_ancla', random.choice(COMENTARIOS_FIJOS))

    print(f'Titulo: {titulo}')
    print(f'Frases clave: {frases}')

    # TTS + SRT
    audio_voz = '/tmp/smr/audio_voz.mp3'
    srt_largo = '/tmp/subs_largo.srt'
    asyncio.run(tts_con_srt(guion, audio_voz, srt_largo, VOZ))

    audio_voz_short = '/tmp/smr/audio_voz_short.mp3'
    srt_short = '/tmp/subs_short.srt'
    asyncio.run(tts_con_srt(guion_short, audio_voz_short, srt_short, VOZ))

    # Musica
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
    crear_video_largo(audio_largo, srt_largo, frases, videos_h, titulo, video_largo)

    video_short = '/tmp/smr/video_short.mp4'
    crear_short(audio_short_mix, srt_short, frases[:3], videos_v, titulo_short, video_short)

    # Subir
    youtube = get_youtube()

    vid_id = subir_youtube(youtube, video_largo, titulo, descripcion, tags, thumbnail)
    agregar_comentario(youtube, vid_id, comentario_ancla)
    send_telegram(f'✅ <b>Video largo subido</b>\n{titulo}\nhttps://youtu.be/{vid_id}')

    short_id = subir_youtube(youtube, video_short, titulo_short, descripcion, tags, is_short=True)
    send_telegram(f'✅ <b>Short subido</b>\n{titulo_short}\nhttps://youtu.be/{short_id}')

    send_telegram(f'🎉 <b>SaludMentalReal</b> — Completado\nTema: {tema}')

if __name__ == '__main__':
    main()