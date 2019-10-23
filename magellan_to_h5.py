import numpy as np
import h5py
from write_functions import write_attribute
from pygellan.magellan_data import MagellanDataset
"""
data_path = 'E:\\Data\\TestData\\MagellanTest\\201978_AgedOvary_Nobox_3umSteps_2'
save_path = 'E:\\Data\\TestData\\MagellanTest'
save_name = 'E:\\Data\\TestData\\MagellanTest\\201978_AgedOvary_Nobox_3umSteps_2\\test.ims'
"""
data_path = 'E:\\Data\\SPIM\\Cortex_3umStep_1'
save_path = 'E:\\Data\\SPIM'
save_name = 'E:\\Data\\SPIM\\Cortex_3umStep_1_test.ims'

magellan = MagellanDataset(data_path)

all_data = magellan.as_array(stitched=True)
size_array = all_data.shape
print('All Data')
print(size_array)
num_slices = size_array[2]
print(num_slices)
total_height = size_array[3]
print(total_height)
total_width = size_array[4]
print(total_width)

# Get pertinent information
voxel_size_z_um = magellan.summary_metadata['z-step_um']
print(voxel_size_z_um)
pixel_size_xy_um = magellan.summary_metadata['PixelSize_um']
print(pixel_size_xy_um)
num_frames = magellan.get_num_frames()
print(num_frames)
num_positions = magellan.get_num_xy_positions()
print(num_positions)
num_channels = len(magellan.summary_metadata['ChNames'])
print(num_channels)
image_height = magellan.summary_metadata['Height']
print(image_height)
image_width = magellan.summary_metadata['Width']
print(image_width)

# Create h5 file
f = h5py.File(save_name, "w")

# Write file attributes
#f.attrs.create('DataSetDirectoryName', string_obj, dtype=h5py.h5t.C_S1)
write_attribute(f, 'DataSetDirectoryName', 'DataSet')
write_attribute(f, 'DataSetInfoDirectoryName', 'DataSetInfo')
write_attribute(f, 'ImarisDataSet', 'ImarisDataSet')
write_attribute(f, 'ImarisVersion', '5.5.0')
f.attrs.create('NumberOfDataSets', [1], dtype='uint32')
write_attribute(f, 'ThumbnailDirectoryName', 'Thumbnail')

# Create DataSetInfo
group = f.create_group('DataSetInfo')
for c in range(num_channels):
    channel_name_string = 'Channel ' + str(c)
    channel_group = group.create_group(channel_name_string)
    write_attribute(channel_group, 'Color', '1.000 0.000 0.000')
    write_attribute(channel_group, 'ColorMode', 'BaseColor')
    write_attribute(channel_group, 'ColorOpacity', '1.000')
    write_attribute(channel_group, 'ColorRange', '0.000 414.000')
    write_attribute(channel_group, 'Description', '(description not specified)')
    write_attribute(channel_group, 'GammaCorrection', '1.000')
    write_attribute(channel_group, 'Name', '(name not specified)')

# Create and add attributes to Image Group
image_group = group.create_group('Image')
write_attribute(image_group, 'Description', '(description not specified)')
write_attribute(image_group, 'ExtMax0', str(int(total_width * pixel_size_xy_um)))
write_attribute(image_group, 'ExtMax1', str(int(total_height * pixel_size_xy_um)))
write_attribute(image_group, 'ExtMax2', str(int(num_slices * voxel_size_z_um)))
write_attribute(image_group, 'ExtMin0', '0')
write_attribute(image_group, 'ExtMin1', '0')
write_attribute(image_group, 'ExtMin2', '0')
write_attribute(image_group, 'Name', '(name not specified)')
write_attribute(image_group, 'OriginalFormat', 'Bitplane: Imaris 5.5')
write_attribute(image_group, 'OriginalFormatFileIOVersion', 'ImarisFileIO x64 9.3.1')
write_attribute(image_group, 'RecordingDate', '2019-09-12 18:02:37.000')
write_attribute(image_group, 'ResampleDimensionX', 'true')
write_attribute(image_group, 'ResampleDimensionY', 'true')
write_attribute(image_group, 'ResampleDimensionZ', 'true')
write_attribute(image_group, 'Unit', 'um')
write_attribute(image_group, 'X', str(total_width))
write_attribute(image_group, 'Y', str(total_height))
write_attribute(image_group, 'Z', str(num_slices))

