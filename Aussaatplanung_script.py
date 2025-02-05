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
import config as cf
# =====main=====
# Abstract geometric information from geographic coordinates
coords_geo = extract_coordinates_kml(cf.kml_file_path)
utm_zone = get_utm_zone(coords_geo)
coords = geo_to_utm(coords_geo, utm_zone)
outside_polygon, inside_polygon = new_edge(coords, cf.edge_width)
start_time = time.time()# T0 start <<<
# Arrange seeds within the interior area
if cf.optimal:
    points_center = opt_pattern(inside_polygon, cf.distance, cf.move_iter, cf.angle_iter)
else:
    points_center = tri_pattern(*new_coordsys(inside_polygon), inside_polygon, cf.distance)
# Arrange seeds along the boundaries
points_edge = edge_points(outside_polygon, inside_polygon, cf.distance)
# Convert to geographic coordinates and save
test1_time = time.time()# T1 pattern <<<
points_geo = utm_to_geo_points(points_center + points_edge, utm_zone)
test2_time = time.time()# T2 transform back <<<
if cf.save_as_csv:
    print(save_date_csv(points_geo))
else:
    print(save_date_kml(points_geo))
end_time = time.time()# T3 end <<<
# Test
if __name__ == '__main__':
    # =====Elapsed Time=====
    print('The total number of seeds(v2):', len(points_geo))
    print(f'v2_Patterning-time: {test1_time - start_time} seconds')
    print(f'v2_Transformation-time: {test2_time - test1_time} seconds')
    print(f'v2_Data-saving-time: {end_time - test2_time} seconds')
    print(f'v2_Fulltime: {end_time - start_time} seconds')
    # =====Plot=====
    import matplotlib.pyplot as plt
    import pathlib
    import shapely
    plt.figure(pathlib.Path(cf.kml_file_path).stem)
    # -----Geo-----
    # polygon_geo = shapely.geometry.Polygon(coords_geo)
    # plt.plot(*polygon_geo.exterior.xy)
    # x_coords = [point_geo.x for point_geo in points_geo]
    # y_coords = [point_geo.y for point_geo in points_geo]
    # plt.scatter(x_coords, y_coords, color='red')
    # -----UTM-----
    # plt.plot(*outside_polygon.exterior.xy)
    # plt.plot(*inside_polygon.exterior.xy, '--')
    # x_coords = [point.x for point in points_center + points_edge]
    # y_coords = [point.y for point in points_center + points_edge]
    # plt.scatter(x_coords, y_coords, color='red')
    # plt.title(pathlib.Path(cf.kml_file_path).name)
    # plt.grid()
    # plt.axis('equal')
    # plt.show()