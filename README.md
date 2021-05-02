Download youtube playlist, spotify playlist/album or a single song.

# Setup

## Installation:

```
pip install pymusicdl
```

## Usage:
On Linux:

```python
#!/usr/bin/python3
from pymusicdl.musicDL import main

main()
```
On Windows:
```python

from pymusicdl.musicDL import main

main()
```

## Running the code:

* Make a `musicdl.py` file and add the above code.

* For **Linux** run the following commands:
```    
    mv musicdl.py ~/.local/bin
    chmod +x musicdl.py
    musicdl.py
```
* For **Windows** you can place the file in `C:/Program Files/Python3.x/Scripts` and run `py musicdl.py` in command prompt

## Updating the package:
```
pip install pymusicdl -U
```

* or you can use `python3 -m pip install pymusicdl -U` if you are on linux

* and `py -m pip install pymusicdl -U` if you are on windows