import logging
import random
from config import FONT_SM, last_fm
from util_formatting import get_xsmall_icon
from util_os import get_absolute_path
from util_formatting import trim_text

from util_fetch import fetch

LAST_FM_API_KEY = last_fm['api_key']
USERNAME = last_fm['user_name']

PERIODS = {"overall": "Top",
           "7day": "Top 7d",
           "1month": "Top 1m",
           "3month": "Top 3m",
           "6month": "Top 6m",
           "12month": "Top 1y"}


def fetch_top_tracks(period):
    return fetch('http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&api_key='+LAST_FM_API_KEY+'&user='+USERNAME+'&format=json&limit=1&period='+period)


def get_top_tracks():
    period = random.choice(list(PERIODS))
    results = fetch_top_tracks(period)

    if results is None:
        return None

    top_tracks = results['toptracks']
    track_name = top_tracks['track'][0]['name']
    track_artist = top_tracks['track'][0]['artist']['name']
    track_plays = top_tracks['track'][0]['playcount']
    return [period, track_name, track_artist, track_plays]


def print_top_tracks(Himage, draw):
    track_data = get_top_tracks()

    start_x = 1
    start_y = 260
    music_icon = 'python/assets/icons/music.png'

    if track_data is not None:
        period_name = PERIODS[track_data[0]]

        track_name = trim_text(track_data[1], 30)
        track_artist = trim_text(track_data[2], 15)
        track_plays = track_data[3]

        Himage.paste(get_xsmall_icon(
            get_absolute_path(music_icon)), (start_x, start_y))
        draw.text((start_x + 23, start_y),
                  period_name+': '+track_name+' - '+track_artist+' ('+track_plays+')', font=FONT_SM, fill=0)
    else:
        logging.warn('Last.fm data was not retrieved.')
