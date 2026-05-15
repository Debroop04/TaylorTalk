from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    'service_account.json',
    scopes=SCOPES
)

service = build(
    'drive',
    'v3',
    credentials=credentials
)

def search_drive(query):

    results = service.files().list(
        q=query,
        fields="files(id,name,mimeType)"
    ).execute()

    return results.get('files',[])