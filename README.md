<div style="text-align:center"><img width="800" height="300" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/main/assets/banner.png" /></div>


A simple music downloading app which doesn't require any API keys.

---
# Features
* Download single song
* Download Youtube Playlist
* Download Spotify playlist/album
* Convert downloaded songs to mp3 or flac
---

# The final result

### Before the download starts:
<div>
   <img height="540" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/assets/sample1.jpeg" />
   <img height="540" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/assets/sample2.jpeg" />
</div>
<br>

### While It's downloading
<img height="540" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/assets/sample3.jpeg" />
<br>

### In the music player
<img height="540" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/assets/downloaded.jpeg" />
<br>

### And ofcourse the metadata :)
<img height="540" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/assets/metadata.jpeg" />

# Setup

## Installation and usage:

### **Termux:**

* Download Termux. 
   > **DO NOT DOWNLOAD IT FROM PLAYSTORE**, for more info check [this](https://www.xda-developers.com/termux-terminal-linux-google-play-updates-stopped/)
   - If you have Android version >=7, then [click here](https://f-droid.org/repo/com.termux_113.apk) to directly download termux apk
   - Otherwise, download [F-Droid apk](https://f-droid.org/F-Droid.apk) and install it. Then install Termux from it.

* Run the below command for installing everything automatically.
```
curl -sS -o setup.sh https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/setup.sh && chmod +x setup.sh && ./setup.sh
```
<details>
   <summary>Detailed installation</summary>
   
* Install the pymusicdl.
```
pip install pymusicdl-termux
```
* Install FFMPEG based on the distro.
```
apt install ffmpeg
```
* Download "musicdl" to ~/../usr/bin, make it executable.
```
curl -o  ~/../usr/bin/musicdl https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/musicdl && chmod +x  ~/../usr/bin/musicdl && clear && echo -e '\n\nType \033[1m\033[3mmusicdl\033[0m in your terminal to download music :)\n\n'
```
</details>

* Everytime you want to download music just type `musicdl` in termux :)
---
## Updating the package:

```
pip install pymusicdl_termux -U
```

* or you can use `python3 -m pip install pymusicdl -U` in Termux
