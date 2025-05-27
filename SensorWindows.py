import sys
import datetime
import time
import random
from WindowsTemplates import TerminalTemplate, PlotTemplate, ControlTemplate, InfoWindowTemplate, DeviceWindowTemplate
from device_interfaces.SensorInterface import Device
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg
from math import sin, cos
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SensorWindow(DeviceWindowTemplate):

    def __init__(self, parent = None):
        super().__init__()
        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.info_window = InfoWindow(self)
        self.device_interface = Device(self)
        self.device_thread = QThread(self)
        self.createGUI()
        self.connectGUI()
        self.createThreadCommunication()

    def createGUI(self):
        return super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()
    
    def connectElements(self):

        #Connecting buttons to functions
        self.control_window.start_button.clicked.connect(self.device_interface.startDevice)
        self.control_window.stop_button.clicked.connect(self.device_interface.stopDevice)
        self.control_window.start_measure_button.clicked.connect(self.device_interface.measureData)
        self.device_info.triggered.connect(self.device_interface.getDeviceInfo)

        #Connecting signals from device control to functions (slots)
        self.device_interface.data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.data_signal.connect(self.plot_window.updatePlot)
        self.device_interface.info_signal.connect(self.info_window.receiveData)
        self.device_interface.message_signal.connect(self.setStatusBarText)

class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.createGUI()

        
    def createGUI(self):
        
        """
        Function creates graphical user interface GUI
        """
        #properties of ControlPanelWindow
        self.setWindowTitle("Control Panel - Sensor")
        self.setGeometry(100, 100, 300, 500)
        self.sizeIncrement()
        
        #Creating elements of ControlPanelWindow
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_measure_button = QPushButton("Measure", self)

        self.start_button.setMinimumSize(100, 25)
        self.start_button.move(10, 50)

        self.stop_button.setMinimumSize(100, 25)
        self.stop_button.move(10, 100)
        self.start_measure_button.setMinimumSize(100, 25)
        self.start_measure_button.move(10, 150)
        """
        self.start_button.sizeIncrement()
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stop_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.start_measure_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)"""

        
        self.layout = QVBoxLayout()
        #self.layout.addStretch()
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.start_measure_button)
        #self.layout.addStretch()
        #self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.hide()

 



            



class TerminalWindow(TerminalTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()
        """    
        self.setWindowTitle("Terminal")
        self.setGeometry(100, 650, 800, 300)
        self.createGUI()"""
    """
    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)
    """
    @pyqtSlot(tuple)
    def receiveData(self, data):
        current_time = data[0]
        x = str(data[2])
        y = str(data[3])
        self.output_box.insertPlainText("Time: " + current_time + " x: " + x + " y: " + y + "\n")




class PlotWindow(PlotTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.x_values = [0]
        self.y_values = [0]
        self.createGUI()
    
    @pyqtSlot(tuple)
    def updatePlot(self, data):
        
        """
     
        #Multiple pairs of value received
        self.x_values = data[2]
        self.y_values = data[3]
        self.graph_scatter.clear()
        self.center_point = self.center_scatter.addPoints([0], [0])
        self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values) 
        """

                                                      
        """
        #One paired value received
        self.x_values.append(data[2])
        self.y_values.append(data[3])
        duration = data[1]
        
        if duration > 0.5:
            self.x_values = self.x_values[1:]
            self.y_values = self.y_values[1:]
            self.graph_scatter.clear()
            self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values )
        """

        i = 0
        #Multiple pairs of value received
        self.x_values = [0]
        self.y_values = [0]
        for item in data[2]:
            x = cos(data[2][i]) * data[3][i]
            y = sin(data[2][i]) * data[3][i]
            self.x_values.append(x)
            self.y_values.append(y)
            i+=1
        self.graph_scatter.clear()
        #self.center_point = self.center_scatter.addPoints([0], [0])
        
        self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values )
        
      
class InfoWindow(InfoWindowTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    @pyqtSlot(dict)
    def receiveData(self, data):
         self.clearOutputBox()
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)

 


class ManageData:

    def __init__():
        pass




""" 
applicationAK = QApplication(sys.argv)
window = SensorWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop

 """
"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
