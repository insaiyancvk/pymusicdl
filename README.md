Download youtube playlist, spotify playlist/album or a single song.

# Setup

## Installation:

```
pip install pymusicdl
```

## Usage:

**Linux:**
```python
#!/usr/bin/python3
from pymusicdl.musicDL import main

main()
```

**Windows:**
Run the following command in cmd
```
curl -o setup.bat https://raw.githubusercontent.com/insaiyancvk/pymusicdl/pure-python/setup.bat && setup && del setup.bat
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

* If you are on windows just type `musicdl` in cmd.

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