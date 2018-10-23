import urllib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

path = "/home/n4tticus/dataSet/image.jpg"
urllib.urlretrieve("http://static.flickr.com/64/165767963_69207d1fb1.jpg", path)

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

with open(path,"r") as file:
	file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
	file_drive.SetContentString(file.read()) 
	file1_drive.Upload()