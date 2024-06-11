import google.auth
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def folderIndexing(service):

    #TODO: load the correct authentication method
    #*See https://developers.google.com/identity for guides on implementing Oauth2

    #creds, _ = google.auth.default()
    
    try:
        files = []
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q="mimeType = 'application/vnd.google-apps.folder' and 'root' in parents",
                    spaces="drive",
                    fields="nextPageToken, files(*)",
                    pageToken=page_token,
                )
                .execute()
            )
            #for file in response.get("files", []):
                #* process change
                #print(f'Found File: {file.get("name")}, {file.get("id")}')
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error has occured: {error}")
        files = None

    return files

if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    print('test')
    files = folderIndexing(creds)

    for file in files:
        print(f'Found File: {file.get("name")}, {file.get("id")}')