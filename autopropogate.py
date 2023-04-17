import io
import os
import subprocess
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def download_and_install_files_from_folder(folder_id):
    try:
        creds = service_account.Credentials.from_service_account_file('C:\\Users\\joshr\\Downloads\\credentials.json')

        service = build('drive', 'v3', credentials=creds)

        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                if item['mimeType'] != 'application/vnd.google-apps.folder':
                    request = service.files().get_media(fileId=item['id'])
                    file = io.BytesIO()
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print(f"Downloaded {int(status.progress() * 100)}.")
                    
                    file.seek(0)
                    file_name = item['name']
                    with open(file_name, 'wb') as f:
                        f.write(file.read())
                    print(f"Downloaded: {file_name}")

                    if file_name.endswith('.exe'):
                        print(f"Installing {file_name}...")
                        subprocess.run([file_name], check=True)
                        print(f"Installed: {file_name}")
                else:
                    print(f"Skipping folder: {item['name']}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


if __name__ == '__main__':
    folder_id = '13L3kOnPyet5_1PhCooV0Gpi4ZvurWYG4'  # The folder ID from the provided link.
    download_and_install_files_from_folder(folder_id)