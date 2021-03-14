import pafy, time, os, urllib.request, re
from youtube_title_parse import get_artist_title
from urllib.parse import quote

class common():
    def get_url(self,s,n=7):
        """
        Give a video ID as an argument to this function. It returns top n (7 by default) video URLs.
        """

        query = "https://www.youtube.com/results?search_query="+quote(s)
        baseurl = "https://www.youtube.com/watch?v="
        response = urllib.request.urlopen(query)
        html = response.read()
        video_ids = re.findall(r"watch\?v=(\S{11})", html.decode())
        urls = []
        for i in video_ids[:n]:
            urls.append(baseurl+i)
        return urls

    # Download the song
    def download_song(self,url): 
        """
        Download the song by passing the video URL as a parameter
        """

        try:
            v = pafy.new(url)
        except Exception as e:
            print(f"\nSome error occurred while downloading the song : {e}\n")
            return
        name = v.title
        audio = v.getbestaudio(preftype="m4a")
        print(f"\ndownloading {name} as an audio file")
        audio.download()
        time.sleep(1)
        try:
            artist, title = get_artist_title(name)
            dirs = os.listdir()
            for i in dirs:
                if name in i:
                    ind1 = len(i) - 1 - i[::-1].index('.')
                    ext = i[ind1:]
                    os.rename(i,title+" - "+artist+ext)
        except:
            pass