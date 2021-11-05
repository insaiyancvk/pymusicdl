import os, subprocess, sys, logging
import traceback
from rich.console import Console



try:
    from .modules.ytDownloader import yt_downloader
except:
    from modules.ytDownloader import yt_downloader

try:
    from .modules.spotify_downloader import spotify_downloader 
except:
    from modules.spotify_downloader import spotify_downloader 

try:
    from .modules.picker import Picker
except:
    from modules.picker import Picker

def check_ffmpeg():
    ffmpeg_available = True
    try:
        if sys.platform=='linux' or os.name=='posix':
            subprocess.check_output(['which', 'ffmpeg']) 
            
        if sys.platform=='win32' or os.name=='nt':
            subprocess.check_output(['where', 'ffmpeg'])

    except Exception:
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
    if sys.platform=='win32' or os.name=='nt':
        os.system("cls")
    elif sys.platform=='linux' or os.name=='posix':
        os.system("clear")
        
    if check_ffmpeg():

        os.chdir(path)

        picker = Picker(["Download a single song","Download a YouTube Playlist","Download from Spotify"],"Select your choice using arrow keys or press q to quit", indicator=" => ")
        picker.register_custom_handler(ord('q'), lambda picker: exit())
        picker.register_custom_handler(ord('Q'), lambda picker: exit())
        _,ch = picker.start()

        Console().rule("\n[bold]Note that you can always quit the program using \"ctrl+c\" shortcut [bold]", style="black", align="center")
        create_dir()
        LOG_FILE = os.path.expanduser("~/Desktop/musicDL downloads/logger.log")
        logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)
        print()
        ch+=1
        
        if ch == 1:
            try:
                yt_downloader().download_singles()
            except Exception as e:
                logging.exception(e)
                print(f"\n\nLooks like something went wrong :(\n{traceback.format_exc()}\n\n")
                print("The error has been logged to logger.log file in 'musicDL downloads' on Desktop for reference")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 2:
            try:
                yt_downloader().download_playlist()
            except Exception as e:
                logging.exception(e)
                print(f"\n\nLooks like something went wrong :(\n{traceback.format_exc()}\n\n")
                print("The error has been logged to logger.log file in 'musicDL downloads' on Desktop for reference")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 3:
            try:
                spotify_downloader().interface()
            except Exception as e:
                logging.exception(e)
                print(f"\n\nLooks like something went wrong :(\n{traceback.format_exc()}\n\n")
                print("The error has been logged to logger.log file in 'musicDL downloads' on Desktop for reference")
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
            print("ffmpeg.exe not found.")

        elif sys.platform=='linux' or os.name=='posix':
            print("Use \n\tsudo apt install ffmpeg\nif you're on debian")