import sys
import time
from math import sin, cos
from DeviceTemplate import DeviceTemplate
from WindowsTemplates import ControlTemplate, PlotTemplate, TerminalTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from adafruit_rplidar_AK import RPLidar, RPLidarException
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg

class Device(DeviceTemplate):
    data_signal =pyqtSignal(tuple)
    end_thread_signal = pyqtSignal(bool)
    message_signal =  pyqtSignal(str)
    info_signal = pyqtSignal(dict)

    def __init__(self, port):
        super().__init__(self)
        self.port = port
        self.device = RPLidar(None, port, timeout=3)
        self.device.stop_motor()
        self.data_state = True
        self.motor_running = False

    
    def startMotor(self):
        if self.motor_running == False:
            self.device.start_motor()
            self.motor_running = True
        else:
            message = "Motor already started"
            self.message_signal.emit(message)

    def stopMotor(self):

        if self.device_started == True:
            self.stopDevice()
        if self.motor_running == True:
            self.device.stop_motor()
            self.motor_running = False
        else:
            message = "Motor already stopped"
            self.message_signal.emit(message)
        

    def startDevice(self):
        try:
            self.device.start()
            self.device_started = True
        except RPLidarException:
            print("RPLidarException: Device already started.")

    def stopDevice(self):
        try:
            self.end_thread_signal.emit(True) #signal to get out of the thread in case the measure_data function has been called
            self.device.stop()
            self.device_started = False
        except RPLidarException:
            print("RPLidarException: Device already stopped.")

    @pyqtSlot()
    def measureData(self):
        """
        Function for data receive.
        Function generates signal emiting the tuple 'data'. 
        In case termination of function is required it is necessary to terminate the whole thread (use 'end_thread_signal').
        """
        self.device_running = True
        self.motor_running = True
        message = "Measuring state"
        self.message_signal.emit(message)
        while True:
            angle = [0]
            distance = [0]
            time.sleep(0.05)
            #data = self.device.once_measurements()
            try:
                iterator = self.device.iter_scans()
                scan = next(iterator)
                for item in scan:
                    angle.append(item[1])
                    distance.append(item[2])
                data = (angle, distance)
            except RPLidarException:

                #UnboundLocalError: local variable 'data' referenced before assignment
                #in case there is a mistake in data it is necessary to send some data
                data = ([0],[0])
                #Exception for 'Wrong body size' or 'Incorrect descriptor starting bytes' 
                #Device becomes uncontrollable .
                #Solution is reconnection or physical disconnection

                message = """'
                Wrong body size' or 'Incorrect descriptor starting bytes'. 
                Please press 'Stop', -> 'Start' -> 'Measure'"""
                self.message_signal.emit(message)
    

            self.data_signal.emit(data)

    def reconnectDevice(self):

        #Function enables renewing of the connection
        self.device.disconnect()
        self.device_started = False
        self.device = RPLidar(None, self.port, timeout=3)
        self.startDevice()
        self.device.stop_motor()

    def resetDevice(self):
        self.device.reset() #resets device to idle
        self.reconnectDevice() #creates connection again

    def getDeviceInfo(self):
        info_message = self.device.info
        self.info_signal.emit(info_message)

class RPLidarWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Control Panel - RP Lidar")
        self.setGeometry(100, 100, 300, 500)
        
        self.port = port
        self.device_control = Device(self.port)
        self.communication_thread = QThread()
        self.terminal = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.info_terminal = InfoTerminal(self)
        self.createGUI()
        self.adjustGUI()
        self.createMenu()
        self.createStatusBar()
        self.connectGUI()
        self.create_thread_communication()
    
      

    def adjustGUI(self):
        """
        Function creates graphical user interface GUI
        """
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_motor_button = QPushButton("Start motor")
        self.stop_motor_button = QPushButton("Stop motor")
        self.start_measure_button = QPushButton("Measure")
        self.reset_button = QPushButton("Reset")
        self.start_button.setGeometry(50, 50, 200, 25)
        self.stop_button.setGeometry(50, 100, 200, 25)
        self.start_motor_button.setGeometry(50, 150, 200, 25)
        self.stop_motor_button.setGeometry(50, 200, 200, 25)
        self.reset_button.setGeometry(50, 200, 200, 25)
    
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.start_motor_button)
        self.layout.addWidget(self.stop_motor_button)
        self.layout.addWidget(self.start_measure_button)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)


    
    def connectGUI(self):
        """
        Function creates connection between elements in the GUI.
        """

        self.show_terminal.triggered.connect(self.showTerminalWindow)
        self.show_graphics.triggered.connect(self.showGraphicWindow)
        self.device_info.triggered.connect(self.showDeviceInfoWindow)
        self.show_terminal.triggered.connect(self.showTerminalWindow)
        self.device_control.end_thread_signal.connect(self.reinitialize_thread)
        
        #Connecting signals from device control to functions (slots)
        self.device_control.data_signal.connect(self.terminal.receiveData)
        self.device_control.data_signal.connect(self.plot_window.updatePlot)
        self.device_control.message_signal.connect(self.receiveMessage)
        self.device_control.info_signal.connect(self.info_terminal.receiveData)

        #Connecting buttons to functions
        self.start_button.clicked.connect(self.device_control.startDevice)
        self.stop_button.clicked.connect(self.device_control.stopDevice)
        self.start_motor_button.clicked.connect(self.device_control.startMotor)
        self.stop_motor_button.clicked.connect(self.device_control.stopMotor)
        self.start_measure_button.clicked.connect(self.device_control.measureData)
        self.reset_button.clicked.connect(self.device_control.resetDevice)


    
    def showTerminalWindow(self):
        self.terminal.show()
    
    def showGraphicWindow(self):
        self.plot_window.show()

    def showDeviceInfoWindow(self):
        self.device_control.getDeviceInfo()
        self.info_terminal.show()
    
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
    

            



class TerminalWindow(TerminalTemplate):
    def __init__(self, parent):
        super().__init__(parent)
       

    
    @pyqtSlot(tuple)
    def receiveData(self, data):
        i = 0
        for scan in data[0]:
            angle = str(data[0][i])
            distance = str(data[1][i])
            i+=1
            self.output_box.insertPlainText(angle + " " + distance + "\n")


class PlotWindow(PlotTemplate):
    def __init__(self, parent):
        super().__init__(self)
        self.x_values = [0]
        self.y_values = [0]
        
        self.setWindowTitle("Plot")
        self.setGeometry(700, 100, 800, 600)
        self.createGUI()
        
    def createGUI(self):
        self.createPlot()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)
    
    def createPlot(self):
        self.graph = plot()
        self.graph.setBackground('w')
        self.graph_scatter = ScatterPlotItem(size = 10, brush=pg.mkBrush(30, 255, 0, 255) )
        self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values)
        self.graph.addItem(self.graph_scatter)
        self.graph.setXRange(-1500, 1500)
        self.graph.setYRange(-1500,1500)
     
    @pyqtSlot(tuple)
    def updatePlot(self, data):

        i = 0
        #Multiple pairs of value received
        self.x_values = [0]
        self.y_values = [0]
        for item in data[0]:
            x = cos(data[0][i]) * data[1][i]
            y = sin(data[0][i]) * data[1][i]
            self.x_values.append(x)
            self.y_values.append(y)
            i+=1
        self.graph_scatter.clear()
        #self.center_point = self.center_scatter.addPoints([0], [0])
        self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values )

  
class InfoTerminal(TerminalWindow):
    def __init__(self,parent):
        super().__init__(parent)
    
    @pyqtSlot(dict)
    def receiveData(self, data):
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)


"""
applicationAK = QApplication(sys.argv)
window = RPLidarWindow('COM4')
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
"""



"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
