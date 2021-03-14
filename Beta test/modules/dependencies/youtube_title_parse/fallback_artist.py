# -*- coding: utf-8 -*-
"""
Fallback to given artist name when no title/artist detected
"""


def fallback_artist(artist):
    """
    Fallback method
    """

    def fallback_a(title):
        return [artist, title]

    return fallback_a
