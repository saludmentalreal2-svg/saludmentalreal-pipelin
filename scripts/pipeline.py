import os, json, pickle, random, asyncio, requests, subprocess, base64, sys, time
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
VOZ = 'es-MX-JorgeNeural'
VOZ_RATE = '-8%'
VOZ_PITCH = '-3Hz'
VOZ_VOLUME = '+10%'

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
    'como sobrevivir a una crisis de ansiedad nocturna',
    'que es la ansiedad generalizada y como tratarla',
    'por que lloras sin razon y que significa',
    'como dejar de compararte con los demas en redes sociales',
    'señales de que tienes trauma emocional sin saberlo',
    'como manejar la soledad cuando vives solo',
    'por que sientes que no encajas en ningun lado',
    'como recuperar la motivacion cuando todo te da igual',
    'el agotamiento emocional que nadie ve pero todos sienten',
    'como dejar de ser tan duro contigo mismo',
    'por que te cuesta trabajo ser feliz aunque tengas todo',
    'como superar el miedo al fracaso paso a paso',
    'señales de que necesitas terapia urgentemente',
    'como manejar una relacion con alguien deprimido',
    'por que la ansiedad aparece de noche y como calmarla',
    'como hablar de salud mental sin que te juzguen',
    'el poder de decir no sin sentirte mal persona',
    'como salir del ciclo de la negatividad mental',
    'por que tienes miedo al exito y no solo al fracaso',
    'como construir autoestima desde cero cuando esta destruida',
    'señales de que una relacion te esta dañando la salud mental',
    'como manejar los celos sin destruir tu relacion',
    'por que te sientes culpable de ser feliz',
    'como superar la traicion de alguien que amabas',
    'el efecto del alcohol en tu salud mental real',
    'como dejar de pensar demasiado en todo overthinking',
    'por que evitas el conflicto aunque te este lastimando',
    'como hablar con tus hijos sobre salud mental',
    'señales de que eres una persona altamente sensible',
    'como manejar la ansiedad en el trabajo sin renunciar',
    'por que te cuesta perdonar y como hacerlo de verdad',
    'como vivir con alguien que tiene depresion',
    'el impacto de la familia toxica en tu salud mental',
    'como sanar el miedo al abandono en adultos',
    'por que te autosaboteas en el amor',
    'como manejar la ira sin explotar contra los que amas',
    'señales de codependencia emocional y como salir',
    'como meditar cuando tu mente no para ni un segundo',
    'por que el ejercicio es mejor que cualquier antidepresivo',
    'como manejar la ansiedad social en reuniones y eventos'
]

QUERIES_PEXELS_H = [
    'therapy session calm', 'meditation nature peaceful', 'breathing exercise wellness',
    'mental health psychology', 'calm person thinking', 'nature forest peaceful',
    'sunrise morning peaceful', 'yoga meditation outdoor', 'person journaling calm',
    'counseling support mental health', 'mindfulness breathing', 'peaceful lake nature',
    'person walking nature', 'calm ocean waves', 'mental wellness therapy'
]

QUERIES_PEXELS_V = [
    'meditation vertical', 'person breathing calm vertical', 'nature vertical peaceful',
    'therapy vertical wellness', 'mindfulness vertical', 'yoga vertical calm',
    'person thinking vertical', 'forest vertical nature', 'ocean vertical waves',
    'mental health vertical'
]

COMENTARIOS_FIJOS = [
    'Estoy aqui para escucharte. Cuéntame en los comentarios: ¿te identificas con esto? No estás solo/a. 💙',
    '¿Alguna vez has sentido exactamente esto? Escríbelo abajo. Tu historia puede ayudar a alguien más. 🙏',
    'Este video es para quien lo necesita hoy. ¿A quién se lo enviarías? Etiquétalo abajo. ❤️',
    '¿Qué parte de este video te llegó más al corazón? Cuéntame, estoy leyendo todos los comentarios. 💚',
    'El primer paso para sanar es hablarlo. ¿Cómo te sientes hoy? Escríbelo aquí, sin miedo. 🌱',
]

