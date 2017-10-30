from __future__ import print_function
import httplib2
import os
import io
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaIoBaseDownload

BASE_DIR = "/media/ivan/2AC2E2F12DC00F2B/Ivan/Documents/Programming/Simple programs/Flashcards/"
OUT_PATH = "data/"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = BASE_DIR + 'docs/gdrive/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    if os.path.exists(credential_path):
        os.remove(credential_path)


    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def download_file(drive_service, file_id):
    request = drive_service.files().export_media(fileId=file_id,
                                                 mimeType='application/zip')
    os.chdir("..")
    if os.path.exists("data"):
        os.removedirs("data")
    os.makedirs("data")

    fh = io.FileIO("data/Vocabelheft.zip", "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(
        "Download %d%%." % int(status.progress() * 100)
        )


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    file_ids = get_file_id(service)
    if file_ids:
        file_id = file_ids[0]
        download_file(service, file_id)

def get_file_id(service):
    results = service.files().list(q="name contains 'Vokabelheft' and trashed=false",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    file_ids = []
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            file_ids.append(item['id'])

    return file_ids


if __name__ == '__main__':
    main()
