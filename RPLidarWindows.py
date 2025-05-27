import sys
import time
from math import sin, cos
from device_interfaces.RPLidarInterface import Device
from WindowsTemplates import DeviceWindowTemplate, ControlTemplate, PlotTemplate, TerminalTemplate, InfoWindowTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QAction, QLineEdit, QApplication
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg
import numpy as np

class RPLidarWindow(DeviceWindowTemplate):

    def __init__(self, port = 'COM3'):
        super().__init__()
        self.port = port
        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.info_window = InfoWindow(self)
        self.device_interface = Device(self)
        self.device_thread = QThread(self)
        self.device_interface.startDevice()
        self.createGUI()
        self.connectGUI()
        self.createThreadCommunication()
        self.plot_window_area.show()

    def createGUI(self):
        return super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()
    
        
    
    # def adjustGUI(self):
    #     #Creating menu options for disconnection and reconnection of the device
    #     self.disconnect_device = QAction("&Disconnect Device")
    #     self.reconnect_device = QAction("&Reconnect Device")
    #     self.device_menu.addAction(self.disconnect_device)
    #     self.device_menu.addAction(self.reconnect_device)
    
    def closeEvent(self, event):
        #End communication when closing window
        self.device_interface.stopDevice()
        self.destroyThread()
        #super().closeEvent(self, event)
        self.plot_window_area.close()
        self.close()
        # print("Ukoncujeme")

  
    def connectElements(self):

        #Connecting buttons to functions
        self.control_window.start_button.clicked.connect(self.device_interface.measureData) 
        # self.control_window.start_button.clicked.connect(self.CreateThread)  
        self.control_window.stop_button.clicked.connect(self.device_interface.stopDevice)
        # self.control_window.start_motor_button.clicked.connect(self.device_interface.startMotor)
        # self.control_window.stop_motor_button.clicked.connect(self.device_interface.stopMotor)
        # self.control_window.start_measure_button.clicked.connect(self.device_interface.measureData)
        # self.device_info.triggered.connect(self.device_interface.getDeviceInfo)
        # self.reconnect_device.triggered.connect(self.device_interface.reconnectDevice)
        # self.disconnect_device.triggered.connect(self.device_interface.disconnectDevice)


        #Connecting signals from device control to functions (slots)
        self.device_interface.data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.data_signal.connect(self.plot_window.updatePlot)
        self.device_interface.info_signal.connect(self.info_window.receiveData)
        self.device_interface.message_signal.connect(self.setStatusBarText)
        # self.control_window.pwm_value_signal.connect(self.device_interface.setPWM)



