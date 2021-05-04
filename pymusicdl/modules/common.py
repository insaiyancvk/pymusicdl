try:
    import pafy
except:
    print("install 'pafy' library with 'pip install pafy'")

import os, urllib.request, re, subprocess, sys
from rich.console import Console
from rich.table import Table
try:
    from youtube_title_parse import get_artist_title 
except:
    print("install 'youtube_title_parse' using 'pip install youtube_title_parse'")

from urllib.parse import quote

class common():
    
    def __init__(self, spo=False):
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

    def convert(self, old, new, alburl, flac=False):
        """ converts any file format to .mp3 or flac with the help of ffmpeg """
        
        if self.spo:
            if not flac:
                subprocess.call(['ffmpeg','-hide_banner','-loglevel', 'quiet','-i',old,'-b:a', '320k','w'+new])
            elif flac:
                subprocess.call(['ffmpeg','-hide_banner','-loglevel', 'quiet','-i',old,'-c:a', 'flac','w'+new])
            os.remove(old)
            urllib.request.urlretrieve(alburl, "thumb.png")
            subprocess.call(['ffmpeg','-hide_banner','-loglevel','quiet','-i','w'+new,'-i','thumb.png','-map','0:0','-map','1:0','-codec','copy','-id3v2_version','3','-metadata:s:v','title="Album cover"','-metadata:s:v','comment="Cover (front)"',new])
            os.remove("w"+new)
            os.remove("thumb.png")
        else:
            if not flac:
                subprocess.call(["ffmpeg",'-hide_banner','-loglevel','quiet','-i',old,'-b:a', '320k',new])
            elif flac:
                subprocess.call(["ffmpeg",'-hide_banner','-loglevel','quiet','-i',old,'-c:a', 'flac',new])
            os.remove(old)

    # Download the song
    def download_song(self,url, albart, sponame): 
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
        Console().print(f"\n[bold green]Downloading {name}[/bold green]")
        audio.download()

        dirs = os.listdir()

        print("Would you like an mp3 or flac conversion?")
        print("\t\t **** Here's a quick comparison on both codec ****")
        print("\n\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Avaliable Codec")
        table.add_column("Bit-rate")
        table.add_column("File Size")
        table.add_column("Opinion")
        table.add_row(
            "mp3", "320kbps (fixed)","~7.3MB for 3min song","Standard codec with normal experience"
        )
        table.add_row()
        table.add_row(
            "flac", "usually >800kbps (1713kbps while testing, 5x of mp3)","~39MB for 3min song","Takes fair amount of disk space but gives amazing experience"
        )
        Console().print(table)

        print('\nIf you are confused on what to select, select mp3 (which is default)')
        z = input("\tEnter\n\t1 - mp3\n\t2 - flac : ")

        try:

            if self.spo:
                artist, title = get_artist_title(sponame)   
            else:
                artist, title = get_artist_title(name)

            for i in dirs:
                if sys.platform=='win32' or os.name=='nt':
                    if name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_") in i:                    

                        if z == "1" or z == "mp3" or z == "mp" or z == "m":
                            track_name = title+" - "+artist+".mp3"
                            track_name = track_name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_")
                            print(f" Converting the audio format to mp3")
                            self.convert(i, track_name, albart)

                        elif z == "2" or z == "flac" or z == "f":
                            track_name = title+" - "+artist+".flac"
                            track_name = track_name.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("\"","_").replace("<","_").replace(">","_").replace("|","_")
                            print(f" Converting the audio format to flac")
                            self.convert(i, track_name, albart, flac=True)

                elif sys.platform=='linux' or os.name=='posix':
                    if name in i:

                        if z == "1" or z == "mp3" or z == "mp" or z == "m":
                            track_name = title+" - "+artist+".mp3"
                            track_name = track_name.replace("\\"," ").replace("/"," ").replace(":"," ").replace("*"," ").replace("?"," ").replace("\""," ").replace("<"," ").replace(">"," ").replace("|"," ")
                            print(f" Converting the audio format to mp3")
                            self.convert(i, track_name, albart)

                        elif z == "2" or z == "flac" or z == "f":
                            track_name = title+" - "+artist+".flac"
                            track_name = track_name.replace("\\"," ").replace("/"," ").replace(":"," ").replace("*"," ").replace("?"," ").replace("\""," ").replace("<"," ").replace(">"," ").replace("|"," ")
                            print(f" Converting the audio format to flac")
                            self.convert(i, track_name, albart, flac=True)

            for i in os.listdir():
                if "_" in i:
                    try:
                        os.rename(i,i.replace("_"," "))
                    except FileExistsError:
                        try:
                            os.rename(i,i.replace("_","  "))
                        except FileExistsError:
                            pass
        except TypeError:
            for i in dirs:
                if name in i:
                    ind1 = len(i) - 1 - i[::-1].index('.')
                    ext = i[ind1:]
                    if ext in i:

                        if z == "1" or z == "mp3" or z == "mp" or z == "m":
                            track_name = name[:ind1]+".mp3"
                            print(f" Converting the audio format to mp3")
                            self.convert(i, track_name, albart)

                        elif z == "2" or z == "flac" or z == "f":
                            track_name = name[:ind1]+".flac"
                            print(f" Converting the audio format to flac")
                            self.convert(i, track_name, albart, flac=True)

            for i in os.listdir():
                if "_" in i:
                    os.rename(i,i.replace("_"," "))