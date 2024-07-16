'''
Date: 05.07.2024
Description: Arrange seeds in the boundary area.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
from Trapezia import trapezia
from New_Coordsys import new_coordsys
from Tri_Pattern import tri_pattern
def edge_points(polygon_out, polygon_in, distance):
    '''input format: polygon_out = class Polygon,
                     polygon_in = class Polygon,
                     distance = value,
    '''
    # Enable boundary mode
    edge = True
    trapezoids = trapezia(polygon_out, polygon_in)
    points = []
    # Traverse each boundary region and merge points
    for trapezoid in trapezoids:
        mbr, origin, x_v = new_coordsys(trapezoid, edge)
        multipoints = tri_pattern(mbr, origin, x_v, trapezoid, distance)
        # Merge all points
        points += multipoints
    '''output format: points = List of class Point, 
    '''
    return points
# Test
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from coords_kml import extract_coordinates_kml
    from coords_transformation import geo_to_utm, get_utm_zone
    from New_Edge import new_edge
    kml_file_path = r"KML-Dateien\test.kml"
    distance = 0.35
    coords_geo = extract_coordinates_kml(kml_file_path)
    utm_zone = get_utm_zone(coords_geo)
    coords = geo_to_utm(coords_geo, utm_zone)
    #coords = [(0, 0), (120, 10), (90, 70), (20, 80)]
    polygon_out, polygon_in = new_edge(coords, distance)
    points = edge_points(polygon_out, polygon_in, distance)
    # Create a plot
    plt.figure('Pattern2')
    plt.plot(*polygon_out.exterior.xy)
    plt.plot(*polygon_in.exterior.xy)
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    plt.scatter(x_coords, y_coords, color='red')
    plt.title('Edge')
    plt.grid()
    plt.axis('equal')
    plt.show()