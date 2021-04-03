import json, requests
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO


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
    print("Downloading the new update as 'update.zip'")
    url = req[0]['assets'][0]['browser_download_url']
    filename = 'update/update.zip'
    print("Downloading")
    zipresp = urlopen(url)
    print("create new file")
    tempzip = open(filename,'wb')
    print("write zip file contents")
    tempzip.write(zipresp.read())
    tempzip.close()
    zf = ZipFile(filename)
    print('\n\nExtracting all files in "update.zip" \n\n')
    zf.extractall(path='/update/')
    zf.close()
    print("All files Extracted")
else:
    print("Your software is up to date")