'''
Date: 03.05.2024
Description: Shrink the polygon by a certain boundary distance
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import shapely
def new_edge(vertices, width: float):
    '''input format: vertices = List, the boundary vertices of the field
                     width = value, the width of the boundary area
    '''    
    polygon_out = shapely.geometry.Polygon(vertices)
    # Use buffer function to shrink the polygon
    polygon_in = polygon_out.buffer(-width, join_style = 2)
    # Ensure that all vertices are stored in a ccw order
    polygon_out = shapely.geometry.polygon.orient(polygon_out)
    polygon_in = shapely.geometry.polygon.orient(polygon_in)
    '''output format: polygon_out = class Polygon, the original field polygon
                      polygon_in = class Polygon, the field polygon after cutting off the boundary area
    '''
    return polygon_out, polygon_in

# Test
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import coords_kml, coords_transformation
    # Set the vertex coordinates of the polygon and the boundary distance
    coords_geo = coords_kml.extract_coordinates_kml(r'KML-Dateien\feld 3.kml')
    utm_zone = coords_transformation.get_utm_zone(coords_geo)
    vertices = coords_transformation.geo_to_utm(coords_geo, utm_zone)
    # vertices = [(0, 0), (1, 10), (5, 17), (8, 7), (13, 3)]
    width = 10
    # Create a polygon
    polygon_outside, polygon_inside = new_edge(vertices, width)
    # Coordinates of the new polygon
    # for poly_out in polygon_outside.exterior.coords[:-1]:
    #     print(poly_out)
    # for poly_in in polygon_inside.exterior.coords[:-1]:
    #     print(poly_in)
    # Create a plot
    plt.figure('New edge')
    plt.plot(*polygon_outside.exterior.xy)
    plt.fill(*polygon_outside.exterior.xy, facecolor='lightcoral', label='original field')
    plt.plot(*polygon_inside.exterior.xy, color='blue')
    plt.fill(*polygon_inside.exterior.xy, facecolor='lightblue', label='shrunk field')
    plt.title('Origin and New polygon')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.show()