import os

try:
    import pafy # type: ignore
except:
    print("Install 'pafy' library using 'pip install pafy'")

try:
    from pytube import Playlist
except:
    print("Install 'pytube' library using 'pip install pytube'")
try:
    from .common import common # type: ignore
except:
    from common import common

class yt_downloader():

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
        Downloads songs based on youtube search. Takes a string as an input.
        """

        cm = common()
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
        video_url = cm.get_url(s)
        j=1
        for i in video_url:
            t = pafy.new(i)
            print(f"{j} - {t.title}")
            j+=1
        c = int(input("\nEnter the serial number: "))

        cm.download_song(video_url[c-1])
        print(f"\nYour song is downloaded in \"/musicDL downloads/singles\" folder on desktop\n")

    def download_playlist(self):
        """
        Downloads a playlist of songs given the URL
        """

        cm = common()
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
        
        try:
            plLinks = self.get_playlist_url(plLink)
        except Exception as e:
            print(f"Something went wrong. Maybe check your URL. Here's the reason from the compiler: {e}")
            print("Exiting the program")
            quit()

        total_songs = len(plLinks)
        for i in plLinks:
            cm.download_song(i)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        print(f"\nYour playlist is downloaded in \"/musicDL downloads/Playlists/{plName}\" folder on desktop\n")