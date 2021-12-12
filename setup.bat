@echo off & py -x "%~f0" %* & goto :eof

import os,sys,subprocess

try:
    import requests
except:
    subprocess.call(['py', '-m', 'pip', 'install', 'requests'])
    import requests

try:
    import pafy
except:
    subprocess.call([f'{sys.executable}', '-m', 'pip', 'install', 'https://github.com/mps-youtube/pafy/archive/refs/heads/develop.zip'])

try:
    import pymusicdl.musicDL
except ImportError:
    print("pymusicdl not found. installing pymusicdl.")
    subprocess.call(['py', '-m', 'pip', 'install', 'pymusicdl'])
def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None
    def save_response_content(response, destination):
        total = 76383232
        CHUNK_SIZE = 32768
        downloaded=0
        with open(destination, "wb") as f:
            prev_done = 0
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                if done>prev_done:  
                    prev_done = done
                    os.system("cls")
                    print("\n   FFMPEG not fouond.\n\n[*]Downloading FFMPEG\n")
                    print(f'[*][{"="*done}{"."*(50-done)}] {done*2}%',end='')
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)   
    print("\nffmpeg downloaded\n")

os.chdir(sys.executable.replace("python.exe","/Scripts"))
ff = False
try:
    print("Searching for ffmpeg")
    subprocess.check_output(['where', 'ffmpeg'])
    print("ffmpeg found.")
except:
    print("ffmpeg not found.")
    ff=True
if ff:
    print("Downloading ffmpeg")
    download_file_from_google_drive("140PFz74Ncwb4-Ja_3s7HE6iOii3TDo4A","ffmpeg.exe")
if "musicdl.bat" not in os.listdir():
    mdl = open(r"musicdl.bat","w+")
    mdl.write('@echo off & py -x "%~f0" %* & goto :eof\n\nfrom pymusicdl.musicDL import main, check_ffmpeg\n\nif check_ffmpeg():\n    main()')
    mdl.close()
    os.system("cls")
    print("Type 'musicdl' in cmd to download music :)")
input("press any key to exit")
