from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from gcode_viewer.gui.gcode_layer_viewer.gcode_canvas import GCode_Canvas


class GCode_Layer_Viewer_Animated(QWidget):

    def __init__(self, settings):
        super().__init__()

        self.layer_list = None
        self.layer = None
        self.overall_x = None
        self.overall_y = None
        self.overall_color = None
        self.max_iteration = 0
        self.current_iteration = 2
        self.zoomed_in = False
        self.settings = settings

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.grid.addWidget(self.canvas, 0, 0)

        self.setLayout(self.grid)

    def set_layer_list(self, layer_list):
        self.layer_list = layer_list

    def load_layer(self, index):
        self.layer = self.layer_list[index]
        self.overall_x = self.layer.x_data
        self.overall_y = self.layer.y_data
        self.overall_color = self.layer.matplot_color
        self.overall_move = self.layer.move_data

        self.max_iteration = len(self.layer.x_data)
        self.current_iteration = 2

        self.start_showing_animation()

    def start_showing_animation(self):
        self.xdata = self.overall_x[:1]
        self.ydata = self.overall_y[:1]
        self.colordata = self.overall_color[:1]

        self.canvas.axes.cla()
        self.set_limits()
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
        self.set_limits()

        for x, y, color in zip(self.xdata, self.ydata, self.colordata):
            self.canvas.axes.plot(x, y, color)

        self.canvas.draw()

        self.current_iteration += 1

        if self.current_iteration == self.max_iteration:
            self.current_iteration = 2

        self.canvas.draw()

    def set_limits(self):

        if self.zoomed_in:
            self.canvas.axes.set_xlim(self.layer.min_x, self.layer.max_x)
            self.canvas.axes.set_ylim(self.layer.min_y, self.layer.max_y)
        else:
            self.canvas.axes.set_xlim(0, self.settings.environment.printer.bed_width_x)
            self.canvas.axes.set_ylim(0, self.settings.environment.printer.bed_depth_y)
