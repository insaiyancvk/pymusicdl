import json, base64, os, requests, time, sys, subprocess
from pytube import YouTube

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

def get_audio_size(video_url):
    
    try:
        # Create a YouTube object.
        yt = YouTube(video_url)

        # Get the best video stream (highest quality video stream).
        best_video_stream = yt.streams.get_highest_resolution()

        # Get the file size of the best video stream in bytes.
        video_size_bytes = best_video_stream.filesize

        # Convert to human-readable format (e.g., MB or GB).
        video_size_MB = video_size_bytes / (1024 * 1024)  # Convert bytes to megabytes

        return video_size_MB
    except Exception as e:
        return f"An error occurred: {str(e)}"

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
            if os.path.exists(plName):
                os.chdir(plName)

            else:
                os.mkdir(plName)
                os.chdir(plName)
        except:
            os.mkdir(plName)
            os.chdir(plName)
        
    
    def get_json(self):

        id = '15OzK7WMQI6mUO75P57VPMiEUZblYz9uy'
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
        count = 0
        for key in tracks.keys():
            try:
                got_url = (key+"+lyrics+"+tracks[key]).replace(' ','+')
                print(f"{count} Fetching youtube URL of {key} - {tracks[key]}")
                urls.append(self.ytd.get_url(got_url)[0])
            except Exception as e:
                print(f"\nCould not fetch the link for \"{key} {tracks[key]}\" because: {e}\nmaybe download it as a single")
            count += 1
        return urls

    def get_playlist_tracks(self, sp, plID):
        """ returns a dictionary of track name as key and artist name as value of a spotify playlist given the spotipy token credentials object and playlist id """

        alburl = []
        together = {}
        tracks = {}
        playlist = {}
        offset = 0
        total = sp.playlist_tracks(plID)['total']

        count = 1

        while total-offset>=0:
            
            playlist = sp.playlist_tracks(plID,offset=offset)

            for i in range(len(playlist['items'])):
                try:

                    if playlist['items'][i]['track']:

                        track_name = playlist['items'][i]['track']['name']
                        artist_name = playlist['items'][i]['track']['artists'][0]['name']

                        if len(playlist['items'][i]['track']['album']['images']) == 0:
                            
                            together[track_name] = [artist_name,'https://virginradio.co.uk/sites/virginradio.co.uk/files/song_cover/20160626/coverart_1.png']
                        
                        else:
                            together[track_name] = [artist_name,playlist['items'][i]['track']['album']['images'][1]['url']]
                        
                        print(f"{count} Fetched the data for {artist_name} - {track_name}")
                        count += 1
                except:
                    pass

            offset += 100

        for key in together.keys():
            tracks[key] = together[key][0]
            alburl.append(together[key][1])
            
        return tracks, alburl

    def get_album_tracks(self, sp, alID):
        """ returns a dictionary of track name as key and artist name as value of a spotify album given the spotipy token credentials object and album id """

        album = sp.album_tracks(alID)
        tracks = {}
        alburl = []
        count = 1

        for i in range(len(album['items'])):

            track_name = album['items'][i]['name']
            artist_name = album['items'][i]['artists'][0]['name']
            tracks[track_name] = artist_name

            print(f"{count} Fetched the data of {track_name} - {artist_name}")

            count += 1
            
            alburl.append(sp.track(album['items'][i]['id'])['album']['images'][1]['url'])

        return tracks, alburl

    def download_PL(self,plName, urls, alburl, sponame):
        """ downloads all the audio of URLs """

        self.create_PLdir(plName)
        c=1
        # data = 0.0
        # print("\nCalculating total download size...\n")

        # for i in urls:
        #     try:
        #         data += get_audio_size(i)

        #     except:
        #         # print(traceback.format_exc())
        #         # time.sleep(2)
        #         continue

        # data = int(data*100)/100
        
        # Console().print(Columns([Panel(f"\nDownload size: [green]{data} MB[/green]\n")]))
        # print()
        
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
        
        print("\n\tConnecting to spotify...\n")

        self.get_json()

        sponame = []
        sp = self.get_credentials()

        plLink = input("\nEnter the Spotify playlist/album URL: ")
        plName = input("\nGive a name to your playlist: ")

        if "playlist" in plLink:    
            plID = self.get_id(plLink)
            print("Fetching the Playlist tracks\nThis may take a while depending on the size of the playlist")
            tracks,alburls = self.get_playlist_tracks(sp, plID)
        elif "album" in plLink:
            alID = self.get_id(plLink)
            print("Fetching the Album tracks\nThis may take a while depending on the size of the playlist")
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
            elif os.name=='posix':
                if sys.platform=='linux':
                    subprocess.call(['xdg-open','.'])
                elif sys.platform == "darwin":
                    subprocess.call(['open','.'])

        else:
            return