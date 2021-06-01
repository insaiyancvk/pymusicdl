import os, subprocess
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel

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
        subprocess.check_output(['which', 'ffmpeg'])
    except Exception as e:
        ffmpeg_available = False
    return ffmpeg_available
    
def create_dir():
    """
    Creates "musicDL downloads" directory on desktop when called. Takes no parameters.
    """
    
    os.chdir(os.path.expanduser("~/storage"))
    try:
        os.chdir("music")
    except:
        os.mkdir("music")
        os.chdir("music")

path = os.getcwd()+'/'
def main():
    
    os.system("clear")
        
    if check_ffmpeg():

        os.chdir(path)

        picker = Picker(["Download a single song","Download a YouTube Playlist","Download from Spotify"],"Use arrow keys to select\nor press q to quit", indicator=" => ")
        picker.register_custom_handler(ord('q'), lambda picker: exit())
        picker.register_custom_handler(ord('Q'), lambda picker: exit())
        _,ch = picker.start()

        Console().rule("", style="black", align="center")
        Console().print(Columns([Panel("\n[bold]Note that you can always quit the program \nusing \"ctrl+c\" shortcut [bold]")]))
        create_dir()
        print()
        
        if ch == 0:
            try:
                yt_downloader().download_singles()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 1:
            try:
                yt_downloader().download_playlist()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass

        elif ch == 2:
            try:
                spotify_downloader().interface()
            except Exception as e:
                print(f"\n\nLooks like something went wrong :(\n{e}\n\n")
                print("Take a screenshort and raise an issue in github or send it to the devs\n")
                pass
        n = input("Do you want to continue? (Y/N): ")
        if n.lower() == 'y':
            main()
        else:
            print("\nSee you later!\n")
    else:
        print("Please install FFMPEG")  
        print("Use \n\tapt install ffmpeg\n")
        subprocess.call(['apt','install','ffmpeg'])