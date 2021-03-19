try:
    import pafy
except:
    print("install 'pafy' library with 'pip install pafy'")

import os, urllib.request, re
from subprocess import Popen, PIPE
try:
    from youtube_title_parse import get_artist_title 
except:
    print("install 'youtube_title_parse' using 'pip install youtube_title_parse'")

from urllib.parse import quote

class common():
    
    def __init__(self, ffmpeg, spo=False):
        self.ffmpeg = ffmpeg
        self.spo = spo

    def get_url(self,s):
        """
        Give a video ID as an argument to this function. It returns top n (7 by default) video URLs.
        """

        query = "https://www.youtube.com/results?search_query="+quote(s)
        baseurl = "https://www.youtube.com/watch?v="
        response = urllib.request.urlopen(query)
        html = response.read()
        video_ids = re.findall(r"watch\?v=(\S{11})", html.decode())
        urls = []
        if self.spo:
            for i in video_ids:
                try:
                    pafy.new(baseurl+i)
                    urls.append(baseurl+i)
                    return urls
                except:
                    continue
        else:
            j = 0
            for i in video_ids:
                try:
                    pafy.new(baseurl+i)
                    urls.append(baseurl+i)
                    j+=1
                    if j==7:
                        break
                except:
                    continue
            return urls

    def convert(self, old, new, alburl):
        """ converts any file format to .mp3 with the help of ffmpeg """
        
        if self.spo:
            os.system(self.ffmpeg+' -hide_banner -loglevel quiet -i \"'+old+'\" -b:a 320k \"w'+new+"\"")
            os.remove(old)
            urllib.request.urlretrieve(alburl, "thumb.png")
            os.system(self.ffmpeg+' -hide_banner -loglevel quiet -i "w'+new+'" -i thumb.png -map 0:0 -map 1:0 -codec copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" "'+new+'"')
            os.remove("w"+new)
            os.remove("thumb.png")
        else:
            os.system(self.ffmpeg+' -hide_banner -loglevel quiet -i \"'+old+'\" -b:a 320k \"'+new+"\"")
            os.remove(old)

    # Download the song
    def download_song(self,url, albart): 
        """
        Download the song by passing the video URL as a parameter
        """

        try:
            v = pafy.new(url)
        except Exception as e:
            print(f"\nSome error occurred while fetching the details of the song : {e}\n")
            return
        name = v.title
        audio = v.getbestaudio()
        print(f"\n\033[96mdownloading {name} as an audio file\033[97m")
        audio.download()
        dirs = os.listdir()
        try:
            artist, title = get_artist_title(name)
            for i in dirs:
                if name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_") in i:
                    track_name = title+" - "+artist+".mp3"
                    track_name = track_name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_")
                    print(f"\033[92m Converting \"{i}\" to \"{track_name}\" \033[97m")
                    self.convert(i, track_name, albart)
            for i in os.listdir():
                if "_" in i:
                    os.rename(i,i.replace("_"," "))
        except TypeError:
            for i in dirs:
                if name in i:
                    ind1 = len(i) - 1 - i[::-1].index('.')
                    ext = i[ind1:]
                    if ext in i:
                        track_name = name[:ind1]+".mp3"
                        print(f"\033[92m Converting \"{i}\" to \"{track_name}\" \033[97m")
                        self.convert(i, track_name, albart)
                        print("\033[92m Successfully Converted \033[97m")
            for i in os.listdir():
                if "_" in i:
                    os.rename(i,i.replace("_"," "))