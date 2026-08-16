import os, json, pickle, random, asyncio, requests, subprocess, base64, sys, re
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

GROQ_API_KEY = os.environ['GROQ_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PEXELS_API_KEY = os.environ['PEXELS_API_KEY']
CHANNEL_NAME = 'SaludMentalReal'
CHANNEL_HANDLE = '@SaludMentalReal1'
VOZ_ES = 'es-MX-JorgeNeural'
VOZ_EN = 'en-US-GuyNeural'
VOZ_RATE = '-10%'
VOZ_PITCH = '-4Hz'
VOZ_VOLUME = '+15%'
PLAYLIST_ES_NAME = 'Salud Mental en Espanol'
PLAYLIST_EN_NAME = 'Mental Health English'

TEMAS_ES = [
    'como controlar la ansiedad en momentos de crisis',
    'tecnicas de respiracion para calmar el estres',
    'como dormir mejor cuando la mente no para',
    'señales de burnout y como recuperarte',
    'como manejar un ataque de panico paso a paso',
    'la depresion no es tristeza lo que nadie explica',
    'como salir de una adiccion cuando no puedes',
    'tecnicas para dejar de rumiar pensamientos negativos',
    'como hablar con alguien que esta en depresion',
    'el impacto del telefono en tu salud mental',
    'como poner limites sin sentir culpa',
    'ansiedad social como superarla poco a poco',
    'autoestima baja de donde viene y como mejorarla',
    'como manejar el duelo cuando pierdes a alguien',
    'señales de que necesitas ayuda psicologica',
    'mindfulness para principiantes en 5 minutos',
    'como dejar de procrastinar cuando la ansiedad paraliza',
    'el sindrome del impostor como combatirlo',
    'como recuperarse de una ruptura sin destruirte',
    'trauma infantil como reconocerlo en tu vida adulta',
    'como ayudarte cuando nadie mas puede',
    'el poder del ejercicio para la salud mental',
    'como manejar la ira antes de explotar',
    'soledad emocional como enfrentarla de verdad',
    'adiccion a redes sociales como salir',
    'como mantener la calma en conflictos',
    'pensamientos intrusivos que son y como manejarlos',
    'como construir rutinas que protejan tu salud mental',
    'el sueno y su rol en la ansiedad y depresion',
    'como decirle no a personas toxicas',
    'por que te sientes vacio sin razon',
    'como dejar de buscar aprobacion de los demas',
    'señales de inmadurez emocional',
    'como sanar relaciones toxicas',
    'el miedo al rechazo y como vencerlo',
    'por que te saboteas inconscientemente',
    'duelo emocional lo que nadie te prepara para sentir',
    'por que te cuesta pedir ayuda',
    'como sobrevivir una crisis de ansiedad nocturna',
    'que es la ansiedad generalizada y como tratarla',
    'por que lloras sin razon',
    'como dejar de compararte en redes sociales',
    'señales de trauma emocional sin saberlo',
    'como manejar la soledad cuando vives solo',
    'por que sientes que no encajas en ningun lado',
    'como recuperar la motivacion cuando todo da igual',
    'el agotamiento emocional que nadie ve',
    'como dejar de ser tan duro contigo mismo',
    'por que te cuesta ser feliz aunque tengas todo',
    'como superar el miedo al fracaso',
    'señales de que necesitas terapia urgente',
    'como manejar relacion con alguien deprimido',
    'por que la ansiedad aparece de noche',
    'como hablar de salud mental sin que te juzguen',
    'el poder de decir no sin sentirte mal',
    'como salir del ciclo de la negatividad',
    'por que tienes miedo al exito',
    'como construir autoestima desde cero',
    'señales de que una relacion daña tu salud mental',
    'como manejar los celos sin destruir tu relacion',
    'por que te sientes culpable de ser feliz',
    'como superar la traicion de alguien que amabas',
    'el efecto del alcohol en tu salud mental',
    'como dejar de pensar demasiado overthinking',
    'por que evitas el conflicto aunque te lastime',
    'señales de que eres altamente sensible',
    'como manejar la ansiedad en el trabajo',
    'por que te cuesta perdonar de verdad',
    'el impacto de la familia toxica en tu salud mental',
    'como sanar el miedo al abandono en adultos',
    'por que te autosaboteas en el amor',
    'señales de codependencia emocional',
    'como meditar cuando tu mente no para',
    'por que el ejercicio ayuda mas que un antidepresivo',
    'como manejar la ansiedad social en eventos',
    'por que sientes que no mereces ser amado',
    'como salir de la depresion cuando no tienes fuerzas',
    'el papel de la alimentacion en tu salud mental',
    'como manejar crisis emocionales en el trabajo',
    'por que te sientes solo rodeado de personas'
]

TEMAS_EN = [
    'how to control anxiety during a crisis',
    'breathing techniques to calm stress immediately',
    'how to sleep better when your mind wont stop',
    'signs of burnout and how to recover',
    'how to handle a panic attack step by step',
    'depression is not sadness what no one tells you',
    'how to overcome addiction when you feel you cant',
    'techniques to stop negative rumination',
    'how to talk to someone who is depressed',
    'the impact of phones on your mental health',
    'how to set boundaries without feeling guilty',
    'social anxiety how to overcome it gradually',
    'low self esteem where it comes from and how to improve',
    'how to handle grief when you lose someone',
    'signs you need psychological help now',
    'mindfulness for beginners in 5 minutes a day',
    'how to stop procrastinating when anxiety paralyzes you',
    'imposter syndrome what it is and how to fight it',
    'how to recover from a breakup without destroying yourself',
    'childhood trauma how to recognize it in your adult life'
]

QUERIES_PEXELS_H = [
    'therapy session calm', 'meditation nature peaceful', 'breathing exercise wellness',
    'mental health calm person', 'nature forest peaceful sunrise', 'yoga meditation outdoor',
    'person journaling calm', 'mindfulness breathing nature', 'peaceful lake morning',
    'calm ocean waves beach', 'person walking nature path', 'mental wellness calm',
    'stress relief nature', 'emotional healing peaceful', 'counseling support'
]

QUERIES_PEXELS_V = [
    'meditation vertical calm', 'person breathing vertical', 'nature vertical peaceful',
    'yoga vertical wellness', 'mindfulness vertical', 'forest vertical nature',
    'ocean vertical waves', 'person thinking vertical', 'wellness vertical nature',
    'calm vertical portrait'
]

COMENTARIOS_ES = [
    'Estoy aqui para escucharte. Te identificas con esto? Cuentame abajo, no estas solo.',
    'Alguna vez sentiste exactamente esto? Tu historia puede ayudar a alguien mas. Escribela abajo.',
    'Este video es para quien lo necesita hoy. A quien se lo enviarias?',
    'Que parte de este video te llego mas? Cuentame, leo todos los comentarios.',
    'El primer paso para sanar es hablarlo. Como te sientes hoy? Escribelo aqui.',
    'Si esto te ayudo, imagina cuanto puede ayudar a alguien que conoces. Compartelo.',
    'Recuerda: pedir ayuda es el acto mas valiente que existe. Como estas hoy?',
]

COMENTARIOS_EN = [
    'I am here to listen. Does this resonate with you? Tell me below, you are not alone.',
    'Have you ever felt exactly this? Your story might help someone else. Share it below.',
    'This video is for whoever needs it today. Who would you send this to?',
    'Which part of this video hit you the most? Tell me, I read every comment.',
    'Remember: asking for help is the bravest thing you can do. How are you today?',
]

PALETAS = [
    {'fondo': (8,15,45), 'acento': (0,200,255), 'texto': (255,255,255)},
    {'fondo': (45,8,15), 'acento': (255,80,80), 'texto': (255,255,255)},
    {'fondo': (8,35,15), 'acento': (0,220,100), 'texto': (255,255,255)},
    {'fondo': (30,8,45), 'acento': (180,80,255), 'texto': (255,255,255)},
    {'fondo': (40,25,5), 'acento': (255,160,0), 'texto': (255,255,255)},
]

def limpiar_texto_voz(texto):
    texto = re.sub(r'[^\w\s\.,;:!?\-\(\)áéíóúñüÁÉÍÓÚÑÜa-zA-Z0-9]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def send_telegram(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except: pass

def run_ffmpeg(cmd, label=''):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'FFmpeg [{label}] error: {result.stderr[-300:]}')
    else:
        if label: print(f'FFmpeg [{label}] OK')
    return result.returncode == 0

def get_youtube():
    token_data = base64.b64decode(os.environ['TOKEN_PICKLE_B64'])
    creds = pickle.loads(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds)

def buscar_playlist_existente(youtube, nombre):
    try:
        resp = youtube.playlists().list(part='snippet', mine=True, maxResults=50).execute()
        for item in resp.get('items', []):
            if nombre.lower() in item['snippet']['title'].lower():
                print(f'Playlist encontrada: {item["snippet"]["title"]} ({item["id"]})')
                return item['id']
    except Exception as e:
        print(f'Buscar playlist error: {e}')
    return None

def crear_playlist(youtube, nombre, descripcion, idioma='es'):
    try:
        pl = youtube.playlists().insert(part='snippet,status', body={
            'snippet': {'title': nombre, 'description': descripcion, 'defaultLanguage': idioma},
            'status': {'privacyStatus': 'public'}
        }).execute()
        print(f'Playlist creada: {nombre} ({pl["id"]})')
        return pl['id']
    except Exception as e:
        print(f'Crear playlist error: {e}')
        return None

def obtener_o_crear_playlist(youtube, nombre, descripcion, idioma='es'):
    pl_id = buscar_playlist_existente(youtube, nombre)
    if pl_id:
        return pl_id
    return crear_playlist(youtube, nombre, descripcion, idioma)

def agregar_a_playlist(youtube, video_id, playlist_id):
    if not playlist_id: return
    try:
        youtube.playlistItems().insert(part='snippet', body={
            'snippet': {'playlistId': playlist_id,
                'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}
        }).execute()
        print('Agregado a playlist OK')
    except Exception as e:
        print(f'Playlist add error: {e}')

def descargar_videos_pexels(queries, orientacion, n=5):
    os.makedirs('/tmp/pexels', exist_ok=True)
    videos = []
    headers = {'Authorization': PEXELS_API_KEY}
    intentos = 0
    while len(videos) < n and intentos < 3:
        intentos += 1
        query = random.choice(queries)
        print(f'Pexels [{orientacion}]: {query}')
        try:
            r = requests.get('https://api.pexels.com/videos/search',
                headers=headers,
                params={'query': query, 'orientation': orientacion, 'per_page': 15, 'size': 'medium'},
                timeout=30)
            items = r.json().get('videos', [])
            random.shuffle(items)
            for item in items:
                if len(videos) >= n: break
                try:
                    files = [f for f in item.get('video_files', []) if f.get('width', 0) >= 640]
                    if not files: continue
                    files.sort(key=lambda x: x.get('width', 0))
                    url = files[0]['link']
                    raw = f'/tmp/pexels/raw_{orientacion}_{len(videos)}.mp4'
                    vr = requests.get(url, timeout=60, stream=True)
                    with open(raw, 'wb') as f:
                        for chunk in vr.iter_content(chunk_size=1024*1024):
                            f.write(chunk)
                    if not os.path.exists(raw) or os.path.getsize(raw) < 100000:
                        continue
                    proc = f'/tmp/pexels/proc_{orientacion}_{len(videos)}.mp4'
                    if orientacion == 'landscape':
                        vf = 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    else:
                        vf = 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    ok = run_ffmpeg(['ffmpeg','-y','-i',raw,'-vf',vf,'-t','12',
                        '-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',proc],
                        f'pexels_{len(videos)}')
                    if ok and os.path.exists(proc) and os.path.getsize(proc) > 50000:
                        videos.append(proc)
                        print(f'  Video {len(videos)}/{n} OK')
                except Exception as e:
                    print(f'  Item error: {e}')
        except Exception as e:
            print(f'Pexels error: {e}')
    if len(videos) < 2:
        carpeta = 'assets/videos_h_small' if orientacion == 'landscape' else 'assets/videos_v_small'
        if os.path.exists(carpeta):
            exts = ('.mp4','.mov','.avi','.mkv','.webm')
            local = [os.path.join(carpeta,f) for f in os.listdir(carpeta) if f.lower().endswith(exts)]
            random.shuffle(local)
            videos.extend(local[:n])
            print(f'Fallback local: {len(local)} videos')
    return videos

def generar_guion(tema, idioma='es'):
    client = Groq(api_key=GROQ_API_KEY)
    if idioma == 'es':
        prompt = f'''Eres un psicologo clinico latinoamericano con canal viral de YouTube.
Estilo: empatico, directo, conversacional. Como un amigo que entiende tu dolor.
CRITICO: El guion sera leido por una voz sintetica. NO uses emojis, asteriscos, hashtags, 
ni ningun simbolo especial en el guion o guion_short. Solo texto limpio con puntos y comas.

Estructura guion:
  1. GANCHO: pregunta o dato impactante menos de 12 palabras
  2. VALIDACION: sus sentimientos son validos, no estan solos
  3. EXPLICACION: el problema en terminos simples con ejemplos cotidianos
  4. SOLUCION: 3 pasos concretos aplicables hoy
  5. CIERRE: esperanza real e invitacion a comentar

Tema: {tema}

JSON puro sin markdown:
{{
  "titulo": "titulo viral en español con 2 emojis al inicio, numero o pregunta impactante, maximo 68 caracteres, NO hashtags en titulo",
  "descripcion": "500 palabras: primera linea pregunta engancha, segunda linea invita suscribirse y campana, parrafos con emojis, timestamps: 0:00 Introduccion | 0:45 El problema real | 1:30 Por que te sucede | 2:45 Tres soluciones | 4:00 Mensaje final, parrafo recursos de crisis, 25 hashtags al final",
  "guion": "520 palabras SOLO TEXTO LIMPIO sin emojis sin simbolos sin hashtags. Frases max 10 palabras. Pausas con puntos y comas. Primera persona plural. Natural y empatico.",
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara","TerapiaOnline","SaludMentalJovenes","AnsiedadSocial","ManejoDeLaAnsiedad","SaludEmocional","PsicologiaColombia","PsicologiaMexico","SaludMentalLatam","MentePositiva","BienEstar"],
  "guion_short": "80 palabras SOLO TEXTO LIMPIO sin emojis sin simbolos. Frases max 8 palabras. Dato impactante inicio. Pregunta empatica final.",
  "titulo_short": "titulo Short español 2 emojis max 48 caracteres sin hashtags",
  "comentario_ancla": "comentario empatico 2 lineas sin emojis invitando a comentar"
}}'''
    else:
        prompt = f'''You are a clinical psychologist with a viral YouTube channel.
Style: empathetic, direct, conversational. Like a friend who truly understands pain.
CRITICAL: The script will be read by synthetic voice. NO emojis, asterisks, hashtags
or special symbols in guion or guion_short. Clean text only with periods and commas.

Topic: {tema}

Pure JSON no markdown:
{{
  "titulo": "viral English title 2 emojis at start, number or impactful question, max 68 chars, NO hashtags in title",
  "descripcion": "400 words: engaging question, subscribe line, emoji paragraphs, timestamps: 0:00 Introduction | 0:45 The problem | 1:30 Why it happens | 2:45 Three solutions | 4:00 Hope message, crisis resources, 20 hashtags at end",
  "guion": "450 words CLEAN TEXT ONLY no emojis no symbols no hashtags. Max 10 words per sentence. Natural empathetic. First person plural.",
  "tags": ["MentalHealth","Anxiety","Depression","EmotionalWellness","Psychology","MindOverMatter","MentalHealthMatters","SelfCare","Motivation","Mindfulness","PersonalGrowth","Therapy","MentalHealthAwareness","AnxietyRelief","HealingJourney","EmotionalHealth","MentalWellness","SelfLove","Mindset","PositivePsychology"],
  "guion_short": "70 words CLEAN TEXT ONLY no emojis no symbols. Max 8 words per sentence. Impactful opening. Empathetic question at end.",
  "titulo_short": "English Short title 2 emojis max 48 chars no hashtags",
  "comentario_ancla": "empathetic 2 line comment no emojis inviting community"
}}'''
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user','content':prompt}],
        response_format={'type':'json_object'},
        temperature=0.85
    )
    return json.loads(resp.choices[0].message.content, strict=False)

async def tts_con_srt(texto, audio_file, srt_file, voz):
    import edge_tts
    texto_limpio = limpiar_texto_voz(texto)
    communicate = edge_tts.Communicate(texto_limpio, voz, rate=VOZ_RATE, pitch=VOZ_PITCH, volume=VOZ_VOLUME)
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
    print(f'TTS [{voz}]: {len(audio_data)} bytes | {len(words)} palabras')
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
        print(f'SRT: {len(grupos)} grupos OK')
        return True
    return False

def get_audio_duration(audio_file):
    result = subprocess.run(
        ['ffprobe','-v','quiet','-print_format','json','-show_format',audio_file],
        capture_output=True, text=True)
    try:
        return float(json.loads(result.stdout)['format']['duration'])
    except:
        return 60.0

def get_music_file():
    carpeta = 'assets/music_small'
    if not os.path.exists(carpeta): return None
    archivos = [os.path.join(carpeta,f) for f in os.listdir(carpeta) if f.lower().endswith('.mp3')]
    return random.choice(archivos) if archivos else None

def mezclar_audio(voz_mp3, musica, salida, vol=0.08):
    import shutil
    ok = run_ffmpeg([
        'ffmpeg','-y','-i',voz_mp3,'-i',musica,
        '-filter_complex',
        f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];[1:a]volume={vol},aformat=sample_rates=44100:channel_layouts=stereo,aloop=loop=-1:size=2e+09[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[out]',
        '-map','[out]','-c:a','aac','-b:a','128k','-ar','44100',salida
    ], 'mezcla')
    if not ok or not os.path.exists(salida) or os.path.getsize(salida) < 1000:
        shutil.copy(voz_mp3, salida)
        print('Mezcla fallida - solo voz')

def agregar_marca_agua(video_in, video_out, w=1280, h=720):
    try:
        font_size = 28 if w == 1280 else 20
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except:
        font = ImageFont.load_default()
    img = Image.new('RGBA', (w, 50), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        bbox = draw.textbbox((0,0), CHANNEL_HANDLE, font=font)
        tw = bbox[2]-bbox[0]
    except:
        tw = len(CHANNEL_HANDLE)*14
    x = (w-tw)//2
    draw.text((x+2,10), CHANNEL_HANDLE, font=font, fill=(0,0,0,160))
    draw.text((x,8), CHANNEL_HANDLE, font=font, fill=(255,255,255,210))
    marca_path = '/tmp/marca_agua.png'
    img.save(marca_path)
    ok = run_ffmpeg([
        'ffmpeg','-y','-i',video_in,'-i',marca_path,
        '-filter_complex',f'[1:v]scale={w}:50[wm];[0:v][wm]overlay=(W-w)/2:8',
        '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast',video_out
    ], 'marca_agua')
    return ok and os.path.exists(video_out) and os.path.getsize(video_out) > 10000

def crear_thumbnail(titulo, archivo, paleta=None):
    if not paleta: paleta = random.choice(PALETAS)
    W, H = 1280, 720
    img = Image.new('RGB', (W,H), color=paleta['fondo'])
    draw = ImageDraw.Draw(img)
    for i in range(H):
        factor = i/H
        r = min(255, paleta['fondo'][0]+int(factor*35))
        g = min(255, paleta['fondo'][1]+int(factor*25))
        b = min(255, paleta['fondo'][2]+int(factor*45))
        draw.line([(0,i),(W,i)], fill=(r,g,b))
    for i in range(0,W,45):
        draw.line([(i,0),(i,H)], fill=(min(255,paleta['fondo'][0]+12),min(255,paleta['fondo'][1]+8),min(255,paleta['fondo'][2]+18)), width=1)
    for i in range(0,H,45):
        draw.line([(0,i),(W,i)], fill=(min(255,paleta['fondo'][0]+12),min(255,paleta['fondo'][1]+8),min(255,paleta['fondo'][2]+18)), width=1)
    draw.rectangle([0,0,W,6], fill=paleta['acento'])
    draw.rectangle([0,H-6,W,H], fill=paleta['acento'])
    draw.rectangle([0,0,6,H], fill=paleta['acento'])
    draw.rectangle([W-6,0,W,H], fill=paleta['acento'])
    draw.rectangle([50,85,W-50,H-65], fill=(0,0,0))
    draw.rectangle([53,88,W-53,H-68], fill=(max(0,paleta['fondo'][0]-5),max(0,paleta['fondo'][1]-5),max(0,paleta['fondo'][2]-5)))
    draw.rectangle([50,85,W-50,91], fill=paleta['acento'])
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 76)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
    titulo_limpio = re.sub(r'[^\w\s\?!.,]', '', titulo).strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea+' '+p).strip()
        try:
            if draw.textbbox((0,0),test,font=font_big)[2] < W-140: linea=test
            else:
                if linea: lineas.append(linea)
                linea=p
        except: linea=test
    if linea: lineas.append(linea)
    total_h = len(lineas)*88
    y = (H-total_h)//2-20
    for ln in lineas:
        try: tw=draw.textbbox((0,0),ln,font=font_big)[2]
        except: tw=len(ln)*38
        for dx,dy in [(4,4),(3,3)]:
            draw.text(((W-tw)//2+dx,y+dy),ln,font=font_big,fill=(0,0,0))
        draw.text(((W-tw)//2,y),ln,font=font_big,fill=paleta['texto'])
        y += 88
    draw.rectangle([90,H-60,W-90,H-55], fill=paleta['acento'])
    try: tw2=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_med)[2]
    except: tw2=300
    draw.text(((W-tw2)//2,H-52),CHANNEL_HANDLE,font=font_med,fill=paleta['acento'])
    img.save(archivo, quality=95)

def agregar_subtitulos(video_in, srt_file, video_out, fontsize=20, margenv=40):
    if not srt_file or not os.path.exists(srt_file) or os.path.getsize(srt_file)<10:
        return False
    srt_esc = srt_file.replace('\\','/').replace(':','\\:')
    style = (f"FontName=Arial,FontSize={fontsize},PrimaryColour=&H00FFFFFF,"
             f"OutlineColour=&H00000000,Outline=3,Shadow=1,Bold=1,Alignment=2,MarginV={margenv}")
    ok = run_ffmpeg([
        'ffmpeg','-y','-i',video_in,
        '-vf',f"subtitles='{srt_esc}':force_style='{style}'",
        '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast',video_out
    ], 'subs')
    return ok and os.path.exists(video_out) and os.path.getsize(video_out)>10000

def crear_video(audio_file, srt_file, videos, output_file, w=1280, h=720, is_short=False):
    duracion = get_audio_duration(audio_file)
    print(f'Creando video {w}x{h} | Audio: {duracion:.1f}s')
    dur_clip = 9
    n_clips = max(3, int(duracion/dur_clip)+3)
    clips = []
    pool = videos*(n_clips//max(len(videos),1)+3)
    for i in range(n_clips):
        src = pool[i%len(pool)]
        clip = f'/tmp/clip_{w}_{i}.mp4'
        vf = f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
        ok = run_ffmpeg(['ffmpeg','-y','-i',src,'-vf',vf,'-t',str(dur_clip),
            '-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',clip], f'clip_{i}')
        if os.path.exists(clip) and os.path.getsize(clip)>5000:
            clips.append(clip)
    if not clips:
        print('ERROR: Sin clips'); sys.exit(1)
    lista = f'/tmp/lista_{w}.txt'
    with open(lista,'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    video_mudo = f'/tmp/mudo_{w}.mp4'
    run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista,
        '-c:v','libx264','-pix_fmt','yuv420p',video_mudo], 'concat')
    video_subs = f'/tmp/subs_{w}.mp4'
    subs_ok = agregar_subtitulos(video_mudo, srt_file, video_subs,
        18 if not is_short else 16, 40 if not is_short else 55)
    video_base = video_subs if subs_ok else video_mudo
    video_marca = f'/tmp/marca_{w}.mp4'
    marca_ok = agregar_marca_agua(video_base, video_marca, w, h)
    video_final = video_marca if marca_ok else video_base
    run_ffmpeg(['ffmpeg','-y','-i',video_final,'-i',audio_file,
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac',
        '-b:a','192k' if not is_short else '128k','-shortest',output_file], 'final')
    size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
    print(f'Video OK: {size//1024}KB | subs:{"si" if subs_ok else "no"} | marca:{"si" if marca_ok else "no"}')

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False, idioma='es'):
    if not os.path.exists(video_file) or os.path.getsize(video_file)<10000:
        print(f'ERROR: {video_file} invalido'); sys.exit(1)
    if is_short and '#Shorts' not in titulo:
        titulo = titulo+' #Shorts'
    body = {
        'snippet': {
            'title': titulo[:100], 'description': descripcion,
            'tags': tags, 'categoryId': '26',
            'defaultLanguage': idioma, 'defaultAudioLanguage': idioma
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
        youtube.commentThreads().insert(part='snippet', body={
            'snippet': {'videoId': video_id,
                'topLevelComment': {'snippet': {'textOriginal': comentario}}}
        }).execute()
        print('Comentario OK')
    except Exception as e:
        print(f'Comentario error: {e}')

def main():
    send_telegram('🧠 <b>SaludMentalReal</b> — Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)

    print('Descargando videos Pexels...')
    videos_h = descargar_videos_pexels(QUERIES_PEXELS_H, 'landscape', 5)
    videos_v = descargar_videos_pexels(QUERIES_PEXELS_V, 'portrait', 3)

    if not videos_h or not videos_v:
        send_telegram('ERROR: Sin videos disponibles')
        sys.exit(1)

    musica = get_music_file()
    youtube = get_youtube()

    # Obtener o crear playlists (una sola vez, no duplicar)
    pl_es = obtener_o_crear_playlist(youtube, PLAYLIST_ES_NAME,
        'Videos de psicologia y bienestar emocional en español latino', 'es')
    pl_en = obtener_o_crear_playlist(youtube, PLAYLIST_EN_NAME,
        'Psychology and emotional wellness videos in English', 'en')

    # Generar contenido ES e IN paralelo
    tema_es = random.choice(TEMAS_ES)
    tema_en = random.choice(TEMAS_EN)
    print(f'Tema ES: {tema_es}')
    print(f'Tema EN: {tema_en}')

    datos_es = generar_guion(tema_es, 'es')
    datos_en = generar_guion(tema_en, 'en')

    # TTS
    audio_es = '/tmp/smr/audio_es.mp3'
    srt_es = '/tmp/subs_es.srt'
    asyncio.run(tts_con_srt(datos_es['guion'], audio_es, srt_es, VOZ_ES))

    audio_es_short = '/tmp/smr/audio_es_short.mp3'
    srt_es_short = '/tmp/subs_es_short.srt'
    asyncio.run(tts_con_srt(datos_es['guion_short'], audio_es_short, srt_es_short, VOZ_ES))

    audio_en = '/tmp/smr/audio_en.mp3'
    srt_en = '/tmp/subs_en.srt'
    asyncio.run(tts_con_srt(datos_en['guion'], audio_en, srt_en, VOZ_EN))

    audio_en_short = '/tmp/smr/audio_en_short.mp3'
    srt_en_short = '/tmp/subs_en_short.srt'
    asyncio.run(tts_con_srt(datos_en['guion_short'], audio_en_short, srt_en_short, VOZ_EN))

    # Mezcla audio
    def mix(voz, salida):
        if musica: mezclar_audio(voz, musica, salida)
        else:
            import shutil; shutil.copy(voz, salida)

    largo_es = '/tmp/smr/largo_es.mp3'
    short_es_audio = '/tmp/smr/short_es.mp3'
    largo_en = '/tmp/smr/largo_en.mp3'
    short_en_audio = '/tmp/smr/short_en.mp3'
    mix(audio_es, largo_es)
    mix(audio_es_short, short_es_audio)
    mix(audio_en, largo_en)
    mix(audio_en_short, short_en_audio)

    # Thumbnails
    thumb_es = '/tmp/smr/thumb_es.jpg'
    thumb_en = '/tmp/smr/thumb_en.jpg'
    crear_thumbnail(datos_es['titulo'], thumb_es)
    crear_thumbnail(datos_en['titulo'], thumb_en)

    # Crear videos
    vid_largo_es = '/tmp/smr/video_largo_es.mp4'
    crear_video(largo_es, srt_es, videos_h, vid_largo_es, 1280, 720)

    vid_short_es = '/tmp/smr/video_short_es.mp4'
    crear_video(short_es_audio, srt_es_short, videos_v, vid_short_es, 608, 1080, True)

    vid_largo_en = '/tmp/smr/video_largo_en.mp4'
    crear_video(largo_en, srt_en, videos_h, vid_largo_en, 1280, 720)

    vid_short_en = '/tmp/smr/video_short_en.mp4'
    crear_video(short_en_audio, srt_en_short, videos_v, vid_short_en, 608, 1080, True)

    # Subir video largo ES
    id_es = subir_youtube(youtube, vid_largo_es, datos_es['titulo'],
        datos_es['descripcion'], datos_es['tags'], thumb_es, idioma='es')
    agregar_comentario(youtube, id_es, datos_es.get('comentario_ancla', random.choice(COMENTARIOS_ES)))
    agregar_a_playlist(youtube, id_es, pl_es)
    send_telegram(f'✅ <b>Video ES</b>\n{datos_es["titulo"]}\nhttps://youtu.be/{id_es}')

    # Subir short ES
    id_short_es = subir_youtube(youtube, vid_short_es, datos_es['titulo_short'],
        datos_es['descripcion'], datos_es['tags'], is_short=True, idioma='es')
    agregar_comentario(youtube, id_short_es, random.choice(COMENTARIOS_ES))
    agregar_a_playlist(youtube, id_short_es, pl_es)
    send_telegram(f'✅ <b>Short ES</b>\n{datos_es["titulo_short"]}\nhttps://youtu.be/{id_short_es}')

    # Subir video largo EN
    id_en = subir_youtube(youtube, vid_largo_en, datos_en['titulo'],
        datos_en['descripcion'], datos_en['tags'], thumb_en, idioma='en')
    agregar_comentario(youtube, id_en, datos_en.get('comentario_ancla', random.choice(COMENTARIOS_EN)))
    agregar_a_playlist(youtube, id_en, pl_en)
    send_telegram(f'✅ <b>Video EN</b>\n{datos_en["titulo"]}\nhttps://youtu.be/{id_en}')

    # Subir short EN
    id_short_en = subir_youtube(youtube, vid_short_en, datos_en['titulo_short'],
        datos_en['descripcion'], datos_en['tags'], is_short=True, idioma='en')
    agregar_comentario(youtube, id_short_en, random.choice(COMENTARIOS_EN))
    agregar_a_playlist(youtube, id_short_en, pl_en)
    send_telegram(f'✅ <b>Short EN</b>\n{datos_en["titulo_short"]}\nhttps://youtu.be/{id_short_en}')

    send_telegram(f'🎉 <b>SaludMentalReal</b> — 4 videos publicados\nES: {tema_es}\nEN: {tema_en}')

if __name__ == '__main__':
    main()