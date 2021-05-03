@echo off & py -x "%~f0" %* & goto :eof

from pymusicdl.musicDL import main, check_ffmpeg

if check_ffmpeg():
    main()