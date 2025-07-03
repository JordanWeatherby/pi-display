import logging
from config import FONT_SM, TUBE_LINES

from utils.util_fetch import fetch


def fetch_tube_status():
    formattedLines = ",".join(TUBE_LINES)
    return fetch("https://api.tfl.gov.uk/Line/" + formattedLines + "/Status")


def get_tube_status():
    results = fetch_tube_status()
    if results is None:
        logging.warning("Tube data was not retrieved.")
        return None

    data = []
    for line in results:
        if "lineStatuses" in line and len(line["lineStatuses"]) > 0:
            data.append(
                [line["name"], line["lineStatuses"][0]["statusSeverityDescription"]]
            )
        else:
            logging.warning(f"No status found for line: {line.get('name', 'Unknown')}")

    return data


def draw_tube_status(draw):
    tube_data = get_tube_status()

    start_x = 5
    start_y = 180
    line_height = 17
    if tube_data is not None:
        for idx, line in enumerate(tube_data):
            draw.text(
                (start_x, start_y + (idx * line_height)), line[0], font=FONT_SM, fill=0
            )
            draw.text(
                (start_x + 70, start_y + (idx * line_height)),
                line[1],
                font=FONT_SM,
                fill=0,
            )
    else:
        logging.warning("Tube data was not retrieved.")
