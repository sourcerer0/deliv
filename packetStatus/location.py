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

    def up_time(self): return self.__time

    def set_timezone(self):
        new_timezone = Location.search_timezone(self.__location)
        self.time.shift(new_timezone)



    @property
    def time(self): return self.__time.now()

    @property
    def location(self):
        try: print("Coordinates: %f, %f" % (self.__location["lat"], self.__location["lon"]))
        except: print("No coordinates founded")
        for key in self.__location["address"]: print(key.upper(), self.__location[key])

    @location.setter
    def location(self, place): self.__location = self.geo_locator.geocode(place, addressdetails=True, language="en").raw



    @staticmethod
    def search_timezone(PLACE, accpt_distance=250):
        COUNTRY_ID = pycountry.countries.get(official_name=PLACE["address"].get("country"))
        ERRORS, CHECKED = 0, 0

        TIMEZONE = ["", 1000]

        for zone in pytz.country_timezones[COUNTRY_ID.alpha_2]:
            CHECKED+=1
            try:
                tz_location_info = Location.geo_locator.geocode(Location.edit_tz(zone), addressdetails=True, language="en")
                tz_location_info.point[0] = PLACE["lat"]

                distance = great_circle((PLACE["lat"], PLACE["lon"]), tz_location_info.point).km
                if distance < TIMEZONE[1]: TIMEZONE = [zone, distance]
                if distance < accpt_distance: break

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
