# from io import BytesIO
import json, requests, wget, time
from send2trash import send2trash
import os, shutil, subprocess
from zipfile import ZipFile

if 'updater' in str(os.getcwd()):
    cwd = str(os.getcwd()).replace('\\updater','\\')
else:
    cwd = os.getcwd()+'\\'
version = {}
with open(cwd+'version.json', 'r') as f:
    version = json.load(f)
    f.close()
cver = version['version']

basegiturl = 'https://api.github.com'
headers = {"Accept": "application/vnd.github.v3+json"}

req = requests.get(basegiturl+'/repos/insaiyancvk/music_downloader/releases',headers = headers).json()

checkver = req[0]['tag_name']
details = req[0]['body']
print("\nHere are the new update details: \n")
print(details)

# print("\nGetting the redirected download link of the update file\n")
j=0
for i in range(len(req[0]['assets'])):
    if 'update' in req[0]['assets'][i]['name']:
        j=i
fileurl = req[0]['assets'][j]['browser_download_url']
# u = urllib.request.urlopen(req[0]['assets'][j]['browser_download_url'])
# url = u.geturl()
print("\t\t***** This step could take a while depending on your internet speed *****\n")
print("Getting details from the redirected link\n")    
start_time = time.time()
updater = wget.download(fileurl)
# r = requests.get(
#     url,
#     # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36'},
#     stream=True,
#     timeout = 10
# ).content
# r = urllib.request.urlopen(urllib.request.Request(
#     url
#     # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36'}
# )).read()
end_time = time.time()
print(f"\nTime taken to download the new update: %.2f secs\n"%(end_time-start_time))
# print("Content of 'update.zip' retrieved\n")
print("Reading the zip file\n")
f = ZipFile(updater)

a = f.namelist()
topdir = []
for i in a:
    if '/' in i:
        if i[:i.find('/')] not in topdir:
            topdir.append(i[:i.find('/')])
    else:
        topdir.append(i)
# print(topdir)

# quit()
ignore = ['libcrypto-1_1.dll', 'libssl-1_1.dll', 'select.pyd', 'unicodedata.pyd', '_bz2.pyd', '_hashlib.pyd', '_lzma.pyd', '_queue.pyd', '_socket.pyd', '_ssl.pyd']
existing = os.listdir(cwd)
common = list(set(topdir).intersection(existing))
print("\nChecking if 'deleteme' directory exists\n")
if 'deleteme' in os.listdir(cwd):
    print("\n'deleteme' dir found, deleting it.\n")
    send2trash('deleteme')

if 'deleteme' not in os.listdir():
    print("\ncreating 'deleteme'\n")
    os.mkdir('deleteme')

print("\nMoving files to 'deleteme'\n")
for file in common:
    if file not in ignore:
        shutil.move(file,'deleteme')

print("\nExtracting updated files from 'update.zip'\n")
for i in a:
    if i not in os.listdir(cwd):
        f.extract(i,cwd)
f.close()
send2trash(updater)
version['version'] = checkver
print("\nUpdating version\n")
with open(cwd+'version.json', 'w') as f:
    json.dump(version, f)
    f.close()
with open(cwd+'version.json', 'r') as f:
    print(f"Your software has been updated to {json.load(f)['version']}")
    f.close()
print("\nRedirecting to main program\n")
subprocess.call([cwd+'musicDL.exe'])