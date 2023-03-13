import pylast
import config 
import argparse
import pandas as pd
import sys

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = config.api_key
API_SECRET = config.shared_secret


def track_and_timestamp(track):
    return f"{track.playback_date}",f"{track.track}"



def print_track(track):
    print(track_and_timestamp(track))


TRACK_SEPARATOR = " - "

def split_artist_track(artist_track):
    artist_track = artist_track.replace(" – ", " - ")
    artist_track = artist_track.replace("“", '"')
    artist_track = artist_track.replace("”", '"')
    try:
        artist, track = artist_track.split(TRACK_SEPARATOR)
    except:
        artist = 'Deu Ruim'
        track = artist_track
    artist = artist.strip()
    track = track.strip()
    print("Artist:\t\t'" + artist + "'")
    print("Track:\t\t'" + track + "'")

    # Validate
    if len(artist) == 0 and len(track) == 0:
        sys.exit("Error: Artist and track are blank")
    if len(artist) == 0:
        sys.exit("Error: Artist is blank")
    if len(track) == 0:
        sys.exit("Error: Track is blank")

    return (artist, track)

def get_recent_tracks(username, number):
    recent_tracks = network.get_user(username).get_recent_tracks(limit=number)
    list_music = []
    for i, track in enumerate(recent_tracks):
        time,track_name = track_and_timestamp(track)
        artist,track_name = split_artist_track(track_name)
        list_music.append([time,artist,track_name])
        
    list_music = pd.DataFrame(list_music)
    list_music.to_csv("recent_tracks.csv", index=False)
    
    return recent_tracks
    


if __name__ == "__main__":
    # In order to perform a write operation you need to authenticate yourself
    username = "jvtgj"
    password_hash = pylast.md5("^6R81&PLcsfG")

    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=username,
        password_hash=password_hash,
    )
    parser = argparse.ArgumentParser(
        description="Show 999 last played tracks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--username", help="Last.fm username")
    parser.add_argument(
        "-n",
        "--number",
        default=999,
        type=int,
        help="Number of tracks to show (when no artist given)",
    )
    args = parser.parse_args()

    if not args.username:
        args.username = username
    try:
        get_recent_tracks(args.username, args.number)
    except pylast.WSError as e:
        print("Error: " + str(e))