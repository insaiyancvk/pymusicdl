<div style="text-align:center"><img width="800" height="300" src="https://raw.githubusercontent.com/insaiyancvk/pymusicdl/main/assets/banner.png" /></div>


A simple music downloading app which doesn't require any API keys.

Check [pymusicdl-termux](https://github.com/insaiyancvk/pymusicdl-termux) for android setup.

---
# Features
* Download single song
* Download Youtube Playlist
* Download Spotify playlist/album (searches on youtube and downloads the top result)
* Convert downloaded songs to mp3 or flac
---

# The final result
![https://open.spotify.com/playlist/4WtqLI6gaRFaWB4g6mDnAX](https://github.com/insaiyancvk/pymusicdl/raw/main/assets/downloads.jfif)

# Setup

Check it out on YouTube!

<a href="https://www.youtube.com/watch?v=1_BmOtZoo1o"><img width="400" src="https://img.youtube.com/vi/1_BmOtZoo1o/maxresdefault.jpg"></a>

## Installation and usage:

<br>
<details>
   <summary><b>Windows</b></summary>

<details>
   <summary><b>Note</b></summary>

**Read the instructions carefully**
* Make sure Python is added to your Path.
    * You can check it by typing `py --version` in cmd.
      * Consider running this piece of code (in cmd) for installing python (if you don't have python installed): 
      ```
      curl -o python.exe https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe && python.exe
      ```
      **make sure to check "add to PATH"**
* Make sure PIP is added to your Path.
    * You can check it by typing `pip --version` or `py -m pip --version` in cmd.
      * Consider running this piece of code (in cmd) for installing pip (if you don't have PIP installed): 
      ```
      curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py && py get-pip.py
      ```
</details>

* Run the following command in Command prompt

```
curl -o setup.bat https://raw.githubusercontent.com/insaiyancvk/pymusicdl/main/setup.bat && setup && del setup.bat
```

* Everytime you want to download music just type `musicdl` in cmd :)
</details>
<br>

<details>
   <summary><b>Linux</b></summary>

* Install the pymusicdl.
```
pip install pymusicdl
pip install https://github.com/mps-youtube/pafy/archive/refs/heads/develop.zip
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
</details>
<br>

<details>
   <summary><b>Android</b></summary>
<br>

[Check pymusicdl-termux for sample images](https://github.com/insaiyancvk/pymusicdl-termux)

* Download Termux. 
   > **DO NOT DOWNLOAD IT FROM PLAYSTORE**, for more info check [here](https://www.xda-developers.com/termux-terminal-linux-google-play-updates-stopped/)
   - If you have Android version >=7, then [click here](https://f-droid.org/repo/com.termux_113.apk) to directly download termux apk
   - Otherwise, download [F-Droid apk](https://f-droid.org/F-Droid.apk) and install it. Then install Termux from it.

* Run the below command for installing everything automatically.
```
curl -sS -o setup.sh https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pymusicdl-termux/setup.sh && chmod +x setup.sh && ./setup.sh
```

* Everytime you want to download music just type `musicdl` in termux :)
---
## Updating the package:

```
pip install pymusicdl_termux -U
```

* or you can use `python3 -m pip install pymusicdl -U` in Termux
</details>

<br>

## To fix the 'dislike_count' error:
- Uninstall pafy and install from github repository.

   (run the following command in command prompt)
   
   ``` pip uninstall pafy && pip install git+https://github.com/mps-youtube/pafy.git#egg=pafy ```

---

## Updating the package:

```
pip install pymusicdl -U
```

* or you can use `python3 -m pip install pymusicdl -U` if you are on **linux**

* and `py -m pip install pymusicdl -U` if you are on **windows**

### Fun fact: I did this project when I got covid :)
