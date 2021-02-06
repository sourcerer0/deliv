from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from delorean import Delorean

import pycountry
import pytz

class Location():
    def __init__(self, location="", **kwargs):
        self._geo_locator = Nominatim(user_agent="locator-sourcerer0")

        self.__time = Delorean()
        self.__timezone = "UTC"

        if location != "": self.location = (location)
        else: self.__location = None

    def up_time(self): print(self.__time.format_datetime())

    def set_timezone(self):
        print("Checking nearby timezones...")
        self.__timezone = Location.__search_timezone(self.__location)
        self.__time = self.__time.shift(self.__timezone)



    @property
    def time(self): return self.__time.now().shift(self.__timezone)

    @property
    def human_time(self): print(self.time.format_datetime())

    @property
    def location(self):
        try: print("Coordinates:".upper(), self.__location["lat"], self.__location["lon"])
        except KeyError: print("No coordinates founded")

        for key in self.__location["address"]: print("%s: %s" % (key.upper(), self.__location["address"][key]))

    @location.setter
    def location(self, place):
        if type(place) == type(()):
            self.__location = self._geo_locator.reverse(place, addressdetails=True, language="en").raw
        elif type(place) == type(""):
            self.__location = self._geo_locator.geocode(place, addressdetails=True, language="en").raw



    @staticmethod
    def __search_timezone(PLACE, max_dist=250):
        COUNTRY_ID = PLACE["address"]["country_code"]
        ERRORS, CHECKED = 0, 0

        TIMEZONE = ["", 1000]

        for zone in pytz.country_timezones[COUNTRY_ID]:
            CHECKED+=1
            try:
                tz_location_info = Nominatim(user_agent="search_timezone-deliv-sourcerer0").geocode(Location._edit_tz(zone), addressdetails=True, language="en")

                tz_location_info.point[0] = PLACE["lat"]
                distance = great_circle((PLACE["lat"], PLACE["lon"]), tz_location_info.point).km

                if distance < TIMEZONE[1]: TIMEZONE = [zone, distance]
                # print("%s %.2f " % (zone, distance))

                if distance < max_dist: break

            except: ERRORS+=1

        print("\nErrors: %d\nPlaces checked: %d"%(ERRORS, CHECKED))
        return TIMEZONE[0]

    @staticmethod
    def _edit_tz(word):
        word = list(word.split("/")[1])

        for pos, letter in enumerate(word):
            if letter == "_": word[pos] = " "

        return "".join(word)