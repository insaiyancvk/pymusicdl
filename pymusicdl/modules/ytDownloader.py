import os, time, glob, sys, subprocess
from youtube_title_parse import get_artist_title
try:
    import pafy # type: ignore
except:
    print("Install 'pafy' library using 'pip install pafy'")
from rich.console import Console
try:
    from pytube import Playlist
except:
    print("Install 'pytube' library using 'pip install pytube'")
try:
    from .common import common # type: ignore
except:
    from common import common # type: ignore

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

        Console().print("\ntip:\n  [bold white]* give the name of song and the artist for better search results)\n  * you could paste the video url itself if you're looking for a specific song.[/bold white]\n")
        s = input("Enter the song name: ")
        print(f"\nHere are the top 7 search results for {s}. Enter the serial number to download it.\n")
        s = s.replace(" ","+")

        # Get top 7 video URLs
        video_url = cm.get_url(s)
        j=1
        for i in video_url:
            if len(video_url) == 0:
                print("\nThere were no results :(\nmaybe try checking the spelling of the song\n")
                quit()
            try:
                t = pafy.new(i)
                print(f"{j} - {t.title}  ({t.duration})")
                j+=1
            except:
                j+=1
                continue
        c = int(input("\nEnter the serial number: "))

        cm.download_song(video_url[c-1],'','')
        print("\n\n")
        print("\t","="*100)
        Console().print(f"\n\n\t    Your song is downloaded in \"[bold]/musicDL downloads/singles[/bold]\" folder on desktop\n")
        print("\t","="*100)
        print("\n\n")
        op = input("Enter:\n  1 - open the folder where the song is downloaded\n  2 - open the song that's downloaded\n  3 - exit : ")
        
        if op == '1':
            if sys.platform=='win32' or os.name=='nt':
                os.startfile(".")
            elif sys.platform=='linux' or os.name=='posix':
                subprocess.call(['xdg-open','.'])

        elif op == '2':
            file = pafy.new(video_url[c-1]).title
            a,t = get_artist_title(file)

            if file+".mp3" in os.listdir():

                if sys.platform=='win32' or os.name=='nt':
                    os.startfile(file+".mp3")

                elif sys.platform=='linux' or os.name=='posix':
                    subprocess.call(['xdg-open',file+".mp3"])
                
            elif t+" - "+a+".mp3" in os.listdir():
                if sys.platform=='win32' or os.name=='nt':
                    os.startfile(t+" - "+a+".mp3")

                elif sys.platform=='linux' or os.name=='posix':
                    subprocess.call(['xdg-open',t+" - "+a+".mp3"])
                
            else:
                files = glob.glob("./*")
                song = max(files, key = os.path.getctime)
                if sys.platform=='win32' or os.name=='nt':
                    os.startfile(song)
                elif sys.platform=='linux' or os.name=='posix':
                    subprocess.call(['xdg-open',song])
        else:
            return
        
    
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
        Console().print(" "*20,"*","          ","[bold red]MAKE SURE YOUR PLAYLIST IS PUBLIC[/bold red]","           ","*")
        Console().print(" "*20,"*","     ","[bold red]YOU CAN MAKE IT PRIVATE LATER AFTER DOWNLOADING[/bold red]","  ","*")
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
        
        start_time = time.time()
        try:
            plLinks = self.get_playlist_url(plLink)
        except Exception as e:
            print(f"Something went wrong. Maybe check your URL. Here's the reason from the compiler: {e}")
            print("Exiting the program")
            return
        end_time = time.time()
        print(f"Time taken to fetch the URLs from Youtube: %.2f secs\n"%(end_time-start_time))
        total_songs = len(plLinks)
        for i in plLinks:
            cm.download_song(i,"",'')
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        print("\n\n")
        print("\t","="*100)
        Console().print(f"\n\n\t     Your playlist is downloaded in \"[bold]/musicDL downloads/Playlists/{plName}[/bold]\" folder on desktop \n")
        print("\t","="*100)
        print("\n\n")
        op = input("Would you like to open the the playlist? (Y/N) ")
        if op.lower() == "y":
            if sys.platform=='win32' or os.name=='nt':
                os.startfile(".")
            elif sys.platform=='linux' or os.name=='posix':
                subprocess.call(['xdg-open','.'])
        else:
            return