import logging
from PIL import Image

from config import (
    FONT_LG,
    FONT_MD,
    ICON_SIZE_SM,
    PADDING,
    PADDING_SM,
    weather,
)
from utils.util_dates import get_time_from_ms
from utils.util_fetch import fetch
from utils.util_formatting import get_small_icon
from utils.util_os import get_absolute_path, path_exists
from utils.weather_data import WeatherData


def get_weather_data():
    results = fetch_weather_data()
    if results is None:
        return None

    error_code = results.get("cod")
    if error_code != 200:
        logging.error(str(error_code) + " " + results.get("message"))
        return None
    else:
        weather = WeatherData()
        weather_id = results["weather"][0]["id"]

        weather.current_icon_id = str(weather_id)
        weather.current_icon = get_weather_icon(weather_id)  # Current weather icon
        # Current weather short description (ex. 'Clouds')
        weather.current_desc = results["weather"][0]["main"]
        weather.current_temp = str(round(results["main"]["temp"])) + "°"

        weather.sunrise = get_time_from_ms(
            results["sys"]["sunrise"] + results["timezone"]
        )
        weather.sunset = get_time_from_ms(
            results["sys"]["sunset"] + results["timezone"]
        )
        return weather


def fetch_weather_data():
    api_key = weather["api_key"]
    if api_key:
        return fetch(
            "https://api.openweathermap.org/data/2.5/weather?lat="
            + weather.get("lat")
            + "&lon="
            + weather.get("lon")
            + "&units=metric"
            + "&appid="
            + api_key
        )
    else:
        logging.error(
            "Open Weather Map API key ("
            + weather.get("env_var")
            + ") is not defined in environment variables."
        )
        return None


def get_weather_icon(weather_id):
    # ID definitions: https://openweathermap.org/weather-conditions
    if weather_id == 800:
        return "assets/icons/clear.png"
    elif weather_id >= 300 and weather_id < 400:
        return "assets/icons/drizzle.png"
    elif weather_id >= 500 and weather_id < 600:
        return "assets/icons/rain.png"
    elif weather_id == 801 or weather_id == 802:  # 11-50% clouds
        return "assets/icons/partly-cloudy.png"
    elif weather_id >= 800 and weather_id < 900:
        return "assets/icons/cloudy.png"  # 50%+ clouds
    elif weather_id >= 210 and weather_id <= 221:
        return "assets/icons/thunderstorm.png"
    elif weather_id >= 200 and weather_id < 300:
        return "assets/icons/rain-thunderstorm.png"
    elif weather_id == 600 or weather_id == 620:
        return "assets/icons/light-snow.png"
    elif (weather_id >= 611 and weather_id <= 613) or weather_id == 511:
        return "assets/icons/sleet.png"
    elif weather_id == 615 or weather_id == 616:
        return "assets/icons/rain-snow.png"
    elif weather_id == 602:
        return "assets/icons/heavy-snow.png"
    elif weather_id >= 600 and weather_id < 700:
        return "assets/icons/snow.png"
    elif weather_id == 781:
        return "assets/icons/tornado.png"
    elif weather_id >= 700 and weather_id < 800:
        return "assets/icons/atmosphere.png"
    else:
        return "assets/icons/unknown.png"
        # 701	Mist	mist	 50d
        # 711	Smoke	Smoke	 50d
        # 721	Haze	Haze	 50d
        # 731	Dust	sand/ dust whirls	 50d
        # 741	Fog	fog	 50d
        # 751	Sand	sand	 50d
        # 761	Dust	dust	 50d
        # 762	Ash	volcanic ash	 50d
        # 771	Squall	squalls	 50d


def draw_weather(Himage, draw):
    weather_data = get_weather_data()
    if weather_data is not None:
        x = 20
        y = 80
        weather_icon = get_absolute_path(weather_data.current_icon)
        if path_exists(weather_icon):
            # Current weather icon
            Himage.paste(Image.open(weather_icon), (x, y))
        else:
            logging.warning(
                "No icon for current weather: "
                + weather_data.current_icon_id
                + " "
                + weather_data.current_desc
            )
        logging.info("current temp: " + weather_data.current_temp)
        draw.text(
            (x + 60, y + 5), weather_data.current_temp, font=FONT_LG, fill=0
        )  # Current temperature

        x = 180
        y = 80
        Himage.paste(
            get_small_icon(get_absolute_path(weather_data.get_sunrise_icon())), (x, y)
        )  # Sunrise icon
        draw.text(
            (x + ICON_SIZE_SM + PADDING_SM, y + PADDING),
            weather_data.sunrise,
            font=FONT_MD,
            fill=0,
        )  # Sunrise time

        Himage.paste(
            get_small_icon(get_absolute_path(weather_data.get_sunset_icon())),
            (x, y + ICON_SIZE_SM),
        )  # Sunset icon
        draw.text(
            (x + ICON_SIZE_SM + PADDING_SM, y + ICON_SIZE_SM + PADDING),
            weather_data.sunset,
            font=FONT_MD,
            fill=0,
        )  # Sunset time
    else:
        logging.warn("Weather data was not retrieved.")
