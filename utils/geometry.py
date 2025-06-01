from shapely.geometry import LineString, Polygon
from models.noflyzone import NoFlyZone

def intersects_nfz(start_pos, end_pos, nfz: NoFlyZone):
    path = LineString([start_pos, end_pos])
    polygon = Polygon(nfz.coordinates)
    return path.intersects(polygon)
