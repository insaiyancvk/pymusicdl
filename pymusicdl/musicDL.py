import os, subprocess, requests, json, shutil, sys
from rich.console import Console
from .modules.ytDownloader import yt_downloader 
from .modules.spotify_downloader import spotify_downloader 

def check_ffmpeg():
    ffmpeg_available = True
    try:
        if sys.platform=='linux' or os.name=='posix':
            subprocess.check_output(['which', 'ffmpeg']) 
            
        if sys.platform=='win32' or os.name=='nt':
            subprocess.check_output(['where', 'ffmpeg'])

    except Exception as e:
        print(e)
        ffmpeg_available = False
    return ffmpeg_available
    
def create_dir():
    """
    Creates "musicDL downloads" directory on desktop when called. Takes no parameters.
    """
    
    os.chdir(os.path.expanduser("~/Desktop"))
    try:
        os.chdir("musicDL downloads")
    except:
        os.mkdir("musicDL downloads")
        os.chdir("musicDL downloads")

path = os.getcwd()+'/'
def main():
    Console().rule("\n[bold]Note that you can always quit the program using \"ctrl+c\" shortcut [bold]", style="black", align="center")
    if check_ffmpeg():

        os.chdir(path)
        
        create_dir()
        print()
        print(f"\n Enter \n\n 1 - download a song \n 2 - download a YouTube Playlist\n 3 - download from Spotify")    
        try:
            ch = int(input("\n  Enter the serial number: "))
        except ValueError:
            Console().rule("[red]Invalid input, try 1/2/3[/red]\n",align="left",style="black")
            main()
        yt = yt_downloader()
        spdl = spotify_downloader()
        if ch == 1:
            try:
                yt.download_singles()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 2:
            try:
                yt.download_playlist()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 3:
            try:
                spdl.interface()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        else:
            print("\ninvalid option :(\n")
            main()
        n = input("Do you want to continue? (Y/N): ")
        if n.lower() == 'y':
            main()
        else:
            print("\nSee you later!\n")
    else:
        print("Please install FFMPEG and add it to your environment variable")  
        if sys.platform=='win32' or os.name=='nt':
            print("You can download FFMPEG.exe from insaiyancvk/pymusicdl repository and add it to your path")
        elif sys.platform=='linux' or os.name=='posix':
            print("Use \n\tsudo apt install ffmpeg\nif you're on debian")