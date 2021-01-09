from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5 import QtGui

from gcode_viewer.util.file_handler import File_Handler
from gcode_viewer.util.mapper_util import Mapper_Util


class Change_Environment_Window(QDialog):

    def __init__(self, settings = None):
        super().__init__()
        self.settings = settings

        self.initUI()

    def initUI(self):
        self.diameter_chosen = 0
        self.entries_to_check = []

        file_handler = File_Handler()

        self.setWindowTitle("Environment Change")
        self.setWindowIcon(QtGui.QIcon(str(file_handler.icon_png_path)))

        self.setWindowFlags(Qt.WindowFlags())

        grid = QGridLayout()

        top_label = QLabel("What do you want to change in the settings?")
        top_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(top_label, 0, 0, 1, 6)

        environment_label = QLabel("Printer Dimensions")
        environment_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(environment_label, 1, 0, 1, 3)

        printer_width_x_label = QLabel("Print Bed Width (X)")
        grid.addWidget(printer_width_x_label, 2, 0)

        self.printer_width_x_entry = QLineEdit()
        grid.addWidget(self.printer_width_x_entry, 2, 1)
        self.entries_to_check.append(self.printer_width_x_entry)

        printer_depth_y_label = QLabel("Print Bed Depth (Y)")
        grid.addWidget(printer_depth_y_label, 3, 0)

        self.printer_depth_y_entry = QLineEdit()
        grid.addWidget(self.printer_depth_y_entry, 3, 1)
        self.entries_to_check.append(self.printer_depth_y_entry)

        printer_height_z_label = QLabel("Printer Height (Z)")
        grid.addWidget(printer_height_z_label, 4, 0)

        self.printer_height_z_entry = QLineEdit()
        grid.addWidget(self.printer_height_z_entry, 4, 1)
        self.entries_to_check.append(self.printer_height_z_entry)

        sponge_label = QLabel("Sponge Dimensions")
        sponge_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(sponge_label, 1, 3, 1, 3)

        sponge_width_x_label = QLabel("Sponge Width (X)")
        grid.addWidget(sponge_width_x_label, 2, 3)

        self.sponge_width_x_entry = QLineEdit()
        grid.addWidget(self.sponge_width_x_entry, 2, 4)
        self.entries_to_check.append(self.sponge_width_x_entry)

        sponge_depth_y_label = QLabel("Sponge Depth (Y)")
        grid.addWidget(sponge_depth_y_label, 3, 3)

        self.sponge_depth_y_entry = QLineEdit()
        grid.addWidget(self.sponge_depth_y_entry, 3, 4)
        self.entries_to_check.append(self.sponge_depth_y_entry)

        sponge_height_z_label = QLabel("Sponge Height (Z)")
        grid.addWidget(sponge_height_z_label, 4, 3)

        self.sponge_height_z_entry = QLineEdit()
        grid.addWidget(self.sponge_height_z_entry, 4, 4)
        self.entries_to_check.append(self.sponge_height_z_entry)

        for row_printer_dimension in range(2, 5):
            mm_label = QLabel("mm")
            grid.addWidget(mm_label, row_printer_dimension, 2)

        for row_sponge_dimension in range(2, 5):
            mm_label = QLabel("mm")
            grid.addWidget(mm_label, row_sponge_dimension, 5)

        for entry in self.entries_to_check:
            entry.setMaximumWidth(36)
            entry.setAlignment(Qt.AlignCenter)

        accept_button = QPushButton("Accept")
        grid.addWidget(accept_button, 5, 1, 1, 3)
        accept_button.clicked.connect(self.accept_pressed)

        self.setLayout(grid)

        if self.settings != None:
            self.printer_width_x_entry.setText(str(self.settings.environment.printer.bed_width_x))
            self.printer_depth_y_entry.setText(str(self.settings.environment.printer.bed_depth_y))
            self.printer_height_z_entry.setText(str(self.settings.environment.printer.height_z))

            self.sponge_width_x_entry.setText(str(self.settings.environment.sponge.width_x))
            self.sponge_depth_y_entry.setText(str(self.settings.environment.sponge.depth_y))
            self.sponge_height_z_entry.setText(str(self.settings.environment.sponge.height_z))

    def accept_pressed(self):

        if self.sanity_check():

            entries_as_float= list(map(lambda x: float(x.text()), self.entries_to_check))
            new_settings = Mapper_Util.float_to_settings(entries_as_float)

            self.set_settings(new_settings)

    def sanity_check(self):
        mistake = False

        for entry in self.entries_to_check:
            try:
                float_input = float(entry.text())
                if float_input < 0.0 or float_input > 1000.0:
                    raise Exception
            except Exception:
                mistake = True
                entry.setText("")

        if mistake:
            error_text = "All inputs need to be a real number between 0 and 100"
            error_message_box = QMessageBox()
            error_message_box.setText(error_text)
            error_message_box.setWindowTitle("Input Error")
            error_message_box.setIcon(QMessageBox.Warning)
            error_message_box.exec_()
            return False

        return True

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.close()

    @staticmethod
    def change_environment(settings):
        change_environment_window = Change_Environment_Window(settings)
        change_environment_window.exec_()
        return change_environment_window.settings
