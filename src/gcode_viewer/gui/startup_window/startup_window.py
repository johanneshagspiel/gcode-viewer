from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog

from gcode_viewer.util.file_handler import File_Handler


class Startup_Window(QWidget):

    def __init__(self):
        super().__init__()
        file_handler = File_Handler()
        self.setWindowIcon(QtGui.QIcon(str(file_handler.icon_png_path)))

    def get_initial_file_path(self):
        file_path, _ = QFileDialog(self).getOpenFileName(caption="Select A GCode File That You Want To Load",
                                                         filter="GCode (*.gcode)", initialFilter="GCode (*.gcode)")

        return file_path
