import math
from typing import List, Dict, Union
import json

from turf.distance._distance import calculate_radians_distance
from turf.helpers import degrees_to_radians, radians_to_degrees
from turf.helpers import point, line_string
from turf.helpers import units_factors
from turf.helpers import Feature, LineString, Point
from turf.utils.exceptions import InvalidInput
from turf.utils.error_codes import error_code_messages


class Coordinate:
    def __init__(self, lon: float, lat: float, decimals=6):

        self.lon = lon
        self.lat = lat
        self.x = degrees_to_radians(lon)
        self.y = degrees_to_radians(lat)
        self.decimals = decimals

    @property
    def coords(self) -> List[Union[float, float]]:
        return self._rnd([self.lon, self.lat])

    @property
    def point(self) -> Point:
        return point(self._rnd([self.lon, self.lat]))

    def to_dict(self):
        d = {"lat": self.lat, "lon": self.lon}
        return d

    def __repr__(self):
        return f"Position({self.lon},{self.lat})"

    def __str__(self):
        return json.dumps(self.to_dict())

    def _rnd(self, x):
        return [round(i, self.decimals) for i in x]


class GreatCircle:
    def __init__(self, start, end, properties):

        self.start = Coordinate(start[0], start[1])
        self.end = Coordinate(end[0], end[1])

        self._check_antipodal()

        self.properties = properties
        self.distance = self._get_distance()
        self.arc_coordinates = self._calculate_arc_coordinates()

    def _check_antipodal(self):
        """
        Antipodes are coordinates that are diametrically opposite to each
        other on Earth. Antipodal points are connected by an infinite number of
        great circles
        """
        dif_lon = self.start.lon - self.end.lon
        dif_lat = self.start.lat - self.end.lat

        if (dif_lat == 0) and ((abs(dif_lon % 360) - 180) == 0):
            raise InvalidInput(
                error_code_messages["InvalidGreatCirclePoints"](
                    self.start.coords, self.end.coords
                )
            )

    @property
    def linestring(self) -> Union[Feature, Dict]:
        return line_string(self.arc_coordinates, self.properties)

    def _get_distance(self) -> float:
        """
        Gets the distance between start and end

        :return: distance_radians
        """
        dif_lon = self.start.x - self.end.x
        dif_lat = self.start.y - self.end.y

        distance = calculate_radians_distance(
            dif_lon, dif_lat, self.start.y, self.end.y
        )

        return distance

    def _get_intermediate_coord(self, fraction: float) -> List[Union[float, float]]:
        """
        Calculates the intermediate point on a great circle line
        http://www.edwilliams.org/avform.htm#Intermediate

        :param fraction: input fraction of the whole great circle
        :return: a tuple of cordinates
        """
        A = math.sin((1 - fraction) * self.distance) / math.sin(self.distance)
        B = math.sin(fraction * self.distance) / math.sin(self.distance)

        x = A * math.cos(self.start.y) * math.cos(self.start.x) + B * math.cos(
            self.end.y
        ) * math.cos(self.end.x)

        y = A * math.cos(self.start.y) * math.sin(self.start.x) + B * math.cos(
            self.end.y
        ) * math.sin(self.end.x)

        z = A * math.sin(self.start.y) + B * math.sin(self.end.y)

        lat = radians_to_degrees(
            math.atan2(z, math.sqrt(math.pow(x, 2) + math.pow(y, 2)))
        )
        lon = radians_to_degrees(math.atan2(y, x))

        return Coordinate(lon, lat).coords

    def _calculate_arc_coordinates(self) -> LineString:
        """
        Calculates intermediate points on a great circle line

        :param n_points: amount of intermediate points on the great circle
        :return: list of coordinates
        """
        coordinates = []
        n_points = self.properties.get("npoints", 0)

        coordinates.append(self.start.coords)

        if n_points > 2:

            for i in range(n_points - 2):
                coord = self._get_intermediate_coord((i + 1) / (n_points - 2 + 1))
                coordinates.append(coord)

        coordinates.append(self.end.coords)

        return coordinates

    def to_geojson(self):
        return self.linestring
