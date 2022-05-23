
class Layer():

    def __init__(self):
        self.number = None

        self.layer_as_string = []

        self.move_data = []
        self.x_data = []
        self.y_data = []
        self.z_data = []

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.pyqtgraph_color = []
        self.matplot_color = []

        self.largest_extrusion_value = 0