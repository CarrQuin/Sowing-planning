'''
Date: 15.07.2024
Description: Uniformly fill a polygon with an equilateral triangle
<Notes>: Not applicable for concave polygons.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import numpy as np
from shapely.geometry import Point, LineString
def tri_pattern(mbr, i, v_x, polygon, distance):
    '''input format: mbr = class Polygon, minimum bounding rectangle
                     i = value, the vertex index of origin
                     v_x = func Array, 
                     polygon = class Polygon, 
                     distance = value, size of every two adjacent points
    '''
    # Translate polygon vertices and remove duplicates
    mbr_vertices = np.array(mbr.exterior.coords[:-1])
    # Get the ring of the polygon
    exterior = polygon.exterior
    # Identify the origin and the points immediately before and after it
    m3 = mbr_vertices[i-1]
    m0 = mbr_vertices[i]
    m1 = mbr_vertices[(i + 1) %len(mbr_vertices)]
    # Calculate the direction vector of the row
    v_y = np.array([-v_x[1], v_x[0]])
    # Calculate the translation vectors for rows and columns
    move_x = v_x * distance
    move_y = v_y * distance * (np.sqrt(3) / 2)
    # Set the initial value for the loop
    points = []
    y1 = 0.5 * move_y + m0
    y2 = 0.5 * move_y + m1
    even_row = True
    # Error troubleshooting variables
    error_count = 0
    # Pattern loop
    while np.linalg.norm(y1 - m0) <= np.linalg.norm(m3 - m0):
        # Determine the rows of points to be arranged
        line = LineString([y1, y2])
        #Calculate the range of points that need to be arranged
        intersections = line.intersection(exterior)
        # Determine the type of intersection points to prevent critical errors
        # => Further optimization is possible
        if not intersections.geom_type == 'MultiPoint':
            # Determine if two polygons are approximately equal
            union_area = polygon.union(mbr).area
            intersection_area = polygon.intersection(mbr).area
            area_difference = union_area - intersection_area
            # Approximately equal if the area difference is less than 0.1%
            if area_difference <= 0.001 * union_area:
                p_min = y1
                p_max = y2
            else:
                y1 += move_y
                y2 += move_y
                even_row = not even_row
                error_count += 1
                continue
        else:
            # Select the first intersection point as the minimum value
            itsct_0 = np.array(intersections.geoms[0].coords)
            # Select the last intersection point as the maximum value
            itsct_n = np.array(intersections.geoms[-1].coords)
            # Determine which intersection point is closer to the starting position
            if np.linalg.norm(itsct_0 - y1) < np.linalg.norm(itsct_n - y1):
                p_min = itsct_0
                p_max = itsct_n
            else:
                p_min = itsct_n
                p_max = itsct_0
        # Exclude unnecessary ranges
        largest_multiple = (np.linalg.norm(p_min - y1) // distance + 1) * distance
        # Move the starting point when changing rows
        if even_row: 
            x = np.array(y1 +largest_multiple * v_x)
        else:
            x = np.array(y1 + (-(distance / 2) + largest_multiple) * v_x)
            # Prevent points from overflowing outside the polygon
            if not polygon.contains(Point(x)):
                x = np.array(y1 + ((distance / 2) + largest_multiple) * v_x)
        # Record a point at regular intervals along the same row
        while np.linalg.norm(x - y1) <= np.linalg.norm(p_max - y1):
            point = Point(x)
            points.append(point)
            x += move_x
        # Move one row spacing each time a new row is started
        y1 += move_y
        y2 += move_y
        even_row = not even_row
    # Error troubleshooting module
    if error_count > 0:
        print(error_count, 'errors occurred with type', intersections.geom_type)
        print('The erroneous graph: ', polygon)
    '''output format: points = List of class Point, '''
    return points

# Test
if __name__ == '__main__':
    import time
    import matplotlib.pyplot as plt
    from shapely.geometry import Polygon
    from New_Coordsys import new_coordsys
    polygon = Polygon([(0, 0), (1200, 100), (900, 700), (200, 800)])
    distance = 1
    mbr, i, v_x = new_coordsys(polygon)
    #print('input',mbr.exterior.coords[i], v_x)
    start_time = time.time()
    points = tri_pattern(mbr, i, v_x, polygon, distance)
    end_time = time.time()
    print(f'Elapsed time new2: {end_time - start_time} seconds')
    print('The total number of points2:', len(points))
    # Create a plot
    plt.figure('Pattern1')
    plt.plot(*polygon.exterior.xy)
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    plt.scatter(x_coords, y_coords, color='red')
    plt.title('Equilateral triangle pattern')
    plt.grid()
    plt.axis('equal')
    plt.show()