import logging

from PIL import Image, ImageDraw

import utils.epd4in2 as epd4in2
from config import (DISPLAY_H, DISPLAY_W)
from modules.co2 import draw_co2
from modules.last_fm import draw_lastfm_info
from modules.tube import draw_tube_status
from utils.util_dates import (get_current_date_time,
                              draw_last_updated, draw_todays_date, draw_progress_bar)
from utils.util_logging import set_logging_config
from modules.weather import draw_weather

set_logging_config()

try:
    logging.info('********* Initializing display refresh *********')

    # Init display
    epd = epd4in2.EPD()
    epd.init()

    # Init new image to draw
    Himage = Image.new('1', (DISPLAY_W, DISPLAY_H), 255)
    draw = ImageDraw.Draw(Himage)

    draw_todays_date(draw)

    draw_tube_status(draw)

    draw_lastfm_info(Himage, draw)

    # if (weather['enabled']):
    draw_weather(Himage, draw)
    draw_co2(draw)

    draw_progress_bar(draw)

    last_updated = draw_last_updated(draw, DISPLAY_W)
    logging.debug(last_updated)

    Himage = Himage.rotate(180)
    epd.display(epd.getbuffer(Himage))

    logging.debug('Going to Sleep...')
    epd.sleep()

    logging.info('Completed refresh ' + get_current_date_time())


except IOError as e:
    logging.exception('IOError')

except KeyboardInterrupt:
    logging.warning('ctrl + c:')
    epd4in2.epdconfig.module_exit()
    exit()
