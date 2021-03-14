# -*- coding: utf-8 -*-
"""
Base method to parse title
"""
import re
from functools import reduce

SEPARATORS = [
    " -- ",
    "--",
    " - ",
    " – ",
    " — ",
    " _ ",
    "-",
    "–",
    "—",
    ":",
    "|",
    "///",
    " / ",
    "_",
    "/",
]


def clean_mvpv(text):
    """
    Remove various versions of "MV" and "PV" markers
    """
    text = re.sub(
        r"\s*\[\s*(?:off?icial\s+)?([PM]\/?V)\s*]", "", text, flags=re.IGNORECASE
    )  # [MV] or [M/V]
    text = re.sub(
        r"\s*\(\s*(?:off?icial\s+)?([PM]\/?V)\s*\)", "", text, flags=re.IGNORECASE
    )  # (MV) or (M/V)
    text = re.sub(
        r"\s*【\s*(?:off?icial\s+)?([PM]\/?V)\s*】", "", text, flags=re.IGNORECASE
    )  # 【MV】 or 【M/V】
    text = re.sub(
        r"[\s\-–_]+(?:off?icial\s+)?([PM]\/?V)\s*", "", text, flags=re.IGNORECASE
    )  # MV or M/V at the end
    text = re.sub(
        r"(?:off?icial\s+)?([PM]\/?V)[\s\-–_]+", "", text
    )  # MV or M/V at the start
    return text


def clean_fluff(text):
    """
    Remove fluff
    """
    text = clean_mvpv(text)
    text = re.sub(r"\s*\[[^\]]+]$", "", text)  # [whatever] at the end
    text = re.sub(r"^\s*\[[^\]]+]\s*", "", text)  # [whatever] at the start
    text = re.sub(
        r"\s*\([^)]*\bver(\.|sion)?\s*\)$", "", text, flags=re.IGNORECASE
    )  # (whatever version)
    text = re.sub(
        r"\s*[a-z]*\s*\bver(\.|sion)?$", "", text, flags=re.IGNORECASE
    )  # ver. & 1 word before (no parens)
    text = re.sub(
        r"\s*(of+icial\s*)?(music\s*)?video", "", text, flags=re.IGNORECASE
    )  # (official)? (music)? video
    text = re.sub(r"\s*(full\s*)?album", "", text, flags=re.IGNORECASE)  # (full)? album
    text = re.sub(
        r"\s*(ALBUM TRACK\s*)?(album track\s*)", "", text, flags=re.IGNORECASE
    )  # (ALBUM TRACK)
    text = re.sub(r"\s*\(\s*of+icial\s*\)", "", text, flags=re.IGNORECASE)  # (official)
    text = re.sub(r"\s*\(\s*lyric(s)?\s*\)", "", text, flags=re.IGNORECASE)  # (lyrics)
    text = re.sub(
        r"\s*\(\s*(of+icial)?\s*lyric(s)?\s*\)", "", text, flags=re.IGNORECASE
    )  # (official lyrics)
    text = re.sub(r"\s*\(\s*[0-9]{4}\s*\)", "", text, flags=re.IGNORECASE)  # (1999)
    text = re.sub(
        r"\s+\(\s*(HD|HQ|[0-9]{3,4}p|4K)\s*\)$", "", text
    )  # (HD) (HQ) (1080p) (4K)
    text = re.sub(
        r"[\s\-–_]+(HD|HQ|[0-9]{3,4}p|4K)\s*$", "", text
    )  # - HD - HQ - 720p - 4K
    return text


def clean_title(title):
    """
    Clean song title
    """
    title = title.strip(" ")
    title = clean_fluff(title)
    title = re.sub(r"\s*\*+\s?\S+\s?\*+$", "", title)  # **NEW**
    title = re.sub(r"\s*video\s*clip", "", title, flags=re.IGNORECASE)  # video clip
    title = re.sub(r"\s+\(?live\)?$", "", title, flags=re.IGNORECASE)  # live
    title = re.sub(r"\(\s*\)", "", title)  # Leftovers after e.g. (official video)
    title = re.sub(r"\[\s*]", "", title)  # Leftovers after e.g. [1080p]
    title = re.sub(r"【\s*】", "", title)  # Leftovers after e.g. 【MV】
    title = re.sub(
        r"^(|.*\s)\"(.*)\"(\s.*|)$", r"\2", title
    )  # Artist - The new "Track title" featuring someone
    title = re.sub(r"^(|.*\s)'(.*)'(\s.*|)$", r"\2", title)  # 'Track title'
    title = re.sub(
        r"^[/\s,:;~\-–_\s\"]+", "", title
    )  # trim starting white chars and dash
    title = re.sub(
        r"[/\s,:;~\-–_\s\"]+$", "", title
    )  # trim trailing white chars and dash
    return title


def clean_artist(artist):
    """
    Clean artist name
    """
    artist = artist.strip(" ")
    artist = clean_fluff(artist)
    artist = re.sub(
        r"\s*[0-1][0-9][0-1][0-9][0-3][0-9]\s*", "", artist
    )  # date formats ex. 130624
    artist = re.sub(
        r"^[/\s,:;~\-–_\s\"]+", "", artist
    )  # trim starting white chars and dash
    artist = re.sub(
        r"[/\s,:;~\-–_\s\"]+$", "", artist
    )  # trim trailing white chars and dash
    return artist


def in_quotes(text, idx):
    open_chars = "([{«"
    close_chars = ")]}»"
    toggle_chars = "\"'"
    open_pars = {")": 0, "]": 0, "}": 0, "»": 0, '"': 0, "'": 0}
    for character in text[:idx]:
        index = open_chars.find(character)
        if index != -1:
            open_pars[close_chars[index]] += 1
        elif close_chars.find(character) != -1 and open_pars[character] > 0:
            open_pars[character] -= 1
        if toggle_chars.find(character) != -1:
            open_pars[character] = 1 - open_pars[character]
    return reduce((lambda acc, value: acc + value), open_pars.values()) > 0


def split_artist_title(text):
    """
    Split text at separators
    """
    for separator in SEPARATORS:
        try:
            idx = text.index(separator)
        except ValueError:
            continue
        if idx > -1 and not in_quotes(text, idx):
            return [text[:idx], text[idx + len(separator) :]]
