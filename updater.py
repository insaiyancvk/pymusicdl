import json, requests
import os
from zipfile import ZipFile

version = {}
with open('version.json', 'r') as f:
    version = json.load(f)
cver = version['version']

basegiturl = 'https://api.github.com'
headers = {"Accept": "application/vnd.github.v3+json"}

req = requests.get(basegiturl+'/repos/insaiyancvk/mygitbin/releases',headers = headers).json()

checkver = req[0]['tag_name']

if cver!=checkver:
    j=0
    for i in range(len(req[0]['assets'])):
        if 'update' in req[0]['assets'][i]['name']:
            j=i
    print("New update found!")
    print(req[0]['assets'][j]['browser_download_url'])
    print("Getting the redirected download link of the update file")
    # git = requests.get(req[0]['assets'][j]['browser_download_url'], timeout=1, allow_redirects = True)

    # url = git.url
    filename = 'update/update.zip'
    print("Downloading the new update as 'update.zip'")
    
    # r = requests.get(url, stream=True)
    # handle = open(filename, 'wb')
    # for chunk in r.iter_content(chunk_size=512):
    #     if chunk:
    #         handle.write(chunk)
    # handle.close
    with ZipFile(filename,'r') as zip:
        zip.extractall('/update')
    with ZipFile(filename,'r') as zip:
        a = zip.namelist()
    topdir = []
    for i in a:
        if '/' in i:
            if i[:i.find('/')] not in topdir:
                topdir.append(i[:i.find('/')])
        else:
            topdir.append(i)
    existing = os.listdir("C:\\Users\\Asus\\Desktop\\setup\\Music Downloader")
    common = list(set(topdir).intersection(existing))
    print(len(common))
else:
    print("Your software is up to date")