#@mmfahmi
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def list_files_efficiently(drive_service, folder_id='root'):
    result = []
    seen_files = set()
    folders_to_process = [folder_id]  # Start processing from the specified folder

    while folders_to_process:
        parent_id = folders_to_process.pop(0)  # Get the ID of the folder to process

        page_token = None

        while True:
            params = {
                'fields': 'nextPageToken, files(*)', 
                'q': f"'{parent_id}' in parents"  # Base query: files in the current folder
            }
            if page_token:
                params['pageToken'] = page_token

            try:
                response = drive_service.files().list(**params).execute()
                files = response.get('files', [])

                for file in files:
                    if file['id'] not in seen_files:  
                        seen_files.add(file['id'])
                        result.append(file)
                        if file['mimeType'] == 'application/vnd.google-apps.folder':
                            folders_to_process.append(file['id'])  # Append folder IDs for processing

                if not files or not response.get('nextPageToken'):
                    break

                page_token = response.get('nextPageToken')

            except HttpError as error:
                print(f"An error occurred: {error}")

    return result


