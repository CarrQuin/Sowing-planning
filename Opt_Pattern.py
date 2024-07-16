'''
Last modification date: 22.05.2024
Description: Rotate the polygon within the grid 
             to find the arrangement that contains the most points.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import numpy as np
from shapely.geometry import Point, MultiPoint 
from shapely import affinity
def opt_pattern(polygon, distance, opt_move=1, opt_angle=1):
    '''
    input format:   polygon = class Polygon,
                    distance = value, size of every two adjacent points
                    opt_move = value, translation iterations
                    opt_angle = value, rotation iterations
    '''
    # Calculate the area required for grid placement.
    triangle_height = distance * (np.sqrt(3) / 2)
    centroid = polygon.centroid
    radius = centroid.hausdorff_distance(polygon)
    min_x = centroid.x - radius
    max_x = centroid.x + (radius + 2 * distance)
    min_y = centroid.y - radius
    max_y = centroid.y + (radius + 2 * triangle_height)
    # Lay out an even regular triangular grid.
    points = []
    y = min_y
    even_row = True
    while y <= max_y:
        if even_row: 
            x = min_x 
        else:
            x = min_x + (distance / 2)
        while x <= max_x:
            point = Point(x, y)
            points.append(point)
            x += distance
        even_row = not even_row
        y += triangle_height
    points = MultiPoint(points)
    # Rotate and translate to find the optimal direction.
    i = 0
    opt_steps = [0, 0, 0]
    opt_points = MultiPoint()
    move_y_steps = move_x_steps = 100 / opt_move
    angle_steps = 60 / opt_angle
    for steps1 in range(opt_move):
        pattern_move_x = move_x_steps*steps1
        for steps2 in range(opt_move):
            pattern_move_y = move_y_steps*steps2
            for steps3 in range(opt_angle):
                angle_degrees = angle_steps*steps3
                # Log the loop execution progress
                i += 1
                print('Optimization calculation in progress:', i, end='\r')
                x_m = (pattern_move_x/100)*distance
                y_m = (pattern_move_y/100)*(2*triangle_height)
                # Translate and rotate the polygon within the grid
                moved_polygon = affinity.translate(polygon,x_m,y_m)
                polygon_new = affinity.rotate(moved_polygon, angle_degrees, 'centroid')
                # Calculate the number of points in the shape and determine if it contains more points
                point_s = points.intersection(polygon_new)
                if len(point_s.geoms) > len(opt_points.geoms):
                    #print('pattern_move_x:', pattern_move_x,end=';')
                    #print('pattern_move_y:', pattern_move_y, end=';')
                    #print('angle_degrees:', angle_degrees)
                    #print('intersections:', len(point_s.geoms))
                    opt_points = point_s
                    opt_steps = [x_m, y_m, angle_degrees]
    # Restore the points to the original polygon
    moved_points = affinity.translate(opt_points, xoff=-opt_steps[0], yoff=-opt_steps[1])
    rotated_points = affinity.rotate(moved_points, -opt_steps[2], 'centroid')
    '''output: moved_points = List of class Point, '''
    return list(rotated_points.geoms)

# Test
if __name__ == "__main__":
    from shapely.geometry import Polygon
    import time
    import matplotlib.pyplot as plt
    polygon = Polygon([(0, 0), (120, 10), (90, 70), (20, 80)])
    distance = 1
    start_time1 = time.time()
    points = opt_pattern(polygon, distance,10,6)
    end_time1 = time.time()
    print(f'Elapsed time new: {end_time1 - start_time1} seconds')
    print('The total number of points:', len(points))
    # Create a plot
    plt.figure('Pattern_opt')
    plt.plot(*polygon.exterior.xy, label='original')
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    plt.scatter(x_coords, y_coords, color='red')
    plt.title('Equilateral triangle pattern')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.show()