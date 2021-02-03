from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle
from .search_tz import search_country_tz
from delorean import Delorean


def distance(current, last,  *coordinates):
    distance_dic = {}
    distance_dic["euclid_distance"] = geodesic(coordinates[0], coordinates[1]).km
    distance_dic["geod_distance"] = great_circle(coordinates[0], coordinates[1]).km
    return distance_dic

def location_info(raw_address, region):
    print("INFO")
    try:
        print("Coordinates: ", region.point)
    except:
        print("No coordinates founded")
    for key in raw_address:
        print(key, raw_address[key])

class GPS():
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
