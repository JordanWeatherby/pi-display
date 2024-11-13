from datetime import datetime
import calendar
import logging

from config import (
    FONT_SM_SIZE,
    FONT_LG,
    FONT_MD,
    FONT_MD_SIZE,
    FONT_SM,
    DISPLAY_W,
    DISPLAY_H,
)

day_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_day_of_week_from_ms(ms):
    date = get_date_from_ms(ms)
    return get_day_of_week(date)


def get_time_from_ms(ms):
    date = get_date_from_ms(ms)
    return date.strftime("%H:%M")


def get_date_from_ms(ms):
    return datetime.utcfromtimestamp(ms)


def get_day_of_week(date):
    return day_of_week[date.weekday()]


def suffix(d):
    return {1: "st", 2: "nd", 3: "rd"}.get(d % 20, "th")


def custom_strftime(format, t):
    return t.strftime(format).replace("{S}", str(t.day) + suffix(t.day))


def get_current_date():
    date = datetime.today()
    return get_day_of_week(date) + ", \n" + custom_strftime("{S} %B", date)


def get_current_date_time():
    date = datetime.now()
    return date.strftime("%b %-d, %-I:%M:%S %p")


def get_current_time():
    date = datetime.now()
    return date.strftime("%H:%M")


def get_current_short_date_time():
    date = datetime.now()
    return date.strftime("%Y%m%d")  # yyyymmdd


def print_current_date():
    logging.info(get_current_date())


def days_in_year():
    return 365 + calendar.isleap(datetime.today().year)


def get_year_percentage():
    return datetime.today().timetuple().tm_yday / days_in_year()


# Print last updated date + time in bottom right of screen


def draw_last_updated(draw, DISPLAY_W):
    last_updated = get_current_time()
    width = FONT_SM.getsize(last_updated)[0]
    draw.text(
        (DISPLAY_W - FONT_SM.getsize("updated")[0], 0), "updated", font=FONT_SM, fill=0
    )
    draw.text((DISPLAY_W - width - 5, FONT_SM_SIZE), last_updated, font=FONT_SM, fill=0)
    return last_updated


# Print day of the week and date in designated space


def draw_todays_date(draw):
    day_and_date = get_current_date().split("\n")
    draw.text((5, 0), day_and_date[0], font=FONT_MD, fill=0)
    draw.text((5, 0 + FONT_MD_SIZE), day_and_date[1], font=FONT_LG, fill=0)


def draw_progress_bar(draw):
    percentage = get_year_percentage()
    percentage_text = str(int(percentage * 100)) + "%"
    text_width, text_height = FONT_SM.getsize(percentage_text)
    text_pad = 10

    height = 10
    start_x = 5
    start_y = DISPLAY_H - height - 1
    width = DISPLAY_W - start_x - text_pad - text_width

    draw.rectangle(
        (start_x, start_y, start_x + width, start_y + height),
        fill=None,
        outline=0,
        width=1,
    )
    draw.rectangle(
        (start_x, start_y, start_x + (width * percentage), start_y + height),
        fill=0,
        outline=0,
        width=1,
    )
    draw.text(
        (start_x + width + (text_pad / 2), start_y),
        percentage_text,
        font=FONT_SM,
        anchor="lt",
        fill=0,
    )