PALETAS = [
    {'fondo': (8,15,45), 'acento': (0,200,255), 'texto': (255,255,255), 'barra': (0,150,220)},
    {'fondo': (45,8,15), 'acento': (255,80,80), 'texto': (255,255,255), 'barra': (200,50,50)},
    {'fondo': (8,35,15), 'acento': (0,220,100), 'texto': (255,255,255), 'barra': (0,170,80)},
    {'fondo': (30,8,45), 'acento': (180,80,255), 'texto': (255,255,255), 'barra': (140,50,220)},
    {'fondo': (40,25,5), 'acento': (255,160,0), 'texto': (255,255,255), 'barra': (220,120,0)},
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

def descargar_videos_pexels(queries, orientacion, n=6, w=1280, h=720):
    os.makedirs('/tmp/pexels', exist_ok=True)
    videos = []
    headers = {'Authorization': PEXELS_API_KEY}
    query = random.choice(queries)
    print(f'Pexels query: {query} ({orientacion})')
    try:
        r = requests.get(
            f'https://api.pexels.com/videos/search',
            headers=headers,
            params={'query': query, 'orientation': orientacion, 'per_page': 15, 'size': 'medium'},
            timeout=30
        )
        data = r.json()
        items = data.get('videos', [])
        random.shuffle(items)
        for item in items[:n*2]:
            try:
                files = item.get('video_files', [])
                files_hd = [f for f in files if f.get('width', 0) >= 640]
                if not files_hd: continue
                files_hd.sort(key=lambda x: x.get('width', 0))
                video_url = files_hd[0]['link']
                vid_path = f'/tmp/pexels/vid_{orientacion}_{len(videos)}.mp4'
                vr = requests.get(video_url, timeout=60, stream=True)
                with open(vid_path, 'wb') as f:
                    for chunk in vr.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
                if os.path.exists(vid_path) and os.path.getsize(vid_path) > 100000:
                    out_path = f'/tmp/pexels/proc_{orientacion}_{len(videos)}.mp4'
                    if orientacion == 'landscape':
                        vf = f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    else:
                        vf = f'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    ok = run_ffmpeg([
                        'ffmpeg', '-y', '-i', vid_path,
                        '-vf', vf, '-t', '12',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', out_path
                    ], f'pexels_proc_{len(videos)}')
                    if ok and os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
                        videos.append(out_path)
                        print(f'  Video Pexels {len(videos)}/{n} OK')
                if len(videos) >= n:
                    break
            except Exception as e:
                print(f'  Video error: {e}')
                continue
    except Exception as e:
        print(f'Pexels error: {e}')
    print(f'Pexels descargados: {len(videos)} videos {orientacion}')
    return videos

def get_youtube():
    token_data = base64.b64decode(os.environ['TOKEN_PICKLE_B64'])
    creds = pickle.loads(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds)

