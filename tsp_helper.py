"""Helper functions and classes for TSP applications."""

from tsp_config import api_key
import simplejson
import urllib


class GeoPoint(object):
    """Simple structure for a geopoint with a given latitude and longitude."""

    def __init__(self, lat, lng):
        """Initialize geopoint."""
        self.lat = lat
        self.lng = lng


def get_distance(p1, p2):
    """Return the distance between two GeoPoints: *p1* and *p2* in meters."""
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?" \
          "origins={0},{1}&destinations={2},{3}&mode=driving&language=en-EN&" \
          "sensor=false&key={4}".format(
            str(p1.lat), str(p1.lng), str(p2.lat), str(p2.lng), api_key)
    result = simplejson.load(urllib.urlopen(url))
    return result["rows"][0]["elements"][0]["distance"]["value"]
