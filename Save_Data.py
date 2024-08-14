'''
Date: 10.07.2024
Description: Save seed locations to a KML or CSV file.
<Notes>:CSV format saves more time when saving large amounts of data.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import simplekml, csv
from pathlib import Path
from datetime import datetime
# Save as .csv
def save_date_csv(points_c):
    '''input format: points_c = List of class Point, the coordinates of the seeds calculated from the sowing
    '''
    # Create the file save location and define the filename
    file_path_c = Path("Koordinaten_Saatpunkte.csv")
    with file_path_c.open( 'w', newline='') as file_c:
        c_writer = csv.writer(file_c)
        # Write the header
        c_writer.writerow(['ID', 'X Coordinate', 'Y Coordinate'])
        # Save the coordinates of each point
        for i, point_c in enumerate(points_c, 1):
            c_writer.writerow([i, point_c.x, point_c.y])
    '''Return the absolute path of the file'''
    return str(file_path_c.resolve())
# Save as .kml
def save_date_kml(points_k):
    '''input format: points_k = List of class Point, the coordinates of the seeds calculated from the sowing
    '''
    kml = simplekml.Kml()
    # Timestamp
    current_time_k = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    kml.document.description = f"File generated at {current_time_k}"
    # Save the coordinates of each point
    for i, point_k in enumerate(points_k, 1):
            kml.newpoint(name=f"Point{i}", coords=[(point_k.x, point_k.y)])
    # Create the file save location and define the filename
    file_path_k = Path("Koordinaten_Saatpunkte.kml")
    kml.save(file_path_k)
    '''Return the absolute path of the file'''
    return str(file_path_k.resolve())
# Test
if __name__ == "__main__":
    from shapely import MultiPoint
    point_s = MultiPoint([(120.0, 30.0), (121.0, 31.0), (124.0, 32.0)])
    points = list(point_s.geoms)
    print(save_date_csv(points))
