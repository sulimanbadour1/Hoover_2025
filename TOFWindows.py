import sys
import time
from math import sin, cos
from DeviceTemplate import DeviceTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from TOFLibrary import TOFController, TOFControllerException
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg

class Device(DeviceTemplate):
    data_signal =pyqtSignal(float)
    info_signal = pyqtSignal(str)
    end_thread_signal = pyqtSignal(bool)

    def __init__(self, port):
        super().__init__(self)
        self.port = port
        self.device = TOFController(self.port)
        self.data_state = True
    
    def startDevice(self):
        try:
            self.device.start_controller()
            self.device_started = True
        except TOFControllerException:
            print("TOFControllerException: Device already started.")

    def stopDevice(self):
        try:
            self.end_thread_signal.emit(True) #signal to get out of the thread in case the measure_data function has been called
            self.device.stop_controller()
            self.device_started = False
        except TOFControllerException:
            print("TOFController Exception: Device already stopped.")

    @pyqtSlot()
    def measureData(self):
        """
        Function for data receive.
        Function generates signal emiting the tuple 'data'. 
        In case termination of function is required it is necessary to terminate the whole thread (use 'end_thread_signal').
        """
        time.sleep(0.01)
        while True:
            time.sleep(0.01)

            received_data =self.device.measure_continuous()
            
            if received_data is not None: 
                data = float(received_data) 
                self.data_signal.emit(data)
       

    def reconnectDevice(self):
        self.device.stop_controller()
        self.device.start_controller()
    
    @pyqtSlot()
    def getInfo(self):
        text = self.device.get_info()
        self.info_signal.emit(text)


class TOFWindow(QWidget):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Control Panel - RP Lidar")
        self.setGeometry(100, 100, 300, 500)
        self.createGUI()
        self.port = port
        self.device_control = Device(self.port)
        self.communication_thread = QThread()
        self.terminal = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.connectGUI()
        self.create_thread_communication()
        

    def createGUI(self):
        """
        Function creates graphical user interface GUI
        """
        self.menu_bar = QMenuBar(self)
        self.menu_bar.move(0, 0)
        self.menu_bar.setMaximumHeight(30)
        self.control_menu = self.menu_bar.addMenu("&Device")
        self.show_menu = self.menu_bar.addMenu("&Show")
        self.data_menu = self.menu_bar.addMenu("&Data")
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_measure_button = QPushButton("Measure", self)

        self.start_button.setGeometry(50, 50, 200, 25)
        self.stop_button.setGeometry(50, 100, 200, 25)

        self.show_terminal = QAction("&Terminal window")
        self.show_plot = QAction("&Plot window")

        self.show_menu.addAction(self.show_terminal)
        self.show_menu.addAction(self.show_plot)

        self.layout = QVBoxLayout(self)
        self.layout.setMenuBar(self.menu_bar)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.start_measure_button)
        self.setLayout(self.layout)


    
    def connectGUI(self):
        """
        Function creates connection between elements in the GUI.
        """
        self.show_terminal.triggered.connect(self.show_terminal_window)
        self.show_plot.triggered.connect(self.show_plot_window)
        self.device_control.end_thread_signal.connect(self.reinitialize_thread)
        self.start_button.clicked.connect(self.device_control.startDevice)
        self.stop_button.clicked.connect(self.device_control.stopDevice)
        self.device_control.data_signal.connect(self.terminal.receiveData)
        #self.device_control.data_signal.connect(self.plot_window.update_plot)
        self.start_measure_button.clicked.connect(self.device_control.measureData)

    
    def show_terminal_window(self):
        self.terminal.show()
    
    def show_plot_window(self):
        self.plot_window.show()

    def create_thread_communication(self):
        """
        Function moves the object self.device_control into this thread and starts the thread.
        """
        self.device_control.moveToThread(self.communication_thread)
        self.communication_thread.start()
    
    def reinitialize_thread(self, state):
        """
        Function terminates the thread and starts it again.
        """
        if state == True:
            self.communication_thread.terminate()
            self.create_thread_communication()
    

            



class TerminalWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Terminal")
        self.setGeometry(700, 100, 500, 300)
        self.createGUI()
    
    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)
    
    @pyqtSlot(float)
    def receiveData(self, data):
        
        distance = str(data)
        self.output_box.insertPlainText(distance + "\n")


class PlotWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.x_values = [0]
        self.y_values = [0]
        
        self.setWindowTitle("Plot")
        self.setGeometry(700, 100, 800, 600)
        self.createGUI()
        
    def createGUI(self):
        self.graph = plot()
        self.graph.setBackground('w')
        self.graph_scatter = ScatterPlotItem(size = 10, brush=pg.mkBrush(30, 255, 0, 255) )
        self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values)
        self.graph.addItem(self.graph_scatter)
        self.graph.setXRange(-1500, 1500)
        self.graph.setYRange(-1500,1500)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)
    

    @pyqtSlot(float)
    def update_plot(self, data):

        i = 0
        #Multiple pairs of value received
        self.x_values = [0]
        self.y_values = [0]
       
        #self.center_point = self.center_scatter.addPoints([0], [0])
        self.plot_data = self.graph_scatter.addPoints(self.y_values )

  


"""
applicationAK = QApplication(sys.argv)
window = TOFWindow('COM6')
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
"""

"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
