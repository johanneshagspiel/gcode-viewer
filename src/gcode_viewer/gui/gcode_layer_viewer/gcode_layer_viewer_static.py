from PyQt5.QtWidgets import QWidget, QGridLayout

from gcode_viewer.gui.gcode_layer_viewer.gcode_canvas import GCode_Canvas


class GCode_Layer_Viewer_Static(QWidget):

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

    def set_layer_list(self, layer_list):
        self.layer_list = layer_list
        self.load_layer(0)

    def load_layer(self, index):
        self.layer = self.layer_list[index]
        self.overall_x = self.layer.x_data

        self.overall_y = self.layer.y_data
        self.overall_color = self.layer.color_data

        self.max_iteration = len(self.layer.x_data)
        self.current_iteration = 2

        self.start_showing_static()

    def initUI(self):
        self.grid = QGridLayout()
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.grid.addWidget(self.canvas, 0, 0)
        self.setLayout(self.grid)

    def start_showing_static(self):
        self.xdata = self.overall_x
        self.ydata = self.overall_y
        self.colordata = self.overall_color

        self.canvas.axes.cla()
        # self.canvas.axes.set_xlim(0, 220)
        # self.canvas.axes.set_ylim(0, 220)

        for x, y, color in zip(self.xdata, self.ydata, self.colordata):
            self.canvas.axes.plot(x, y, color)

        self.canvas.draw()
        self.show()