# Create and add attributes to Imaris Group
imaris_group = group.create_group('Imaris')
write_attribute(imaris_group, 'ThumbnailMode', 'thumbnailMiddleSection')
write_attribute(imaris_group, 'ThumbnialSize', '256')
write_attribute(imaris_group, 'Version', '7.6')

# Create and add attributes to ImarisDataSet Group
IDS_group = group.create_group('ImarisDataSet')
write_attribute(IDS_group, 'Creator', 'Imaricumpiler')
write_attribute(IDS_group, 'Version', '9.3.1')

# Create and add attributes to Log Group
log_group = group.create_group('Log')
write_attribute(log_group, 'Entries', '0')

# Ctrate and add attributes to TimeInfo Group
time_info_group = group.create_group('TimeInfo')
write_attribute(time_info_group, 'DatasetTimePoints', str(num_frames))
write_attribute(time_info_group, 'FileTimePoints', str(num_frames))
write_attribute(time_info_group, 'TimePoint1', '2019-09-12 18:02:37.000')

# Create DataSetTimes
data_set_times_group = f.create_group("DataSetTimes")
time_dset = data_set_times_group.create_dataset("Time", (1,), dtype='uint64')
time_begin_dset = data_set_times_group.create_dataset("TimeBegin", (1,), dtype='uint64')

# Create Thumbnail
thumbnail_group = f.create_group("Thumbnail")
data_dset = thumbnail_group.create_dataset("Data", (256, 1024), dtype='uint8')

for t in range(num_frames):
    time_name_string = '/TimePoint ' + str(t)
    for c in range(num_channels):
        channel_name_string = '/Channel ' + str(c)
        channel_group_data = f.create_group("DataSet/ResolutionLevel 0" + time_name_string + channel_name_string)
        write_attribute(channel_group_data, 'HistogramMax', '65535.000')
        write_attribute(channel_group_data, 'HistogramMin', '0.000')
        write_attribute(channel_group_data, 'ImageBlockSizeX', '256')
        write_attribute(channel_group_data, 'ImageBlockSizeY', '256')
        write_attribute(channel_group_data, 'ImageBlockSizeZ', '256')
        write_attribute(channel_group_data, 'ImageSizeX', str(total_width))
        write_attribute(channel_group_data, 'ImageSizeY', str(total_height))
        write_attribute(channel_group_data, 'ImageSizeZ', str(num_slices))

        data_temp = f.create_dataset("DataSet/ResolutionLevel 0" + time_name_string + channel_name_string + "/Data",
                                     (1, total_height, total_width), chunks=(8, 256, 256),
                                     maxshape=(num_slices, total_height, total_width), compression="gzip",
                                     compression_opts=2, dtype='uint16')
        data_temp.write_direct(np.array(all_data[t, c, 1]))
        for z in range(num_slices - 1):
            data_temp.resize(data_temp.shape[0] + 1, axis=0)
            data_temp[z + 1, :, :] = np.array(all_data[t, c, z + 1])
            print('T:' + str(t) + ', C:' + str(c) + ', Z:' + str(z))
        """
        data_temp = f.create_dataset("DataSet/ResolutionLevel 0" + time_name_string + channel_name_string + "/Data",
                                     (num_slices, total_height, total_width), chunks=(8, 256, 256), compression="gzip",
                                     compression_opts=2, dtype='uint16')
        data_temp.write_direct(np.array(all_data[t, c]))
        
        data_temp = f.create_dataset("DataSet/ResolutionLevel 0" + time_name_string + channel_name_string + "/Data",
                                     (272, 5888, 4096), chunks=(8, 256, 256), compression="gzip",
                                     compression_opts=2, dtype='uint16')
        data_temp.write_direct(np.pad((np.array(all_data[t, c])), pad_width=((2, 3), (178, 178), (204, 204)), mode='constant'))
        """
        histogram_temp = f.create_dataset("DataSet/ResolutionLevel 0" + time_name_string + channel_name_string +
                                          "/Histogram", (256,), dtype='uint64')

print('COMPLETE')
