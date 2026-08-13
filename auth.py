import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
credentials = flow.run_local_server(port=8080)

with open('token.pickle', 'wb') as f:
    pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)
channel = youtube.channels().list(part='snippet', mine=True).execute()
print('Canal:', channel['items'][0]['snippet']['title'])
print('Token guardado correctamente')