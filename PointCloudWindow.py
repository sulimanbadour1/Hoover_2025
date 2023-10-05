#Script contains window for pointcloud visualisation 
from WindowsTemplates import PlotTemplate
from PyQt5.QtWidgets import *
from PyQt5.Qt import pyqtSlot
import pyqtgraph.opengl as gl
import numpy as np

class PointCloudWindow(PlotTemplate):

    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Point Cloud Window")
        self.camera_running = False
        self.setGeometry(700, 100, 640, 480)
        self.createGUI()

    def createGUI(self):
        self.layout = QVBoxLayout(self)
        self.createPlot()
        self.layout.addWidget(self.pt_cld_graph)

    def createPlot(self):
        self.pt_cld_graph = gl.GLViewWidget(self)
        self.pt_cld_scatter = gl.GLScatterPlotItem()

        #Creating axis of the graph
        self.x_axis = gl.GLAxisItem()
        self.y_axis = gl.GLAxisItem()
        self.z_axis = gl.GLAxisItem()
        
        #Adding axis to plot
        self.pt_cld_graph.addItem(self.x_axis)
        self.pt_cld_graph.addItem(self.y_axis)
        self.pt_cld_graph.addItem(self.z_axis)

        self.pt_cld_graph.show()

   
    
    @pyqtSlot(np.ndarray)
    def receiveDepthData(self, data):
        """
        Function receives data and plots them.

        parameters:
        data (numpy object (N, 3)) - point cloud of data
        """
            
        if self.data_flow == True:

            self.plt_cld_graph.clear()
            self.pt_cld_scatter.setData(pos = data, size = 2)

    @pyqtSlot(dict)
    def setDataFlow(self, flow_settings):
        """
        Function controls data_flow to the plot. 
        It receives data from signal of DataFlowWindow.

        """
        
        self.data_flow = flow_settings["point cloud"]




"""
Sources:

https://pyqtgraph.readthedocs.io/en/latest/getting_started/3dgraphics.html


"""