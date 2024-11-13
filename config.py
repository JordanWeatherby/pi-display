from dotenv import load_dotenv
from PIL import ImageFont

from utils.epd4in2 import EPD_HEIGHT, EPD_WIDTH
from utils.util_os import get_absolute_path, get_env_var

load_dotenv()

WEATHER_ENV_VAR = "OWM_API_KEY"
GCAL_ENV_VAR = "GOOGLE_CALENDAR_ID"
LOCATION_LAT, LOCATION_LON = get_env_var("LOCATION_LAT_LON").split(",")

weather = {
    "enabled": True,
    "api_key": get_env_var(WEATHER_ENV_VAR),
    "env_var": WEATHER_ENV_VAR,
    "lon": LOCATION_LON,
    "lat": LOCATION_LAT,
    "units": "metric",  # 'standard', 'metric' or 'imperial'
}

last_fm = {
    "api_key": get_env_var("LAST_FM_API_KEY"),
    "user_name": get_env_var("LAST_FM_USERNAME"),
}

google_cal = {"enabled": False, "cal_id": get_env_var(GCAL_ENV_VAR)}
FONT_SM_SIZE = 15
FONT_MD_SIZE = 18
FONT_LG_SIZE = 30
FONT_ITALIC_SM = ImageFont.truetype(
    get_absolute_path("assets/fonts/Roboto-Italic.ttf"), FONT_SM_SIZE
)
FONT_ITALIC = ImageFont.truetype(
    get_absolute_path("assets/fonts/Roboto-Italic.ttf"), FONT_MD_SIZE
)
# FONT_SM = ImageFont.truetype(get_absolute_path(
#     'assets/fonts/Roboto-Regular.ttf'), FONT_SM_SIZE)
# FONT_MD = ImageFont.truetype(get_absolute_path('assets/fonts/Roboto-Regular.ttf'), FONT_MD_SIZE)
FONT_SM = ImageFont.truetype(
    get_absolute_path("assets/fonts/Alegreya-Regular.ttf"), FONT_SM_SIZE
)
FONT_MD = ImageFont.truetype(
    get_absolute_path("assets/fonts/Alegreya-Regular.ttf"), FONT_MD_SIZE
)
FONT_LG = ImageFont.truetype(
    get_absolute_path("assets/fonts/Roboto-Regular.ttf"), FONT_LG_SIZE
)

FONT_PIXEL = ImageFont.truetype(
    get_absolute_path("assets/fonts/SUBWT.ttf"), FONT_MD_SIZE
)
ICON_SIZE_SM = 40
ICON_SIZE_XS = 18
PADDING = 10
PADDING_SM = PADDING / 2
DISPLAY_W = EPD_HEIGHT  # Flipped because display is rotated
DISPLAY_H = EPD_WIDTH
