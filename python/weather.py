import logging
from PIL import Image

from config import (COL_1_W, FONT_LG, FONT_MD, FONT_SM,
                    ICON_SIZE_SM, PADDING, PADDING_SM, weather)
from config import weather
from util_dates import get_day_of_week_from_ms, get_time_from_ms
from util_fetch import fetch
from util_formatting import get_small_icon
from util_os import get_absolute_path, path_exists
from weather_data import WeatherData, WeatherDay


def get_weather_data():
    results = fetch_weather_data()
    if results is None:
        return None

    error_code = results.get('cod')
    if (error_code != 200):
        logging.error(str(error_code) + ' ' + results.get('message'))
        return None
    else:
        weather = WeatherData()
        weather_id = results['weather'][0]['id']

        weather.current_icon_id = str(weather_id)
        weather.current_icon = get_weather_icon(
            weather_id)  # Current weather icon
        # Current weather short description (ex. 'Clouds')
        weather.current_desc = results['weather'][0]['main']
        weather.current_temp = str(round(results['main']['temp'])) + '°C'

        weather.sunrise = get_time_from_ms(
            results['sys']['sunrise'] + results['timezone'])
        weather.sunset = get_time_from_ms(
            results['sys']['sunset'] + results['timezone'])
        return weather


def fetch_weather_data():
    api_key = weather['api_key']
    if (api_key):
        return fetch(
            'https://api.openweathermap.org/data/2.5/weather?lat=' +
            weather.get('lat') +
            '&lon=' +
            weather.get('lon') +
            '&units=metric' +
            '&appid=' +
            api_key)
    else:
        logging.error(
            'Open Weather Map API key (' +
            weather.get('env_var') +
            ') is not defined in environment variables.')
        return None


def get_weather_icon(weather_id):
    # ID definitions: https://openweathermap.org/weather-conditions
    if (weather_id == 800):
        return 'python/assets/icons/clear.png'
    elif (weather_id >= 300 and weather_id < 400):
        return 'python/assets/icons/drizzle.png'
    elif (weather_id >= 500 and weather_id < 600):
        return 'python/assets/icons/rain.png'
    elif (weather_id == 801 or weather_id == 802):  # 11-50% clouds
        return 'python/assets/icons/partly-cloudy.png'
    elif (weather_id >= 800 and weather_id < 900):
        return 'python/assets/icons/cloudy.png'   # 50%+ clouds
    elif (weather_id >= 210 and weather_id <= 221):
        return 'python/assets/icons/thunderstorm.png'
    elif (weather_id >= 200 and weather_id < 300):
        return 'python/assets/icons/rain-thunderstorm.png'
    elif (weather_id == 600 or weather_id == 620):
        return 'python/assets/icons/light-snow.png'
    elif ((weather_id >= 611 and weather_id <= 613) or weather_id == 511):
        return 'python/assets/icons/sleet.png'
    elif (weather_id == 615 or weather_id == 616):
        return 'python/assets/icons/rain-snow.png'
    elif (weather_id == 602):
        return 'python/assets/icons/heavy-snow.png'
    elif (weather_id >= 600 and weather_id < 700):
        return 'python/assets/icons/snow.png'
    elif (weather_id == 781):
        return 'python/assets/icons/tornado.png'
    elif (weather_id >= 700 and weather_id < 800):
        return 'python/assets/icons/atmosphere.png'
    else:
        return 'python/assets/icons/unknown.png'
        # 701	Mist	mist	 50d
        # 711	Smoke	Smoke	 50d
        # 721	Haze	Haze	 50d
        # 731	Dust	sand/ dust whirls	 50d
        # 741	Fog	fog	 50d
        # 751	Sand	sand	 50d
        # 761	Dust	dust	 50d
        # 762	Ash	volcanic ash	 50d
        # 771	Squall	squalls	 50d


def print_weather(Himage, draw):
    weather_data = get_weather_data()
    if weather_data is not None:
        x = 20
        y = 95
        weather_icon = get_absolute_path(weather_data.current_icon)
        if path_exists(weather_icon):
            # Current weather icon
            Himage.paste(Image.open(weather_icon), (x, y))
        else:
            logging.warning(
                'No icon for current weather: ' +
                weather_data.current_icon_id +
                ' ' +
                weather_data.current_desc)
        logging.info('current temp: ' + weather_data.current_temp)
        draw.text((x + 60, y), weather_data.current_temp,
                  font=FONT_LG, fill=0)   # Current temperature

        x = 180
        y = 95
        Himage.paste(
            get_small_icon(
                get_absolute_path(
                    weather_data.get_sunrise_icon())),
            (x,
             y))   # Sunrise icon
        draw.text((x + ICON_SIZE_SM + PADDING_SM, y + PADDING),
                  weather_data.sunrise, font=FONT_MD, fill=0)   # Sunrise time

        Himage.paste(get_small_icon(get_absolute_path(weather_data.get_sunset_icon())),
                     (x, y + ICON_SIZE_SM))   # Sunset icon
        draw.text((x + ICON_SIZE_SM + PADDING_SM, y + ICON_SIZE_SM + PADDING),
                  weather_data.sunset, font=FONT_MD, fill=0)   # Sunset time
    else:
        logging.warn('Weather data was not retrieved.')