def generar_guion(tema):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f'''Eres un psicologo clinico latinoamericano con canal viral de YouTube.
Estilo: empatico, directo, cercano. Como un amigo que entiende tu dolor.
Estructura del guion obligatoria:
  1. GANCHO (10 palabras max): pregunta o dato que impacte inmediatamente
  2. VALIDACION: que no estan solos, es real lo que sienten
  3. EXPLICACION: el problema en terminos simples con ejemplos cotidianos
  4. SOLUCION: 3 pasos concretos que puedan aplicar hoy
  5. CIERRE: esperanza real + invitacion empatica a comentar

Tema: {tema}

Responde SOLO con JSON puro:
{{
  "titulo": "titulo VIRAL 2 emojis inicio, numero o pregunta impactante, maximo 68 caracteres",
  "descripcion": "500 palabras: linea 1 pregunta engancha, lineas 2-3 suscribirse y activar campana, parrafos con emojis explicando contenido, timestamps: 0:00 Intro / 0:45 El problema / 1:30 Por que te pasa / 2:45 3 soluciones reales / 4:00 Mensaje final, parrafo de recursos y apoyo, 25 hashtags: #SaludMental #Ansiedad #Depresion #BienestarEmocional #PsicologiaLatina #MenteLibre #SaludMentalReal #Autoestima #Motivacion #Mindfulness #CrecimientoPersonal #TerapiaOnline #SaludMentalMexico #SaludMentalColombia #PsicologiaPositiva #MenteClara #SaludMentalJovenes #AnsiedadSocial #VidaSaludable #SuperacionPersonal",
  "guion": "500 palabras estructura 5 partes. Frases max 10 palabras separadas por punto. Natural empatico. Primera persona plural. Pausas naturales con comas y puntos.",
  "frases_clave": ["frase impactante max 7 palabras", "frase impactante max 7 palabras", "frase impactante max 7 palabras", "frase impactante max 7 palabras", "frase impactante max 7 palabras"],
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara","TerapiaOnline","SaludMentalJovenes","AnsiedadSocial","ManejoDeLaAnsiedad","SaludEmocional","PsicologiaColombia","PsicologiaMexico","SaludMentalLatam","MentePositiva","BienEstar"],
  "guion_short": "80 palabras Short. Dato impacta 3 segundos. Frases max 8 palabras. Pregunta empatica final.",
  "titulo_short": "titulo Short 2 emojis max 48 caracteres intriga o identificacion",
  "comentario_ancla": "comentario empatico 2 lineas invita comunidad"
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
    communicate = edge_tts.Communicate(texto, voz, rate=VOZ_RATE, pitch=VOZ_PITCH, volume=VOZ_VOLUME)
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

def get_music_file():
    carpeta = 'assets/music_small'
    if not os.path.exists(carpeta): return None
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith('.mp3')]
    return random.choice(archivos) if archivos else None

def mezclar_audio(voz_mp3, musica, salida, vol=0.08):
    import shutil
    ok = run_ffmpeg([
        'ffmpeg', '-y', '-i', voz_mp3, '-i', musica,
        '-filter_complex',
        f'[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];[1:a]volume={vol},aformat=sample_rates=44100:channel_layouts=stereo,aloop=loop=-1:size=2e+09[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[out]',
        '-map', '[out]', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', salida
    ], 'mezcla')
    if not ok or not os.path.exists(salida) or os.path.getsize(salida) < 1000:
        shutil.copy(voz_mp3, salida)
        print('Mezcla fallida - solo voz')

def limpiar_emojis(texto):
    for e in ['😰','🧠','💙','❤️','🌱','🔥','⚡','💪','🙏','😔','😢','💊','🚨','⚠️','✅','🎯','💡','🧘','🌿','💚','💛','🤍','💜','🧡','😥','😓','🤯','💔','🫀','🫁','🧬','🩺','💭','🗣️','✨','🌟','⭐','💫','🎭','🎨']:
        texto = texto.replace(e, '')
    return texto.strip()

def crear_thumbnail(titulo, archivo, paleta=None):
    if not paleta: paleta = random.choice(PALETAS)
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), color=paleta['fondo'])
    draw = ImageDraw.Draw(img)
    for i in range(H):
        factor = i/H
        r = min(255, paleta['fondo'][0]+int(factor*30))
        g = min(255, paleta['fondo'][1]+int(factor*20))
        b = min(255, paleta['fondo'][2]+int(factor*40))
        draw.line([(0,i),(W,i)], fill=(r,g,b))
    for i in range(0, W, 45):
        draw.line([(i,0),(i,H)], fill=(min(255,paleta['fondo'][0]+15),min(255,paleta['fondo'][1]+10),min(255,paleta['fondo'][2]+20)), width=1)
    for i in range(0, H, 45):
        draw.line([(0,i),(W,i)], fill=(min(255,paleta['fondo'][0]+15),min(255,paleta['fondo'][1]+10),min(255,paleta['fondo'][2]+20)), width=1)
    draw.rectangle([0,0,W,8], fill=paleta['acento'])
    draw.rectangle([0,H-8,W,H], fill=paleta['acento'])
    draw.rectangle([0,0,8,H], fill=paleta['barra'])
    draw.rectangle([W-8,0,W,H], fill=paleta['barra'])
    draw.rectangle([55,95,W-55,H-75], fill=(0,0,0))
    draw.rectangle([58,98,W-58,H-78], fill=(max(0,paleta['fondo'][0]-3),max(0,paleta['fondo'][1]-3),max(0,paleta['fondo'][2]-3)))
    draw.rectangle([55,95,W-55,101], fill=paleta['acento'])
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 76)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
    titulo_limpio = limpiar_emojis(titulo)
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea+' '+p).strip()
        try:
            if draw.textbbox((0,0),test,font=font_big)[2] < W-150: linea = test
            else:
                if linea: lineas.append(linea)
                linea = p
        except: linea = test
    if linea: lineas.append(linea)
    total_h = len(lineas)*88
    y = (H-total_h)//2-22
    for ln in lineas:
        try: tw = draw.textbbox((0,0),ln,font=font_big)[2]
        except: tw = len(ln)*38
        for dx,dy in [(4,4),(3,3),(5,5)]:
            draw.text(((W-tw)//2+dx,y+dy),ln,font=font_big,fill=(0,0,0))
        draw.text(((W-tw)//2,y),ln,font=font_big,fill=paleta['texto'])
        y += 88
    draw.rectangle([100,H-68,W-100,H-63], fill=paleta['acento'])
    try: tw2 = draw.textbbox((0,0),CHANNEL_HANDLE,font=font_med)[2]
    except: tw2 = 300
    draw.text(((W-tw2)//2,H-60),CHANNEL_HANDLE,font=font_med,fill=paleta['acento'])
    img.save(archivo, quality=95)

def crear_intro(titulo, output, w=1280, h=720, dur=3):
    paleta = random.choice(PALETAS)
    img = Image.new('RGB',(w,h),color=paleta['fondo'])
    draw = ImageDraw.Draw(img)
    for i in range(h):
        factor=i/h
        draw.line([(0,i),(w,i)],fill=(min(255,paleta['fondo'][0]+int(factor*30)),min(255,paleta['fondo'][1]+int(factor*20)),min(255,paleta['fondo'][2]+int(factor*40))))
    draw.rectangle([0,0,w,5],fill=paleta['acento'])
    draw.rectangle([0,h-5,w,h],fill=paleta['acento'])
    draw.rectangle([0,0,5,h],fill=paleta['barra'])
    draw.rectangle([w-5,0,w,h],fill=paleta['barra'])
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',56 if w==1280 else 38)
        font_s=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24 if w==1280 else 16)
    except:
        font=ImageFont.load_default(); font_s=font
    tl=limpiar_emojis(titulo).upper().split()
    lineas,linea=[],''
    for p in tl:
        test=(linea+' '+p).strip()
        try:
            if draw.textbbox((0,0),test,font=font)[2]<w-100: linea=test
            else:
                if linea: lineas.append(linea)
                linea=p
        except: linea=test
    if linea: lineas.append(linea)
    total_h=len(lineas)*70
    y=(h-total_h)//2-15
    for ln in lineas:
        try: tw=draw.textbbox((0,0),ln,font=font)[2]
        except: tw=len(ln)*28
        draw.text(((w-tw)//2+3,y+3),ln,font=font,fill=(0,0,0))
        draw.text(((w-tw)//2,y),ln,font=font,fill=paleta['texto'])
        y+=70
    try: tw2=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_s)[2]
    except: tw2=200
    draw.text(((w-tw2)//2,h-40),CHANNEL_HANDLE,font=font_s,fill=paleta['acento'])
    img_path=output.replace('.mp4','_frame.jpg')
    img.save(img_path,quality=95)
    run_ffmpeg(['ffmpeg','-y','-loop','1','-i',img_path,'-t',str(dur),'-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',output],'intro')

def crear_frases_overlay(frases, dur_frase, output, w=1280, h=720):
    if not frases: return None
    clips=[]
    paleta=random.choice(PALETAS)
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',54 if w==1280 else 38)
        font_s=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20 if w==1280 else 15)
    except:
        font=ImageFont.load_default(); font_s=font
    for i,frase in enumerate(frases):
        img=Image.new('RGB',(w,h),color=paleta['fondo'])
        draw=ImageDraw.Draw(img)
        for row in range(h):
            factor=row/h
            draw.line([(0,row),(w,row)],fill=(min(255,paleta['fondo'][0]+int(factor*35)),min(255,paleta['fondo'][1]+int(factor*25)),min(255,paleta['fondo'][2]+int(factor*45))))
        draw.rectangle([0,0,w,5],fill=paleta['acento'])
        draw.rectangle([0,h-5,w,h],fill=paleta['acento'])
        fu=limpiar_emojis(frase).upper().split()
        lineas,linea=[],''
        for p in fu:
            test=(linea+' '+p).strip()
            try:
                if draw.textbbox((0,0),test,font=font)[2]<w-80: linea=test
                else:
                    if linea: lineas.append(linea)
                    linea=p
            except: linea=test
        if linea: lineas.append(linea)
        total_h=len(lineas)*68
        y=(h-total_h)//2-10
        for ln in lineas:
            try: tw=draw.textbbox((0,0),ln,font=font)[2]
            except: tw=len(ln)*28
            draw.rectangle([(w-tw)//2-18,y-10,(w+tw)//2+18,y+62],fill=(0,0,0))
            draw.text(((w-tw)//2+2,y+2),ln,font=font,fill=(0,0,0))
            draw.text(((w-tw)//2,y),ln,font=font,fill=paleta['acento'])
            y+=68
        try: tw_s=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_s)[2]
        except: tw_s=200
        draw.text(((w-tw_s)//2,h-35),CHANNEL_HANDLE,font=font_s,fill=(100,150,200))
        img_path=f'/tmp/frase_{i}.jpg'
        img.save(img_path,quality=90)
        clip=f'/tmp/frase_clip_{i}.mp4'
        run_ffmpeg(['ffmpeg','-y','-loop','1','-i',img_path,'-t',str(dur_frase),'-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',clip],f'frase_{i}')
        if os.path.exists(clip) and os.path.getsize(clip)>1000:
            clips.append(clip)
    if not clips: return None
    lista='/tmp/lista_frases.txt'
    with open(lista,'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista,'-c:v','libx264','-pix_fmt','yuv420p',output],'frases_concat')
    return output if os.path.exists(output) and os.path.getsize(output)>1000 else None

def agregar_subtitulos(video_in, srt_file, video_out, fontsize=20, margenv=40):
    if not srt_file or not os.path.exists(srt_file) or os.path.getsize(srt_file)<10:
        return False
    srt_esc=srt_file.replace('\\','/').replace(':','\\:')
    style=(f"FontName=Arial,FontSize={fontsize},PrimaryColour=&H00FFFFFF,"
           f"OutlineColour=&H00000000,Outline=3,Shadow=1,Bold=1,Alignment=2,MarginV={margenv}")
    ok=run_ffmpeg(['ffmpeg','-y','-i',video_in,'-vf',f"subtitles='{srt_esc}':force_style='{style}'",
        '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast',video_out],f'subs_{fontsize}')
    return ok and os.path.exists(video_out) and os.path.getsize(video_out)>10000

def crear_video_largo(audio_file, srt_file, frases, videos_h, titulo, output_file):
    duracion=get_audio_duration(audio_file)
    print(f'Duracion: {duracion:.1f}s')
    intro='/tmp/intro_largo.mp4'
    crear_intro(titulo,intro,1280,720,3)
    frases_v='/tmp/frases_video.mp4'
    frases_ok=crear_frases_overlay(frases,3.5,frases_v,1280,720) if frases else None
    dur_clip=9
    n_clips=max(4,int((duracion-3)/dur_clip)+3)
    clips=[]
    pool=videos_h*(n_clips//max(len(videos_h),1)+3)
    for i in range(n_clips):
        src=pool[i%len(pool)]
        clip=f'/tmp/hclip_{i}.mp4'
        ok=run_ffmpeg(['ffmpeg','-y','-i',src,
            '-vf','scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
            '-t',str(dur_clip),'-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',clip],f'hclip_{i}')
        if os.path.exists(clip) and os.path.getsize(clip)>5000:
            clips.append(clip)
    if not clips:
        print('ERROR: Sin clips'); sys.exit(1)
    mitad=len(clips)//2
    segs=[]
    if os.path.exists(intro) and os.path.getsize(intro)>1000: segs.append(intro)
    for c in clips[:mitad]: segs.append(c)
    if frases_ok and os.path.exists(frases_v) and os.path.getsize(frases_v)>1000: segs.append(frases_v)
    for c in clips[mitad:]: segs.append(c)
    lista='/tmp/lista_largo.txt'
    with open(lista,'w') as f:
        for s in segs: f.write(f"file '{s}'\n")
    video_mudo='/tmp/video_mudo_largo.mp4'
    run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista,'-c:v','libx264','-pix_fmt','yuv420p',video_mudo],'concat_largo')
    video_subs='/tmp/video_largo_subs.mp4'
    subs_ok=agregar_subtitulos(video_mudo,srt_file,video_subs,20,40)
    video_base=video_subs if subs_ok else video_mudo
    print(f'Largo: {"CON subs" if subs_ok else "SIN subs"}')
    run_ffmpeg(['ffmpeg','-y','-i',video_base,'-i',audio_file,
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',output_file],'final_largo')

def crear_short(audio_file, srt_file, frases, videos_v, titulo, output_file):
    duracion=get_audio_duration(audio_file)
    intro_v='/tmp/intro_short.mp4'
    crear_intro(titulo,intro_v,608,1080,2)
    src=random.choice(videos_v)
    clip_v='/tmp/clip_v_base.mp4'
    ok=run_ffmpeg(['ffmpeg','-y','-i',src,
        '-vf','scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1',
        '-t',str(int(duracion)+2),'-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',clip_v],'clip_v')
    segs_v=[]
    if os.path.exists(intro_v) and os.path.getsize(intro_v)>1000: segs_v.append(intro_v)
    if os.path.exists(clip_v) and os.path.getsize(clip_v)>1000: segs_v.append(clip_v)
    video_mudo_v='/tmp/video_mudo_short.mp4'
    if len(segs_v)>1:
        lista_v='/tmp/lista_short.txt'
        with open(lista_v,'w') as f:
            for s in segs_v: f.write(f"file '{s}'\n")
        run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista_v,'-c:v','libx264','-pix_fmt','yuv420p',video_mudo_v],'concat_short')
    else:
        import shutil; shutil.copy(segs_v[0] if segs_v else clip_v,video_mudo_v)
    video_subs_v='/tmp/video_short_subs.mp4'
    subs_ok=agregar_subtitulos(video_mudo_v,srt_file,video_subs_v,17,55)
    video_base_v=video_subs_v if subs_ok else video_mudo_v
    run_ffmpeg(['ffmpeg','-y','-i',video_base_v,'-i',audio_file,
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','128k','-shortest',output_file],'final_short')

def subir_youtube(youtube, video_file, titulo, descripcion, tags, thumbnail=None, is_short=False):
    if not os.path.exists(video_file) or os.path.getsize(video_file)<10000:
        print(f'ERROR: {video_file} invalido'); sys.exit(1)
    if is_short and '#Shorts' not in titulo:
        titulo=titulo+' #Shorts'
    body={
        'snippet':{'title':titulo[:100],'description':descripcion,'tags':tags,
            'categoryId':'26','defaultLanguage':'es','defaultAudioLanguage':'es'},
        'status':{'privacyStatus':'public','selfDeclaredMadeForKids':False}
    }
    media=MediaFileUpload(video_file,mimetype='video/mp4',resumable=True,chunksize=5*1024*1024)
    req=youtube.videos().insert(part='snippet,status',body=body,media_body=media)
    response=None
    while response is None:
        _,response=req.next_chunk()
    video_id=response['id']
    if thumbnail and os.path.exists(thumbnail):
        try:
            youtube.thumbnails().set(videoId=video_id,
                media_body=MediaFileUpload(thumbnail,mimetype='image/jpeg')).execute()
            print('Thumbnail OK')
        except Exception as e:
            print(f'Thumbnail error: {e}')
    return video_id

def agregar_comentario(youtube, video_id, comentario):
    try:
        youtube.commentThreads().insert(part='snippet',body={
            'snippet':{'videoId':video_id,'topLevelComment':{'snippet':{'textOriginal':comentario}}}
        }).execute()
        print('Comentario OK')
    except Exception as e:
        print(f'Comentario error: {e}')

def main():
    send_telegram('🧠 <b>SaludMentalReal</b> — Iniciando produccion...')
    os.makedirs('/tmp/smr',exist_ok=True)

    # Descargar videos frescos de Pexels
    print('Descargando videos de Pexels...')
    videos_h=descargar_videos_pexels(QUERIES_PEXELS_H,'landscape',6,1280,720)
    videos_v=descargar_videos_pexels(QUERIES_PEXELS_V,'portrait',4,608,1080)

    # Fallback a assets locales si Pexels falla
    if len(videos_h)<2 and os.path.exists('assets/videos_h_small'):
        videos_h=get_video_files('assets/videos_h_small')
        print(f'Fallback a assets locales H: {len(videos_h)}')
    if len(videos_v)<2 and os.path.exists('assets/videos_v_small'):
        videos_v=get_video_files('assets/videos_v_small')
        print(f'Fallback a assets locales V: {len(videos_v)}')

    if not videos_h or not videos_v:
        send_telegram('❌ Error: Sin videos disponibles')
        sys.exit(1)

    musica=get_music_file()
    print(f'Assets: {len(videos_h)}H | {len(videos_v)}V | Musica: {bool(musica)}')

    tema=random.choice(TEMAS)
    print(f'Tema: {tema}')
    datos=generar_guion(tema)

    titulo=datos['titulo']
    descripcion=datos['descripcion']
    guion=datos['guion']
    tags=datos['tags']
    titulo_short=datos['titulo_short']
    guion_short=datos['guion_short']
    frases=datos.get('frases_clave',[])
    comentario_ancla=datos.get('comentario_ancla',random.choice(COMENTARIOS_FIJOS))

    print(f'Titulo: {titulo}')

    # TTS + SRT
    audio_voz='/tmp/smr/audio_voz.mp3'
    srt_largo='/tmp/subs_largo.srt'
    asyncio.run(tts_con_srt(guion,audio_voz,srt_largo,VOZ))

    audio_voz_short='/tmp/smr/audio_voz_short.mp3'
    srt_short='/tmp/subs_short.srt'
    asyncio.run(tts_con_srt(guion_short,audio_voz_short,srt_short,VOZ))

    # Musica
    if musica:
        audio_largo='/tmp/smr/audio_largo.mp3'
        mezclar_audio(audio_voz,musica,audio_largo)
        audio_short_mix='/tmp/smr/audio_short.mp3'
        mezclar_audio(audio_voz_short,musica,audio_short_mix)
    else:
        audio_largo=audio_voz
        audio_short_mix=audio_voz_short

    thumbnail='/tmp/smr/thumbnail.jpg'
    crear_thumbnail(titulo,thumbnail)

    video_largo='/tmp/smr/video_largo.mp4'
    crear_video_largo(audio_largo,srt_largo,frases,videos_h,titulo,video_largo)

    video_short='/tmp/smr/video_short.mp4'
    crear_short(audio_short_mix,srt_short,frases[:3],videos_v,titulo_short,video_short)

    youtube=get_youtube()
    vid_id=subir_youtube(youtube,video_largo,titulo,descripcion,tags,thumbnail)
    agregar_comentario(youtube,vid_id,comentario_ancla)
    send_telegram(f'✅ <b>Video largo subido</b>\n{titulo}\nhttps://youtu.be/{vid_id}')

    short_id=subir_youtube(youtube,video_short,titulo_short,descripcion,tags,is_short=True)
    agregar_comentario(youtube,short_id,comentario_ancla)
    send_telegram(f'✅ <b>Short subido</b>\n{titulo_short}\nhttps://youtu.be/{short_id}')

    send_telegram(f'🎉 <b>SaludMentalReal</b> — Completado\nTema: {tema}')

def get_video_files(carpeta):
    exts=('.mp4','.mov','.avi','.mkv','.webm')
    archivos=[os.path.join(carpeta,f) for f in os.listdir(carpeta) if f.lower().endswith(exts)]
    random.shuffle(archivos)
    return archivos

if __name__=='__main__':
    main()