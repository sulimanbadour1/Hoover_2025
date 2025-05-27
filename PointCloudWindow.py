#Script contains window for pointcloud visualisation 
from WindowsTemplates import PlotTemplate
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QObject
from PyQt5.QtGui import QVector3D
import pyqtgraph.opengl as gl
import numpy as np
import sys

class PointCloudWindow(PlotTemplate):
    data_signal = pyqtSignal(np.ndarray) 

    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Point Cloud Window")
        self.camera_running = False
        self.setGeometry(700, 100, 640, 480)
        self.createGUI()
        self.show()
        self.data_signal.connect(self.receiveData)
        self.data_flow = True

    def createGUI(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.createPlot()
        self.layout.addWidget(self.pt_cld_graph)

    def createPlot(self):
        self.pt_cld_graph = gl.GLViewWidget()
        self.pt_cld_scatter = gl.GLScatterPlotItem()

        #Creating view point 
        self.position = QVector3D(0, 0, 0)
        self.pt_cld_graph.setCameraPosition(pos = self.position, elevation=28, azimuth=180 )

        #Creating axis of the graph
        self.x_axis = gl.GLAxisItem()
        self.y_axis = gl.GLAxisItem()
        self.z_axis = gl.GLAxisItem()
        
        #Adding plot elements to plot
        self.pt_cld_graph.addItem(self.x_axis)
        self.pt_cld_graph.addItem(self.y_axis)
        self.pt_cld_graph.addItem(self.z_axis)
        self.pt_cld_graph.addItem(self.pt_cld_scatter)

        self.pt_cld_graph.show()

   
    
    @pyqtSlot(np.ndarray)
    def receiveData(self, data):
        """
        Function receives data and plots them.

        parameters:
        data (numpy object (N, 3)) - point cloud of data
        """
            
        if self.data_flow == True:
            clr = np.array([[1.0, 0.0, 1.0, 1.0]] * len(data))
            self.pt_cld_scatter.setData(pos = data, size = 5, color = clr)
            self.pt_cld_scatter.setGLOptions('translucent')

    @pyqtSlot(dict)
    def setDataFlow(self, flow_settings):
        """
        Function controls data_flow to the plot. 
        It receives data from signal of DataFlowWindow.

        """
        
        self.data_flow = flow_settings["point cloud"]

"""     
def create_data():
     points = np.random.normal(
                loc=0.0, scale=1.0, size=(100000, 3)) 
     
     print (type(points))
     print(points)
    
     
     return points """


#create_data()
""" applicationAK = QApplication(sys.argv)
window = PointCloudWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop
points = create_data()
window.data_signal.emit(points) """

"""
Sources:

https://pyqtgraph.readthedocs.io/en/latest/getting_started/3dgraphics.html


"""