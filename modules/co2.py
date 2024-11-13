from config import DISPLAY_H, FONT_SM
import logging
import math
import os


def read_file():
    # about 200 minutes of data per graph
    num_lines = 1200

    try:
        with os.popen(f"tail -n {num_lines} ../co2.log") as file:
            lines = file.read().strip()

        if not lines:
            return None

        # More efficient list comprehension with direct splitting
        return [int(line.split()[1]) for line in lines.splitlines()]
    except (IndexError, ValueError, OSError):
        return None


def get_points(values, max_value, height, start_x, start_y):
    # logging roughly every 10 seconds so this should turn about a minute into one pixel
    points_to_average_over = 6

    drawpoints = []
    for i in range(0, len(values), points_to_average_over):
        # average out the 6 values
        block = values[i : i + points_to_average_over]
        average = math.floor(sum(block) / len(block))

        # scale to screen pixel values
        scaled_value = round((average / max_value) * height)
        drawpoints.append(
            (start_x + i / points_to_average_over, height + start_y - scaled_value)
        )

    return drawpoints


def draw_graph(values, draw):
    max_value = 5000
    height = 80
    start_x = 30
    start_y = DISPLAY_H - 170

    drawpoints = get_points(values, max_value, height, start_x, start_y)

    # draw lines for axes
    draw.line([(start_x, start_y), (start_x, height + start_y)], fill=0)
    draw.line([(start_x, height + start_y), (start_x + 200, height + start_y)], fill=0)

    draw.text((3, start_y), "CO₂", font=FONT_SM, fill=0)
    draw.point(drawpoints, fill=0)


def draw_co2(draw):
    co2_data = read_file()
    start_x = 1
    start_y = DISPLAY_H - 120

    if co2_data is not None:
        draw_graph(co2_data, draw)
    else:
        logging.warn("CO2 data was not retrieved.")


# if __name__ == '__main__':
#     # print(read_file())
#     draw_graph(read_file())
