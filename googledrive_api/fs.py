import httplib2
import os, io

from apiclient import discovery
from oauth2client import tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
from gdrive_api import generate_token 

generate_token()
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'googledrive_api/credentials.json'
APPLICATION_NAME = 'AmongUSTH'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

filepath = "requirements.txt"

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) 

#listFiles(10)
def uploadFile(filename, mimetype = "application/vnd.google-apps.file", folder_id= "1n5jjLnBStcS9oJ_4xwOQ3IlA53yGLUAg"): # "test.txt" , "document"
    file_metadata = {'name': filename, "parents": [folder_id]}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
#uploadFile('ÔN TẬP KIẾN THỨC ANDROID CẤP TỐC updated.docx','ÔN TẬP KIẾN THỨC ANDROID CẤP TỐC updated.docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document')              

def downloadFile(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

#searchFile(10,"name contains 'Getting'")                    

uploadFile("requirements.txt", "document/text")
downloadFile("1yK2DDa1Eo0YXXtbVDxOxELNkviyGn_V4")
# createFolder("tetditKien")