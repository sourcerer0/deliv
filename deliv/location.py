from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from delorean import Delorean

import pycountry
import pytz

class Location():
    def __init__(self, **kwargs):
        self.geo_locator = Nominatim(user_agent="locator-sourcerer0")
        self.__time = Delorean()
        self.__location = None

        try: self.location = (kwargs["location"])
        except KeyError: pass

    def up_time(self): return self.__time.format_datetime()

    def set_timezone(self):
        new_timezone = Location.search_timezone(self.__location)
        self.__time.shift(new_timezone)



    @property
    def time(self): return self.__time.now().format_datetime()

    @property
    def location(self):
        try: print("Coordinates:".upper(), self.__location["lat"], self.__location["lon"])
        except KeyError: print("No coordinates founded")

        for key in self.__location["address"]: print("%s: %s" % (key.upper(), self.__location["address"][key]))

    @location.setter
    def location(self, place):
        if type(place) == type(()):
            self.__location = self.geo_locator.reverse(place, addressdetails=True, language="en").raw
        elif type(place) == type(""):
            self.__location = self.geo_locator.geocode(place, addressdetails=True, language="en").raw



    @staticmethod
    def search_timezone(PLACE, distance=250):
        COUNTRY_ID = PLACE["address"]["country_code"]
        ERRORS, CHECKED = 0, 0

        TIMEZONE = ["", 1000]

        for zone in pytz.country_timezones[COUNTRY_ID]:
            CHECKED+=1
            try:
                tz_location_info = Location.geo_locator.geocode(Location.edit_tz(zone), addressdetails=True, language="en")
                tz_location_info.point[0] = PLACE["lat"]

                distance = great_circle((PLACE["lat"], PLACE["lon"]), tz_location_info.point).km
                if distance < TIMEZONE[1]: TIMEZONE = [zone, distance]
                if distance < distance: break

                if CHECKED % 3: key = ""
                else: key = "\n"
                print("CHECK %d: %s %.2f " % (CHECKED,TIMEZONE,distance))

            except: ERRORS+=1

        print("\nErrors: %d\nPlaces checked: %d"%(ERRORS, CHECKED))
        return TIMEZONE

    @staticmethod
    def edit_tz(word):
        word = list(word.split("/")[1])

        for pos, letter in enumerate(word):
            if letter == "_": word[pos] = " "

        return "".join(word)
