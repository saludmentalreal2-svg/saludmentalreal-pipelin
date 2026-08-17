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
VOZ_RATE = random.choice(['-8%', '-10%', '-12%'])
VOZ_PITCH = random.choice(['-3Hz', '-4Hz', '-5Hz'])
VOZ_VOLUME = '+15%'
PLAYLIST_ES_NAME = 'Salud Mental en Espanol'
PLAYLIST_EN_NAME = 'Mental Health English'
SERIE_ES_NAME = '30 Dias de Salud Mental'

TEMAS_ES = [
    'como controlar la ansiedad en momentos de crisis',
    'tecnicas de respiracion para calmar el estres',
    'como dormir mejor cuando la mente no para',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de burnout y como recuperarte',
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
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de que necesitas ayuda psicologica',
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
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de inmadurez emocional',
    'como sanar relaciones toxicas',
    'el miedo al rechazo y como vencerlo',
    'por que te saboteas inconscientemente',
    'duelo emocional lo que nadie te prepara para sentir',
    'por que te cuesta pedir ayuda',
    'como sobrevivir una crisis de ansiedad nocturna',
    'que es la ansiedad generalizada y como tratarla',
    'por que lloras sin razon',
    'como dejar de compararte en redes sociales',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de trauma emocional sin saberlo',
    'como manejar la soledad cuando vives solo',
    'por que sientes que no encajas en ningun lado',
    'como recuperar la motivacion cuando todo da igual',
    'el agotamiento emocional que nadie ve',
    'como dejar de ser tan duro contigo mismo',
    'por que te cuesta ser feliz aunque tengas todo',
    'como superar el miedo al fracaso',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de que necesitas terapia urgente',
    'como manejar relacion con alguien deprimido',
    'por que la ansiedad aparece de noche',
    'como hablar de salud mental sin que te juzguen',
    'el poder de decir no sin sentirte mal',
    'como salir del ciclo de la negatividad',
    'por que tienes miedo al exito',
    'como construir autoestima desde cero',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de que una relacion daÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±a tu salud mental',
    'como manejar los celos sin destruir tu relacion',
    'por que te sientes culpable de ser feliz',
    'como superar la traicion de alguien que amabas',
    'el efecto del alcohol en tu salud mental',
    'como dejar de pensar demasiado overthinking',
    'por que evitas el conflicto aunque te lastime',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de que eres altamente sensible',
    'como manejar la ansiedad en el trabajo',
    'por que te cuesta perdonar de verdad',
    'el impacto de la familia toxica en tu salud mental',
    'como sanar el miedo al abandono en adultos',
    'por que te autosaboteas en el amor',
    'seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ales de codependencia emocional',
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
    'Dia 28: aprende a celebrar tus pequeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±os avances',
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

QUERIES_PEXELS_THUMB = [
    'person meditation peaceful', 'woman thinking calm', 'man breathing nature',
    'person nature peaceful', 'therapy calm woman', 'mindfulness person outdoor',
    'calm person portrait', 'person yoga nature', 'emotional healing person',
    'wellness calm portrait'
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

COMMUNITY_POSTS_ES = [
    'Pregunta del dia: Cual es la cosa mas pequeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±a que puedes hacer HOY por tu salud mental? Escribela abajo.',
    'Si pudieras darle un consejo a tu yo de hace 5 aÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±os sobre salud mental, cual seria?',
    'Verdad o mito: La ansiedad desaparece sola con el tiempo. Que piensas tu?',
    'Hoy te pregunto: Del 1 al 10, como esta tu salud mental esta semana? Sin juicios.',
    'Comparte una cosa que te ayuda cuando la ansiedad ataca. Puede ayudar a alguien mas.',
    'Sabias que 1 de cada 4 personas sufre un trastorno mental en su vida? No estas solo.',
    'Cual es el mayor obstaculo que enfrentas para cuidar tu salud mental?',
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
    if hoy.day == 10 and hoy.month == 10:
        return 'dia_mundial_salud_mental'
    if hoy.day == 10 and hoy.month == 9:
        return 'dia_prevencion_suicidio'
    if hoy.weekday() == 0:
        return 'lunes_motivacional'
    return None

def get_tema_especial(tipo):
    temas = {
        'dia_mundial_salud_mental': ['hoy es el dia mundial de la salud mental por que importa tanto', 'dia mundial salud mental lo que todos debemos saber hoy'],
        'dia_prevencion_suicidio': ['como ayudar a alguien que esta pensando en rendirse', 'hablar salva vidas lo que debes saber hoy'],
        'lunes_motivacional': ['como empezar la semana con tu salud mental en orden', 'rutina de lunes para proteger tu mente toda la semana']
    }
    return random.choice(temas.get(tipo, [None]))

def limpiar_texto_voz(texto):
    texto = re.sub(r'[^\w\s\.,;:!?\-\(\)ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â­ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â³ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂºÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¼ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¹ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œa-zA-Z0-9]', ' ', texto)
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
            'snippet': {'playlistId': playlist_id,
                'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}
        }).execute()
        print('Playlist OK')
    except Exception as e:
        print(f'Playlist add error: {e}')

def obtener_dia_serie():
    if os.path.exists('serie_dia.txt'):
        try:
            return min(int(open('serie_dia.txt').read().strip()), len(SERIE_30_DIAS))
        except: pass
    return 1

def avanzar_dia_serie():
    dia = obtener_dia_serie()
    nuevo = (dia % len(SERIE_30_DIAS)) + 1
    with open('serie_dia.txt', 'w') as f:
        f.write(str(nuevo))
    return dia

def publicar_community_post(youtube, texto):
    try:
        youtube.communityPosts().insert(part='snippet', body={
            'snippet': {'type': 'textPost', 'textOriginal': texto}
        }).execute()
        print('Community post OK')
    except Exception as e:
        print(f'Community post error: {e}')

def obtener_analytics_semana(youtube):
    try:
        from googleapiclient.discovery import build as gbuild
        analytics = gbuild('youtubeAnalytics', 'v2', credentials=youtube._http.credentials)
        hoy = datetime.now().strftime('%Y-%m-%d')
        hace7 = (datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')
        resp = analytics.reports().query(
            ids='channel==MINE', startDate=hace7, endDate=hoy,
            metrics='views,estimatedMinutesWatched,subscribersGained', dimensions='day'
        ).execute()
        rows = resp.get('rows', [])
        return sum(int(r[1]) for r in rows), sum(int(r[2]) for r in rows), sum(int(r[3]) for r in rows)
    except Exception as e:
        print(f'Analytics error: {e}')
        return 0, 0, 0

def descargar_imagen_pexels(query, w=1280, h=720):
    headers = {'Authorization': PEXELS_API_KEY}
    try:
        r = requests.get('https://api.pexels.com/v1/search',
            headers=headers,
            params={'query': query, 'per_page': 15, 'orientation': 'landscape'},
            timeout=20)
        items = r.json().get('photos', [])
        if not items: return None
        item = random.choice(items[:10])
        url = item['src'].get('large', item['src']['original'])
        ir = requests.get(url, timeout=30)
        img_path = '/tmp/thumb_bg.jpg'
        with open(img_path, 'wb') as f:
            f.write(ir.content)
        img = Image.open(img_path).convert('RGB')
        img = img.resize((w, h), Image.LANCZOS)
        img.save(img_path, quality=95)
        return img_path
    except Exception as e:
        print(f'Pexels imagen error: {e}')
        return None

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
                    if not os.path.exists(raw) or os.path.getsize(raw) < 100000: continue
                    proc = f'/tmp/pexels/proc_{orientacion}_{len(videos)}.mp4'
                    vf = 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1' if orientacion == 'landscape' else 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1'
                    ok = run_ffmpeg(['ffmpeg','-y','-i',raw,'-vf',vf,'-t','12',
                        '-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',proc], f'px_{len(videos)}')
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

def generar_guion(tema, idioma='es', video_anterior_url=None):
    client = Groq(api_key=GROQ_API_KEY)
    link_anterior = f'Video anterior: {video_anterior_url}' if video_anterior_url else ''
    if idioma == 'es':
        prompt = f'''Eres un psicologo clinico latinoamericano con canal viral de YouTube.
Estilo: empatico, directo, conversacional. Como un amigo que entiende tu dolor.
CRITICO: El guion sera leido por voz sintetica. CERO emojis, asteriscos, hashtags o simbolos especiales en guion y guion_short. Solo texto limpio.

Estructura guion 5 partes:
1. GANCHO: pregunta o dato impactante menos 12 palabras
2. VALIDACION: sus sentimientos son validos, no estan solos
3. EXPLICACION: problema en terminos simples con ejemplos cotidianos
4. SOLUCION: 3 pasos concretos aplicables hoy
5. CIERRE: esperanza real, {link_anterior}, invita suscribirse y comentar

Tema: {tema}

JSON puro sin markdown:
{{
  "titulo": "titulo viral espaÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ol 2 emojis inicio, numero o pregunta impactante, max 68 caracteres, sin hashtags",
  "descripcion": "500 palabras: primera linea pregunta engancha, segunda linea suscribirse y campana, parrafos con emojis relevantes, CAPITULOS: 0:00 Introduccion | 0:45 El problema real | 1:30 Por que te sucede | 2:45 3 soluciones que funcionan | 4:00 Mensaje de esperanza, recursos crisis LATAM con numeros reales, {link_anterior}, 25 hashtags: #SaludMental #Ansiedad #Depresion #BienestarEmocional #PsicologiaLatina #MenteLibre #SaludMentalReal #Autoestima #Motivacion #Mindfulness #CrecimientoPersonal #TerapiaOnline #SaludMentalMexico #SaludMentalColombia #PsicologiaPositiva #MenteClara #SaludMentalJovenes #AnsiedadSocial #VidaSaludable #SuperacionPersonal #SaludMentalLatam #PsicologiaColombia #PsicologiaMexico #MentePositiva #BienEstar",
  "guion": "520 palabras SOLO TEXTO LIMPIO sin emojis sin simbolos. Frases max 10 palabras. Pausas con puntos y comas. Primera persona plural. Natural y empatico.",
  "tags": ["SaludMental","Ansiedad","Depresion","BienestarEmocional","PsicologiaLatina","MenteLibre","Autoestima","Mindfulness","SaludMentalReal","MotivacionDiaria","CrecimientoPersonal","PsicologiaPositiva","SuperacionPersonal","VidaSaludable","MenteClara","TerapiaOnline","SaludMentalJovenes","AnsiedadSocial","ManejoDeLaAnsiedad","SaludEmocional","PsicologiaColombia","PsicologiaMexico","SaludMentalLatam","MentePositiva","BienEstar"],
  "guion_short": "100 palabras SOLO TEXTO LIMPIO sin emojis sin simbolos. Frases max 8 palabras. Dato impactante inicio. Pregunta empatica final.",
  "titulo_short": "titulo Short espaÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ol 2 emojis max 48 caracteres sin hashtags",
  "comentario_ancla": "comentario empatico 2 lineas sin emojis invitando comunidad",
  "query_imagen": "query en ingles de 3 palabras para buscar imagen de fondo del thumbnail en Pexels relacionada al tema"
}}'''
    else:
        prompt = f'''You are a clinical psychologist with a viral YouTube channel.
Style: empathetic, direct, conversational. CRITICAL: ZERO emojis in guion/guion_short.

Topic: {tema}

Pure JSON:
{{
  "titulo": "VIRAL English title 2 emojis REQUIRED at start. MUST include: number OR painful question OR concrete promise. Good examples: '😰 Why Do You Feel Anxious for No Reason?', '🧠 5 Signs Your Mind Needs Help NOW', '💔 Stop Torturing Yourself: 3 Steps to Heal'. Max 68 chars. No hashtags.",
  "descripcion": "400 words: engaging question, subscribe line, emoji paragraphs, CHAPTERS: 0:00 Introduction | 0:45 The problem | 1:30 Why it happens | 2:45 Three solutions | 4:00 Hope message, crisis helplines, {link_anterior}, 20 hashtags",
  "guion": "450 words CLEAN TEXT ONLY no emojis. Max 10 words per sentence. Natural empathetic.",
  "tags": ["MentalHealth","Anxiety","Depression","EmotionalWellness","Psychology","MindOverMatter","MentalHealthMatters","SelfCare","Motivation","Mindfulness","PersonalGrowth","Therapy","MentalHealthAwareness","AnxietyRelief","HealingJourney","EmotionalHealth","MentalWellness","SelfLove","Mindset","PositivePsychology"],
  "guion_short": "70 words CLEAN TEXT ONLY no emojis. Max 8 words per sentence. Impactful opening. Empathetic question end.",
  "titulo_short": "English Short title 2 emojis max 48 chars no hashtags",
  "comentario_ancla": "empathetic 2 line comment no emojis",
  "query_imagen": "3 word English query for Pexels background image related to topic"
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
        import shutil; shutil.copy(voz_mp3, salida)
        print('Mezcla fallida - solo voz')

def crear_thumbnail_profesional(titulo, archivo, query_imagen=None, paleta=None):
    if not paleta: paleta = random.choice(PALETAS)
    W, H = 1280, 720

    # Intentar obtener imagen de fondo de Pexels
    bg_path = None
    if query_imagen:
        bg_path = descargar_imagen_pexels(query_imagen, W, H)
    if not bg_path:
        bg_path = descargar_imagen_pexels(random.choice(QUERIES_PEXELS_THUMB), W, H)

    if bg_path and os.path.exists(bg_path):
        img = Image.open(bg_path).convert('RGB')
        img = img.resize((W, H), Image.LANCZOS)
        # Oscurecer la imagen para que el texto se lea bien
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.35)
        # Blur suave
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
    else:
        img = Image.new('RGB', (W,H), color=paleta['fondo'])
        draw_tmp = ImageDraw.Draw(img)
        for i in range(H):
            factor = i/H
            r = min(255, paleta['fondo'][0]+int(factor*35))
            g = min(255, paleta['fondo'][1]+int(factor*25))
            b = min(255, paleta['fondo'][2]+int(factor*45))
            draw_tmp.line([(0,i),(W,i)], fill=(r,g,b))

    draw = ImageDraw.Draw(img)

    # Overlay degradado inferior para legibilidad
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    draw_ov = ImageDraw.Draw(overlay)
    for i in range(H):
        alpha = int(180 * (i/H)**0.7)
        draw_ov.line([(0,i),(W,i)], fill=(0,0,0,alpha))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Barra de acento superior
    draw.rectangle([0,0,W,8], fill=paleta['acento'])
    # Barra inferior
    draw.rectangle([0,H-80,W,H], fill=(0,0,0))
    draw.rectangle([0,H-8,W,H], fill=paleta['acento'])

    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
    except:
        font_big = ImageFont.load_default()
        font_med = font_big
        font_small = font_big

    titulo_limpio = re.sub(r'[^\w\s\?!.,]','',titulo).strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''
    for p in palabras:
        test = (linea+' '+p).strip()
        try:
            if draw.textbbox((0,0),test,font=font_big)[2] < W-80: linea=test
            else:
                if linea: lineas.append(linea)
                linea=p
        except: linea=test
    if linea: lineas.append(linea)

    total_h = len(lineas)*90
    y = (H-80-total_h)//2 + 20

    for ln in lineas:
        try: tw=draw.textbbox((0,0),ln,font=font_big)[2]
        except: tw=len(ln)*40
        # Sombra fuerte
        for dx,dy in [(4,4),(3,3),(5,5),(-2,2)]:
            draw.text(((W-tw)//2+dx,y+dy),ln,font=font_big,fill=(0,0,0))
        draw.text(((W-tw)//2,y),ln,font=font_big,fill=(255,255,255))
        y += 90

    # Linea de acento debajo del titulo
    draw.rectangle([W//4, y+5, W*3//4, y+9], fill=paleta['acento'])

    # Canal en barra inferior
    try: tw2=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_med)[2]
    except: tw2=300
    draw.text(((W-tw2)//2, H-62), CHANNEL_HANDLE, font=font_med, fill=paleta['acento'])

    img.save(archivo, quality=95)
    print(f'Thumbnail profesional OK')

def agregar_texto_short(video_in, titulo_short, video_out, w=608, h=1080):
    titulo_limpio = re.sub(r'[^\w\s\?!.,]','',titulo_short).strip()
    palabras = titulo_limpio.upper().split()
    lineas, linea = [], ''

    img_test = Image.new('RGB', (w,50))
    draw_test = ImageDraw.Draw(img_test)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 42)
    except:
        font = ImageFont.load_default()

    for p in palabras:
        test = (linea+' '+p).strip()
        try:
            if draw_test.textbbox((0,0),test,font=font)[2] < w-40: linea=test
            else:
                if linea: lineas.append(linea)
                linea=p
        except: linea=test
    if linea: lineas.append(linea)

    texto_drawtext = []
    y_start = 80
    paleta = random.choice(PALETAS)
    r,g,b = paleta['acento']
    color_hex = f'#{r:02x}{g:02x}{b:02x}'

    for i, ln in enumerate(lineas):
        y = y_start + i*55
        texto_drawtext.append(
            f"drawtext=text='{ln}':fontsize=42:fontcolor=white:x=(w-text_w)/2:y={y}:shadowcolor=black:shadowx=3:shadowy=3:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        )

    if texto_drawtext:
        filtro = ','.join(texto_drawtext)
        ok = run_ffmpeg([
            'ffmpeg','-y','-i',video_in,
            '-vf', filtro,
            '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast',video_out
        ], 'texto_short')
        return ok and os.path.exists(video_out) and os.path.getsize(video_out) > 10000
    return False

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

def crear_pantalla_final(titulo_siguiente, output, w=1280, h=720, dur=5):
    paleta = random.choice(PALETAS)
    bg = descargar_imagen_pexels('peaceful nature calm', w, h)
    if bg and os.path.exists(bg):
        img = Image.open(bg).convert('RGB').resize((w,h), Image.LANCZOS)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.25)
    else:
        img = Image.new('RGB',(w,h),color=paleta['fondo'])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,w,6], fill=paleta['acento'])
    draw.rectangle([0,h-6,w,h], fill=paleta['acento'])
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
    except:
        font_big = ImageFont.load_default(); font_med = font_big; font_small = font_big

    txt1 = 'SUSCRIBETE PARA MAS CONTENIDO'
    try: tw1=draw.textbbox((0,0),txt1,font=font_small)[2]
    except: tw1=500
    draw.text(((w-tw1)//2,h//5),txt1,font=font_small,fill=paleta['acento'])

    try: tw2=draw.textbbox((0,0),CHANNEL_HANDLE,font=font_big)[2]
    except: tw2=400
    draw.text(((w-tw2)//2+3,h//2-30+3),CHANNEL_HANDLE,font=font_big,fill=(0,0,0))
    draw.text(((w-tw2)//2,h//2-30),CHANNEL_HANDLE,font=font_big,fill=(255,255,255))

    txt3 = 'SIGUIENTE VIDEO:'
    try: tw3=draw.textbbox((0,0),txt3,font=font_small)[2]
    except: tw3=300
    draw.text(((w-tw3)//2,h*3//4-30),txt3,font=font_small,fill=paleta['acento'])

    sig = re.sub(r'[^\w\s\?!.,]','',titulo_siguiente)[:50].upper()
    try: tw4=draw.textbbox((0,0),sig,font=font_small)[2]
    except: tw4=300
    draw.text(((w-tw4)//2,h*3//4),sig,font=font_small,fill=(255,255,255))

    img_path = output.replace('.mp4','_frame.jpg')
    img.save(img_path, quality=95)
    run_ffmpeg(['ffmpeg','-y','-loop','1','-i',img_path,'-t',str(dur),
        '-c:v','libx264','-pix_fmt','yuv420p','-r','25','-an',output],'pantalla_final')

def crear_video(audio_file, srt_file, videos, output_file, titulo_siguiente='', titulo_short='', w=1280, h=720, is_short=False):
    duracion = get_audio_duration(audio_file)
    print(f'Video {w}x{h} | {duracion:.1f}s')
    dur_clip = 12
    n_clips = max(6, int(duracion/dur_clip)+5)
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
        print('ERROR: Sin clips'); sys.exit(1)

    if not is_short and titulo_siguiente:
        pantalla = f'/tmp/pantalla_{w}.mp4'
        crear_pantalla_final(titulo_siguiente, pantalla, w, h, 5)
        if os.path.exists(pantalla) and os.path.getsize(pantalla)>1000:
            clips.append(pantalla)

    lista = f'/tmp/lista_{w}.txt'
    with open(lista,'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    video_mudo = f'/tmp/mudo_{w}.mp4'
    run_ffmpeg(['ffmpeg','-y','-f','concat','-safe','0','-i',lista,
        '-c:v','libx264','-pix_fmt','yuv420p',video_mudo],'concat')

    # Subtitulos
    video_subs = f'/tmp/subs_{w}.mp4'
    subs_ok = agregar_subtitulos(video_mudo, srt_file, video_subs,
        18 if not is_short else 16, 40 if not is_short else 55)
    video_base = video_subs if subs_ok else video_mudo

    # Texto hook en shorts
    if is_short and titulo_short:
        video_hook = f'/tmp/hook_{w}.mp4'
        hook_ok = agregar_texto_short(video_base, titulo_short, video_hook, w, h)
        if hook_ok: video_base = video_hook

    # Marca de agua
    video_marca = f'/tmp/marca_{w}.mp4'
    marca_ok = agregar_marca_agua(video_base, video_marca, w, h)
    video_final = video_marca if marca_ok else video_base

    run_ffmpeg(['ffmpeg','-y','-i',video_final,'-i',audio_file,
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac',
        '-b:a','192k' if not is_short else '128k','-shortest',output_file],'final')
    size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
    print(f'OK: {size//1024}KB | subs:{"si" if subs_ok else "no"} | marca:{"si" if marca_ok else "no"}')

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

def enviar_reporte_analytics(youtube):
    try:
        if datetime.now().weekday() != 0: return
        views, watch, subs = obtener_analytics_semana(youtube)
        msg = (f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  <b>Reporte Semanal SaludMentalReal</b>\n'
               f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¹ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â Vistas: {views:,}\n'
               f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â± Horas vistas: {watch//60:,}h\n'
               f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¹ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¥ Suscriptores: +{subs:,}\n'
               f'Meta: 1,000 subs y 4,000 horas')
        send_telegram(msg)
    except Exception as e:
        print(f'Reporte error: {e}')

def main():
    send_telegram('ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â  <b>SaludMentalReal</b> ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â Iniciando produccion...')
    os.makedirs('/tmp/smr', exist_ok=True)

    print('Descargando videos Pexels...')
    videos_h = descargar_videos_pexels(QUERIES_PEXELS_H, 'landscape', 5)
    videos_v = descargar_videos_pexels(QUERIES_PEXELS_V, 'portrait', 3)

    if not videos_h or not videos_v:
        send_telegram('ERROR: Sin videos disponibles')
        sys.exit(1)

    musica = get_music_file()
    youtube = get_youtube()

    pl_es = obtener_o_crear_playlist(youtube, PLAYLIST_ES_NAME, 'Videos psicologia y bienestar emocional en espaÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â±ol', 'es')
    pl_en = obtener_o_crear_playlist(youtube, PLAYLIST_EN_NAME, 'Psychology and emotional wellness in English', 'en')
    pl_serie = obtener_o_crear_playlist(youtube, SERIE_ES_NAME, 'Serie 30 dias para mejorar tu salud mental', 'es')

    dia_serie = obtener_dia_serie()
    tema_serie = SERIE_30_DIAS[dia_serie-1]
    fecha_especial = detectar_fecha_especial()
    tema_especial = get_tema_especial(fecha_especial) if fecha_especial else None
    tema_es = tema_especial if tema_especial else random.choice(TEMAS_ES)
    if fecha_especial: print(f'Fecha especial detectada: {fecha_especial}')
    tema_en = random.choice(TEMAS_EN)
    print(f'ES: {tema_es} | Serie dia {dia_serie} | EN: {tema_en}')

    datos_es = generar_guion(tema_es, 'es')
    datos_serie = generar_guion(tema_serie, 'es')
    datos_en = generar_guion(tema_en, 'en')

    # TTS
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

    # Thumbnails profesionales con imagen real
    thumb_es='/tmp/smr/thumb_es.jpg'
    thumb_serie='/tmp/smr/thumb_serie.jpg'
    thumb_en='/tmp/smr/thumb_en.jpg'
    crear_thumbnail_profesional(datos_es['titulo'], thumb_es, datos_es.get('query_imagen'))
    crear_thumbnail_profesional(datos_serie['titulo'], thumb_serie, datos_serie.get('query_imagen'))
    crear_thumbnail_profesional(datos_en['titulo'], thumb_en, datos_en.get('query_imagen'))

    # Videos
    v_l_es='/tmp/smr/v_l_es.mp4'
    crear_video(l_es, srt_es, videos_h, v_l_es, datos_serie['titulo'], '', 1280, 720)
    v_s_es='/tmp/smr/v_s_es.mp4'
    crear_video(s_es, srt_es_s, videos_v, v_s_es, '', datos_es['titulo_short'], 608, 1080, True)
    v_serie='/tmp/smr/v_serie.mp4'
    crear_video(l_serie, srt_serie, videos_h, v_serie, datos_en['titulo'], '', 1280, 720)
    v_l_en='/tmp/smr/v_l_en.mp4'
    crear_video(l_en, srt_en, videos_h, v_l_en, datos_es['titulo'], '', 1280, 720)
    v_s_en='/tmp/smr/v_s_en.mp4'
    crear_video(s_en, srt_en_s, videos_v, v_s_en, '', datos_en['titulo_short'], 608, 1080, True)

    # Subir
    id_es = subir_youtube(youtube, v_l_es, datos_es['titulo'], datos_es['descripcion'], datos_es['tags'], thumb_es, idioma='es')
    agregar_comentario(youtube, id_es, datos_es.get('comentario_ancla', random.choice(COMENTARIOS_ES)))
    agregar_a_playlist(youtube, id_es, pl_es)
    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ <b>Video ES</b>\n{datos_es["titulo"]}\nhttps://youtu.be/{id_es}')

    id_s_es = subir_youtube(youtube, v_s_es, datos_es['titulo_short'], datos_es['descripcion'], datos_es['tags'], is_short=True, idioma='es')
    agregar_comentario(youtube, id_s_es, random.choice(COMENTARIOS_ES))
    agregar_a_playlist(youtube, id_s_es, pl_es)
    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ <b>Short ES</b>\nhttps://youtu.be/{id_s_es}')

    id_serie = subir_youtube(youtube, v_serie, datos_serie['titulo'], datos_serie['descripcion'], datos_serie['tags'], thumb_serie, idioma='es')
    agregar_comentario(youtube, id_serie, f'Este es el dia {dia_serie} de nuestra serie de 30 dias. Manana viene el siguiente. Nos vemos aqui.')
    agregar_a_playlist(youtube, id_serie, pl_serie)
    agregar_a_playlist(youtube, id_serie, pl_es)
    avanzar_dia_serie()
    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ <b>Serie Dia {dia_serie}</b>\n{datos_serie["titulo"]}\nhttps://youtu.be/{id_serie}')

    id_en = subir_youtube(youtube, v_l_en, datos_en['titulo'], datos_en['descripcion'], datos_en['tags'], thumb_en, idioma='en')
    agregar_comentario(youtube, id_en, datos_en.get('comentario_ancla', random.choice(COMENTARIOS_EN)))
    agregar_a_playlist(youtube, id_en, pl_en)
    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ <b>Video EN</b>\n{datos_en["titulo"]}\nhttps://youtu.be/{id_en}')

    id_s_en = subir_youtube(youtube, v_s_en, datos_en['titulo_short'], datos_en['descripcion'], datos_en['tags'], is_short=True, idioma='en')
    agregar_comentario(youtube, id_s_en, random.choice(COMENTARIOS_EN))
    agregar_a_playlist(youtube, id_s_en, pl_en)
    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ <b>Short EN</b>\nhttps://youtu.be/{id_s_en}')

    publicar_community_post(youtube, random.choice(COMMUNITY_POSTS_ES))
    enviar_reporte_analytics(youtube)

    send_telegram(f'ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â½ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â° <b>SaludMentalReal</b> ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â 5 videos publicados\nES: {tema_es}\nSerie dia {dia_serie}\nEN: {tema_en}')

if __name__ == '__main__':
    main()