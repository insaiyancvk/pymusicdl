# -*- coding: utf-8 -*-
"""
Remove file extensions from string
"""
import re

VIDEO_EXTENSIONS = [
    "3g2",
    "3gp",
    "aaf",
    "asf",
    "avchd",
    "avi",
    "drc",
    "flv",
    "m2v",
    "m4p",
    "m4v",
    "mkv",
    "mng",
    "mov",
    "mp2",
    "mp4",
    "mpe",
    "mpeg",
    "mpg",
    "mpv",
    "mxf",
    "nsv",
    "ogg",
    "ogv",
    "qt",
    "rm",
    "rmvb",
    "roq",
    "svi",
    "vob",
    "webm",
    "wmv",
    "yuv",
]

AUDIO_EXTENSIONS = [
    "wav",
    "bwf",
    "raw",
    "aiff",
    "flac",
    "m4a",
    "pac",
    "tta",
    "wv",
    "ast",
    "aac",
    "mp2",
    "mp3",
    "mp4",
    "amr",
    "s3m",
    "3gp",
    "act",
    "au",
    "dct",
    "dss",
    "gsm",
    "m4p",
    "mmf",
    "mpc",
    "ogg",
    "oga",
    "opus",
    "ra",
    "sln",
    "vox",
]

FILE_EXTENSIONS = VIDEO_EXTENSIONS + AUDIO_EXTENSIONS
FILE_EXTENSIONS_RX = re.compile(
    r"\.(" + "|".join(FILE_EXTENSIONS) + ")$", re.IGNORECASE
)


def remove_file_extensions(title):
    return FILE_EXTENSIONS_RX.sub("", title)
