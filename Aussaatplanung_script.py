'''
Date: 15.07.2024
Description: The results can be saved as KML or CSV files.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
from New_Edge import new_edge
from New_Coordsys import new_coordsys
from Tri_Pattern import tri_pattern
from Opt_Pattern import opt_pattern
from Edge_Points import edge_points
from Save_Data import save_date_kml, save_date_csv
from coords_kml import extract_coordinates_kml
from coords_transformation import utm_to_geo_points, geo_to_utm, get_utm_zone
import time
import configparser
# =====Variables=====
config = configparser.ConfigParser()
config.read('config.ini')
kml_file_path = config.get('path', 'kml_file_path')
save_as_csv = config.getboolean('settings', 'save_as_csv')
distance = config.getfloat('variables', 'distance')
edge_width = config.getfloat('variables', 'edge_width')
optimal = config.getboolean('settings', 'optimal')
move_iter = config.getint('variables', 'move_iter')
angle_iter = config.getint('variables', 'angle_iter')
# =====main=====
# Abstract geometric information from geographic coordinates
start_time = time.time()# T0 start <<<
coords_geo = extract_coordinates_kml(kml_file_path)
utm_zone = get_utm_zone(coords_geo)
coords = geo_to_utm(coords_geo, utm_zone)
outside_polygon, inside_polygon = new_edge(coords, edge_width)
test1_time = time.time()# T1 trans to <<<
# Arrange seeds within the interior area
if optimal:
    multipoints = opt_pattern(inside_polygon, distance, move_iter, angle_iter)
else:
    mbr, index, x_v = new_coordsys(inside_polygon)
    multipoints = tri_pattern(mbr, index, x_v, inside_polygon, distance)
# Arrange seeds along the boundaries
points_edge = edge_points(outside_polygon, inside_polygon, distance)
# Convert to geographic coordinates and save
points_all = multipoints + points_edge
test2_time = time.time()# T2 pattern <<<
points_geo = utm_to_geo_points(points_all, utm_zone)
print('The new total points:', len(points_all))
test3_time = time.time()# T3 transform back <<<
if save_as_csv:
    print(save_date_csv(points_geo))
else:
    print(save_date_kml(points_geo))
end_time = time.time()# T4 end <<<
# Test
if __name__ == '__main__':
    # =====Elapsed Time=====
    print(f'new_Transto-time: {test1_time - start_time} seconds')
    print(f'new_Pattern-time: {test2_time - test1_time} seconds')
    print(f'new_transback-time: {test3_time - test2_time} seconds')
    print(f'new_savedate-time: {end_time - test3_time} seconds')
    print(f'new_Fulltime: {end_time - start_time} seconds')
    # =====Plot=====
    import matplotlib.pyplot as plt
    import pathlib
    plt.figure(pathlib.Path(kml_file_path).stem)
    plt.plot(*outside_polygon.exterior.xy)
    plt.plot(*inside_polygon.exterior.xy)
    x_coords = [point.x for point in points_all]
    y_coords = [point.y for point in points_all]
    plt.scatter(x_coords, y_coords, color='red')
    plt.title(pathlib.Path(kml_file_path).name)
    plt.grid()
    plt.axis('equal')
    plt.show()