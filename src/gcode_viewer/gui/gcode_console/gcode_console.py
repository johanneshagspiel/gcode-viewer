from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit

class GCode_Console(QWidget):

    def __init__(self):
        super().__init__()

        self.layer_list = None
        self.layer = None
        self.overall_x = None
        self.overall_y = None
        self.overall_color = None
        self.max_iteration = 0
        self.current_iteration = 2
        self.zoomed_in = False

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.test = QTextEdit("Test")
        self.grid.addWidget(self.test, 0, 0)
        self.test.setReadOnly(True)

        self.setLayout(self.grid)