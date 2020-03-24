from turf import bearing


def along(coords, distance):

    travelled = 0
    for i in range(len(coords)):
        if distance >= travelled and i == len(coords) - 1:
            break
        elif travelled >= distance:
            overshot = distance - travelled
            if not overshot:
                return coords[i]
            else:
                direction = bearing(coords[i], coords[i - 1]) - 180
                interpolated = destination(coords[i], overshot, direction)
                return interpolated
        else:
            travelled += measure_distance(coords[i], coords[i + 1])

    return coords[-1]
