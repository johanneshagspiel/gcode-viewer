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
        faces_list = []
        edge_color_list= []

        first = True
        not_skip = True

        for layer in layer_list:
            for x_data, y_data, z_data, color_data in zip(layer.x_data, layer.y_data, layer.z_data, layer.pyqtgraph_color):
                for vertex in zip(x_data, y_data, z_data):
                    if first:
                        first = False
                        vertexes_list.append(vertex)
                        edge_color_list.append(color_data)
                    elif not_skip:
                        not_skip = False
                        vertexes_list.append(vertex)
                        edge_color_list.append(color_data)
                    else:
                        not_skip = True

        from_index = 0
        end = len(vertexes_list)
        for to_index in range(1, end):
            faces_list.append((from_index, to_index, from_index))
            from_index = to_index

        vertexes_array = np.array(vertexes_list)
        faces_array = np.array(faces_list)
        edge_color_array = np.array(edge_color_list[1:])

        meshdata = gl.MeshData(vertexes=vertexes_array, faces=faces_array)
        meshdata.setEdgeColors(edge_color_array)
        mesh = gl.GLMeshItem(meshdata=meshdata, drawFaces=True, drawEdges=True)
        self.viewer.addItem(mesh)
