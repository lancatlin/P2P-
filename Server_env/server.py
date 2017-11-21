from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
url = gauth.GetAuthUrl()
code = 

drive = GoogleDrive(gauth)

file = drive.CreateFile({'title': 'Hello.txt'})
file.SetContentString('Hello World!')
file.Upload()