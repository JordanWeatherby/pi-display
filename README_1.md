# Pi Display - Back End

Displays data on a Waveshare 5.83in e-ink display powered by a Raspberry Pi.

## Prerequisites

1. [Python 3.7+](https://www.python.org/downloads/)
1. Create API keys for all the data modules listed below that you want to utilize.
    * Weather: [OpenWeatherMap API](https://openweathermap.org/api/one-call-api)
    * Crypto prices: [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/)
    * News: [New York Times API](https://developer.nytimes.com/) and/or [Newsapi.org](https://newsapi.org/)
    * Word of the day: [Wordnik API](https://developer.wordnik.com/)
1. Get the Google Calendar id for the calendar that contains events you want to display. To find your calendar id:
    1. Go to your [Google Calendar settings](https://calendar.google.com/calendar/u/0/r/settings).
    1. Click your desired calendar on the left sidebar under "Settings for my calendars".
    1. Scroll down to the "Integrate calendar" section and copy the `Calendar ID`.
1. Set your environment variables in a `.env` file in the root `/pi-display` directory (note that the IP address for your Pi-Hole also needs to be stored):
    ```
    OWM_API_KEY=[open_weather_map_key]
    CMC_API_KEY=[coinmarketcap_key]
    NYTIMES_API_KEY=[nytimes_api_key]
    NEWSAPI_API_KEY=[newsapi_api_key]
    WORDNIK_API_KEY=[wordnik_api_key]
    PIHOLE_ADDRESS=[ip_address_for_your_pihole]
    GOOGLE_CALENDAR_ID=[google_calendar_id]
    ```
1. Install the python-dotenv python dependency: `pip install python-dotenv`
1. Install the Pillow python dependency: `pip install Pillow`

## Configuration

Some module settings can be set in the `src/config.py` file. Use this file to enable/disable various data modules and adjust their settings. Default is all enabled.

## Run

To run the python program to retrieve and print the display data, run the command `python main.py` from the root folder.

![Photo of the Pi display displaying all data](assets/pi-display.jpg)

## Data Modules

The information displayed is optained from the folowing sources.

### OpenWeatherMap

Weather data is retrieved from the [OpenWeatherMap one call API](https://openweathermap.org/api/one-call-api). It includes current temperature, 3-day forecast, sunrise/sunset, and weather description (used to generate weather icon). Your OpenWeatherMap API key needs to be set in the OWM_API_KEY environment variable in order for this functionality to work. Default location is Philadelphia, PA.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display the weather information
* `lat`: Latitude for the weather location
* `lon`: Longitude for the weather location

### Pi-Hole

The Pi-Hole status information is retrieved from the local [Pi-Hole API](https://discourse.pi-hole.net/t/pi-hole-api/1863). It includes current status (enabled/disabled), number of queries blocked, and percentage of queries blocked. Your Pi-Hole's IP address needs to be set in the PIHOLE_ADDRESS environment variable in order for this functionality to work.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display the Pi-Hole information

### Wordnik

[Wordnik](https://developer.wordnik.com/) is used to get the word of the day definition. Your Wordnik API key needs to be set in the WORDNIK_API_KEY environment variable in order for this functionality to work.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display the word of the day

### News

The source for news headlines is set in the `config.py`. News can either be fetched from the New York Times API or News API. Set the `source` to `'nytimes'` to use the NY Times API or any [source ID from News API](https://newsapi.org/docs/endpoints/sources) to use the News API (ex. `'the-washington-post'`). 

#### New York Times API

News headlines can be retrieved from the [New York Times API](https://developer.nytimes.com/). Your NYTimes API key needs to be set in the NYTIMES_API_KEY environment variable in order for this functionality to work and the configuration's `source` needs to be set to `nytimes`.

#### News API

News headlines can also be retrieved from the [News API](https://newsapi.org/). Your News API key needs to be set in the NEWSAPI_API_KEY environment variable in order for this functionality to work and the configuration's `source` needs to be set to a [valid Newsapi source ID](https://newsapi.org/docs/endpoints/sources). Note: Articles are delayed a hour if you are using the free version.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display news headlines
* `source`: Source for the articles. Can be 'nytimes' or any [source ID from News API](https://newsapi.org/docs/endpoints/sources)
* `num`: Number of headlines to display

### Google Calendar

The [Google Calendar API](https://developer.wordnik.com/) is used to display the next calendar event. Your Google Calendar ID needs to be set in the GOOGLE_CALENDAR_ID environment variable in order for this functionality to work.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display Google Calendar data

## In Progress...

The following integrations are in the codebase but have not been implemented to print on the display.

### Fast CLI

Network speed information is run in local speed tests via the Fast CLI. This data is pretty slow to collect and the results don't seem very precise. 

#### Configuration Options

* `enabled`: Boolean to declare whether to calculate and display the network speed

### CoinMarketCap

Cypto prices are retrieved from the [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/). Your CoinMarketCap API key needs to be set in the CMC_API_KEY environment variable in order for this functionality to work.

#### Configuration Options

* `enabled`: Boolean to declare whether to get and display cryptocurrency prices
* `tokens`: Array of coins/tokens to retrieve values for
* `currency`: Currency to display prices in (ex. USD, GBP, etc.)

## Icons

Icons are from [Icons8](https://icons8.com).

## Linting

[autopep8](https://pypi.org/project/autopep8/) is used for Python linting.

```
autopep8 --in-place --aggressive --aggressive --max-line-length 100 --in-place --ignore E302 -v --recursive .
```
