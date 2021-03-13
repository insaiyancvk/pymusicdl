import json, base64, time, os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_downloader import yt_downloader # type: ignore

with open('musicdl/modules/sec.json') as f:
  data = json.load(f)

for key in data.keys():
    data[key] = base64.b64decode(data[key]).decode('utf8')

client_id = data['id']
client_secret = data['secret']

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def create_dir():
    """
    Creates "musicDL downloads" directory on desktop when called. Takes no parameters.
    """

    os.chdir(os.path.expanduser("~/Desktop"))
    try:
        os.chdir("musicDL downloads")
    except:
        os.mkdir("musicDL downloads")
        os.chdir("musicDL downloads")

create_dir()

plLink = input("Enter the Spotify playlist URL: ")
plName = input("Give a name to your playlist: ")

def get_playlist_id(url):
    if "playlist/" in url:
        ind = url.index("playlist/")
        return url[ind+9:ind+31]
plID = get_playlist_id(plLink)

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

trackIDs = getTrackIDs('',plID)

def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  name = meta['name']
  artist = meta['album']['artists'][0]['name']

  track = [name, artist]
  return track

tracks = {}
print("\nFetching the details all tracks (name, artist)")
for i in trackIDs:
    time.sleep(.5)
    temp = getTrackFeatures(i)
    tracks[temp[0]] = temp[1]
print("Successfully fetched all the track details")
ytd = yt_downloader()
urls = []
# print("\nFetching a download link to each track")
# print(tracks)
not_fetched = {}
for key in tracks.keys():
    try:
        if u"\u2018" or u"\u2019" in key+"+"+tracks[key]:
            got_url = (key+"+"+tracks[key]).replace(' ','+').replace(u"\u2018", "'").replace(u"\u2019", "'")
            urls.append(ytd.get_url(got_url)[0])
        else:
            got_url = (key+"+"+tracks[key]).replace(' ','+')
            # got_url - urllib.parse.urlsplit(got_url)
            # got_url = list(got_url)
            urls.append(ytd.get_url(got_url)[0])
    except Exception as e:
        # print(got_url)
        print(f"\nCould not fetch the link for \"{key} {tracks[key]}\" because: {e}\nmaybe download it as a single")
        not_fetched[key] = tracks[key]

if len(tracks)-len(urls)>0:
    print(f"\n{len(tracks)-len(urls)}/{len(tracks)} were not fetched")
    print("\nHere is the list: ")
    for oh in not_fetched.keys():
        print(f"{oh} - {not_fetched[oh]}")
print("\nDownloading the songs\n")
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

for i in urls:
    ytd.download_song(i)

total_songs = len(urls)
downloaded_songs = len(os.listdir())
if total_songs-downloaded_songs!=0:
    print(f"\n{total_songs-downloaded_songs}/{total_songs} songs were not downloaded due to some error")
print(f"\nYour playlist is downloaded in \"/musicDL downloads/Playlists/{plName}\" folder on desktop\n")