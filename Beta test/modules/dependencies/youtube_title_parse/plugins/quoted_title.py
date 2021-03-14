# -*- coding: utf-8 -*-
"""
Handle titles with quotes
"""
import re
from functools import reduce

QUOTES = ["“”", ("\x9c", "\xe2\x80\x9d"), '""', "''"]


def looseRegs(sset):
    open_set = sset[0]
    close_set = sset[1]
    return re.compile(open_set + r"(.*?)" + close_set)


def startRegs(sset):
    open_set = sset[0]
    close_set = sset[1]
    return re.compile(r"^" + open_set + r"(.*?)" + close_set + r"\s*")


def split_text(text):
    for loose_rex in map(looseRegs, QUOTES):
        text = re.sub(loose_rex, lambda re_match: r" %s " % re_match.group(), text, 1)
        match = re.search(loose_rex, text)
        if match:
            split = match.start()
            title = text[split:]
            artist = text[:split]
            return [artist, title]


def clean(artistOrTitle):
    return reduce(
        (lambda text, rx: re.sub(rx, r"\1 ", text)),
        map(startRegs, QUOTES),
        artistOrTitle,
    ).strip()
