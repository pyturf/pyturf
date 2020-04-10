import math
from typing import List, Tuple, Union
import json

from turf.helpers import degrees_to_radians, radians_to_degrees
from turf.helpers import feature_collection, point, line_string
from turf.helpers import units_factors
from turf.helpers import LineString, Point
from turf.invariant import get_coord
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages


class Coordinate:

    def __init__(self, lon: float, lat: float):
        self.lon = lon
        self.lat = lat
        self.x = degrees_to_radians(lon)
        self.y = degrees_to_radians(lat)

    @property
    def coords(self) -> Tuple[float, float]:
        return (self.lon, self.lat)

    @property
    def point(self) -> Point:
        return point([self.lon, self.lat]).to_geojson()

    def to_dict(self):
        d = {
            "lat": self.lat,
            "lon": self.lon
        }
        return d

    def __repr__(self):
        return f"Position({self.lon}, {self.lat})"

    def __str__(self):
        return json.dumps(self.to_dict())


class GreatCircle():

    def __init__(self, start, end, properties):

        self.start = Coordinate(start[0], start[1])
        self.end = Coordinate(end[0], end[1])
        self.properties = properties
        self.distance = self._calculate_distance()
        self.arc_coordinates = self._calculate_arc_coordinates()

    @property
    def linestring(self) -> LineString:
        return line_string(self.arc_coordinates, self.properties).to_geojson()

    def _calculate_distance(self) -> float:
        """
        Calculates the distance between start and end
        http://www.edwilliams.org/avform.htm#Dist
        https://en.wikipedia.org/wiki/Great-circle_distance

        :return: distance_radians
        """

        # Using A mathematically equivalent formula, which is less subject
        # to rounding error for short distances
        w = self.start.x - self.end.x
        h = self.start.y - self.end.y

        z = math.pow(math.sin(h / 2), 2) + \
            math.cos(self.start.y) * \
            math.cos(self.end.y) * \
            math.pow(math.sin(w / 2), 2)

        distance = 2 * math.asin(math.sqrt(z))

        return distance

    def _get_intermediate_coord(self, fraction: float) \
         -> List[Union[float, float]]:
        """
        Calculates the intermediate point on a great circle line
        http://www.edwilliams.org/avform.htm#Intermediate

        :param fraction: input fraction of the whole great circle
        :return: a tuple of cordinates
        """
        A = math.sin((1-fraction)*self.distance) / math.sin(self.distance)
        B = math.sin(fraction*self.distance) / math.sin(self.distance)

        x = A * math.cos(self.start.y) * math.cos(self.start.x) + \
            B * math.cos(self.end.y) * math.cos(self.end.x)

        y = A * math.cos(self.start.y) * math.sin(self.start.x) + \
            B * math.cos(self.end.y) * math.sin(self.end.x)

        z = A * math.sin(self.start.y) + B * math.sin(self.end.y)

        lat = radians_to_degrees(
            math.atan2(z, math.sqrt(math.pow(x, 2) + math.pow(y, 2))))
        lon = radians_to_degrees(math.atan2(y, x))

        return [round(lon,6), round(lat,6)]

    def _calculate_arc_coordinates(self) -> LineString:
        """
        Calculates intermediate points on a great circle line

        :param n_points: amount of intermediate points on the great circle
        :return: list of coordinates
        """
        coordinates = []
        n_points = self.properties.get('npoints',0)

        coordinates.append([round(self.start.lon, 6),
                            round(self.start.lat, 6)])

        if n_points > 0:

            for i in range(n_points):
                coord = self._get_intermediate_coord((i+1)/(n_points+1))
                coordinates.append(coord)

        coordinates.append([round(self.end.lon, 6),
                            round(self.end.lat, 6)])

        return coordinates

    def to_geojson(self):
        return feature_collection([self.linestring,
                                   self.start.point,
                                   self.end.point], {})
