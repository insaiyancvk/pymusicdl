A simple music downloading app which doesn't require any API keys.

---
# Features
* Download single song
* Download Youtube Playlist
* Download Spotify playlist/album
---

# Setup

## Installation and usage:

### **Windows:**

* Run the following command in Command prompt

```
curl -o setup.bat https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pure-python/setup.bat && setup && del setup.bat
```

* Everytime you want to download music just type `musicdl` in cmd :)

#### **Note:**
* Make sure Python is added to your Path.
    * You can check it by typing `py --version` in cmd.
* Make sure PIP is added to your Path.
    * You can check it by typing `pip --version` or `py -m pip --version` in cmd.

---
### **Linux:**

* Install the pymusicdl.
```
pip install pymusicdl
```
* Install FFMPEG based on the distro.
    * Debian/Ubuntu - `sudo apt install ffmpeg`
    * Fedora/RHEL - `sudo dnf install ffmpeg`
    * Arch - `sudo pacman -S ffmpeg`

    Referred from [ubuntupit](https://www.ubuntupit.com/how-to-install-and-use-ffmpeg-on-linux-distros-beginners-guide/)
* Download "musicdl" to ~/.local/bin, make it executable.
```
curl -o ~/.local/bin/musicdl https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pure-python/musicdl && chmod +x ~/.local/bin/musicdl && clear && echo -e '\n\nType \033[1m\033[3mmusicdl\033[0m in your terminal to download music :)\n\n'
```

* Everytime you want to download music just type `musicdl` in terminal :)
---
## Updating the package:

```
pip install pymusicdl -U
```

* or you can use `python3 -m pip install pymusicdl -U` if you are on **linux**

* and `py -m pip install pymusicdl -U` if you are on **windows**