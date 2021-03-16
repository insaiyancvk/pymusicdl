import json, base64, time, os, requests

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
    
    ytd = common()
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

    def get_playlist_id(self,url):
        """ returns the playlist ID given the playlist URI """

        if "playlist" in url:
            ind = url.index("playlist")
            return url[ind+9:ind+31]
        elif "playlist/" not in url:
            print("Invalid URL. Make sure that it's a playlist URL. Exiting")
            quit()

    def getTrackIDs(self,sp, user, playlist_id):
        """ returns IDs of tracks in the playlist as a list given Playlist ID"""

        ids = []
        playlist = sp.user_playlist(user, playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
        return ids

    def getTrackFeatures(self,sp,id):
        """ returns track name and artist name as a list"""

        meta = sp.track(id)
        name = meta['name']
        artist = meta['album']['artists'][0]['name']
        track = [name, artist]
        return track

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

    def get_yt_urls(self,tracks):
        """ returns a list of urls that are fetched successfully and dictionary of urls that were failed to be fetched. """

        not_fetched = {}
        urls = []
        for key in tracks.keys():
            try:
                got_url = (key+"+"+tracks[key]).replace(' ','+')
                urls.append(self.ytd.get_url(got_url)[0])
            except Exception as e:
                print(f"\nCould not fetch the link for \"{key} {tracks[key]}\" because: {e}\nmaybe download it as a single")
                not_fetched[key] = tracks[key]
        return urls, not_fetched

    def get_track_details(self,sp,trackIDs):
        """ returns a dictionary of track name as key and artist name as value given the track ID """

        tracks = {}
        for i in trackIDs:
            time.sleep(.5)
            temp = self.getTrackFeatures(sp,i)
            tracks[temp[0]] = temp[1]
        return tracks

    def download_PL(self,plName, urls):
        """ downloads all the audio of URLs """

        self.create_PLdir(plName)
        for i in urls:
            self.ytd.download_song(i)

    def interface(self):      

        self.get_json()
        sp = self.get_credentials()
        plLink = input("Enter the Spotify playlist URL: ")
        plName = input("Give a name to your playlist: ")        
        plID = self.get_playlist_id(plLink)
        trackIDs = self.getTrackIDs(sp,'',plID)
        print("\nFetching the details all tracks (name, artist)")
        tracks = self.get_track_details(sp,trackIDs)
        print("Successfully fetched all the track details")
        urls, not_fetched = self.get_yt_urls(tracks)
        #check for track URLs that were failed to be fetched
        if len(tracks)-len(urls)>0:
            print(f"\n{len(tracks)-len(urls)}/{len(tracks)} were not fetched")
            print("\nHere is the list: ")
            for oh in not_fetched.keys():
                print(f"{oh} - {not_fetched[oh]}")
        print("\nDownloading the songs\n")

        # download the tracks
        self.download_PL(plName, urls)

        # check if all the songs are downloaded
        total_songs = len(urls)
        downloaded_songs = len(os.listdir())
        if total_songs-downloaded_songs!=0:
            print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
        print(f"\nYour playlist is downloaded in \"/musicDL downloads/Playlists/{plName}\" folder on desktop\n")