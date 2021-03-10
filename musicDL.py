from __future__ import unicode_literals
import urllib.request, re, requests, pafy, os, time
from bs4 import BeautifulSoup
from pytube import Playlist
from youtube_title_parse import get_artist_title

def create_dir():
    try:
        os.chdir("musicDL downloads")
    except:
        os.mkdir("musicDL downloads")
        os.chdir("musicDL downloads")

os.chdir(os.path.expanduser("~/Desktop"))
create_dir()

def get_url(s,n=7):
    """
    Give a video ID as an argument to this function. It returns top n (7 by default) video URLs.
    """
    query = "https://www.youtube.com/results?search_query="+s
    baseurl = "https://www.youtube.com/watch?v="
    response = urllib.request.urlopen(query)
    html = response.read()
    video_ids = re.findall(r"watch\?v=(\S{11})", html.decode())
    urls = []
    for i in video_ids[:n]:
        urls.append(baseurl+i)
    return urls

# Download the song based on URL
def download_song(url):
    """
    Download the song by passing the video URL as a parameter
    """
    try:
        v = pafy.new(url)
    except:
        print("Some error occurred while downloading the song\n")
        return
    name = v.title
    audio = v.getbestaudio(preftype="m4a")
    print(f"\ndownloading {name} as an audio file")
    audio.download()
    time.sleep(1)
    try:
        artist, title = get_artist_title(name)
        dirs = os.listdir()
        for i in dirs:
            if name in i:
                ind1 = len(i) - 1 - i[::-1].index('.')
                ext = i[ind1:]
                os.rename(i,title+" - "+artist+ext)
    except:
        pass

def get_playlist_url(plLink):
    """
    Returns all the song links of a playlist. Given the playlist URL.
    """
    pl_links = []
    pl = Playlist(plLink)
    for url in pl.video_urls:
        pl_links.append(url)
    return pl_links

ch = int(input("Enter 1 to download a song and 2 to download a playlist: "))

if ch == 1:
    print("(tip: give the name of song and the artist for better search results)")
    s = input("Enter the song name: ")
    s = s.replace(" ","+")

    # Get top 7 video URLs
    video_url = get_url(s)
    print(f"Here are the top 10 search results for {s}. Enter the serial number to download it.\n")
    j=1
    for i in video_url:
        t = pafy.new(i)
        print(f"{j} - {t.title}")
        j+=1
    c = int(input("\nEnter the serial number: "))

    download_song(video_url[c-1])
    print("All the songs are downloaded in \"musicDL downloads\" folder on desktop")

elif ch == 2:

    print("\n"," "*20,"*"*60)
    print(" "*20,"*"," "*56,"*")
    print(" "*20,"*","          ","MAKE SURE YOUR PLAYLIST IS PUBLIC","           ","*")
    print(" "*20,"*","     ","YOU CAN MAKE IT PRIVATE LATER AFTER DOWNLOADING","  ","*")
    print(" "*20,"*"," "*56,"*")
    print(" "*20,"*"*60,"\n")

    plLink = input("Enter your YouTube playlist URL: ")
    if "https://www" in plLink:
        plLink = plLink.replace("https://www","https://music")
    plLinks = get_playlist_url(plLink)

    for i in plLinks:
        download_song(i)
    print("All the songs are downloaded in \"musicDL downloads\" folder on desktop")
    
else:
    print("invalid option :(")