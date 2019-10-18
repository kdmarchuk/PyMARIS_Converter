
import numpy as np
from pygellan.magellan_data import MagellanDataset
import matplotlib.pyplot as plt

#data_path = 'C:\\Users\\Kyle\\Desktop\\test_1'
#data_path = 'J:\\MagellanTest\\Cortex_10um_2timepoints_1'
data_path = 'E:\\Data\\TestData\\MagellanTest\\PyMARIS_test_z10_c4_t3_1'

magellan = MagellanDataset(data_path)
channel_list = magellan.get_channel_names()

print(channel_list)

#img, img_metadata = magellan.read_image(channel_index=0, z_index=0, pos_index=0, read_metadata=True)
#print(img_metadata)
"""
all_data = magellan.as_array(stitched=True)
print(all_data)

sub_data = np.array(all_data[0, 2, 5])
print(sub_data.shape)
z_1 = sub_data.dtype
#max_intensity = np.max(sub_data[0, 0], axis=0)
print(z_1)

#plt.imshow(sub_data, cmap='gray')
#plt.show()
"""