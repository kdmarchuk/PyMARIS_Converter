from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox, QGraphicsRectItem, QFileDialog
#from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QCoreApplication
#from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pygellan.magellan_data import MagellanDataset
import pathlib
import time
#import pyqtgraph as pg

from PyMARIS_Converter_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.magellan_dataset_dictionary = {}
        self.converter_dictionary = {}

        # Connections start now
        self._ui.load_magellan_pushButton.clicked.connect(self.get_working_directory)
        self._ui.remove_pushButton.clicked.connect(self.remove_working_directory)
        self._ui.magellan_dataset_listWidget.itemClicked.connect(self.refresh_gui)
        self._ui.browse_pushButton.clicked.connect(self.set_save_directory)
        self._ui.reset_time_pushButton.clicked.connect(self.refresh_time)
        self._ui.reset_space_pushButton.clicked.connect(self.refresh_space)
        self._ui.remove_channels_pushButton.clicked.connect(self.remove_channels)
        self._ui.add_channels_pushButton.clicked.connect(self.return_channels)
        self._ui.auto_generate_pushButton.clicked.connect(self.generate_file_name)
        self._ui.add_output_pushButton.clicked.connect(self.generate_output)

    def get_working_directory(self):
        # Get the string version
        magellan_directory_str = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # Convert to path version for OS compatibility
        magellan_directory_path = pathlib.Path(magellan_directory_str)
        try:
            magellan = MagellanDataset(magellan_directory_path)
        except Exception:
            print('Not a Magellan Dataset')
            return
        print('PATH: ' + str(magellan_directory_path))
        self._ui.magellan_dataset_listWidget.addItem(magellan_directory_str)
        self.store_magellan_metadata(magellan_directory_str)

    def remove_working_directory(self):
        self._ui.magellan_dataset_listWidget.takeItem(self._ui.magellan_dataset_listWidget.currentRow())

        # Magellan Related
    def store_magellan_metadata(self, magellan_directory):
        print('Collecting Metadata: ' + magellan_directory)
        magellan = MagellanDataset(magellan_directory)
        all_data = magellan.as_array(stitched=True)
        # Get size of dataset
        size_array = all_data.shape
        num_slices = size_array[2]
        total_height = size_array[3]
        total_width = size_array[4]
        voxel_size_z_um = magellan.summary_metadata['z-step_um']
        pixel_size_xy_um = magellan.summary_metadata['PixelSize_um']
        num_frames = magellan.get_num_frames()
        num_positions = magellan.get_num_xy_positions()
        try:
            num_channels = len(magellan.summary_metadata['ChNames'])
            channel_names = magellan.summary_metadata['ChNames']
        except Exception:
            num_channels = len(magellan.get_channel_names())
            channel_names = magellan.get_channel_names()

        image_height = magellan.summary_metadata['Height']
        image_width = magellan.summary_metadata['Width']

        # Add it all to the local dictionary
        local_dictionary = {'directory': magellan_directory,
                            'slices': num_slices,
                            'width': total_width,
                            'height': total_height,
                            'zSize': voxel_size_z_um,
                            'xySize': pixel_size_xy_um,
                            'frames': num_frames,
                            'positions': num_positions,
                            'channels': num_channels,
                            'channel_names': channel_names,
                            'single_image_height': image_height,
                            'single_image_width': image_width
                            }
        # append to global dictionary
        self.magellan_dataset_dictionary[magellan_directory] = local_dictionary

    def set_save_directory(self):
        save_directory = str(QFileDialog.getExistingDirectory(self, "Select Save Directory"))
        self._ui.save_directory_lineEdit.setText(save_directory)

    def refresh_gui(self):

        # Get highlighted entry
        self.active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()

        # Save Directory entry
        self._ui.save_directory_lineEdit.setText(self.active_magellan)

        # Channels tab
        self._ui.included_listWidget.clear()
        self._ui.excluded_listWidget.clear()
        num_channels = self.magellan_dataset_dictionary[self.active_magellan]['channels']
        for c in range(num_channels):
            temp_channel_list = self.magellan_dataset_dictionary[self.active_magellan]['channel_names']
            temp_channel_name = temp_channel_list[c]
            self._ui.included_listWidget.addItem('Channel ' + str(c) + ': ' + temp_channel_name)

        # Space tab
        # x max and min
        self._ui.x_min_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['width']))
        self._ui.x_min_lineEdit.setText(str(1))
        self._ui.x_max_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['width']))
        self._ui.x_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['width']))
        # y max and min
        self._ui.y_min_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['height']))
        self._ui.y_min_lineEdit.setText(str(1))
        self._ui.y_max_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['height']))
        self._ui.y_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['height']))
        # z max and min
        self._ui.z_min_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['slices']))
        self._ui.z_min_lineEdit.setText(str(1))
        self._ui.z_max_lineEdit.setValidator(QIntValidator(1, self.magellan_dataset_dictionary[self.active_magellan]['slices']))
        self._ui.z_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['slices']))

        # Time tab
        self._ui.first_frame_spinBox.setMinimum(1)
        self._ui.first_frame_spinBox.setMaximum(self.magellan_dataset_dictionary[self.active_magellan]['frames'])
        self._ui.final_frame_spinBox.setMinimum(1)
        self._ui.final_frame_spinBox.setMaximum(self.magellan_dataset_dictionary[self.active_magellan]['frames'])
        self._ui.first_frame_spinBox.setValue(1)
        self._ui.final_frame_spinBox.setValue(self.magellan_dataset_dictionary[self.active_magellan]['frames'])

        # file name
        file_path = pathlib.PurePath(self.magellan_dataset_dictionary[self.active_magellan]['directory'])
        file_name = file_path.parts[-1]
        self._ui.save_name_lineEdit.setText(file_name + '.ims')

    def refresh_space(self):
        # Get highlighted entry
        #active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()
        self._ui.x_min_lineEdit.setText(str(1))
        self._ui.x_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['width']))
        self._ui.y_min_lineEdit.setText(str(1))
        self._ui.y_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['height']))
        self._ui.z_min_lineEdit.setText(str(1))
        self._ui.z_max_lineEdit.setText(str(self.magellan_dataset_dictionary[self.active_magellan]['slices']))

    def refresh_time(self):
        # Get highlighted entry
        #active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()
        self._ui.first_frame_spinBox.setValue(1)
        self._ui.final_frame_spinBox.setValue(self.magellan_dataset_dictionary[self.active_magellan]['frames'])

    def remove_channels(self):
        try:
            self._ui.excluded_listWidget.addItem(self._ui.included_listWidget.currentItem().text())
            self._ui.included_listWidget.takeItem(self._ui.included_listWidget.currentRow())
        except Exception:
            print('Select a Channel')
            return

    def return_channels(self):
        try:
            self._ui.included_listWidget.addItem(self._ui.excluded_listWidget.currentItem().text())
            self._ui.excluded_listWidget.takeItem(self._ui.excluded_listWidget.currentRow())
        except Exception:
            print('Select a Channel')
            return

    # Individual functions to get values and error check
    def get_time_values(self):
        time_start = self._ui.first_frame_spinBox.value()
        time_end = self._ui.final_frame_spinBox.value()
        # Make sure time start is less than or equal to time end
        if time_start > time_end:
            self.show_dialog("Time Value")
            return
        else:
            return [time_start, time_end]

    def get_space_values(self):
        x_min_new = int(self._ui.x_min_lineEdit.text())
        x_max_new = int(self._ui.x_max_lineEdit.text())
        if x_min_new > x_max_new:
            self.show_dialog("X Value cropping")
            return

        y_min_new = int(self._ui.y_min_lineEdit.text())
        y_max_new = int(self._ui.y_max_lineEdit.text())
        if y_min_new > y_max_new:
            self.show_dialog("Y Value cropping")
            return
        z_min_new = int(self._ui.z_min_lineEdit.text())
        z_max_new = int(self._ui.z_max_lineEdit.text())
        if z_min_new > z_max_new:
            self.show_dialog("Z Value cropping")
            return

        return [x_min_new, x_max_new, y_min_new, y_max_new, z_min_new, z_max_new]

    def get_channel_values(self):
        file_channel_list = []
        for channels in range(self._ui.included_listWidget.count()):
            temp_index = self._ui.included_listWidget.item(channels).text()
            # Grab just the channel number
            file_channel_list.append(int(temp_index[8]))
        file_channel_list.sort()
        print(file_channel_list)
        if len(file_channel_list) == 0:
            self.show_dialog("Channel subsampling")
            return
        else:
            return file_channel_list

    def generate_file_name(self):
        # File name
        file_path = pathlib.PurePath(self.magellan_dataset_dictionary[self.active_magellan]['directory'])
        file_name = file_path.parts[-1]
        # Time logic and string
        [time_start, time_end] = self.get_time_values()
        if time_start > 1 or time_end < self.magellan_dataset_dictionary[self.active_magellan]['frames']:
            time_name_string = 't' + str(time_start) + 't' + str(time_end) + '_'
        else:
            time_name_string = ''
        print('Time: ' + time_name_string)

        # Space logic and string
        [x_min_new, x_max_new, y_min_new, y_max_new, z_min_new, z_max_new] = self.get_space_values()
        space_name_string = ''
        if x_min_new > 1 or x_max_new < self.magellan_dataset_dictionary[self.active_magellan]['width']:
            space_name_string = space_name_string + 'x' + str(x_min_new) + 'x' + str(x_max_new)
        else:
            space_name_string = space_name_string
        if y_min_new > 1 or y_max_new < self.magellan_dataset_dictionary[self.active_magellan]['height']:
            space_name_string = space_name_string + 'y' + str(y_min_new) + 'y' + str(y_max_new)
        else:
            space_name_string = space_name_string
        if z_min_new > 1 or z_max_new < self.magellan_dataset_dictionary[self.active_magellan]['slices']:
            space_name_string = space_name_string + 'z' + str(z_min_new) + 'z' + str(z_max_new)
        else:
            space_name_string = space_name_string

        if space_name_string != '':
            space_name_string = space_name_string + '_'

        # Channel logic an string
        file_channel_list = self.get_channel_values()
        c_name_string = ''
        if len(file_channel_list) < self.magellan_dataset_dictionary[self.active_magellan]['channels']:
            for c in file_channel_list:
                c_name_string = c_name_string + 'c' + str(c)
        if c_name_string != '':
            c_name_string = c_name_string + '_'

        # Generate final file string
        file_name_string = time_name_string + c_name_string + space_name_string + file_name + '.ims'
        self._ui.save_name_lineEdit.setText(file_name_string)

    def generate_output(self):
        magellan_folder = self.active_magellan
        ims_save_directory = self._ui.save_directory_lineEdit.text()
        file_name = self._ui.save_name_lineEdit.text()
        all_channels_list = self.magellan_dataset_dictionary[self.active_magellan]['channel_names']
        xy_pixel_size = self.magellan_dataset_dictionary[self.active_magellan]['xySize']
        z_voxel_size = self.magellan_dataset_dictionary[self.active_magellan]['zSize']
        [time_start, time_end] = self.get_time_values()
        [x_min_new, x_max_new, y_min_new, y_max_new, z_min_new, z_max_new] = self.get_space_values()
        file_channel_list = self.get_channel_values()
        image_height = self.magellan_dataset_dictionary[self.active_magellan]['single_image_height']
        image_width = self.magellan_dataset_dictionary[self.active_magellan]['single_image_width']
        save_directory = pathlib.PurePath(ims_save_directory, file_name)
        local_output_dictionary = {'magellan_directory': magellan_folder,
                                   'save_directory': save_directory,
                                   'file_name': file_name,
                                   'all_channels': all_channels_list,
                                   'file_channel_list': file_channel_list,
                                   'pixel_size': xy_pixel_size,
                                   'z_size': z_voxel_size,
                                   'time_start': time_start,
                                   'time_end': time_end,
                                   'x_min': x_min_new,
                                   'x_max': x_max_new,
                                   'y_min': y_min_new,
                                   'y_max': y_max_new,
                                   'z_min': z_min_new,
                                   'z_maz': z_max_new,
                                   'single_image_height': image_height,
                                   'single_image_width': image_width
                                   }
        #print(local_output_dictionary['magellan_directory'])
        self._ui.output_listWidget.addItem(str(save_directory))
        
    def show_dialog(self, parameter_string):
        time_msg = QMessageBox()
        time_msg.setIcon(QMessageBox.Warning)
        time_msg.setText(parameter_string + " Warning")
        time_msg.setInformativeText("Please adjust your cropping accordingly.")
        time_msg.setWindowTitle("Parameter Warning")
        time_msg.setStandardButtons(QMessageBox.Ok)
        time_msg.show()
        return_value = time_msg.exec()
        if return_value == QMessageBox.Ok:
            return






