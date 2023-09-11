import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QTextEdit, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from WindowsTemplates import DeviceWindowTemplate, TerminalTemplate, ControlTemplate, InfoWindowTemplate, PlotTemplate

class TIRadarWindow(DeviceWindowTemplate):
     
    def __init__(self, parent, cli_port = "COM8", data_port = "COM7"):
        super().__init__()

        self.cli_port = cli_port
        self.data_port = data_port

        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.info_window = InfoWindow(self)
        #self.device_interface = Device(self)
        #self.device_thread = QThread(self)
        self.createGUI()
        self.connectGUI()
        self.createThreadCommunication()

    def createGUI(self):
        return super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()
    
    """
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

    """



class ControlPanelWindow(ControlTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    def createGUI(self):
        self.layout = QVBoxLayout()

        self.measure_button = QPushButton("Measure")
        self.stop_button = QPushButton("Stop Measure")
        self.reset_button = QPushButton("Reset")

        self.layout.addWidget(self.measure_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)
        
        self.setLayout(self.layout)

class TerminalWindow(TerminalTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    @pyqtSlot(dict)
    def receiveData(self, data):
        current_time = data[0]
        x = str(data["x"])
        y = str(data["y"])
        self.output_box.insertPlainText(" x: " + x + " y: " + y + "\n")



class PlotWindow(PlotTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.x_values = [0]
        self.y_values = [0]
        self.createGUI()
    
    @pyqtSlot(dict)
    def updatePlot(self, data):
    
        #Multiple pairs of value received
        self.x_values = data["x"]
        self.y_values = data["y"]
        
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
