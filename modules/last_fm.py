import logging
import random
from config import DISPLAY_H, FONT_SM, last_fm
from utils.util_formatting import get_xsmall_icon
from utils.util_os import get_absolute_path
from utils.util_formatting import trim_text

from utils.util_fetch import fetch

LAST_FM_API_KEY = last_fm["api_key"]
USERNAME = last_fm["user_name"]

PERIODS = {
    "overall": "Top All Time",
    "7day": "Top 7 Days",
    "1month": "Top 1 Month",
    "3month": "Top 3 Months",
    "6month": "Top 6 Months",
    "12month": "Top 1 Year",
}

PERIOD = random.choice(list(PERIODS))


def fetch_lastfm_data(method, period):
    return fetch(
        "http://ws.audioscrobbler.com/2.0/?method="
        + method
        + "&api_key="
        + LAST_FM_API_KEY
        + "&user="
        + USERNAME
        + "&format=json&limit=1&period="
        + period
    )


def get_lastfm_data(data_type):
    if data_type == "track":
        results = fetch_lastfm_data("user.gettoptracks", PERIOD)
        if results is None:
            return None
        top_data = results["toptracks"]["track"][0]
        name = top_data["name"]
        artist = top_data["artist"]["name"]
        plays = top_data["playcount"]
        return {"name": name, "artist": artist, "plays": plays}
    elif data_type == "artist":
        results = fetch_lastfm_data("user.gettopartists", PERIOD)
        if results is None:
            return None
        top_data = results["topartists"]["artist"][0]
        name = top_data["name"]
        plays = top_data["playcount"]
        return {"name": name, "plays": plays}
    return None


def _draw_lastfm_item(Himage, draw, start_x, start_y, icon_path, data, is_track=False):
    if data is not None:
        name = trim_text(data["name"], 18)
        plays = data["plays"]
        text = f"{name} ({plays})"
        if is_track:
            artist = trim_text(data["artist"], 18)
            text = f"{name} - {artist} ({plays})"

        Himage.paste(
            get_xsmall_icon(get_absolute_path(icon_path)), (start_x, start_y)
        )
        draw.text(
            (start_x + 23, start_y - 3),
            text,
            font=FONT_SM,
            fill=0,
        )
    else:
        logging.warning("Last.fm data was not retrieved.")


def draw_artist_info(Himage, draw, start_x, start_y):
    artist_data = get_lastfm_data("artist")
    artist_icon = "assets/icons/person.png"
    _draw_lastfm_item(Himage, draw, start_x, start_y, artist_icon, artist_data)


def draw_lastfm_track_info(Himage, draw, start_x, start_y):
    track_data = get_lastfm_data("track")
    track_icon = "assets/icons/cd.png"
    _draw_lastfm_item(Himage, draw, start_x, start_y, track_icon, track_data, is_track=True)


def draw_lastfm_info(Himage, draw):

    start_x = 1
    start_y = DISPLAY_H - 74

    period_name = PERIODS[PERIOD]
    draw.text((start_x + 5, start_y), period_name + ":", font=FONT_SM, fill=0)
    draw_lastfm_track_info(Himage, draw, start_x, start_y + 21)
    draw_artist_info(Himage, draw, start_x, start_y + 39)
