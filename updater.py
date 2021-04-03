from io import BytesIO
import json, requests
import stat
import os, shutil, sys, subprocess
from zipfile import ZipFile

if 'updater' in str(os.getcwd()):
    cwd = str(os.getcwd()).replace('\\updater','\\')
else:
    cwd = os.getcwd()+'\\'
version = {}
with open('version.json', 'r') as f:
    version = json.load(f)
    f.close()
cver = version['version']

basegiturl = 'https://api.github.com'
headers = {"Accept": "application/vnd.github.v3+json"}

req = requests.get(basegiturl+'/repos/insaiyancvk/music_downloader/releases',headers = headers).json()

checkver = req[0]['tag_name']
details = req[0]['body']

if cver!=checkver:
    j=0
    for i in range(len(req[0]['assets'])):
        if 'update' in req[0]['assets'][i]['name']:
            j=i
    print(f"\n\t***** New update {checkver} avaliable! *****\n")
    choice = input("Would you like to update? (Y/N): ")
    if choice.lower() == 'y':
        print("\nHere are the new update details: \n")
        print(details)
        print("\nGetting the redirected download link of the update file\n")

        git = requests.get(req[0]['assets'][j]['browser_download_url'], allow_redirects = True)
        url = git.url
        print("Getting details from the redirected link\n")    
        r = requests.get(url, stream=True)
        f = ZipFile(BytesIO(r.content))
        a = f.namelist()
        
        topdir = []
        for i in a:
            if '/' in i:
                if i[:i.find('/')] not in topdir:
                    topdir.append(i[:i.find('/')])
            else:
                topdir.append(i)
        ignore = ['libcrypto-1_1.dll', 'libssl-1_1.dll', 'select.pyd', 'unicodedata.pyd', '_bz2.pyd', '_hashlib.pyd', '_lzma.pyd', '_queue.pyd', '_socket.pyd', '_ssl.pyd']
        existing = os.listdir(cwd)
        common = list(set(topdir).intersection(existing))
        if 'deleteme' not in os.listdir(cwd):
            os.mkdir(cwd+'deleteme')
        
        for file in common:
            if file not in ignore:
                shutil.move(cwd+file,cwd+'deleteme')

        for i in a:
            if i not in os.listdir(cwd):
                f.extract(i,cwd)

        if 'deleteme' in os.listdir(cwd):
            if sys.platform == 'win32':
                os.system(f'rmdir /S /Q {cwd+"deleteme"}')
                if 'deleteme' in os.listdir(cwd):
                    try:
                        os.chmod(f'{cwd+"deleteme"}',0o777)
                        shutil.rmtree(f'{cwd+"deleteme"}', stat.S_IWUSR)
                    except:
                        pass
        version['version'] = checkver
        with open('version.json', 'w') as f:
            json.dump(version, f)
            f.close()
        with open('version.json', 'r') as f:
            print(f"Your software has been updated to {json.load(f)['version']}")
            f.close()
        subprocess.call([cwd+'musicDL.exe'])
    else:
        print("\nRestart musicDL for downloading the updates :) ")
        subprocess.call([cwd+'musicDL.exe'])

else:
    print(f"\nYou are running {cver}")
    subprocess.call([cwd+'musicDL.exe'])
