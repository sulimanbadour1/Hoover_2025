import sys
import datetime
import time
import random
from WindowsTemplates import TerminalTemplate, PlotTemplate, ControlTemplate, SettingsInfoTemplate
from DeviceTemplate import DeviceTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg
from math import sin, cos

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self, parent):
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
        
      
class InfoWindow(SettingsInfoTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    @pyqtSlot(dict)
    def receiveData(self, data):
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)

 


class ManageData:

    def __init__():
        pass




"""
applicationAK = QApplication(sys.argv)
window = ControlPanelWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
"""

"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
