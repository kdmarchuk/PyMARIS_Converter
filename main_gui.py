from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox, QGraphicsRectItem, QFileDialog
#from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QCoreApplication
#from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pygellan.magellan_data import MagellanDataset
import pathlib
#import pyqtgraph as pg

from PyMARIS_Converter_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.magellan_dataset_dictionary = {}

        # Connections start now
        self._ui.load_magellan_pushButton.clicked.connect(self.get_working_directory)
        self._ui.remove_pushButton.clicked.connect(self.remove_working_directory)
        self._ui.magellan_dataset_listWidget.itemClicked.connect(self.refresh_gui)
        self._ui.browse_pushButton.clicked.connect(self.set_save_directory)
        self._ui.reset_time_pushButton.clicked.connect(self.refresh_time)
        self._ui.reset_space_pushButton.clicked.connect(self.refresh_space)

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
        print(magellan_directory_path)
        self._ui.magellan_dataset_listWidget.addItem(magellan_directory_str)
        self.store_magellan_metadata(magellan_directory_str)
        print(self.magellan_dataset_dictionary[magellan_directory_str]["positions"])

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
        num_channels = len(magellan.summary_metadata['ChNames'])
        channel_names = magellan.summary_metadata['ChNames']
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
        active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()

        # Save Directory entry
        self._ui.save_directory_lineEdit.setText(active_magellan)

        # Channels tab
        num_channels = self.magellan_dataset_dictionary[active_magellan]['channels']
        for c in range(num_channels):
            temp_channel_list = self.magellan_dataset_dictionary[active_magellan]['channel_names']
            temp_channel_name = temp_channel_list[c]
            self._ui.included_listWidget.addItem('Channel ' + str(c) + ': ' + temp_channel_name)

        # Space tab
        self._ui.x_min_lineEdit.setText(str(1))
        self._ui.x_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['width']))
        self._ui.y_min_lineEdit.setText(str(1))
        self._ui.y_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['height']))
        self._ui.z_min_lineEdit.setText(str(1))
        self._ui.z_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['slices']))

        # Time tab
        self._ui.first_frame_spinBox.setValue(1)
        self._ui.final_frame_spinBox.setValue(self.magellan_dataset_dictionary[active_magellan]['frames'])

        # file name
        file_path = pathlib.PurePath(self.magellan_dataset_dictionary[active_magellan]['directory'])
        file_name = file_path.parts[-1]
        self._ui.save_name_lineEdit.setText(file_name)

    def refresh_space(self):
        # Get highlighted entry
        active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()
        self._ui.x_min_lineEdit.setText(str(1))
        self._ui.x_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['width']))
        self._ui.y_min_lineEdit.setText(str(1))
        self._ui.y_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['height']))
        self._ui.z_min_lineEdit.setText(str(1))
        self._ui.z_max_lineEdit.setText(str(self.magellan_dataset_dictionary[active_magellan]['slices']))

    def refresh_time(self):
        # Get highlighted entry
        active_magellan = self._ui.magellan_dataset_listWidget.currentItem().text()
        self._ui.first_frame_spinBox.setValue(1)
        self._ui.final_frame_spinBox.setValue(self.magellan_dataset_dictionary[active_magellan]['frames'])






