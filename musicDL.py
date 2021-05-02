import os, subprocess, requests, json, signal, shutil
from rich.console import Console
from send2trash import send2trash
from modules.ytDownloader import yt_downloader 
from modules.spotify_downloader import spotify_downloader 

ffmpeg=""
def check_ffmpeg():
    ffmpeg_available = True
    try:
        if sys.platform=='linux' or os.name=='posix':
            subprocess.check_output(['which', 'ffmpeg']) 
            ffmpeg = "ffmpeg"
            
        elif sys.platform=='win32' or os.name=='nt':
            subprocess.check_output(['where', 'ffmpeg'])
            ffmpeg="ffmpeg.exe"

    except Exception as e:
        print(e, e.output)
        ffmpeg_available = False
    return ffmpeg_available
print(ffmpeg)
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

def main():
    
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
        yt = yt_downloader(ffmpeg)
        spdl = spotify_downloader(ffmpeg)
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
            print("You can download FFMPEG.exe from insaiyancvk/music_downloader repository and add it to your path")
        elif sys.platform=='linux' or os.name=='posix':
            print("Use \n\tsudo apt install ffmpeg\nif you're on debian")

if __name__ == '__main__':
    global path
    path = os.getcwd()+'/'
    Console().rule("\n[bold]Note that you can always quit the program using \"ctrl+c\" shortcut [bold]", style="black", align="center")
    main()
#TODO 1: create playlist and singles directories in musicDL downloads foler ✔
#TODO 2: Ask user to give a name to the playlist and download the music to that folder ✔
#TODO 3: make functions for song and playlist downloading ✔
#TODO 4: implement OOP ✔
#TODO 5: use a different file for storing all the defined functions  ✔
#TODO 6: Add spotify support ✔
#TODO 7: make seperate classes for yt and spotify modules ✔
#TODO 8: use environment variables for storing API key and secret. {dropped}
#TODO 9: get dependencies folders into another folder and import from that. (aka beta test) {doesn't work}
#TODO 10: secure the client ID and Secret. ✔
#TODO 11: add different colors to different commands (https://ozzmaker.com/add-colour-to-text-in-python/) {just few, not all}
#TODO 11: convert all the audio files to mp3 or flac based on user choice {mp3 ✔ }{flac dropped}
#TODO 11: add thumbnails to the downloaded songs (https://www.geeksforgeeks.org/pafy-getting-thumbnail/) ✔
#TODO 12: release an executable file ✔
#TODO 13: Make GUI
#TODO 14: Automatically add the exe file to Windows system variables.