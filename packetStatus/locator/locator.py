from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle
from delorean import Delorean

import pycountry
import pytz

class Locator():
    def __init__(self):
        super().__init__()
        self.__geolocator = Nominatim(user_agent="locator-sourcerer0")
        self.__listRegion = None

        self.__location = None
        self.__time = Delorean()
        print(self.time.now().format_datetime())

    @property
    def time(self): return self.__time

    @property
    def location(self): return self.__location

    def locate(self, place):
        self.set_location(self.__geolocator.geocode(place, addressdetails=True, language="en"))
        self.__listRegion = self.location.raw["address"]
        location_info(self.__listRegion, self.location)

    def set_timezone(self):
        results = search_country_tz(self.time, self.location, self.__listRegion)
        print("Errors: %d\nPlaces checked: %d"%(results[3], results[2]))
        print("Operation Time: ", results[1])
        self.time.shift(results[0])
        print("Presenting timezone(s) for: ", self.time.timezone, "\n", self.time.format_datetime())

    @staticmethod
    def distance(current, last,  *coordinates):
        distance_dic = {}
        distance_dic["euclid_distance"] = geodesic(coordinates[0], coordinates[1]).km
        distance_dic["geod_distance"] = great_circle(coordinates[0], coordinates[1]).km
        return distance_dic

    @staticmethod
    def location_info(raw_address, location):
        print("INFO")
        try: print("Coordinates: ", location.point)
        except:
            print("No coordinates founded")
        for key in raw_address:
            print(key, raw_address[key])

    @staticmethod
    def search_country_tz(TIME, PLACE, listRegion, accpt_distance=250):
        measured_distances = []
        distances_dic = {}
        print("Calculating a probable time zone...")
        COUNTRY_ID = pycountry.countries.get(name=listRegion.get("country"))
        if COUNTRY_ID == None: COUNTRY_ID = pycountry.countries.get(official_name=listRegion.get("country"))

        ERRORS = 0
        CHECKED = 0
        for ver in pytz.country_timezones[COUNTRY_ID.alpha_2]:
            CHECKED+=1
            try:
                timezone = edit_tz(ver)
                tz_location_info = Nominatim(user_agent="timezone").geocode(timezone, addressdetails=True, language="en")
                tz_location_info.point[0] = PLACE.point[0]

                distance = great_circle(PLACE.point, tz_location_info.point).km
                measured_distances.append(distance)
                distances_dic[distance] = ver
                if distance < accpt_distance: break

                if CHECKED % 3: key = ""
                else: key = "\n"
                print("CHECK %d: %s %.2f " % (CHECKED,timezone,distance))
            except: ERRORS+=1

        measured_distances.sort()
        timezone = distances_dic.get(measured_distances[0])
        OP_TIME = (TIME.now() - TIME).seconds

        return [timezone, OP_TIME, CHECKED, ERRORS]

    @staticmethod
    def edit_tz(word):
        rev = word.split("/")
        del(rev[0])
        word = "".join(rev)

        word = list(word)
        for pos, letter in enumerate(word):
            if letter == "_": word[pos] = " "
            else: continue
        word = "".join(word)
        return word

