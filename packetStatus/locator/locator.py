from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle
from .search_tz import search_country_tz
from delorean import Delorean


from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pycountry

import pytz

class Locator():
    def __init__(self):
        super().__init__()
        self.__geolocator = Nominatim(user_agent="locator")
        self.__listRegion = None

        self.__region = None
        self.__standard_time = Delorean()
        print(self.__standard_time.now().format_datetime())

    def get_time(self):
        return self.__standard_time
    standard_time = property(fget=get_time)

    def set_region(self, value):
        self.__region = value
    def get_region(self):
        return self.__region
    region = property(fget=get_region)

    def locate(self, place):
        self.set_region(self.__geolocator.geocode(place, addressdetails=True, language="en"))
        self.__listRegion = self.region.raw["address"]
        location_info(self.__listRegion, self.region)

    def set_timezone(self):
        results = search_country_tz(self.standard_time, self.region, self.__listRegion)
        print("Errors: %d\nPlaces checked: %d"%(results[3], results[2]))
        print("Operation Time: ", results[1])
        self.standard_time.shift(results[0])
        print("Presenting timezone(s) for: ", self.standard_time.timezone, "\n", self.standard_time.format_datetime())

    @staticmethod
    def distance(current, last,  *coordinates):
        distance_dic = {}
        distance_dic["euclid_distance"] = geodesic(coordinates[0], coordinates[1]).km
        distance_dic["geod_distance"] = great_circle(coordinates[0], coordinates[1]).km
        return distance_dic

    @staticmethod
    def location_info(raw_address, region):
        print("INFO")
        try: print("Coordinates: ", region.point)
        except:
            print("No coordinates founded")
        for key in raw_address:
            print(key, raw_address[key])



measured_distances = []
distances_dic = {}

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

def search_country_tz(TIME, PLACE, listRegion, accpt_distance=250):
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
            #print("CHECK %d: %s %.2f " % (CHECKED,timezone,distance), end = key)
        except: ERRORS+=1

    measured_distances.sort()
    timezone = distances_dic.get(measured_distances[0])
    OP_TIME = (TIME.now() - TIME).seconds

    return [timezone, OP_TIME, CHECKED, ERRORS]

