import json, base64, os, requests, time, sys, subprocess, spotipy, pafy
from spotipy.oauth2 import SpotifyClientCredentials
try:
    from .common import common
except:
    from common import common

class Downloader:
    def __init__(self, link:str, plname:str):
        self.link = link
        self.plname = plname
        self.destination = "/"
        self.ytd = common(spo=True)

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
        with open(self.destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def get_credentials(self):
        """ returns a token object after authentication. """

        empty = {}
        with open(self.destination, 'r') as f:
            data = json.load(f)
        with open(self.destination,'w') as f:
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

    def download_PL(self,plName, urls, alburl, sponame):
        """ downloads all the audio of URLs """

        os.mkdir(plName)
        os.chdir(plName)

        c=1
        
        # print('\nIf you are confused on what to select, select mp3 (default)')
        # z = input("\tEnter\n\t1/flac/f - flac\n\tany key - mp3 : ")

        for i,j,k in zip(urls, alburl, sponame):
            self.ytd.download_song(i, j, k, '')
            c+=1
    
    def spodl(self):
        self.get_json()
        sponame = []
        sp = self.get_credentials()
        if "playlist" in self.link:    
            plID = self.get_id(self.link)
            tracks,alburls = self.get_playlist_tracks(sp, plID)
        elif "album" in self.link:
            alID = self.get_id(self.link)
            tracks, alburls = self.get_album_tracks(sp,alID)
        else: 
            print("Invalid link, exiting")
            return
        start_time = time.time()
        print("\nFetching all the relevant URLs\n")
        urls = self.get_yt_urls(tracks)
        end_time = time.time()
        print(f"Time taken to fetch the URLs from Youtube: %.2f secs\n"%(end_time-start_time))
        print("\nDownloading the songs\n")
        for i in tracks.keys():
            sponame.append(tracks[i]+" - "+i)
        self.download_PL(self.plName, urls, alburls, sponame)
        os.chdir('..')
         #TODO: zip all mp3 converted songs
    
    def ytdl(self):
        pass
    
    def download(self):
        if 'spotify' in self.link:
            self.spodl()
        elif 'youtube' in self.link:
            self.ytdl()
        else:
            print("Invalid URL")
            return