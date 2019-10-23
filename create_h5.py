
import h5py


def create_h5(output_dictionary):
    channel_color_list = ['0.000 0.000 1.000', '0.000 1.000 0.000', '1.000 0.000 0.000',
                          '0.000 1.000 1.000', '1.000 0.000 1.000', '1.000 1.000 0.000',
                          '1.000 0.500 0.000', '1.000 0.000 0.500', '0.000 1.000 0.500']
    # Create the .ims file
    f = write_ims_file(output_dictionary)
    # Write attributes at the file level
    f = write_file_attributes(f)
    # Write DataSetInfo
    f = write_data_set_info_attributes(f, output_dictionary, channel_color_list)
    # Write DataSetTimes
    f = write_dataset_times(f, output_dictionary)
    # Write Thumbnail
    f = write_thumbnail(f)
    return f


def write_ims_file(output_dictionary):
    print('Writing ims file')
    save_pure_path = output_dictionary['save_directory']
    save_name = str(save_pure_path)
    f = h5py.File(save_name, "w")
    return f


def write_file_attributes(file):
    print('writing file attributes')
    write_attribute(file, 'DataSetDirectoryName', 'DataSet')
    write_attribute(file, 'DataSetInfoDirectoryName', 'DataSetInfo')
    write_attribute(file, 'ImarisDataSet', 'ImarisDataSet')
    write_attribute(file, 'ImarisVersion', '5.5.0')
    file.attrs.create('NumberOfDataSets', [1], dtype='uint32')
    write_attribute(file, 'ThumbnailDirectoryName', 'Thumbnail')
    return file


def write_data_set_info_attributes(file, output_dictionary, channel_color_list):
    # Channel Groups
    print('writing data set info attributes')
    channel_list = output_dictionary['file_channel_list']
    channel_names = output_dictionary['all_channels']
    data_set_info_group = file.create_group('DataSetInfo')
    for c in channel_list:
        channel_name_string = 'Channel ' + str(c)
        channel_group = data_set_info_group.create_group(channel_name_string)
        write_attribute(channel_group, 'Color', channel_color_list[c])
        write_attribute(channel_group, 'ColorMode', 'BaseColor')
        write_attribute(channel_group, 'ColorOpacity', '1.000')
        write_attribute(channel_group, 'ColorRange', '0.000 20000.000')
        write_attribute(channel_group, 'Description', '(description not specified)')
        write_attribute(channel_group, 'GammaCorrection', '1.000')
        write_attribute(channel_group, 'Name', channel_names[c])

    # Image Group
    print('writing image group')
    x_min = output_dictionary['x_min']
    x_max = output_dictionary['x_max']
    y_min = output_dictionary['y_min']
    y_max = output_dictionary['y_max']
    z_min = output_dictionary['z_min']
    z_max = output_dictionary['z_max']
    pixel_size = output_dictionary['pixel_size']
    image_group = data_set_info_group.create_group('Image')
    write_attribute(image_group, 'Description', '(description not specified)')
    print('pixel:size')
    write_attribute(image_group, 'ExtMax0', str(x_max * pixel_size))
    write_attribute(image_group, 'ExtMax1', str(y_max * pixel_size))
    write_attribute(image_group, 'ExtMax2', str(z_max * pixel_size))
    write_attribute(image_group, 'ExtMin0', str(x_min * pixel_size))
    write_attribute(image_group, 'ExtMin1', str(y_min * pixel_size))
    write_attribute(image_group, 'ExtMin2', str(z_min * pixel_size))
    print('post pixel size')
    write_attribute(image_group, 'Name', '(name not specified)')
    write_attribute(image_group, 'OriginalFormat', 'Bitplane: Imaris 5.5')
    write_attribute(image_group, 'OriginalFormatFileIOVersion', 'ImarisFileIO x64 9.3.1')
    write_attribute(image_group, 'RecordingDate', '2019-09-12 18:02:37.000')
    write_attribute(image_group, 'ResampleDimensionX', 'true')
    write_attribute(image_group, 'ResampleDimensionY', 'true')
    write_attribute(image_group, 'ResampleDimensionZ', 'true')
    write_attribute(image_group, 'Unit', 'um')
    write_attribute(image_group, 'X', str(x_max - x_min + 1))
    write_attribute(image_group, 'Y', str(y_max - y_min + 1))
    write_attribute(image_group, 'Z', str(z_max - z_min + 1))

    # Imaris group
    print('writing Imaris group')
    imaris_group = data_set_info_group.create_group('Imaris')
    write_attribute(imaris_group, 'ThumbnailMode', 'thumbnailMiddleSection')
    write_attribute(imaris_group, 'ThumbnailSize', '256')
    write_attribute(imaris_group, 'Version', '9.3')

    # ImarisDataSet group
    print('writing data set group')
    IDS_group = data_set_info_group.create_group('ImarisDataSet')
    write_attribute(IDS_group, 'Creator', 'Imaricumpiler')
    write_attribute(IDS_group, 'Version', '9.3.1')

    # Log group
    print('writing log group')
    log_group = data_set_info_group.create_group('Log')
    write_attribute(log_group, 'Entries', '0')

    # TimeInfo group
    print('writing time info group')
    time_start = output_dictionary['time_start']
    time_end = output_dictionary['time_end']
    time_list = output_dictionary['time_list']
    time_info_group = data_set_info_group.create_group('TimeInfo')
    write_attribute(time_info_group, 'DatasetTimePoints', str(time_end - time_start + 1))
    write_attribute(time_info_group, 'FileTimePoints', str(time_end - time_start + 1))

    for t in range(time_start, (time_end + 1)):
        time_string = 'TimePoint' + str(t)
        write_attribute(time_info_group, time_string, time_list[t-1])
    return file


def write_dataset_times(file, output_dictionary):
    print('writing DataSetTimes')
    # Create DataSetTimes
    time_start = output_dictionary['time_start']
    time_end = output_dictionary['time_end']
    data_set_times_group = file.create_group("DataSetTimes")
    data_set_times_group.create_dataset("Time", (time_end - time_start + 1,), dtype='uint64')
    data_set_times_group.create_dataset("TimeBegin", (1,), dtype='uint64')
    return file


def write_thumbnail(file):
    thumbnail_group = file.create_group("Thumbnail")
    thumbnail_group.create_dataset("Data", (256, 1024), dtype='uint8')
    return file


def write_attribute(group_name, attribute_name, attribute_value):
    group_name.attrs.create(attribute_name, [x for x in attribute_value], dtype=h5py.h5t.C_S1)


