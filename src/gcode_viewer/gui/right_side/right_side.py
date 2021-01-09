from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel,  QWidget,  QPushButton

from gcode_viewer.gui.gcode_layer_viewer.gcode_layer_viewer_animated import GCode_Layer_Viewer_Animated
from gcode_viewer.gui.gcode_layer_viewer.gcode_layer_viewer_static import GCode_Layer_Viewer_Static


class Right_Side(QWidget):

    def __init__(self):
        super().__init__()

        self.gcode_loaded = False
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 1)

        self.layer_list = None
        self.row_position = 0
        self.current_layer = 0
        self.max_layer = 0
        self.animation = False

        top_label = QLabel("2D Viewer")
        self.grid.addWidget(top_label, self.row_position, 0, 1, 2)
        top_label.setAlignment(Qt.AlignCenter)
        self.row_position += 1

        self.gcode_layer_viewer = GCode_Layer_Viewer_Animated()
        self.gcode_layer_viewer.setHidden(True)
        self.grid.addWidget(self.gcode_layer_viewer, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.gcode_layer_viewer_static = GCode_Layer_Viewer_Static()
        self.grid.addWidget(self.gcode_layer_viewer_static, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.current_layer_label = QLabel("Current Layer: " + str(self.current_layer) + "/" + str(self.max_layer))
        self.grid.addWidget(self.current_layer_label, self.row_position, 0, 1 ,2)
        self.row_position += 1

        self.previous_layer_button = QPushButton("Previous layer")
        self.previous_layer_button.clicked.connect(lambda: self.load_layer(-1))
        self.grid.addWidget(self.previous_layer_button, self.row_position, 0)

        self.next_layer_button = QPushButton("Next layer")
        self.next_layer_button.clicked.connect(lambda: self.load_layer(1))
        self.grid.addWidget(self.next_layer_button, self.row_position, 1)
        self.row_position += 1

        self.turn_on_off_button = QPushButton("Turn Animation On")
        self.turn_on_off_button.clicked.connect(lambda: self.turn_on_off_animation(self.turn_on_off_button.text()))
        self.grid.addWidget(self.turn_on_off_button, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.show_3d_button = QPushButton("Show 3D Animation")
        #self.show_3d_button.clicked.connect(self.show_3d_animation)
        self.grid.addWidget(self.show_3d_button, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.setLayout(self.grid)

    def turn_on_off_animation(self, text):
        if self.gcode_loaded:
            if text == "Turn Animation On":
                self.turn_on_off_button.setText("Turn Animation Off")
                self.animation = True
                self.gcode_layer_viewer.setHidden(False)
                self.gcode_layer_viewer_static.setHidden(True)
                self.gcode_layer_viewer.set_layer_list(self.layer_list)
                self.gcode_layer_viewer.load_layer(self.current_layer)

            if text == "Turn Animation Off":
                self.turn_on_off_button.setText("Turn Animation On")
                self.animation = False
                self.gcode_layer_viewer_static.setHidden(False)
                self.gcode_layer_viewer.setHidden(True)
                self.gcode_layer_viewer_static.layer_list(self.layer_list)
                self.gcode_layer_viewer_static.load_layer(self.current_layer)

    def load_new_gcode(self, layer_list):
        self.current_layer = 0
        self.layer_list = layer_list
        self.max_layer = len(layer_list)
        if self.animation:
            self.gcode_layer_viewer.set_layer_list(layer_list)
        else:
            self.gcode_layer_viewer_static.set_layer_list(layer_list)
        self.update_labels()

    def load_layer(self, index):
        if self.gcode_loaded:
            if index == 1 and self.current_layer == (self.max_layer-1):
                self.current_layer = 0
            elif index == -1 and self.current_layer == 0:
                self.current_layer = self.max_layer-1
            else:
                self.current_layer += index

            if self.animation:
                self.gcode_layer_viewer.load_layer(self.current_layer)
            else:
                self.gcode_layer_viewer_static.load_layer(self.current_layer)
            self.update_labels()

    def update_labels(self):
        new_label_text = "Current Layer: " + str(self.current_layer + 1) + "/" + str(self.max_layer)
        self.current_layer_label.setText(new_label_text)
