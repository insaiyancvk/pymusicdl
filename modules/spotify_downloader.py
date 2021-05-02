import json, base64, os, requests, time, sys, subprocess
from rich.console import Console
try:
    import spotipy 
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    print("Install spotipy library using 'pip install spotipy'")

try:
    from common import common # type: ignore
except ImportError:
    from .common import common # type: ignore

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
                got_url = (key+"+"+tracks[key]).replace(' ','+')
                print(f"Fetching the details of {key} - {tracks[key]}")
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
        for i,j,k in zip(urls, alburl, sponame):
            print(c)
            self.ytd.download_song(i, j, k)
            c+=1

    def interface(self):      
        
        self.get_json()
        sponame = []
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
        print("\n\n")
        print("\t","="*100)
        Console().print(f"\n\n\t    Your playlist is downloaded in \"[bold]/musicDL downloads/Playlists/{plName}[/bold]\" folder on desktop\n\n")
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