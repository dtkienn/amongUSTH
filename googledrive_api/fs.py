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


#listFiles(10)
def uploadFile(filename, folder_id, mimetype = "application/pdf"): # "test.txt" , "document"
    file_metadata = {'name': filename, "parents": [folder_id]}
    filepath = filename
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')
#uploadFile('ÔN TẬP KIẾN THỨC ANDROID CẤP TỐC updated.docx','ÔN TẬP KIẾN THỨC ANDROID CẤP TỐC updated.docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document')              

def uploadFile_image(filename, folder_id, mimetype = "image/jpeg"): # "test.txt" , "document"
    file_metadata = {'name': filename, "parents": [folder_id]}
    filepath = filename
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print (exception)
        else:
            print ("Permission Id: %s" % response.get('id'))

    batch = drive_service.new_batch_http_request(callback=callback)
    domain_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(drive_service.permissions().create(
            fileId=file.get('id'),
            body=domain_permission,
            fields='id',
    ))
    batch.execute()

    return file.get('id')

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print (exception)
        else:
            print ("Permission Id: %s" % response.get('id'))

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


#searchFile(10,"name contains 'Getting'")                    


# createFolder("tetditKien")