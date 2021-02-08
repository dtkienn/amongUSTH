import httplib2
import os, io

from googleapiclient import discovery
from oauth2client import tools
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import googledrive_api.auth as auth
from googledrive_api.gdrive_api import generate_token 

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

global mimeType
mimeType = ["application/pdf",'application/vnd.google-apps.folder']

def callback(request_id, response, exception):
        if exception:
            # Handle error
            print (exception)
        else:
            print ("Permission Id: %s" % response.get('id'))

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

    batch = drive_service.new_batch_http_request(callback=callback)
    domain_permission = {
        'type': 'domain',
        'role': 'reader',
        'domain': 'st.usth.edu.vn'
    }
    batch.add(drive_service.permissions().create(
            fileId=file.get('id'),
            body=domain_permission,
            fields='id',
    ))
    batch.execute()

    return file.get('id')

def searchFile(name, type_):
    page_token = None
    file_id = ''
    file_mimeType = ''
    if type_ == 'folder':
        response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        while True:
            for file in response.get('files', []):
                # Process change
                if file.get('name') == name:
                    file_id = file.get('id')
                    print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    break
            page_token = response.get('nextPageToken', None)
            if page_token is None and file_id == '':  
                print('No file found!')
                return False
            
            elif file_id != '':
                return file_id

    elif type_ == 'pdf':
        response = drive_service.files().list(q="mimeType='application/pdf'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        while True:
            for file in response.get('files', []):
                if file.get('name') == name:
                    file_id = file.get('id')
                    print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    break
            page_token = response.get('nextPageToken', None)
            if page_token is None and file_id == '':  
                print('No file found!')
                return False
            
            elif file_id != '':
                return file_id

folder_id = searchFile('AmongUSTH', 'folder')

def uploadFile(filepath, filename, folder_id = folder_id, mimetype = "application/pdf"): # "test.txt" , "document"
    type_ = filename.split('.')[-1]
    if searchFile(filename, type_):
        print('File exsits')
    else:
        file_metadata = {'name': filename, "parents": [folder_id]}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
        return file.get('id')


