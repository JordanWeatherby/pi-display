import logging

from PIL import Image, ImageDraw

import epd4in2
from config import (DISPLAY_H, DISPLAY_W)
from co2 import draw_co2
from last_fm import draw_lastfm_info
from tube import draw_tube_status
from util_dates import (get_current_date_time,
                        draw_last_updated, draw_todays_date, draw_progress_bar)
from util_logging import set_logging_config
from util_server import is_display_busy, send_status
from weather import draw_weather

set_logging_config()

try:
    if (not is_display_busy()):
        send_status(False, True, "Starting display refresh...")
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
            send_status(False, True, "Fetching weather data...")
            draw_weather(Himage, draw)
            draw_co2(draw)

            draw_progress_bar(draw)

            last_updated = draw_last_updated(draw, DISPLAY_W)
            logging.debug(last_updated)

            send_status(False, True, "Printing to display...")
            Himage = Himage.rotate(180)
            epd.display(epd.getbuffer(Himage))

            logging.debug('Going to Sleep...')
            epd.sleep()

            logging.info('Completed refresh ' + get_current_date_time())

            send_status(False, False, "Display refresh complete.")

        except IOError as e:
            logging.exception('IOError')
            send_status(True, False, "IOError while refreshing display.")

        except KeyboardInterrupt:
            logging.warning('ctrl + c:')
            epd4in2.epdconfig.module_exit()
            send_status(
                True, False, "Keyboard interrupt while refreshing display.")
            exit()
    else:
        logging.info(
            'Server is processing or waiting. Can not refresh right now.')

except BaseException as e:
    logging.exception("Exception while running refresh script")
    send_status(True, False, str(e))

'''
if (network['enabled']):
    print_network_speed()

if (crypto['enabled']):
    print_crypto_prices()
'''
