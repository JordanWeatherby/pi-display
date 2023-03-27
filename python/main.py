import logging

from PIL import Image, ImageDraw

import epd4in2
from config import (DISPLAY_H, DISPLAY_W)
from last_fm import print_top_tracks
# from google_cal import print_gcal_event
# from news import print_news_data
from tube import print_tube_status
# from septa import print_septa_data
from util_dates import (get_current_date_time,
                        print_last_updated, print_todays_date, print_progress_bar)
from util_logging import set_logging_config
from util_server import is_display_busy, send_status
from weather import print_weather
# from word_of_the_day import print_word_of_the_day
from network import print_wifi_info

set_logging_config()

'''
from crypto import print_crypto_prices
from network import print_network_speed, print_network_name
'''

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

            send_status(False, True, "Getting wifi info...")
            # print_wifi_info(Himage, draw)

            print_todays_date(draw)

            print_tube_status(draw)

            print_top_tracks(Himage, draw)

            # if (weather['enabled']):
            send_status(False, True, "Fetching weather data...")
            print_weather(Himage, draw)

            # send_status(False, True, "Fetching Pi-Hole status...")
            # print_pihole_data(draw)

            print_progress_bar(draw)

            # if (septa['enabled']):
            #     send_status(False, True, "Fetching SEPTA bus data...")
            #     print_septa_data(Himage, draw)

            # if (word_of_the_day['enabled']):
            #     send_status(False, True, "Fetching word of the day...")
            #     print_word_of_the_day(draw)

            # if (news['enabled']):
            #     send_status(False, True, "Fetching news...")
            #     print_news_data(draw)

            # if (google_cal['enabled']):
            # send_status(False, True, "Fetching Google Calendar events...")
            # print_gcal_event(draw)

            last_updated = print_last_updated(draw, DISPLAY_W)
            logging.debug(last_updated)

            send_status(False, True, "Printing to display...")
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
