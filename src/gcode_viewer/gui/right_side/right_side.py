from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel,  QWidget,  QPushButton

from gcode_viewer.gui.gcode_console.gcode_console import GCode_Console
from gcode_viewer.gui.gcode_layer_viewer.gcode_layer_viewer_animated import GCode_Layer_Viewer_Animated
from gcode_viewer.gui.gcode_layer_viewer.gcode_layer_viewer_static import GCode_Layer_Viewer_Static


class Right_Side(QWidget):

    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.gcode_loaded = False
        self.layer_list = None
        self.row_position = 0
        self.current_layer = 0
        self.max_layer = 0
        self.animation = False

        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 1)

        # gcode_consol_label = QLabel("GCode Console")
        # self.grid.addWidget(gcode_consol_label, self.row_position, 0)
        # gcode_consol_label.setAlignment(Qt.AlignCenter)

        viewer_2D_label = QLabel("2D Viewer")
        self.grid.addWidget(viewer_2D_label, self.row_position, 1)
        viewer_2D_label.setAlignment(Qt.AlignCenter)
        self.row_position += 1

        # self.gcode_console = GCode_Console()
        # self.grid.addWidget(self.gcode_console, self.row_position, 0)
        # self.gcode_console.setMaximumWidth(200)

        self.gcode_layer_viewer_animated = GCode_Layer_Viewer_Animated(self.settings)
        self.gcode_layer_viewer_animated.setHidden(True)
        self.grid.addWidget(self.gcode_layer_viewer_animated, self.row_position, 1)
        self.row_position += 1

        self.gcode_layer_viewer_static = GCode_Layer_Viewer_Static(self.settings)
        self.grid.addWidget(self.gcode_layer_viewer_static, self.row_position, 1)
        self.row_position += 1

        labels_grid = QGridLayout()
        self.grid.addLayout(labels_grid, self.row_position, 0, 1 ,2)
        self.row_position += 1

        self.current_layer_label = QLabel("Current Layer: " + str(self.current_layer) + "/" + str(self.max_layer))
        labels_grid.addWidget(self.current_layer_label, 0, 0, 1 ,2)

        self.previous_layer_button = QPushButton("Previous layer")
        self.previous_layer_button.clicked.connect(lambda: self.load_layer(-1))
        labels_grid.addWidget(self.previous_layer_button, 1, 0)

        self.next_layer_button = QPushButton("Next layer")
        self.next_layer_button.clicked.connect(lambda: self.load_layer(1))
        labels_grid.addWidget(self.next_layer_button, 1, 1)

        self.turn_on_off_button = QPushButton("Turn Animation On")
        self.turn_on_off_button.clicked.connect(lambda: self.turn_on_off_animation(self.turn_on_off_button.text()))
        labels_grid.addWidget(self.turn_on_off_button, 2, 0, 1, 2)

        self.zoom_in_out_button = QPushButton("Zoom In")
        self.zoom_in_out_button.clicked.connect(lambda: self.zoom_in_out(self.zoom_in_out_button.text()))
        labels_grid.addWidget(self.zoom_in_out_button, 3, 0, 1, 2)

        self.setLayout(self.grid)

    def zoom_in_out(self, text):
        if self.gcode_loaded:
            if text == "Zoom In":
                self.zoom_in_out_button.setText("Zoom Out")
                self.gcode_layer_viewer_static.zoomed_in = True
                self.gcode_layer_viewer_animated.zoomed_in = True
            if text == "Zoom Out":
                self.zoom_in_out_button.setText("Zoom In")
                self.gcode_layer_viewer_static.zoomed_in = False
                self.gcode_layer_viewer_animated.zoomed_in = False
            self.refresh_gcode_viewer()

    def turn_on_off_animation(self, text):
        if self.gcode_loaded:
            if text == "Turn Animation On":
                self.turn_on_off_button.setText("Turn Animation Off")
                self.animation = True
                self.gcode_layer_viewer_animated.setHidden(False)
                self.gcode_layer_viewer_static.setHidden(True)
                #self.gcode_layer_viewer_animated.set_layer_list(self.layer_list)
                self.gcode_layer_viewer_animated.load_layer(self.current_layer)
            if text == "Turn Animation Off":
                self.turn_on_off_button.setText("Turn Animation On")
                self.animation = False
                self.gcode_layer_viewer_static.setHidden(False)
                self.gcode_layer_viewer_animated.setHidden(True)
                #self.gcode_layer_viewer_static.layer_list(self.layer_list)
                self.gcode_layer_viewer_static.load_layer(self.current_layer)

    def load_new_gcode(self, layer_list):
        self.current_layer = 0
        self.layer_list = layer_list
        self.max_layer = len(layer_list)
        self.gcode_layer_viewer_animated.set_layer_list(layer_list)
        self.gcode_layer_viewer_static.set_layer_list(layer_list)
        self.update_labels()
        self.refresh_gcode_viewer()

    def load_layer(self, index):
        if self.gcode_loaded:
            if index == 1 and self.current_layer == (self.max_layer-1):
                self.current_layer = 0
            elif index == -1 and self.current_layer == 0:
                self.current_layer = self.max_layer-1
            else:
                self.current_layer += index

            if self.animation:
                self.gcode_layer_viewer_animated.load_layer(self.current_layer)
            else:
                self.gcode_layer_viewer_static.load_layer(self.current_layer)
            self.update_labels()

    def update_labels(self):
        new_label_text = "Current Layer: " + str(self.current_layer + 1) + "/" + str(self.max_layer)
        self.current_layer_label.setText(new_label_text)

    def refresh_gcode_viewer(self):
        if self.animation:
            self.gcode_layer_viewer_animated.load_layer(self.current_layer)
        else:
            self.gcode_layer_viewer_static.load_layer(self.current_layer)
