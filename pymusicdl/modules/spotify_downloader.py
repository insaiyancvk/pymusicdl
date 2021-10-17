import json, base64, os, requests, time, pafy, sys, subprocess
# import traceback
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel
try:
    import spotipy 
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    print("Install spotipy library using 'pip install spotipy'")

try:
    from .common import common
except:
    from common import common

destination = os.getcwd()+'/sec.json'
class spotify_downloader():

    def __init__(self):
        self.ytd =  common(spo=True)
    
    def create_PLdir(self,plName):
        """ creates a playlist directory with the given name """

        try:
            os.chdir("Playlists")
        except:
            os.mkdir("Playlists")
            os.chdir("Playlists")
        try:
            os.chdir(plName)
        except:
            os.mkdir(plName)
            os.chdir(plName)
        
    
    def get_json(self):
        id = '1SFCB1mjcNz3U5X0HZTy4j5kpoMdemKWH'
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
            else:
                token = None
        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    
    def get_credentials(self):
        """ returns a token object after authentication. """

        empty = {}
        with open(destination, 'r') as f:
            data = json.load(f)
        with open(destination,'w') as f:
            json.dump(empty,f)
        for key in data.keys():
            data[key] = base64.b64decode(data[key]).decode('utf8')
        client_id = data['id']
        client_secret = data['secret']
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_id(self,url):
        """ returns the playlist/album ID given the playlist URI """

        if "playlist" in url:
            ind = url.index("playlist")
            return url[ind+9:ind+31]
        elif "album" in url:
            ind = url.index("album")
            return url[ind+6:ind+28]

    def get_yt_urls(self,tracks):
        """ returns a list of urls that are fetched successfully and dictionary of urls that were failed to be fetched. """

        urls = []
        for key in tracks.keys():
            try:
                got_url = (key+"+lyrics+"+tracks[key]).replace(' ','+')
                print(f"Fetching youtube URL of {key} - {tracks[key]}")
                urls.append(self.ytd.get_url(got_url)[0])
            except Exception as e:
                print(f"\nCould not fetch the link for \"{key} {tracks[key]}\" because: {e}\nmaybe download it as a single")
        return urls

    def get_playlist_tracks(self, sp, plID):
        """ returns a dictionary of track name as key and artist name as value of a spotify playlist given the spotipy token credentials object and playlist id """

        alburl = []
        together = {}
        tracks = {}
        playlist = {}
        offset = 0
        total = sp.playlist_tracks(plID)['total']
        while total-offset>=0:
            playlist = sp.playlist_tracks(plID,offset=offset)
            for i in range(len(playlist['items'])):
                if len(playlist['items'][i]['track']['album']['images']) == 0:
                    together[playlist['items'][i]['track']['name']] = [playlist['items'][i]['track']['artists'][0]['name'],'https://virginradio.co.uk/sites/virginradio.co.uk/files/song_cover/20160626/coverart_1.png']
                else:
                    together[playlist['items'][i]['track']['name']] = [playlist['items'][i]['track']['artists'][0]['name'],playlist['items'][i]['track']['album']['images'][1]['url']]
            offset +=100
        for key in together.keys():
            tracks[key] = together[key][0]
            alburl.append(together[key][1])
        return tracks, alburl

    def get_album_tracks(self, sp, alID):
        """ returns a dictionary of track name as key and artist name as value of a spotify album given the spotipy token credentials object and album id """

        album = sp.album_tracks(alID)
        tracks = {}
        alburl = []
        for i in range(len(album['items'])):
            tracks[album['items'][i]['name']] = album['items'][i]['artists'][0]['name']
            alburl.append(sp.track(album['items'][i]['id'])['album']['images'][1]['url'])
        return tracks, alburl

    def download_PL(self,plName, urls, alburl, sponame):
        """ downloads all the audio of URLs """

        self.create_PLdir(plName)
        c=1
        data = 0.0
        print("\nCalculating total download size...\n")
        for i in urls:
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
        z = input("\tEnter\n\tf - flac\n\tany key - mp3 : ")

        for i,j,k in zip(urls, alburl, sponame):
            if os.name == "nt":
                os.system("cls")
            elif os.name == "posix":
                os.system("clear")
            Console().print("[bold][green]Downloaded songs:[/green][/bold]")
            Console().print(Columns([Panel(''.join(list(''.join(iz + '\n' * (N % 3 == 2) for N, iz in enumerate([ii+" " for ii in user.split()]))))+"\n[b][green]Downloaded[/green][/b]", expand=True) for user in os.listdir()]))
            try:
                self.ytd.download_song(i, j, k, z)
            except:
                # print(traceback.format_exc())
                # time.sleep(2)
                continue
            c+=1

    def interface(self):      
        
        self.get_json()
        sponame = []
        print("\n\tConnecting to spotify...\n")
        sp = self.get_credentials()

        plLink = input("\nEnter the Spotify playlist/album URL: ")
        plName = input("\nGive a name to your playlist: ")

        if "playlist" in plLink:    
            plID = self.get_id(plLink)
            tracks,alburls = self.get_playlist_tracks(sp, plID)
        elif "album" in plLink:
            alID = self.get_id(plLink)
            tracks, alburls = self.get_album_tracks(sp,alID)
        else: 
            print("Invalid link, exiting")
            return

        start_time = time.time()
        Console().print(f"\n[bold]Fetching all the relevant URLs[/bold]")
        urls = self.get_yt_urls(tracks)
        end_time = time.time()
        print(f"Time taken to fetch the URLs from Youtube: %.2f secs\n"%(end_time-start_time))

        Console().print("\n[green]Downloading the songs[/green]\n")
        for i in tracks.keys():
            sponame.append(tracks[i]+" - "+i)

        # download the tracks
        self.download_PL(plName, urls, alburls, sponame)

        # check if all the songs are downloaded
        total_songs = len(urls)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        
        Console().print(Columns([Panel(f"\n     Your playlist is downloaded in \"[bold]/musicDL downloads/Playlists/{plName}[/bold]\" folder on desktop     \n")]))
        op = input("Would you like to open the the playlist? (Y/N) ")
        if op.lower() == "y":
            if sys.platform=='win32' or os.name=='nt':
                os.startfile(".")
            elif sys.platform=='linux' or os.name=='posix':
                subprocess.call(['xdg-open','.'])
        else:
            return