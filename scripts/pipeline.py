import os, json, pickle, random, asyncio, requests, subprocess, base64, sys, re
from datetime import datetime, timedelta
from groq import Groq
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
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
VOZ_VOLUME = '+15%'
PLAYLIST_ES_NAME = 'Salud Mental en Espanol'
PLAYLIST_EN_NAME = 'Mental Health English'
SERIE_ES_NAME = '30 Dias de Salud Mental'

TEMAS_ES = [
    'como controlar la ansiedad en momentos de crisis',
    'tecnicas de respiracion para calmar el estres',
    'como dormir mejor cuando la mente no para',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de burnout y como recuperarte',
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
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de que necesitas ayuda psicologica',
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
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de inmadurez emocional',
    'como sanar relaciones toxicas',
    'el miedo al rechazo y como vencerlo',
    'por que te saboteas inconscientemente',
    'duelo emocional lo que nadie te prepara para sentir',
    'por que te cuesta pedir ayuda',
    'como sobrevivir una crisis de ansiedad nocturna',
    'que es la ansiedad generalizada y como tratarla',
    'por que lloras sin razon',
    'como dejar de compararte en redes sociales',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de trauma emocional sin saberlo',
    'como manejar la soledad cuando vives solo',
    'por que sientes que no encajas en ningun lado',
    'como recuperar la motivacion cuando todo da igual',
    'el agotamiento emocional que nadie ve',
    'como dejar de ser tan duro contigo mismo',
    'por que te cuesta ser feliz aunque tengas todo',
    'como superar el miedo al fracaso',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de que necesitas terapia urgente',
    'como manejar relacion con alguien deprimido',
    'por que la ansiedad aparece de noche',
    'como hablar de salud mental sin que te juzguen',
    'el poder de decir no sin sentirte mal',
    'como salir del ciclo de la negatividad',
    'por que tienes miedo al exito',
    'como construir autoestima desde cero',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de que una relacion daÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±a tu salud mental',
    'como manejar los celos sin destruir tu relacion',
    'por que te sientes culpable de ser feliz',
    'como superar la traicion de alguien que amabas',
    'el efecto del alcohol en tu salud mental',
    'como dejar de pensar demasiado overthinking',
    'por que evitas el conflicto aunque te lastime',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de que eres altamente sensible',
    'como manejar la ansiedad en el trabajo',
    'por que te cuesta perdonar de verdad',
    'el impacto de la familia toxica en tu salud mental',
    'como sanar el miedo al abandono en adultos',
    'por que te autosaboteas en el amor',
    'seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de codependencia emocional',
    'como meditar cuando tu mente no para',
    'por que el ejercicio ayuda mas que un antidepresivo',
    'como manejar la ansiedad social en eventos',
    'por que sientes que no mereces ser amado',
    'como salir de la depresion cuando no tienes fuerzas',
    'el papel de la alimentacion en tu salud mental',
    'como manejar crisis emocionales en el trabajo',
    'por que te sientes solo rodeado de personas'
]

SERIE_30_DIAS = [
    'Dia 1: reconoce tus emociones sin juzgarlas',
    'Dia 2: el poder de respirar conscientemente',
    'Dia 3: como identificar tus pensamientos negativos',
    'Dia 4: la importancia del descanso para tu mente',
    'Dia 5: aprende a decir no sin sentir culpa',
    'Dia 6: como hablar contigo mismo con amor',
    'Dia 7: el primer paso para sanar relaciones toxicas',
    'Dia 8: como manejar la ansiedad en el momento',
    'Dia 9: construye una rutina que te de paz',
    'Dia 10: el poder del movimiento para tu salud mental',
    'Dia 11: como dejar de compararte con otros',
    'Dia 12: aprende a perdonarte a ti mismo',
    'Dia 13: como manejar el miedo al rechazo',
    'Dia 14: la semana 2 lo que has logrado hasta hoy',
    'Dia 15: como salir del ciclo de la negatividad',
    'Dia 16: el poder de escribir tus emociones',
    'Dia 17: como manejar la soledad sin que te lastime',
    'Dia 18: aprende a pedir ayuda sin verguenza',
    'Dia 19: como sanar tu autoestima dia a dia',
    'Dia 20: el impacto de la alimentacion en tu mente',
    'Dia 21: como manejar conflictos sin perder la calma',
    'Dia 22: el poder de la gratitud para tu salud mental',
    'Dia 23: como lidiar con personas que te drenan',
    'Dia 24: aprende a vivir el presente sin ansiedad',
    'Dia 25: como reconstruirte despues de una crisis',
    'Dia 26: el rol del sueno en tu bienestar emocional',
    'Dia 27: como mantener limites saludables',
    'Dia 28: aprende a celebrar tus pequeÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±os avances',
    'Dia 29: como prepararte para los dias dificiles',
    'Dia 30: has llegado lejos lo que sigue en tu camino'
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
    'stress relief nature', 'emotional healing peaceful', 'counseling support',
    'person meditating park', 'calm woman nature', 'man breathing outdoor',
    'peaceful river nature', 'person stretching morning', 'wellness spa calm',
    'nature birds peaceful', 'sunrise mountains calm', 'person reading calm',
    'green nature peaceful morning'
]

