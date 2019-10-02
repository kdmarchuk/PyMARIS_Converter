import numpy as np
import json
from pygellan.magellan_data import MagellanDataset
import tifffile as tf
import matplotlib.pyplot as plt

#data_path = 'C:\\Users\\Kyle\\Desktop\\test_1'
data_path = 'J:\\MagellanTest\\Cortex_10um_2timepoints_1'
save_path = 'J:\\MagellanTest\\Cortex_10um_2timepoints_1'
save_name = 'J:\\MagellanTest\\Cortex_10um_2timepoints_1\\test.tif'

magellan = MagellanDataset(data_path)

all_data = magellan.as_array(stitched=True)

z_steps = magellan.summary_metadata['z-step_um']
print("Z Steps")
print(z_steps)

img, img_metadata = magellan.read_image(channel_index=0, z_index=0, pos_index=0, read_metadata=True)
xres = float(img_metadata['PixelSizeUm'])
print(img_metadata['PixelSizeUm'])
print(img_metadata)

# Find xy pixel data type
#data_type = xy_data.dtype
#print('Data Type: ' + str(data_type))

# Get the shape of the data
data_shape = all_data.shape
timepoints = data_shape[0]
num_channels = data_shape[1]
num_slices = data_shape[2]

print('Number of Timepoints: ' + str(data_shape[0]))
print('Number of Channels: ' + str(data_shape[1]))
print('Number of Z Slices: ' + str(data_shape[2]))

ijmetadata = {"Info": json.dumps(img_metadata)}

#
#    tif.save(xy_data, resolution=(xres, xres, 'INCH'), ijmetadata=ijmetadata)
# Get Saving Dir
"""
# Setup saving format for Imaris
for t in range(timepoints):
    time_name_string = '_t' + str(t)
    for c in range(num_channels):
        channel_name_string = '_c' + str(c)
        for z in range(num_slices):
            z_name_string = '_z' + str(z)
            full_name_string = 'J:\\MagellanTest\\Cortex_10um_2timepoints_1\\' + time_name_string + \
                               channel_name_string + z_name_string + '.tif'

            xy_data = np.array(all_data[t, c, z])
            with tf.TiffWriter(full_name_string, imagej=True) as tif:
                tif.save(xy_data, resolution=(xres, xres, 'INCH'), ijmetadata=ijmetadata)
            print(full_name_string)
# tiffile.py for saving
"""
print('COMPLETE!')