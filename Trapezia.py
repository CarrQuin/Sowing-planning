'''
Date: 05.07.2024
Description: Decompose the boundary region into a collection of quadrilaterals.
<Notes>: Ensure that the number of vertices in the inner and outer polygons is consistent.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import shapely
def trapezia(out_polygon, in_polygon):
    '''input: out_polygon = class Polygon, the original field polygon
              in_polygon = class Polygon, the field polygon after cutting off the boundary area
    '''
    # Determine if two polygons have the same orientation
    if in_polygon.exterior.is_ccw == out_polygon.exterior.is_ccw is False:
        in_polygon = shapely.geometry.polygon.orient(in_polygon)
    outside = out_polygon.exterior.coords[:-1]
    inside = in_polygon.exterior.coords[:-1]
    trapezia = []
    # Sequentially extract vertices to create trapezoids for each pair of edges
    for i in range(len(outside)):
        # Initialize the vertex list for each boundary region
        element = []
        # Use the outer edge as the starting edge
        element.append(outside[i])
        element.append(outside[(i + 1) %len(outside)])
        # => Further optimization is possible
        # Reverse the input order of the inner edges to make them non-self-intersecting
        element.append(inside[(i + 1) %len(inside)])
        element.append(inside[i])
        # Save all trapezoids into a list
        trapezia.append(shapely.geometry.Polygon(element))
    '''output format: trapezia = List of class Polygons, the trapezoids after splitting the boundary area'''
    return trapezia
# Test
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from New_Edge import new_edge
    from coords_kml import extract_coordinates_kml
    from coords_transformation import geo_to_utm, get_utm_zone
    kml_file_path = r"KML-Dateien\test.kml"
    distance = 0.35
    #coords = [(0, 0), (1200, 100), (900, 700), (200, 800)]
    coords_geo = extract_coordinates_kml(kml_file_path)
    utm_zone = get_utm_zone(coords_geo)
    coords = geo_to_utm(coords_geo, utm_zone)
    polygon_out, polygon_in = new_edge(coords, distance)
    trapezoids = trapezia(polygon_out, polygon_in)
    print(polygon_out,'\n', polygon_in)
    # Create a plot
    plt.figure('trapezia')
    for trapezoid in trapezoids:
        plt.plot(*trapezoid.exterior.xy)
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.grid()
    plt.axis('equal')
    plt.show()