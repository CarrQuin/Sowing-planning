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
import matplotlib.pyplot as plt
if __name__ == '__main__':
    # Set the vertex coordinates of the polygon and the boundary distance
    vertices = [(0, 0), (1, 10), (5, 17), (8, 7), (13, 3)]
    width = 0.1
    # Create a polygon
    polygon_outside, polygon_inside = new_edge(vertices, width)
    # Coordinates of the new polygon
    for poly_out in polygon_outside.exterior.coords[:-1]:
        print(poly_out)
    for poly_in in polygon_inside.exterior.coords[:-1]:
        print(poly_in)
    # Create a plot
    plt.figure('New edge')
    plt.plot(*polygon_outside.exterior.xy)
    plt.plot(*polygon_inside.exterior.xy)
    plt.title('Origin and New polygon')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.grid()
    plt.axis('equal')
    plt.show()