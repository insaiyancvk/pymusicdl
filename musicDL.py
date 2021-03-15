import os
from modules.ytDownloader import yt_downloader 
from modules.spotify_downloader import spotify_downloader 

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

def main():

    print(f"\nEnter 1 to download a song \n2 to download a YouTube Playlist\n3 to download a Spotify Playlist:")
    ch = int(input())
    yt = yt_downloader()
    spdl = spotify_downloader()
    if ch == 1:
        yt.download_singles()

    elif ch == 2:
        yt.download_playlist()

    elif ch == 3:
        spdl.interface()

    else:
        print("invalid option :(")
    n = input("Do you want to continue? (Y/N): ")
    if n.lower() == 'y':
        main()
    else:
        print("\nSee you later!\n")
        quit()
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
#TODO 11: add different colors to different commands (https://ozzmaker.com/add-colour-to-text-in-python/)
#TODO 11: convert all the audio files to mp3 or flac based on user choice 
#TODO 11: add thumbnails to the downloaded songs (https://www.geeksforgeeks.org/pafy-getting-thumbnail/)
#TODO 12: release an executable file
#TODO 13: Make GUI