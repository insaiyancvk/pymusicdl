# -*- coding: utf-8 -*-
"""
Core parsing methods
"""
try:
    from youtube_title_parse.fallback_artist import fallback_artist
    from youtube_title_parse.fallback_title import fallback_title
except ImportError:
    from fallback_artist import fallback_artist
    from fallback_title import fallback_title


def flow(functions):
    if not functions:

        def failed(arg):
            return arg

        return failed

    def flow_func(arguments):
        result = functions[0](arguments)
        for function in functions[1:]:
            result = function(result)
        return result

    return flow_func


def combine_splitters(splitters):
    def combine_func(text):
        for splitter in splitters:
            result = splitter(text)
            if result:
                return result

    return combine_func


def reduce_plugins(plugins):
    return [
        flow(plugins["before"]),
        combine_splitters(plugins["split"]),
        flow(plugins["after"]),
    ]


def checkPlugin(plugin):
    if not plugin[1]:
        print("no title splitter was specified by any plugin")


def mapArtist(fn):
    def mapA(parts):
        return [fn(parts[0]), parts[1]]

    return mapA


def mapTitle(fn):
    def mapT(parts):
        return [parts[0], fn(parts[1])]

    return mapT


def mapArtistTitle(map_artist, map_title):
    def mapAT(parts):
        return [map_artist(parts[0]), map_title(parts[1])]

    return mapAT


def get_song_artist_title(text, options, plugins):
    if options:
        if "defaultArtist" in options:
            plugins["split"].append(fallback_artist(options["defaultArtist"]))
        if "defaultTitle" in options:
            plugins["split"].append(fallback_title(options["defaultTitle"]))
    plugin = reduce_plugins(plugins)
    checkPlugin(plugin)

    split = plugin[1](plugin[0](text))
    if not split:
        return
    return plugin[2](split)