QUERIES_PEXELS_V = [
    'meditation vertical calm', 'person breathing vertical', 'nature vertical peaceful',
    'yoga vertical wellness', 'mindfulness vertical', 'forest vertical nature',
    'ocean vertical waves', 'person thinking vertical', 'wellness vertical nature',
    'calm vertical portrait', 'woman meditating vertical', 'man nature vertical',
    'sunrise vertical peaceful', 'rain vertical nature', 'flowers vertical calm',
    'person walking vertical', 'breathing vertical outdoor', 'tree vertical nature',
    'mountain vertical calm', 'river vertical peaceful'
]

COMENTARIOS_ES = [
    'Estoy aqui para escucharte. Te identificas con esto? Cuentame abajo, no estas solo.',
    'Alguna vez sentiste exactamente esto? Tu historia puede ayudar a alguien mas. Escribela abajo.',
    'Este video es para quien lo necesita hoy. A quien se lo enviarias?',
    'Que parte de este video te llego mas? Cuentame, leo todos los comentarios.',
    'El primer paso para sanar es hablarlo. Como te sientes hoy? Escribelo aqui.',
]

COMENTARIOS_EN = [
    'I am here to listen. Does this resonate with you? Tell me below, you are not alone.',
    'Have you ever felt exactly this? Your story might help someone else. Share it below.',
    'Which part of this video hit you the most? Tell me, I read every comment.',
]

COMMUNITY_POSTS_ES = [
    'Pregunta del dia: Cual es la cosa mas pequeÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±a que puedes hacer HOY por tu salud mental?',
    'Del 1 al 10, como esta tu salud mental esta semana? Sin juicios, escribe tu numero abajo.',
    'Comparte una cosa que te ayuda cuando la ansiedad ataca. Puede salvar a alguien.',
    'Sabias que 1 de cada 4 personas sufre un trastorno mental? No estas solo.',
    'Si pudieras darle un consejo a tu yo de hace 5 aÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±os sobre salud mental, cual seria?',
]

PALETAS = [
    {'fondo': (8,15,45), 'acento': (0,200,255), 'texto': (255,255,255)},
    {'fondo': (45,8,15), 'acento': (255,80,80), 'texto': (255,255,255)},
    {'fondo': (8,35,15), 'acento': (0,220,100), 'texto': (255,255,255)},
    {'fondo': (30,8,45), 'acento': (180,80,255), 'texto': (255,255,255)},
    {'fondo': (40,25,5), 'acento': (255,160,0), 'texto': (255,255,255)},
]

def detectar_fecha_especial():
    hoy = datetime.now()
    if hoy.day == 10 and hoy.month == 10: return 'dia_mundial_salud_mental'
    if hoy.day == 10 and hoy.month == 9: return 'dia_prevencion_suicidio'
    if hoy.weekday() == 0: return 'lunes_motivacional'
    return None

def get_tema_especial(tipo):
    temas = {
        'dia_mundial_salud_mental': ['hoy es el dia mundial de la salud mental por que importa tanto', 'dia mundial salud mental lo que todos debemos saber hoy'],
        'dia_prevencion_suicidio': ['como ayudar a alguien que esta pensando en rendirse', 'hablar salva vidas lo que debes saber hoy'],
        'lunes_motivacional': ['como empezar la semana con tu salud mental en orden', 'rutina de lunes para proteger tu mente toda la semana']
    }
    opciones = temas.get(tipo, [])
    return random.choice(opciones) if opciones else None

