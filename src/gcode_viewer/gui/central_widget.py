from PyQt5.QtWidgets import QGridLayout, QWidget, QPushButton, QFileDialog
from PyQt5 import QtCore

from gcode_viewer.gcode.layer_parser import Layer_Parser
from gcode_viewer.gui.left_side.left_side import Left_Side
from gcode_viewer.gui.menu_bar.menu_bar import Menu_Bar
from gcode_viewer.gui.right_side.right_side import Right_Side
from gcode_viewer.gui.startup_window.startup_window import Startup_Window
from gcode_viewer.util.file_handler import File_Handler


class Central_Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()
        self.settings = self.file_handler.read_settings()

        self.grid = QGridLayout()

        self.menu_bar = Menu_Bar(self.settings)
        self.grid.addWidget(self.menu_bar, 0, 0, 1, 2)
        self.menu_bar.observer = self

        self.left_side = Left_Side()
        self.grid.addWidget(self.left_side, 1, 0)

        self.right_side = Right_Side()
        self.grid.addWidget(self.right_side, 1, 1)

        bottom_grid = QGridLayout()
        self.grid.addLayout(bottom_grid, 2, 0, 1, 2)

        self.load_file_button = QPushButton("Load Different GCode File")
        bottom_grid.addWidget(self.load_file_button, 0, 1)
        self.load_file_button.clicked.connect(self.get_path_to_file)

        bottom_grid.setColumnStretch(0, 1)
        bottom_grid.setColumnStretch(2, 1)

        self.setLayout(self.grid)

    def start(self):
        test = Startup_Window()
        file_path = test.get_initial_file_path()

        if file_path:
            self.load_gcode_file(file_path)

    def get_path_to_file(self):
        file_path, _ = QFileDialog(self).getOpenFileName(caption="Select A GCode File That You Want To Load",
                                                      filter="GCode (*.gcode)", initialFilter="GCode (*.gcode)")

        if file_path:
            self.load_gcode_file(file_path)

    def load_gcode_file(self, file_path):

        line_list = self.file_handler.read_gcode_file(file_path)
        temp_layer_parser = Layer_Parser()
        layer_list = temp_layer_parser.parse_layer_list(line_list)

        self.load_new_file_on_screen(layer_list)

    def load_new_file_on_screen(self, layer_list):
        self.right_side.load_new_gcode(layer_list)
        self.right_side.gcode_loaded = True

        self.left_side.gcode_3d_viewer.load_gcode(layer_list)

    def update(self, type, par1, par2 = None):

        if type == "new_settings":
            new_settings = par1

            self.settings = new_settings
            #self.left_side.settings = new_settings
            self.menu_bar.settings = new_settings

            self.file_handler.settings_to_file(self.settings)