class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)
    # pwm_value_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()
        self.connectGUI()

    def createGUI(self):
        """
        Function creates graphical user interface GUI
        """
        #window properties
        self.setWindowTitle("Control Panel - RP Lidar")
        self.setGeometry(100, 100, 300, 500)
        

        #Creating layouts snd sublayouts
        self.layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        # self.slider_layout = QVBoxLayout()
        self.button_layout_widget = QWidget()
        # self.slider_layout_widget = QWidget()

        #Creating elements and setting the geometry
        self.start_button = QPushButton("Start Measuring")
        self.stop_button = QPushButton("Stop Measuring")

        #Odmazani nepotrebnych tlacitek

        # self.start_motor_button = QPushButton("Start motor")
        # self.stop_motor_button = QPushButton("Stop motor")
        # self.start_measure_button = QPushButton("Measure")
        self.start_button.setGeometry(50, 50, 200, 25)
        self.stop_button.setGeometry(50, 100, 200, 25)
        # self.start_motor_button.setGeometry(50, 150, 200, 25)
        # self.stop_motor_button.setGeometry(50, 200, 200, 25)
        # self.slider = QSlider(self)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(1000)
        # self.slider.setMinimumHeight(200)
        # self.slider.setMaximumHeight(1000)
        # self.pwm_label = QLabel("PWM: ")
        # self.pwm_input = QLineEdit(self)
    
        #Adding elemts to the layouts
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        #Odmazani nepotrebnych tlacitek

        #self.button_layout.addWidget(self.start_motor_button)
        #self.button_layout.addWidget(self.stop_motor_button)
        # self.button_layout.addWidget(self.start_measure_button)
        # self.slider_layout.addWidget(self.pwm_label, alignment= Qt.AlignCenter)
        # self.slider_layout.addWidget(self.slider, alignment= Qt.AlignCenter )
        # self.slider_layout.addWidget(self.pwm_input, alignment= Qt.AlignCenter)
        

        self.button_layout_widget.setLayout(self.button_layout)
        # self.slider_layout_widget.setLayout(self.slider_layout)

        #Adding sublayouts to the main layout
        self.layout.addWidget(self.button_layout_widget)
        # self.layout.addWidget(self.slider_layout_widget)

        self.setLayout(self.layout)

    def connectGUI(self):
        pass
        # self.slider.valueChanged.connect(self.changePWMInput)
        # self.slider.sliderReleased.connect(self.emitPWMvalueSlider)
        # self.pwm_input.editingFinished.connect(self.emitPWMvalueInput)

    
    def changePWMInput(self, value: int):
        """
        Changes value in the input field when the to correspond with the actual value on slider.
        It must be connected to the function self.slider.valueChanged.connect(self.changePWMInput) 
        while it must be updated even when the slider is changed continuous.
        """
        pwm_value = self.slider.value()
        self.pwm_input.setText(str(pwm_value))
    
    def changePWMSlider(self, value: int):
        """
        Changes value of the slider when the to correspond with the actual value inserted in input field.
        It is called in the function self.editPWMvalueInput while it changes only after pressing enter.
        """
        self.slider.setValue(value)
       

    def emitPWMvalueSlider(self):
        pwm_value = self.slider.value()
        self.pwm_value_signal.emit(pwm_value)

    def emitPWMvalueInput(self):
        
        try:
            pwm_value = int(self.pwm_input.text())
            self.pwm_value_signal.emit(pwm_value)
            self.changePWMSlider(pwm_value)
        except ValueError:
            message = "Wrong Input Type"
            self.message_signal.emit(message)



        #self.pwm_value_signal.emit(pwm_value)

        


class TerminalWindow(TerminalTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()
    
    @pyqtSlot(tuple)
    def receiveData(self, data):
        # i = 0
        # for scan in data[0]:
        #     angle = str(data[0][i])
        #     distance = str(data[1][i])
        #     i+=1
        #     self.output_box.insertPlainText(angle + " " + distance + "\n")
        self.output_box.insertPlainText("lines"+ "\n")

class PlotWindow(PlotTemplate):
    def __init__(self, parent):
        super().__init__(self)
 

        
        self.createGUI()
        
    def adjustGUI(self):

        #Adjjusting plot (plot in original template measures in the meters while RPLidar measures in the milimeters)
        self.graph.setXRange(-5000, 5000)
        self.graph.setYRange(-5000,5000)
          
    @pyqtSlot(tuple)
    def updatePlot(self, data):
        self.blockSignals(True)
        as_np = np.asarray(data)
        y_data = as_np[:, 0]
        x_data = as_np[:, 1]
        self.graph_scatter.clear()
        self.plot_data = self.graph_scatter.setData(x=x_data, y=y_data, brush=pg.mkBrush(30, 255, 0, 255))
        self.sensor_position = self.graph_scatter.addPoints([0], [0], brush=pg.mkBrush('r'))
        self.blockSignals(False)
        


  
class InfoWindow(InfoWindowTemplate):
    def __init__(self,parent):
        super().__init__(parent)
        self.createGUI()
    
    @pyqtSlot(dict)
    def receiveData(self, data):
         self.clearOutputBox()
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)



""" applicationAK = QApplication(sys.argv)
window = RPLidarWindow(port = 'COM4')
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop """



"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
