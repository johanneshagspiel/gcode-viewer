import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np

class GCode_3D_Viewer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)

        self.viewer.setWindowTitle('STL Viewer')
        self.viewer.setCameraPosition(distance=250)

        g = gl.GLGridItem()
        g.setSize(200, 200)
        g.setSpacing(5, 5)
        self.viewer.addItem(g)

    def show_gcode(self, filename):

        points, faces = self.loadSTL(filename)
        meshdata = gl.MeshData(vertexes=points, faces=faces)
        mesh = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        self.viewer.addItem(mesh)

        self.currentSTL = mesh

    def load_gcode(self, layer_list):

        vertexes_list = []
        edges_list = []
        first = True
        not_skip = True

        for layer in layer_list:
            for x_data, y_data, z_data in zip(layer.x_data, layer.y_data, layer.z_data):
                for vertex in zip(x_data, y_data, z_data):
                    if first:
                        first = False
                        vertexes_list.append(vertex)
                    elif not_skip:
                        not_skip = False
                        vertexes_list.append(vertex)
                    else:
                        not_skip = True

        from_index = 0
        end = len(vertexes_list)
        for to_index in range(1, end):
            edges_list.append((from_index, to_index, from_index))
            from_index = to_index

        vertexes_array = np.array(vertexes_list)
        edges_array = np.array(edges_list)

        meshdata = gl.MeshData(vertexes=vertexes_array, faces=edges_array)
        mesh = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        self.viewer.addItem(mesh)

        # m = mesh.Mesh.from_file(filename)
        # shape = m.points.shape
        # points = m.points.reshape(-1, 3)
        # faces = np.arange(points.shape[0]).reshape(-1, 3)
        # return points, faces