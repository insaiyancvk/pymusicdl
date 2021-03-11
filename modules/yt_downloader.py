from __future__ import unicode_literals
import urllib.request, re, requests, pafy, os, time
from bs4 import BeautifulSoup
from pytube import Playlist
from youtube_title_parse import get_artist_title

class yt_downloader():
    def get_url(self,s,n=7):
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
    def download_song(sefl,url):
        """
        Download the song by passing the video URL as a parameter
        """

        try:
            v = pafy.new(url)
        except:
            print("\nSome error occurred while downloading the song\n")
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

    def get_playlist_url(self,plLink):
        """
        Returns all the song links of a playlist. Given the playlist URL.
        """

        pl_links = []
        pl = Playlist(plLink)
        for url in pl.video_urls:
            pl_links.append(url)
        return pl_links

    def download_singles(self):
        """
        Downloads songs based on youtube search. Takes a name as an input.
        """

        try:
            os.chdir("singles")
        except:
            os.mkdir("singles")
            os.chdir("singles")

        print("(tip: give the name of song and the artist for better search results)")
        s = input("Enter the song name: ")
        print(f"\nHere are the top 7 search results for {s}. Enter the serial number to download it.\n")
        s = s.replace(" ","+")

        # Get top 7 video URLs
        video_url = self.get_url(s)
        j=1
        for i in video_url:
            t = pafy.new(i)
            print(f"{j} - {t.title}")
            j+=1
        c = int(input("\nEnter the serial number: "))

        self.download_song(video_url[c-1])
        print(f"\nYour song is downloaded in \"/musicDL downloads/singles\" folder on desktop\n")

    def download_playlist(self):
        """
        Downloads a playlist of songs given the URL
        """

        try:
            os.chdir("Playlists")
        except:
            os.mkdir("Playlists")
            os.chdir("Playlists")
        print()
        print(" "*20,"*"*60)
        print(" "*20,"*"," "*56,"*")
        print(" "*20,"*","          ","MAKE SURE YOUR PLAYLIST IS PUBLIC","           ","*")
        print(" "*20,"*","     ","YOU CAN MAKE IT PRIVATE LATER AFTER DOWNLOADING","  ","*")
        print(" "*20,"*"," "*56,"*")
        print(" "*20,"*"*60,"\n")

        plLink = input("Enter your YouTube playlist URL: ")
        plName = input("Give a name to your playlist: ")

        try:
            os.chdir(plName)
        except:
            os.mkdir(plName)
            os.chdir(plName)

        if "https://www" in plLink:
            plLink = plLink.replace("https://www","https://music")
        plLinks = self.get_playlist_url(plLink)

        total_songs = len(plLinks)
        for i in plLinks:
            self.download_song(i)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        print(f"\nYour playlist is downloaded in \"/musicDL downloads/Playlists/{plName}\" folder on desktop\n")