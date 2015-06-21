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

#gmusicapi requires Python 2. Watch it start being compatible with 3 as soon as I finish.

#Tools: pyItunes and gmusicapi

import plistlib  # Later, I'll use pyItunes
import gmusicapi

# from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# import fuzzywuzzy # Fuzzy string matching!

#Broadly, Functions needed:
#Loading iTunes library
#Loading Google Play Music library
#Match iTunes songs to GPM songs
#Updating Play Counts

#More Specifically:


#Loading iTunes library
def load_itunes(libpath):
    """
    :rtype : list
    :param libpath: path to the XML copy of the iTunes Library
    :return: A list of song dicts
    Songs are considered anything that is "Music" (ie in the Music playlist)
    """
    #One day, I'll be able to use pyItunes for this.
    #That day is not today.
    ituneslib = plistlib.readPlist(libpath)

    music = (playlist for playlist in ituneslib['Playlists']
             if playlist["Name"] == "Music").next()  # StackOverflow #8653516
    assert music['Name'] == 'Music' and music['All Items']

    songids = []
    for element in music['Playlist Items']:
        songids.append(element['Track ID'])
    assert all(isinstance(trackid, int) for trackid in songids)

    songs = []
    for trackid in songids:
        songs.append(ituneslib['Tracks'][str(trackid)])
    assert all(isinstance(song, dict) for song in songs)

    #Later in life, I'll use pyItunes' data cleaning code.
    for song in songs:
        if 'Artist' not in song:
            song['Artist'] = ""
        if 'Name' not in song:
            song['Name'] = ""
    return songs


#Loading Google Play Music Library
def gmusic_login():
    """
    Interactive login for gmusicapi
    :return: Returns a Mobileclient session
    """
    #What do I need to load gmusic?
    username = raw_input("Google Username: ")
    password = raw_input("Password (or app-specific password): ")
    session = gmusicapi.Mobileclient()
    login_result = session.login(username, password)
    if login_result:
        return session
    else:
        raise LoginError


class LoginError(Exception):
    """
    Exception for a bad Google login
    """
    pass


def gmusic_getsongs(session):
    """
    :param session: expects a Mobileclient login session.
    :return: Returns a dict of songs formatted from
    """
    songs = session.get_all_songs()
    #Catch the NotLoggedIn exception
    #Check if I have to do any data cleaning
    #something I noticed, only songs that are from Google will have a trackType
    return songs


#match iTunes songs to GPM songs
def exact_match_songs(isonglist, gsonglist):
    """
    :param isonglist: A dict of songs in an iTunes library, from load_itunes()
    :param gsonglist: A dict of songs in a Google Music library, from gmusic_getsongs()
    :return: A dict of lists. 'match' returns a list of tuples,
    each tuple corresponding to an iTunes TrackID/ Google Music id match pair.
    'imismatch' has iTunes TrackIDs with no match, 'gmusic' has Google Music ids with no match.
    """
    result = {"match": [], "imismatch": [], "gmismatch": []}
    gmatches = []
    imatches = []

    for gsong in gsonglist:
        imatch = next((isong for isong in isonglist
                       if isong['Name'] == gsong['title'] and isong['Artist'] == gsong['artist']), None)
        if imatch:
            gmatches.append(gsong['id'])
            imatches.append(imatch['Track ID'])
            # print(isong['Track ID'])
            result['match'].append((imatch['Track ID'], gsong['id']))
        # else:
            # print("No match.")

    # print("gmatches: " + str(len(gmatches)))
    # print("gmatches: " + str(gmatches[0:4]))

    for gsong in gsonglist:
        if gsong['id'] not in gmatches:
            result['gmismatch'].append(gsong['id'])

    # print("imatches: " + str(len(imatches)))
    # print("imatches: " + str(imatches[0:4]))

    for isong in isonglist:
        if isong['Track ID'] not in imatches:
            result['imismatch'].append(isong['Track ID'])

    return result

def close_match_songs(isonglist, gsonglist, tolerance=80):
    """

    :param isonglist: A dict of songs in an iTunes library, from load_itunes()
    :param gsonglist: A dict of songs in a Google Music library, from gmusic_getsongs()
    :param tolerance: fuzzywuzzy ratio (0-100).
    :return: A dict of lists of tuples with keys match, closematch, imismatch, gmismatch.
    'match': exact match pairs in tuples, 'closematch': close match pairs in tuples,
    'imismatch': iTunes TrackIDs with no match, 'gmismatch' Google Music ids with no match.
    """
    #tuples match itunes trackIDs with gmusic ids

    #Lev D runtime is O(mn), should I worry about performance?
    #^  Note to self: Look up Levenshtein Automata later. O(n)

    exact_match_result = exact_match_songs(isonglist, gsonglist)
    result = {"match": exact_match_result['match'], "closematch": [], "imismatch": [], "gmismatch": []}

    #match gmusic uploaded tracks with itunes tracks
    gmismatches = []
    for trackid in exact_match_result['gmismatch']:
        gmismatches.append(next(song for song in gsonglist if song['id'] == trackid))

    imismatches = []
    for trackid in exact_match_result['imismatch']:
        imismatches.append(next(song for song in isonglist if song['Track ID'] == trackid))

    gmatches = []
    imatches = []

    for gsong in gmismatches:
        imatch = {}
        artistmatch = process.extractOne(gsong['artist'], [isong['Artist'] for isong in imismatches])
        if artistmatch[1] > tolerance:
            titlematch = process.extractOne(gsong['title'],
                                            [isong['Name'] for isong in imismatches
                                                if isong['Artist'] == artistmatch[0]])
            if titlematch[1] > tolerance:
                imatch = next(isong for isong in imismatches
                              if isong['Name'] == titlematch[0]
                              and isong['Artist'] == artistmatch[0])
                if imatch:
                    gmatches.append(gsong['id'])
                    imatches.append(imatch['Track ID'])
                    result['closematch'].append((imatch['Track ID'], gsong['id']))

    # print("gmatches: " + str(len(gmatches)))
    # print("gmatches: " + str(gmatches[0:4]))

    for gsong in gmismatches:
        if gsong['id'] not in gmatches:
            result['gmismatch'].append(gsong['id'])

    # print("imatches: " + str(len(imatches)))
    # print("imatches: " + str(imatches[0:4]))

    for isong in imismatches:
        if isong['Track ID'] not in imatches:
            result['imismatch'].append(isong['Track ID'])

    return result

#Updating Play Counts
#2 ways - Either Applescript (mac only!) or spitting out a new XML file.
def update_itunes_playcount():
    pass

if __name__ == "__main__":
    import sys
    import os.path

    args = sys.argv
    assert os.path.isfile(args[1])

    itunes_song_list = load_itunes(args[1])
    print("Loaded iTunes Library...")
    gsession = gmusic_login()
    print("Logged in to Google...")
    google_song_list = gmusic_getsongs(gsession)
    print("Google Songs Downloaded...")
    matches = exact_match_songs(itunes_song_list, google_song_list)
    print("Matches: " + str(len(matches['match'])) +
          ", iTunes Mismatches: " + str(len(matches['imismatch'])) +
          ", Google Mismatches: " + str(len(matches['gmismatch'])))