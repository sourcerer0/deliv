from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pycountry

import pytz

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
