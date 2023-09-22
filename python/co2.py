from config import DISPLAY_H, FONT_SM
import logging
import math

from util_os import get_absolute_path
import os

def get_co2():
    return [1234, 1235]

def read_file():
    graph_width = 1000

    lines = os.popen('tail -n {} ../../co2.log'.format(graph_width)).read()
    # If the list is empty, return None
    if not lines:
        return None

    values = [int(line.split(' ')[1]) for line in lines[:-1].split('\n')]
    
    return values

def draw_graph(values, draw):
    max_value = 5000
    height = 80
    start_x = 30
    start_y = DISPLAY_H - 170

    drawpoints = []
    for i in range(0,len(values), 5):
        scaled_value = round((values[i] / max_value ) * height)
        drawpoints.append((start_x+i/5, height+start_y-scaled_value))
    draw.line([(start_x, start_y), (start_x, height+start_y)], fill=0)
    draw.line([(start_x, height+start_y), (start_x+200, height+start_y)], fill=0)
    draw.text((3, start_y), 'CO₂', font=FONT_SM, fill=0)
    draw.point(drawpoints, fill=0)



def print_co2_1(draw):
    co2_data = get_co2()
    start_x = 1
    start_y = DISPLAY_H - 120

    if co2_data is not None:
        draw.text((start_x, start_y), 'CO: ' +
                  str(co2_data[0]) + ' ppm', font=FONT_SM, fill=0)
    else:
        logging.warn('CO2 data was not retrieved.')

def draw_co2(draw):
    co2_data = read_file()
    start_x = 1
    start_y = DISPLAY_H - 120

    if co2_data is not None:
        draw_graph(co2_data, draw)
    else:
        logging.warn('CO2 data was not retrieved.')

# if __name__ == '__main__':
#     # print(read_file())
#     draw_graph(read_file())