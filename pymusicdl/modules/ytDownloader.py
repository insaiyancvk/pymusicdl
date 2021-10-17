import os, time, glob, sys, subprocess, pafy
# import traceback
from pytube import Playlist
from youtube_title_parse import get_artist_title
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel

try:
    from .common import common
except:
    from common import common

try:
    from .picker import Picker
except:
    from picker import Picker

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

        Console().print(Columns([Panel("\ntip:\n  [bold white]* give the name of song and the artist for better search results)\n  * you could paste the youtube video url itself if you're looking for a specific song.[/bold white]\n")]))
        s = input("\nEnter the song name: ")
        print(f"\nLoading search results for {s}...\n")
        s = s.replace(" ","+")

        # Get top 7 video URLs
        video_url = cm.get_url(s)
        j=1
        names = []
        for i in video_url:
            if len(video_url) == 0:
                print("\nThere were no results :(\nmaybe try checking the spelling of the song\n")
                quit()
            try:
                t = pafy.new(i)
                names.append(f"{j} - {t.title}  ({t.duration})")
                j+=1
            except:
                j+=1
                # print(traceback.format_exc())
                # time.sleep(2)
                continue
        
        picker = Picker(names,"Select your choice using arrow keys or press q to quit", indicator=" => ")
        picker.register_custom_handler(ord('q'), lambda picker: exit())
        picker.register_custom_handler(ord('Q'), lambda picker: exit())
        op,c = picker.start()
        
        Console().print(Columns([Panel(f"\nDownload size: [green]{int((pafy.new(video_url[c]).getbestaudio().get_filesize()/1048576)*100)/100} MB[/green]\n")]))
        print()
        
        print("\nWould you like an mp3 or flac conversion?\n")
        Console().rule("[bold]**** Here's a quick comparison on both codec ****[bold]", style="black", align="center")
        print("\n")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Avaliable Codec")
        table.add_column("Bit-rate")
        table.add_column("File Size")
        table.add_column("Remarks")
        table.add_row(
            "mp3", "320kbps (default)","~7.3MB for 3min song","Standard codec with normal experience"
        )
        table.add_row()
        table.add_row(
            "flac", "usually >800kbps (1713kbps while testing, 5x of mp3)","~39MB for 3min song","Takes fair amount of disk space but gives amazing experience"
        )
        Console().print(table)
        Console().rule("\n[bold]Note: this step [red]does not use internet[/red] [bold]\n", style="black", align="center")

        print('\nIf you are confused on what to select, select mp3 (default)')
        z = input("\tEnter\n\t1/flac/f - flac\n\tany key - mp3 : ")

        cm.download_song(video_url[c],'','',z)
        print("\n\n")
        Console().print(Columns([Panel(f"\n    Your song is downloaded in \"[bold cyan]/musicDL downloads/singles[/bold cyan]\" folder on desktop    \n")]))
        print("\n\n")
        time.sleep(3)

        picker = Picker(["Open the song directory","Open the song itself"],"Select your choice using arrow keys or press q to quit", indicator=" => ")
        picker.register_custom_handler(ord('q'), lambda picker: 'qq')
        picker.register_custom_handler(ord('Q'), lambda picker: 'QQ')
        _,op = picker.start()

        if op == 0:
            if sys.platform=='win32' or os.name=='nt':
                os.startfile(".")
            elif sys.platform=='linux' or os.name=='posix':
                subprocess.call(['xdg-open','.'])

        elif op == 1:
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
        Console().print(Columns([Panel(f"\n       [bold red]MAKE SURE YOUR PLAYLIST IS PUBLIC[/bold red]\n  [bold red]YOU CAN MAKE IT PRIVATE AFTER DOWNLOADING[/bold red]     \n")]))

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
        print(f"\nTime taken to fetch the URLs from Youtube: %.2f secs"%(end_time-start_time))

        data = 0.0
        print("\nCalculating total download size...\n")
        for i in plLinks:
            try:
                data += pafy.new(i).getbestaudio().get_filesize()
            except:
                # print(traceback.format_exc())
                # time.sleep(2)
                continue
        data = int((data/1048576)*100)/100
        
        Console().print(Columns([Panel(f"\nDownload size: [green]{data} MB[/green]\n")]))
        print()
        
        print("\nWould you like an mp3 or flac conversion?\n")
        Console().rule("[bold]**** Here's a quick comparison on both codec ****[bold]", style="black", align="center")
        print("\n")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Avaliable Codec")
        table.add_column("Bit-rate")
        table.add_column("File Size")
        table.add_column("Remarks")
        table.add_row(
            "mp3", "320kbps (default)","~7.3MB for 3min song","Standard codec with normal experience"
        )
        table.add_row()
        table.add_row(
            "flac", "usually >800kbps (1713kbps while testing, 5x of mp3)","~39MB for 3min song","Takes fair amount of disk space but gives amazing experience"
        )
        Console().print(table)
        Console().rule("\n[bold]Note: this step [red]does not use internet[/red] [bold]\n", style="black", align="center")

        print('\nIf you are confused on what to select, select mp3 (default)')
        z = input("\tEnter\n\t1/flac/f - flac\n\tany key - mp3 : ")

        total_songs = len(plLinks)
        for i in plLinks:
            if sys.platform=='win32' or os.name=='nt':
                os.system("cls")
            elif sys.platform=='linux' or os.name=='posix':
                os.system("clear")
            Console().print("[bold][green]Downloaded songs:[/green][/bold]")
            Console().print(Columns([Panel(''.join(list(''.join(iz + '\n' * (N % 3 == 2) for N, iz in enumerate([ii+" " for ii in user.split()]))))+"\n[b][green]Downloaded[/green][/b]", expand=True) for user in os.listdir()]))
            try:
                cm.download_song(i,"",'',z)
            except Exception:
                # print(traceback.format_exc())
                # time.sleep(2)
                continue
            time.sleep(1)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")

        print("\n\n")
        Console().print(Columns([Panel(f"\n     Your playlist is downloaded in \"[bold]/musicDL downloads/Playlists/{plName}[/bold]\" folder on desktop     \n")]))
        print("\n\n")

        op = input("Would you like to open the the playlist? (Y/N) ")
        if op.lower() == "y":
            if sys.platform=='win32' or os.name=='nt':
                os.startfile(".")
            elif sys.platform=='linux' or os.name=='posix':
                subprocess.call(['xdg-open','.'])
        else:
            return