def limpiar_texto_voz(texto):
    texto = re.sub(r'[^\w\s\.,;:!?\-\(\)ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂºÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¼ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“ÃƒÆ’Ã†â€™Ãƒâ€¦Ã¢â‚¬Å“a-zA-Z0-9]', ' ', texto)
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

def buscar_playlist(youtube, nombre):
    try:
        resp = youtube.playlists().list(part='snippet', mine=True, maxResults=50).execute()
        for item in resp.get('items', []):
            if nombre.lower() in item['snippet']['title'].lower():
                return item['id']
    except: pass
    return None

def obtener_o_crear_playlist(youtube, nombre, descripcion, idioma='es'):
    pl_id = buscar_playlist(youtube, nombre)
    if pl_id:
        print(f'Playlist existente: {nombre}')
        return pl_id
    try:
        pl = youtube.playlists().insert(part='snippet,status', body={
            'snippet': {'title': nombre, 'description': descripcion, 'defaultLanguage': idioma},
            'status': {'privacyStatus': 'public'}
        }).execute()
        print(f'Playlist creada: {nombre}')
        return pl['id']
    except Exception as e:
        print(f'Playlist error: {e}')
        return None

def agregar_a_playlist(youtube, video_id, playlist_id):
    if not playlist_id: return
    try:
        youtube.playlistItems().insert(part='snippet', body={
            'snippet': {'playlistId': playlist_id, 'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}
        }).execute()
        print('Playlist OK')
    except Exception as e:
        print(f'Playlist add error: {e}')

def obtener_dia_serie():
    if os.path.exists('serie_dia.txt'):
        try: return min(int(open('serie_dia.txt').read().strip()), len(SERIE_30_DIAS))
        except: pass
    return 1

def avanzar_dia_serie():
    dia = obtener_dia_serie()
    nuevo = (dia % len(SERIE_30_DIAS)) + 1
    with open('serie_dia.txt', 'w') as f: f.write(str(nuevo))
    return dia

def publicar_community_post(youtube, texto):
    try:
        youtube.communityPosts().insert(part='snippet', body={
            'snippet': {'type': 'textPost', 'textOriginal': texto}
        }).execute()
        print('Community post OK')
    except Exception as e:
        print(f'Community post error: {e}')

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
            r = requests.get('https://api.pexels.com/videos/search', headers=headers,
                params={'query': query, 'orientation': orientacion, 'per_page': 15, 'size': 'medium'}, timeout=30)
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
                        for chunk in vr.iter_content(chunk_size=1024*1024): f.write(chunk)
                    if not os.path.exists(raw) or os.path.getsize(raw) < 100000: continue
                    proc = f'/tmp/pexels/proc_{orientacion}_{len(videos)}.mp4'
                    vf = 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1' if orientacion == 'landscape' else 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    ok = run_ffmpeg(['ffmpeg','-y','-i',raw,'-vf',vf,'-t','15','-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',proc], f'px_{len(videos)}')
                    if ok and os.path.exists(proc) and os.path.getsize(proc) > 50000:
                        videos.append(proc)
                        print(f'  Video {len(videos)}/{n} OK')
                except Exception as e:
                    print(f'  Error: {e}')
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
Estilo: empatico, directo, conversacional como un amigo cercano.
REGLA CRITICA: El guion sera leido por voz sintetica. CERO emojis, asteriscos, hashtags o simbolos. Solo texto limpio.

Tema: {tema}

Escribe el JSON con estos campos exactos:

titulo: titulo VIRAL en espaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ol. OBLIGATORIO: 2 emojis al inicio + pregunta dolorosa O numero O promesa concreta. Ejemplos: "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€¹Ã…â€œÃƒâ€šÃ‚Â° ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Por que sientes ansiedad sin razon? Esto te pasa", "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€šÃ‚Â§Ãƒâ€šÃ‚Â  5 seÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ales de que tu mente necesita ayuda YA", "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Deja de torturarte: 3 pasos para sanar HOY". Maximo 68 caracteres. Sin hashtags.

descripcion: 500 palabras. Primera linea pregunta que engancha. Segunda linea invita suscribirse. Parrafos con emojis. Capitulos: 0:00 Introduccion, 0:45 El problema real, 1:30 Por que te sucede, 2:45 3 soluciones, 4:00 Mensaje final. Recursos de crisis LATAM. 25 hashtags al final.

guion: Texto narrativo de 650 palabras MINIMO. SOLO TEXTO LIMPIO sin emojis sin simbolos. Estructura: primero un gancho impactante de 2 oraciones. Luego validacion de 3 parrafos. Luego explicacion de 3 parrafos. Luego 3 soluciones concretas cada una con 2 parrafos. Luego cierre motivador de 2 parrafos. Frases cortas max 12 palabras. Tono empatico y cercano.

guion_short: Texto de 110 palabras MINIMO. SOLO TEXTO LIMPIO. Gancho en primeras 2 oraciones. Desarrollo rapido. Pregunta final empatica.

titulo_short: titulo Short con 2 emojis max 48 caracteres sin hashtags.

tags: lista de 25 tags SEO en espaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ol e ingles mezclados.

comentario_ancla: comentario empatico 2 lineas sin emojis invitando a comentar.

Responde SOLO con JSON puro sin markdown.'''
    else:
        prompt = f'''You are a clinical psychologist with a viral YouTube channel.
Style: empathetic, direct, conversational. ZERO emojis in guion/guion_short.

Topic: {tema}

Write JSON with these exact fields:

titulo: VIRAL English title. REQUIRED: 2 emojis at start + painful question OR number OR concrete promise. Examples: "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€¹Ã…â€œÃƒâ€šÃ‚Â° Why Do You Feel Anxious for No Reason?", "ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€šÃ‚Â§Ãƒâ€šÃ‚Â  5 Signs Your Mind Needs Help NOW". Max 68 chars. No hashtags.

descripcion: 400 words. Engaging question first. Subscribe line. Emoji paragraphs. Chapters: 0:00 Introduction, 0:45 The problem, 1:30 Why it happens, 2:45 Solutions, 4:00 Hope. Crisis helplines. 20 hashtags.

guion: Narrative text of 550 words MINIMUM. CLEAN TEXT ONLY no emojis no symbols. Hook, validation, explanation, 3 solutions, closing. Short sentences max 12 words.

guion_short: Text of 90 words MINIMUM. CLEAN TEXT ONLY. Strong hook. Quick development. Empathetic question at end.

titulo_short: Short title 2 emojis max 48 chars no hashtags.

tags: list of 20 SEO tags.

comentario_ancla: empathetic 2 line comment no emojis.

Respond ONLY with pure JSON no markdown.'''

    resp = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=[{'role':'user','content':prompt}],
        response_format={'type':'json_object'},
        max_tokens=3000,
        temperature=0.85
    )
    datos = json.loads(resp.choices[0].message.content, strict=False)
    palabras_guion = len(datos.get('guion','').split())
    palabras_short = len(datos.get('guion_short','').split())
    print(f'Guion: {palabras_guion} palabras | Short: {palabras_short} palabras')
    return datos

async def tts_con_srt(texto, audio_file, srt_file, voz):
    import edge_tts
    texto_limpio = limpiar_texto_voz(texto)
    voz_rate = random.choice(['-8%','-10%','-12%'])
    voz_pitch = random.choice(['-3Hz','-4Hz','-5Hz'])
    print(f'TTS: {len(texto_limpio.split())} palabras | rate={voz_rate} pitch={voz_pitch}')
    communicate = edge_tts.Communicate(texto_limpio, voz, rate=voz_rate, pitch=voz_pitch, volume=VOZ_VOLUME)
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
    dur_aprox = len(audio_data) / 16000
    print(f'Audio: {len(audio_data)} bytes | ~{dur_aprox:.1f}s | {len(words)} palabras')
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
    result = subprocess.run(['ffprobe','-v','quiet','-print_format','json','-show_format',audio_file], capture_output=True, text=True)
    try:
        dur = float(json.loads(result.stdout)['format']['duration'])
        print(f'Duracion audio: {dur:.1f}s ({dur/60:.1f}min)')
        return dur
    except:
        return 60.0

def get_music_file():
    carpeta = 'assets/music_small'
    if not os.path.exists(carpeta): return None
    archivos = [os.path.join(carpeta,f) for f in os.listdir(carpeta) if f.lower().endswith('.mp3')]
    return random.choice(archivos) if archivos else None

def mezclar_audio(voz_mp3, musica, salida, vol=0.08):
    import shutil
    dur_voz = get_audio_duration(voz_mp3)
    if dur_voz < 30:
        print(f'ADVERTENCIA: Audio voz muy corto ({dur_voz:.1f}s) - usando solo voz')
        shutil.copy(voz_mp3, salida)
        return
    ok = run_ffmpeg([
        'ffmpeg','-y','-i',voz_mp3,'-i',musica,
        '-filter_complex',
        f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];[1:a]volume={vol},aformat=sample_rates=44100:channel_layouts=stereo,aloop=loop=-1:size=2e+09[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[out]',
        '-map','[out]','-c:a','aac','-b:a','128k','-ar','44100',salida
    ], 'mezcla')
    if not ok or not os.path.exists(salida) or os.path.getsize(salida) < 1000:
        shutil.copy(voz_mp3, salida)
        print('Mezcla fallida - solo voz')
    else:
        print(f'Mezcla OK: {os.path.getsize(salida)//1024}KB')

def crear_thumbnail(titulo, archivo, paleta=None):
    if not paleta: paleta = random.choice(PALETAS)
    W, H = 1280, 720
    img = Image.new('RGB', (W,H), color=paleta['fondo'])
    draw = ImageDraw.Draw(img)
    for i in range(H):
        factor = i/H
        r = min(255, paleta['fondo'][0]+int(factor*40))
        g = min(255, paleta['fondo'][1]+int(factor*30))
        b = min(255, paleta['fondo'][2]+int(factor*50))
        draw.line([(0,i),(W,i)], fill=(r,g,b))
    for i in range(0,W,50):
        draw.line([(i,0),(i,H)], fill=(min(255,paleta['fondo'][0]+8),min(255,paleta['fondo'][1]+6),min(255,paleta['fondo'][2]+12)), width=1)
    for i in range(0,H,50):
        draw.line([(0,i),(W,i)], fill=(min(255,paleta['fondo'][0]+8),min(255,paleta['fondo'][1]+6),min(255,paleta['fondo'][2]+12)), width=1)
    draw.rectangle([0,0,W,10], fill=paleta['acento'])
    draw.rectangle([0,H-10,W,H], fill=paleta['acento'])
    draw.rectangle([0,0,10,H], fill=paleta['acento'])
    draw.rectangle([W-10,0,W,H], fill=paleta['acento'])
    draw.rectangle([40,75,W-40,H-60], fill=(0,0,0))
    draw.rectangle([44,79,W-44,H-64], fill=(max(0,paleta['fondo'][0]-8),max(0,paleta['fondo'][1]-8),max(0,paleta['fondo'][2]-8)))
    draw.rectangle([40,75,W-40,83], fill=paleta['acento'])
    draw.rectangle([40,H-68,W-40,H-60], fill=paleta['acento'])
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 82)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
    titulo_limpio = re.sub(r'[^\w\s\?!.,ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â­ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂºÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¼ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“ÃƒÆ’Ã†â€™Ãƒâ€¦Ã¢â‚¬Å“]','',titulo).strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea+' '+p).strip()
        try:
            if draw.textbbox((0,0),test,font=font_big)[2] < W-120: linea=test
            else:
                if linea: lineas.append(linea)
                linea=p
        except: linea=test
    if linea: lineas.append(linea)
    total_h = len(lineas)*92
    y = (H-total_h)//2-15
    for ln in lineas:
        try: tw=draw.textbbox((0,0),ln,font=font_big)[2]
        except: tw=len(ln)*42
        for dx,dy in [(5,5),(4,4),(3,3)]:
            draw.text(((W-tw)//2+dx,y+dy),ln,font=font_big,fill=(0,0,0))
        draw.text(((W-tw)//2,y),ln,font=font_big,fill=(255,255,255))
        y += 92
    try: tw2=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_med)[2]
    except: tw2=300
    draw.text(((W-tw2)//2,H-56),CHANNEL_HANDLE,font=font_med,fill=paleta['acento'])
    img.save(archivo, quality=95)
    print('Thumbnail OK')

def agregar_marca_agua(video_in, video_out, w=1280, h=720):
    try:
        font_size = 26 if w == 1280 else 18
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except:
        font = ImageFont.load_default()
    img = Image.new('RGBA', (w,45), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        bbox = draw.textbbox((0,0),CHANNEL_HANDLE,font=font)
        tw = bbox[2]-bbox[0]
    except:
        tw = len(CHANNEL_HANDLE)*13
    x = (w-tw)//2
    draw.text((x+2,10),CHANNEL_HANDLE,font=font,fill=(0,0,0,150))
    draw.text((x,8),CHANNEL_HANDLE,font=font,fill=(255,255,255,200))
    marca_path = '/tmp/marca_agua.png'
    img.save(marca_path)
    ok = run_ffmpeg([
        'ffmpeg','-y','-i',video_in,'-i',marca_path,
        '-filter_complex',f'[1:v]scale={w}:45[wm];[0:v][wm]overlay=(W-w)/2:8',
        '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast',video_out
    ], 'marca_agua')
    return ok and os.path.exists(video_out) and os.path.getsize(video_out) > 10000

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
    if duracion < 30:
        print(f'ERROR: Audio muy corto ({duracion:.1f}s) - abortando video')
        return False
    dur_clip = 12
    n_clips = max(4, int(duracion/dur_clip)+4)
    print(f'Creando {n_clips} clips de {dur_clip}s para cubrir {duracion:.1f}s')
    clips = []
    pool = videos*(n_clips//max(len(videos),1)+3)
    for i in range(n_clips):
        src = pool[i%len(pool)]
        clip = f'/tmp/clip_{w}_{i}.mp4'
        vf = f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
        ok = run_ffmpeg(['ffmpeg','-y','-i',src,'-vf',vf,'-t',str(dur_clip),
            '-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',clip],f'clip_{i}')
        if os.path.exists(clip) and os.path.getsize(clip)>5000:
            clips.append(clip)
    if not clips:
        print('ERROR: Sin clips'); return False
    lista = f'/tmp/lista_{w}.txt'
    with open(lista,'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    video_mudo = f'/tmp/mudo_{w}.mp4'
    run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista,
        '-c:v','libx264','-pix_fmt','yuv420p',video_mudo],'concat')
    dur_video_mudo = get_audio_duration(video_mudo)
    print(f'Video mudo: {dur_video_mudo:.1f}s | Audio: {duracion:.1f}s')
    video_subs = f'/tmp/subs_{w}.mp4'
    subs_ok = agregar_subtitulos(video_mudo, srt_file, video_subs,
        18 if not is_short else 16, 40 if not is_short else 55)
    video_base = video_subs if subs_ok else video_mudo
    video_marca = f'/tmp/marca_{w}.mp4'
    marca_ok = agregar_marca_agua(video_base, video_marca, w, h)
    video_final = video_marca if marca_ok else video_base
    ok_final = run_ffmpeg(['ffmpeg','-y','-i',video_final,'-i',audio_file,
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac',
        '-b:a','192k' if not is_short else '128k','-shortest',output_file],'final')
    if ok_final and os.path.exists(output_file):
        size = os.path.getsize(output_file)
        dur_final = get_audio_duration(output_file)
        print(f'Video final: {size//1024}KB | {dur_final:.1f}s | subs:{"si" if subs_ok else "no"} | marca:{"si" if marca_ok else "no"}')
        return True
    return False

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False, idioma='es'):
    if not os.path.exists(video_file) or os.path.getsize(video_file)<10000:
        print(f'ERROR: {video_file} invalido'); return None
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
    if not video_id: return
    try:
        youtube.commentThreads().insert(part='snippet', body={
            'snippet': {'videoId': video_id,
                'topLevelComment': {'snippet': {'textOriginal': comentario}}}
        }).execute()
        print('Comentario OK')
    except Exception as e:
        print(f'Comentario error: {e}')

def enviar_reporte_analytics(youtube):
    try:
        if datetime.now().weekday() != 0: return
        from googleapiclient.discovery import build as gbuild
        analytics = gbuild('youtubeAnalytics', 'v2', credentials=youtube._http.credentials)
        hoy = datetime.now().strftime('%Y-%m-%d')
        hace7 = (datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')
        resp = analytics.reports().query(
            ids='channel==MINE', startDate=hace7, endDate=hoy,
            metrics='views,estimatedMinutesWatched,subscribersGained', dimensions='day'
        ).execute()
        rows = resp.get('rows', [])
        views = sum(int(r[1]) for r in rows)
        watch = sum(int(r[2]) for r in rows)
        subs = sum(int(r[3]) for r in rows)
        send_telegram(f'ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒâ€¦Ã‚Â  <b>Reporte Semanal</b>\nÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸ÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“Ãƒâ€šÃ‚Â Vistas: {views:,}\nÃƒÆ’Ã‚Â¢Ãƒâ€šÃ‚ÂÃƒâ€šÃ‚Â± Horas: {watch//60:,}h\nÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸ÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“Ãƒâ€šÃ‚Â¥ Subs: +{subs:,}')
    except Exception as e:
        print(f'Analytics error: {e}')

def main():
    send_telegram('ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€šÃ‚Â§Ãƒâ€šÃ‚Â  <b>SaludMentalReal</b> ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)

    print('Descargando videos Pexels...')
    videos_h = descargar_videos_pexels(QUERIES_PEXELS_H, 'landscape', 5)
    videos_v = descargar_videos_pexels(QUERIES_PEXELS_V, 'portrait', 3)
    if not videos_h or not videos_v:
        send_telegram('ERROR: Sin videos'); sys.exit(1)

    musica = get_music_file()
    youtube = get_youtube()

    pl_es = obtener_o_crear_playlist(youtube, PLAYLIST_ES_NAME, 'Videos psicologia bienestar emocional espaÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â±ol', 'es')
    pl_en = obtener_o_crear_playlist(youtube, PLAYLIST_EN_NAME, 'Psychology emotional wellness English', 'en')
    pl_serie = obtener_o_crear_playlist(youtube, SERIE_ES_NAME, 'Serie 30 dias salud mental', 'es')

    dia_serie = obtener_dia_serie()
    tema_serie = SERIE_30_DIAS[dia_serie-1]
    fecha_especial = detectar_fecha_especial()
    tema_especial = get_tema_especial(fecha_especial) if fecha_especial else None
    tema_es = tema_especial if tema_especial else random.choice(TEMAS_ES)
    tema_en = random.choice(TEMAS_EN)
    if fecha_especial: print(f'Fecha especial: {fecha_especial}')
    print(f'ES: {tema_es} | Serie dia {dia_serie} | EN: {tema_en}')

    datos_es = generar_guion(tema_es, 'es')
    datos_serie = generar_guion(tema_serie, 'es')
    datos_en = generar_guion(tema_en, 'en')

    audio_es='/tmp/smr/audio_es.mp3'; srt_es='/tmp/subs_es.srt'
    asyncio.run(tts_con_srt(datos_es['guion'], audio_es, srt_es, VOZ_ES))
    audio_es_s='/tmp/smr/audio_es_s.mp3'; srt_es_s='/tmp/subs_es_s.srt'
    asyncio.run(tts_con_srt(datos_es['guion_short'], audio_es_s, srt_es_s, VOZ_ES))
    audio_serie='/tmp/smr/audio_serie.mp3'; srt_serie='/tmp/subs_serie.srt'
    asyncio.run(tts_con_srt(datos_serie['guion'], audio_serie, srt_serie, VOZ_ES))
    audio_en='/tmp/smr/audio_en.mp3'; srt_en='/tmp/subs_en.srt'
    asyncio.run(tts_con_srt(datos_en['guion'], audio_en, srt_en, VOZ_EN))
    audio_en_s='/tmp/smr/audio_en_s.mp3'; srt_en_s='/tmp/subs_en_s.srt'
    asyncio.run(tts_con_srt(datos_en['guion_short'], audio_en_s, srt_en_s, VOZ_EN))

    def mix(voz, salida):
        if musica: mezclar_audio(voz, musica, salida)
        else:
            import shutil; shutil.copy(voz, salida)

    l_es='/tmp/smr/l_es.mp3'; s_es='/tmp/smr/s_es.mp3'
    l_serie='/tmp/smr/l_serie.mp3'
    l_en='/tmp/smr/l_en.mp3'; s_en='/tmp/smr/s_en.mp3'
    mix(audio_es,l_es); mix(audio_es_s,s_es)
    mix(audio_serie,l_serie)
    mix(audio_en,l_en); mix(audio_en_s,s_en)

    thumb_es='/tmp/smr/thumb_es.jpg'
    thumb_serie='/tmp/smr/thumb_serie.jpg'
    thumb_en='/tmp/smr/thumb_en.jpg'
    crear_thumbnail(datos_es['titulo'], thumb_es)
    crear_thumbnail(datos_serie['titulo'], thumb_serie)
    crear_thumbnail(datos_en['titulo'], thumb_en)

    v_l_es='/tmp/smr/v_l_es.mp4'
    ok_l_es = crear_video(l_es, srt_es, videos_h, v_l_es, 1280, 720)
    v_s_es='/tmp/smr/v_s_es.mp4'
    ok_s_es = crear_video(s_es, srt_es_s, videos_v, v_s_es, 608, 1080, True)
    v_serie='/tmp/smr/v_serie.mp4'
    ok_serie = crear_video(l_serie, srt_serie, videos_h, v_serie, 1280, 720)
    v_l_en='/tmp/smr/v_l_en.mp4'
    ok_l_en = crear_video(l_en, srt_en, videos_h, v_l_en, 1280, 720)
    v_s_en='/tmp/smr/v_s_en.mp4'
    ok_s_en = crear_video(s_en, srt_en_s, videos_v, v_s_en, 608, 1080, True)

    if ok_l_es:
        id_es = subir_youtube(youtube, v_l_es, datos_es['titulo'], datos_es['descripcion'], datos_es['tags'], thumb_es, idioma='es')
        if id_es:
            agregar_comentario(youtube, id_es, datos_es.get('comentario_ancla', random.choice(COMENTARIOS_ES)))
            agregar_a_playlist(youtube, id_es, pl_es)
            send_telegram(f'ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ <b>Video ES</b>\n{datos_es["titulo"]}\nhttps://youtu.be/{id_es}')

    if ok_s_es:
        id_s_es = subir_youtube(youtube, v_s_es, datos_es['titulo_short'], datos_es['descripcion'], datos_es['tags'], is_short=True, idioma='es')
        if id_s_es:
            agregar_comentario(youtube, id_s_es, random.choice(COMENTARIOS_ES))
            agregar_a_playlist(youtube, id_s_es, pl_es)
            send_telegram(f'ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ <b>Short ES</b>\nhttps://youtu.be/{id_s_es}')

    if ok_serie:
        id_serie = subir_youtube(youtube, v_serie, datos_serie['titulo'], datos_serie['descripcion'], datos_serie['tags'], thumb_serie, idioma='es')
        if id_serie:
            agregar_comentario(youtube, id_serie, f'Este es el dia {dia_serie} de nuestra serie. Manana viene el siguiente paso. Nos vemos aqui.')
            agregar_a_playlist(youtube, id_serie, pl_serie)
            agregar_a_playlist(youtube, id_serie, pl_es)
            avanzar_dia_serie()
            send_telegram(f'ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ <b>Serie Dia {dia_serie}</b>\n{datos_serie["titulo"]}\nhttps://youtu.be/{id_serie}')

    if ok_l_en:
        id_en = subir_youtube(youtube, v_l_en, datos_en['titulo'], datos_en['descripcion'], datos_en['tags'], thumb_en, idioma='en')
        if id_en:
            agregar_comentario(youtube, id_en, datos_en.get('comentario_ancla', random.choice(COMENTARIOS_EN)))
            agregar_a_playlist(youtube, id_en, pl_en)
            send_telegram(f'ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ <b>Video EN</b>\n{datos_en["titulo"]}\nhttps://youtu.be/{id_en}')

    if ok_s_en:
        id_s_en = subir_youtube(youtube, v_s_en, datos_en['titulo_short'], datos_en['descripcion'], datos_en['tags'], is_short=True, idioma='en')
        if id_s_en:
            agregar_comentario(youtube, id_s_en, random.choice(COMENTARIOS_EN))
            agregar_a_playlist(youtube, id_s_en, pl_en)
            send_telegram(f'ÃƒÆ’Ã‚Â¢Ãƒâ€¦Ã¢â‚¬Å“ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ <b>Short EN</b>\nhttps://youtu.be/{id_s_en}')

    publicar_community_post(youtube, random.choice(COMMUNITY_POSTS_ES))
    enviar_reporte_analytics(youtube)
    send_telegram(f'ÃƒÆ’Ã‚Â°Ãƒâ€¦Ã‚Â¸Ãƒâ€¦Ã‚Â½ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â° <b>SaludMentalReal</b> ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Completado\nES: {tema_es}\nSerie dia {dia_serie}\nEN: {tema_en}')

if __name__ == '__main__':
    main()