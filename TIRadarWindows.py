import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QTextEdit,  QAction, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, QThread
from WindowsTemplates import *
from device_interfaces.TIRadarInterface import Device
from Info import Info


class TIRadarWindow(DeviceWindowTemplate):
     
    def __init__(self, cli_port = "/dev/ttyACM0", data_port = "/dev/ttyACM1"):
        super().__init__()

        self.cli_port = cli_port
        self.data_port = data_port
        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow(self)
        self.plot_window = PlotWindow(self)
        self.info_window = InfoWindow(self)
        self.device_interface = Device(self, self.cli_port, self.data_port) #giving port numbers
        self.device_thread = QThread(self)
        self.central_widget = CentralWidgetWindow()
        self.createGUI()
        self.connectGUI()
        # self.adjustGUI()
        self.createThreadCommunication()
        self.showDefaultWindows()

    def createGUI(self):
        return super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()

    def adjustGUI(self):
        #Creating menu options for dosconnection and reconnection of the device
        self.disconnect_device = QAction("&Disconnect Device")
        self.reconnect_device = QAction("&Reconnect Device")
        # self.device_menu.addAction(self.disconnect_device)
        # self.device_menu.addAction(self.reconnect_device)

        #Setting central window with info
        # self.central_widget.setInfoText(Info.TIRadarInfoCZ, 'CZ' )
        # self.central_widget.setInfoText(Info.TIRadarInfoEN, 'EN' )
        # self.setCentralWidget(self.central_widget)
    

    def connectElements(self):

        #Connecting buttons to functions
        self.control_window.measure_button.clicked.connect(self.device_interface.measureData)
        self.control_window.stop_button.clicked.connect(self.device_interface.reconnectDevice)
        # self.control_window.reset_button.clicked.connect(self.device_interface.reconnectDevice)
        # self.device_info.triggered.connect(self.device_interface.getDeviceInfo)
        # self.reconnect_device.triggered.connect(self.device_interface.reconnectDevice)
        # self.disconnect_device.triggered.connect(self.device_interface.disconnectDevice)
        
        
        #Connecting signals from device control to functions (slots)
        self.device_interface.data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.data_signal.connect(self.plot_window.updatePlot)
        #self.device_interface.info_signal.connect(self.info_window.receiveData)
        self.device_interface.message_signal.connect(self.setStatusBarText)

    def showDefaultWindows(self):
        """
        Function shows default output windows in main window.
        """
        # self.terminal_window_area.show()
        self.plot_window_area.show()
    
    def closeEvent(self, event) -> None:
        
        #closing subwindows when main window is closed
        
        self.control_window.close()
        self.terminal_window.close()
        self.plot_window.close()
        self.info_window.close()
        self.central_widget.close()
        self.device_interface.stopDevice() #End communication when closing window
        self.destroyThread()






class ControlPanelWindow(ControlTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    def createGUI(self):

        self.layout = QVBoxLayout()

        self.measure_button = QPushButton("Measure")
        self.stop_button = QPushButton("Stop Measure")
        # self.reset_button = QPushButton("Reset")

        self.layout.addWidget(self.measure_button)
        self.layout.addWidget(self.stop_button)
        # self.layout.addWidget(self.reset_button)
        
        self.setLayout(self.layout)
        

class TerminalWindow(TerminalTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    @pyqtSlot(dict)
    def receiveData(self, data):
        x = str(data["x"])
        y = str(data["y"])
        self.output_box.insertPlainText(" x: " + x + " y: " + y + "\n")



class PlotWindow(PlotTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.x_values = [0]
        self.y_values = [0]
        self.createGUI()
    
    def adjustGUI(self):

        #Adjusting plot
        self.graph.setXRange(-5000, 5000)
        self.graph.setYRange(-5000,5000)

    @pyqtSlot(dict)
    def updatePlot(self, data):
        self.graph_scatter.clear()
    
        #Multiple pairs of value received #PH: Convert to mm
        self.x_values = 1000 * data["x"]
        self.y_values = 1000 * data["y"]
        
        #self.center_point = self.center_scatter.addPoints([0], [0])
        self.plot_data = self.graph_scatter.setData(self.x_values, self.y_values, brush=pg.mkBrush(30, 255, 0, 255) )
        self.sensor_position = self.graph_scatter.addPoints([0], [0], brush=pg.mkBrush('r'))

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
