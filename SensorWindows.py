import sys
import datetime
import time
import random
from WindowsTemplates import TerminalTemplate, PlotTemplate, ControlTemplate
from DeviceTemplate import DeviceTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg
from math import sin, cos

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Device(DeviceTemplate):
    data_signal =pyqtSignal(tuple)
    end_thread_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(self)   
        self.start_time = 0 #attribute necessary for first 100 ms to collect enough data
        self.current_time = 0
    
    def startDevice(self):
        self.device_running = True

    def stopDevice(self):
        self.device_running = False
        self.measuring_running = False

    @pyqtSlot()
    def measureData(self):
        if self.measuring_running == False:
            self.start_time = time.time()
            self.measuring_running = True
        """
        Function for data receive.
        Function generates signal emiting the tuple 'data'. 
        In case termination of function is required it is necessary to terminate the whole thread (use 'end_thread_signal').
        """
        while self.device_running == True:
            time.sleep(0.05)
            self.current_datetime = datetime.datetime.utcnow()
            self.current_time = time.time()
            duration = self.current_time - self.start_time
            
            """
            #Generating one x, y pair
            x_dec = random.random()
            x_whole = random.randint(0, 3)
            x = x_whole + x_dec
            y_dec = random.random()
            y_whole = random.randint(0, 3)
            y = y_whole + y_dec
            data = (str(self.current_datetime),duration, x, y)
            """
            #Generating multiple x, y pairs
            x_values  = []
            y_values = []
            for i in range (0,5):
                x_dec = random.random()
                x_whole = random.randint(0, 3)
                x = x_whole + x_dec
                y_dec = random.random()
                y_whole = random.randint(0, 3)
                y = y_whole + y_dec
                x_values.append(x)
                y_values.append(y)
            data = ((str(self.current_datetime),duration, x_values, y_values))
            
         
            self.data_signal.emit(data)



class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel - Sensor")
        self.setGeometry(100, 100, 300, 500)
        self.adjustGUI()
        self.device_control = Device(self)
        self.communication_thread = QThread(self)
        self.terminal = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        
        self.connectAdjustedGUI()
        self.createThreadCommunication()
        
    def adjustGUI(self):
        
        """
        Function creates graphical user interface GUI
        """
       
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_measure_button = QPushButton("Measure", self)

        self.start_button.setGeometry(50, 50, 200, 25)
        self.stop_button.setGeometry(50, 100, 200, 25)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.start_measure_button)
        self.setLayout(self.layout)


    
    def connectAdjustedGUI(self):
        """
        Function creates connection between elements in the GUI.
        """
        self.device_control.end_thread_signal.connect(self.reinitializeThread)
        self.start_button.clicked.connect(self.device_control.startDevice)
        self.stop_button.clicked.connect(self.device_control.stopDevice)
        self.device_control.data_signal.connect(self.terminal.receiveData)
        self.device_control.data_signal.connect(self.plot_window.updatePlot)
        self.start_measure_button.clicked.connect(self.device_control.measureData)

    
    def showTerminalWindow(self):
        self.terminal.show()
    
    def showGraphicWindow(self):
        self.plot_window.createPlot()
        self.plot_window.show()


    def createThreadCommunication(self):
        """
        Function moves the object self.device_control into this thread and starts the thread.
        """
        self.device_control.moveToThread(self.communication_thread)
        self.communication_thread.start()
    
    def reinitializeThread(self, state):
        """
        Function terminates the thread and starts it again.
        """
        if state == True:
            self.communication_thread.terminate()
            self.create_thread_communication()
    

            



class TerminalWindow(TerminalTemplate):
    def __init__(self, parent):
        super().__init__(parent)
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
        
      



class ManageData:

    def __init__():
        pass





applicationAK = QApplication(sys.argv)
window = ControlPanelWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop


"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
