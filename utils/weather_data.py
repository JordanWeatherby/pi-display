class WeatherData:
    sunrise_icon = "assets/icons/sunrise.png"
    sunset_icon = "assets/icons/sunset.png"

    def __init__(self):
        self.current = ""
        self.current_temp = ""
        self.current_humidity = ""
        self.current_icon = ""
        self.current_icon_id = ""
        self.current_desc = ""
        self.sunrise = ""
        self.sunset = ""

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, a):
        self._current = a

    @property
    def current_temp(self):
        return self._current_temp

    @current_temp.setter
    def current_temp(self, a):
        self._current_temp = a

    @property
    def current_humidity(self):
        return self._current_humidity

    @current_humidity.setter
    def current_humidity(self, a):
        self._current_humidity = a

    @property
    def current_icon(self):
        return self._current_icon

    @current_icon.setter
    def current_icon(self, a):
        self._current_icon = a

    @property
    def current_icon_id(self):
        return self._current_icon_id

    @current_icon_id.setter
    def current_icon_id(self, a):
        self._current_icon_id = a

    @property
    def current_desc(self):
        return self._current_desc

    @current_desc.setter
    def current_desc(self, a):
        self._current_desc = a

    @property
    def sunrise(self):
        return self._sunrise

    @sunrise.setter
    def sunrise(self, a):
        self._sunrise = a

    @property
    def sunset(self):
        return self._sunset

    @sunset.setter
    def sunset(self, a):
        self._sunset = a

    def get_sunrise_icon(self):
        return self.sunrise_icon

    def get_sunset_icon(self):
        return self.sunset_icon
