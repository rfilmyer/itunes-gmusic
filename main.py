#itunes-gmusic
#By Roger Filmyer, 2015

#Sketching out what I intend to do:
#Provide an interface between iTunes and Google Play Music
#  * Scratching an itch - comparing my 2 decently-large libraries with a 
#    lot of history
#  * When syncing, play counts update *once*: iTunes -> Google Play Music
#First thing I want to do: be able to pull play counts from GPM and
#    update to iTunes.
#Also: Evaluate what songs differ between my iTunes and my GPM library
#Finally: Compare "thumbs upped" songs to star ratings.

#Political Decisions: Python 3 (It's 2015, kids.)

#Tools: pyItunes and gmusicapi

import pyItunes
import gmusicapi

#Broadly, Functions needed:
#Loading iTunes library
#Loading Google Play Music library
#Match iTunes songs to GPM songs
#Updating Play Counts

#More Specifically:

#Loading iTunes library
def load_itunes(library):
    #Should I ask for a file or a path?
    pass

#Loading Google Play Music Library
def load_gmusic():
    #What do I need to load gmusic?
    pass

#match iTunes songs to GPM songs
def match_songs(ituneslib,gmusiclib,exactmatch = True, tolerance = 2):
    #tolerance is the Levenshtein distance between 2 possible track names
    #runtime is O(mn), should I worry about performance? We'll see later!
    #^  Note to self: Look up Levenshtein Automata later. O(n)
    #PS: don't expect these defaults to last until I say it's okay.
    pass

#Updating Play Counts
#2 ways - Either Applescript (mac only!) or spitting out a new XML file.
def update_itunes_playcount():
    pass
