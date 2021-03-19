import json, base64, os, requests, time

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

    def __init__(self, ffmpeg):
        self.ffmpeg = ffmpeg
        self.ytd =  common(ffmpeg, spo=True)
    
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
                print(f"\033[96Fetching the details of {key} - {tracks[key]}\033[97m")
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

    def download_PL(self,plName, urls, alburl):
        """ downloads all the audio of URLs """

        self.create_PLdir(plName)
        for i,j in zip(urls, alburl):
            self.ytd.download_song(i,j)

    def interface(self):      
        
        self.get_json()
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
            exit()
        start_time = time.time()
        print(f"\nFetching all the relevant URLs")
        urls = self.get_yt_urls(tracks)
        end_time = time.time()
        print(f"Time taken to fetch the URLs from Youtube: %.2f secs\n"%(end_time-start_time))
        print("\nDownloading the songs\n")

        # download the tracks
        self.download_PL(plName, urls, alburls)

        # check if all the songs are downloaded
        total_songs = len(urls)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        print(f"\nYour playlist is downloaded in \"/musicDL downloads/Playlists/{plName}\" folder on desktop\n")