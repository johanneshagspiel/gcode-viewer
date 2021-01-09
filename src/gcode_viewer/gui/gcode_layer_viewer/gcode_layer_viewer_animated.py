from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from gcode_viewer.gui.gcode_layer_viewer.gcode_canvas import GCode_Canvas


class GCode_Layer_Viewer_Animated(QWidget):

    def __init__(self):
        super().__init__()

        self.layer_list = None
        self.layer = None
        self.overall_x = None
        self.overall_y = None
        self.overall_color = None
        self.max_iteration = 0
        self.current_iteration = 2

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.grid.addWidget(self.canvas, 0, 0)

        self.current_move_label = QLabel()
        self.grid.addWidget(self.current_move_label, 1, 0)

        self.setLayout(self.grid)

    def set_layer_list(self, layer_list):
        self.layer_list = layer_list
        self.load_layer(0)

    def load_layer(self, index):
        self.layer = self.layer_list[index]
        self.overall_x = self.layer.x_data
        self.overall_y = self.layer.y_data
        self.overall_color = self.layer.color_data
        self.overall_move = self.layer.move_data

        self.max_iteration = len(self.layer.x_data)
        self.current_iteration = 2

        self.start_showing_animation()

    def start_showing_animation(self):
        self.xdata = self.overall_x[0]
        self.ydata = self.overall_y[0]
        self.colordata = self.overall_color[0]

        self.canvas.axes.cla()
        self.canvas.axes.set_xlim(0, 220)
        self.canvas.axes.set_ylim(0, 220)
        self.canvas.axes.plot(self.xdata, self.ydata, self.colordata)
        self.canvas.draw()
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def update_plot(self):

        self.xdata = self.overall_x[:self.current_iteration]
        self.ydata = self.overall_y[:self.current_iteration]
        self.colordata = self.overall_color[:self.current_iteration]

        self.canvas.axes.cla()
        # self.canvas.axes.set_xlim(0, 220)
        # self.canvas.axes.set_ylim(0, 220)

        for x, y, color in zip(self.xdata, self.ydata, self.colordata):
            self.canvas.axes.plot(x, y, color)

        self.canvas.draw()
        self.current_move_label.setText(str(self.overall_move[self.current_iteration]))

        self.current_iteration += 1

        if self.current_iteration == self.max_iteration:
            self.current_iteration = 2

        self.canvas.draw()
