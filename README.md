# Features
* Download single song
* Download Youtube Playlist
* Download Spotify playlist/album

# Setup

## Installation and usage:

### **Windows:**

* Run the following command in Command prompt

```
curl -o setup.bat https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pure-python/setup.bat && setup && del setup.bat
```

* Everytime you want to download music just type `musicdl` in cmd :)

**Note:**
* Make sure Python is added to your Path.
    * You can check it by typing `py --version` in cmd.
* Make sure PIP is added to your Path.
    * You can check it by typing `pip --version` or `py -m pip --version` in cmd.

### **Linux:**
```python
#!/usr/bin/python3
from pymusicdl.musicDL import main

main()
```
## Running the code:

* If you are on linux you can place that file in `~/.local/bin` and run `python3 musicdl.py` in terminal. You might find the following code helpful.
```
cat > musicdl.py
* paste the linux code *
* ctrl+c *
chmod +x musicdl.py
mv musicdl.py ~/.local/bin
musicdl.py
```

## Updating the package:
```
pip install pymusicdl -U
```

* or you can use `python3 -m pip install pymusicdl -U` if you are on linux

* and `py -m pip install pymusicdl -U` if you are on windows

## Planned features:
Will mark those if it's implemented.
- [x] Add flac support
    - [x] Implement for single downloads
    - [x] Implement for youtube playlist download
    - [x] Implement for spotify downloads
- [x] Update the list of downloaded songs while downloading
    - [x] Implement for youtube playlist download
    - [x] Implement for spotify downloads
- [x] Revamp the UI to make it interactive
    - [x] Replace menu driven inputs with tab selection system.