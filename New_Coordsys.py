'''
Date: 07.07.2024
Description: Find the appropriate arrangement direction and starting point.
<Notes>: the endpoints must be provided in a CounterClockWise direction.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import numpy as np
def new_coordsys(polygon, edge=False):
    '''input format: polygon = class Polygon, 
                     edge = bool, boundary mode
    '''
    point = 0
    x_vec = np.array([0, 0])
    mbr = polygon.minimum_rotated_rectangle
    points = np.array(mbr.exterior.coords[:-1])
    # Boundary mode
    if edge:
        # Treat the first edge as the x-axis
        point = 0
        v01 = points[1] - points[0]
        v01_n = np.linalg.norm(v01)
        x_vec = v01 / v01_n
    else:
        # Find the longest edge to serve as the x-axis 
        # in a Cartesian coordinate system
        for i in range(len(points)):
            # vector from i.vertex to i-1.vertex, new y axis
            v03 = points[i-1] - points[i]
            # vector from 1.vertex to i+1.vertex, new x axis
            v01 = points[(i+1) % len(points)] - points[i]
            # Calculate the lengths of two adjacent edges
            v03_n = np.linalg.norm(v03)
            v01_n = np.linalg.norm(v01)
            # Use the shorter edge as the y-axis of the Cartesian coordinates
            if v01_n < v03_n:
                continue
            y_coord = v03[1]
            # Ensure the coordinate axes have minimal rotation
            if y_coord < 0:
                continue
            point = i
            x_vec = v01 / v01_n
            return mbr, point, x_vec
    '''output format: mbr = class Polygon, minimum bounding rectangle
                      point = value, the point of new origin
                      x_vec = func Array, a unit vector of new x-axis
    '''
    return mbr, point, x_vec
# Test
if __name__ == '__main__':
    from shapely.geometry import Polygon
    import matplotlib.pyplot as plt
    polygon = Polygon([(0, 0), (120, 10), (90, 70), (20, 80)])
    mbr, point, x_vecc = new_coordsys(polygon)
    print('mbr:', mbr)
    print('origin:', point)
    print('x direction:', x_vecc)
    plt.figure('new_coordsys')
    plt.plot(*polygon.exterior.xy)
    plt.fill(*polygon.exterior.xy, facecolor='lightblue', label='polygon')
    plt.plot(*mbr.exterior.xy, color='green', label='mbr')
    plt.quiver(*list(mbr.exterior.coords)[point], *x_vecc, scale=15, color='red', label='x-axis')
    plt.title('mbr of polygon and x-axis of pattern')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.show()