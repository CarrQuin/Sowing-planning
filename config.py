'''Date: 18.07.2024
Description: All necessary input variables.
E-mail: k.qian@tu-braunschweig.de
Autor: Kaiyu Qian
'''
import numpy as np
# File path to read.
kml_file_path = r'KML-Dateien\feld 1.kml'

# Whether to save the results in CSV format, with an alternative KML.
save_as_csv = True
# Whether to use an optimization algorithm.
optimal = False

# Spacing between adjacent seeds, in [m]
distance = 3.5
# Width of the boundary region, in[m]
# !Notes!: If the boundary is too wide, it may cause errors.
edge_width = 3*np.sqrt(3)*distance
# (OPT)Number of steps optimization iterations.(Up to a max. of 100.)
# CANNOT BE ZERO
move_iter = 5
# (OPT)Number of steps optimization iterations.(Up to a max. of 60.)
# CANNOT BE ZERO
angle_iter = 6