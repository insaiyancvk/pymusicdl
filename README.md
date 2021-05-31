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
>Yet to be done

# Setup

## Installation and usage:

### **Termux:**

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

> Will make a shell script to install all the required stuff since it's tough to copy the commands and paste in a phone. So it'll be down to copying and pasting a single command

> curl -o setup.sh https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/setup.sh && ./setup.sh

* Everytime you want to download music just type `musicdl` in termux :)
---
## Updating the package:

```
pip install pymusicdl-termux -U
```

* or you can use `python3 -m pip install pymusicdl -U` in Termux
