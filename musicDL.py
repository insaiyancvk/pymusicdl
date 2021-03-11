import os
from modules.yt_downloader import yt_downloader

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

create_dir()


ch = int(input("\nEnter 1 to download a song \n2 to download a playlist: "))
yt = yt_downloader()
if ch == 1:
    yt.download_singles()

elif ch == 2:
    yt.download_playlist()
    
else:
    print("invalid option :(")

#TODO 1: create playlist and singles directories in musicDL downloads foler ✔
#TODO 2: Ask user to give a name to the playlist and download the music to that folder ✔
#TODO 3: make functions for song and playlist downloading ✔
#TODO 4: implement OOP ✔
#TODO 5: use a different file for storing all the defined functions 
#TODO 6: Add spotify support
#TODO 7: make seperate classes for yt and spotify modules