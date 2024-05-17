import logging
import random
from config import DISPLAY_H, FONT_SM, last_fm
from utils.util_formatting import get_xsmall_icon
from utils.util_os import get_absolute_path
from utils.util_formatting import trim_text

from utils.util_fetch import fetch

LAST_FM_API_KEY = last_fm['api_key']
USERNAME = last_fm['user_name']

PERIODS = {"overall": "Top All Time",
           "7day": "Top 7 Days",
           "1month": "Top 1 Month",
           "3month": "Top 3 Months",
           "6month": "Top 6 Months",
           "12month": "Top 1 Year"}

PERIOD = random.choice(list(PERIODS))


def fetch_top_tracks(period):
    return fetch('http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&api_key=' +
                 LAST_FM_API_KEY + '&user=' + USERNAME + '&format=json&limit=1&period=' + period)


def fetch_top_artists(period):
    return fetch('http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&api_key=' +
                 LAST_FM_API_KEY + '&user=' + USERNAME + '&format=json&limit=1&period=' + period)


def get_top_tracks():
    results = fetch_top_tracks(PERIOD)

    if results is None:
        return None

    top_tracks = results['toptracks']
    track_name = top_tracks['track'][0]['name']
    track_artist = top_tracks['track'][0]['artist']['name']
    track_plays = top_tracks['track'][0]['playcount']
    return [track_name, track_artist, track_plays]


def get_top_artists():
    results = fetch_top_artists(PERIOD)

    if results is None:
        return None

    top_artists = results['topartists']
    artist_name = top_artists['artist'][0]['name']
    artist_plays = top_artists['artist'][0]['playcount']
    return [artist_name, artist_plays]

def draw_artist_info(Himage, draw, start_x, start_y):
    artist_data = get_top_artists()
    artist_icon = '../assets/icons/person.png'
    if artist_data is not None:
        artist_name = trim_text(artist_data[0], 18)
        artist_plays = artist_data[1]

        Himage.paste(get_xsmall_icon(
            get_absolute_path(artist_icon)), (start_x, start_y + 39))

        draw.text((start_x + 23, start_y + 37),
                  artist_name + ' (' + artist_plays + ')', font=FONT_SM, fill=0)
    else:
        logging.warn('Last.fm artist data was not retrieved.')

def draw_lastfm_track_info(Himage, draw, start_x, start_y):
    track_data = get_top_tracks()
    track_icon = '../assets/icons/cd.png'

    if track_data is not None:

        track_artist = trim_text(track_data[1], 18)
        track_plays = track_data[2]

        track_name = trim_text(track_data[0], 18)

        Himage.paste(get_xsmall_icon(
            get_absolute_path(track_icon)), (start_x, start_y + 21))
        draw.text((start_x + 23, start_y + 18), track_name + ' - ' +
                  track_artist + ' (' + track_plays + ')', font=FONT_SM, fill=0)
    else:
        logging.warn('Last.fm track data was not retrieved.')

def draw_lastfm_info(Himage, draw):

    start_x = 1
    start_y = DISPLAY_H - 74

    period_name = PERIODS[PERIOD]
    draw.text((start_x + 5, start_y),
              period_name + ':', font=FONT_SM, fill=0)
    draw_lastfm_track_info(Himage, draw, start_x, start_y)
    draw_artist_info(Himage, draw, start_x, start_y)
