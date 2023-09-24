import sys
import time
import typing

from PyQt5 import QtCore, QtGui
from WindowsTemplates import TerminalTemplate, ControlTemplate, PlotTemplate, DeviceWindowTemplate
from device_interfaces.IntelRealSenseInterface import Device
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QPushButton, QTextEdit, QLabel,QWidget, QVBoxLayout, QAction, QMenuBar, QMenu
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
import numpy as np
import cv2

class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self,parent):
        super().__init__(parent)
        self.createGUI()

        

    def createGUI(self):
        """
        Function creates graphical user control GUI
        """
        self.setWindowTitle("Control Panel - Intel Real Sense L500")
        self.setGeometry(100, 100, 300, 500)

        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_measure_button = QPushButton("Measure", self)

        self.start_button.setMinimumSize(100, 25)
        self.start_button.move(10, 50)

        self.stop_button.setMinimumSize(100, 25)
        self.stop_button.move(10, 100)

        self.start_measure_button.setMinimumSize(100, 25)
        self.start_measure_button.move(10, 150)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.start_measure_button)
        self.setLayout(self.layout)





class TerminalWindow(TerminalTemplate):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Terminal")
        self.setGeometry(700, 100, 500, 300)
        self.createGUI()
    
    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)
    
    @pyqtSlot(np.ndarray)
    def receiveData(self, data):
        array = str(data)
        self.output_box.insertPlainText("\nDepth Matrix: ")
        self.output_box.insertPlainText(array)
        rows_number = np.size(data, 0)
        columns_number = np.size(data, 1)
        #print(f"Size: {rows_number} x {columns_number}")


class PlotWindow(PlotTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Camera")
        self.camera_running = False
        self.setGeometry(700, 100, 640, 480)
        self.createGUI()

    def createGUI(self):
        self.layout = QVBoxLayout(self)
        self.depth_image  = QLabel(self)
        self.layout.addWidget(self.depth_image)
        self.depth_image.showMaximized()
   
    
    @pyqtSlot(np.ndarray)
    def receiveDepthData(self, data):
        array = data #depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
        depth_colormap_dim = depth_colormap.shape 

        qt_image_processing = QImage(depth_colormap, 640, 480, 640*3, QImage.Format_RGB888 )
        #qt_image = qt_image_processing.scaled(self.size())
        qt_image_pix_map = QPixmap.fromImage(qt_image_processing)
        self.depth_image.setPixmap(qt_image_pix_map)


        #Displaying window
        
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('RealSense', depth_colormap)


class PlotWindowColor(PlotTemplate):
    resize_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Camera")
        self.camera_running = False
        self.setFixedSize(640, 480)
        self.window_width = 640
        self.window_height = 480
        self.createGUI()

    def createGUI(self):
        self.layout = QVBoxLayout(self)
        self.color_image  = QLabel(self)
        self.layout.addWidget(self.color_image)
        self.color_image.showMaximized()
        #self.showMaximized()
    
    def conntectGUI(self):
        self.resize_signal.connect()

    @pyqtSlot(np.ndarray)
    def receiveColorData(self, data):
        array = data #depth image
        rgb_array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
       

        image_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
        print(image_colormap.shape)
        window_width = self.width()
        window_height = self.height()
        window_size = (window_width, window_height)
        #xresized_colormap = cv2.resize(image_colormap,window_size)
        image_colormap_dim = image_colormap.shape 
        image_height = image_colormap_dim[0]
        image_width = image_colormap_dim[1]
        image_color_num = 3
        image_line_bytes = image_width * image_color_num
        
        image_channels_bumber = image_colormap_dim[2]
        """https://www.tutorialkart.com/opencv/python/opencv-python-get-image-size/#gsc.tab=0"""
        line_bytes_number = image_width * image_channels_bumber
        """
        https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
        """
        #cv2.namedWindow('RealSenseColor', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('RealSenseColor', data)
        qt_image_processing = QImage(rgb_array, 640, 480, 640*3, QImage.Format_RGB888 )
        #qt_image = qt_image_processing.scaled(self.size())
        qt_image_pix_map = QPixmap.fromImage(qt_image_processing)
        self.color_image.setPixmap(qt_image_pix_map)
        
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resize_signal.emit()
        return super().resizeEvent(a0)
    
    """
    def resizeImage(self):
        self.color_image.setFixedSize(self.size())
    """

    





class InfoWindow(TerminalWindow):
    def __init__(self,parent):
        super().__init__(parent)
    
    @pyqtSlot(dict)
    def receiveData(self, data):
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)

class IntelRealSenseWindow(DeviceWindowTemplate):
    resize_signal = pyqtSignal(bool)

    def __init__(self, serial_number = "No number"):
        super().__init__()

        self.serial_number = serial_number
        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow(self)
        self.plot_window_color = PlotWindowColor(self) #color camera of Intel Real Sense Device
        self.plot_window = PlotWindow(self) #depth camera or Intel Real Sense Device
        self.info_window = InfoWindow(self)


        self.device_interface  = Device(serial_number = self.serial_number)
        self.createGUI()
        self.adjustGUI()
        self.connectGUI()
        self.connectAdjustedGUI()
        self.createThreadCommunication()
    
    def adjustGUI(self):
        self.setWindowTitle("IntelRealSenseWindow")

        #Adjusting plot window (depth camera image has set size)
        #self.plot_window_area.setFixedSize(640, 480)

        #Creating Widget Window for color camera
        self.camera_window_area = QDockWidget("Color Camera Window")
        #self.camera_window_area.setFixedSize(640, 480)
        self.camera_window_area.setWidget(self.plot_window_color)
        self.camera_window_area.setAllowedAreas(Qt.RightDockWidgetArea)
        self.camera_window_area.hide()
        self.addDockWidget(Qt.RightDockWidgetArea, self.camera_window_area)

        #Creating menu suncard action for opening color camera
        self.show_graphics_color  = QAction("&Graphical window - color camera")
        self.show_menu.addAction(self.show_graphics_color)

        #
        self.central_widget = QWidget(self)
        self.central_widget.setMaximumSize(100, 100)
        self.setCentralWidget(self.central_widget)


    def connectAdjustedGUI(self):
        self.show_graphics_color.triggered.connect(self.camera_window_area.show)


    def createGUI(self):
        return super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()
    
    def connectElements(self):

        #Data thread initialization
        self.device_interface.end_thread_signal.connect(self.reinitializeThread)

        #Connecting buttons to functions
        self.control_window.start_button.clicked.connect(self.device_interface.startDevice)
        self.control_window.stop_button.clicked.connect(self.device_interface.stopDevice)
        self.control_window.start_measure_button.clicked.connect(self.device_interface.measureData)
        self.device_info.triggered.connect(self.device_interface.getDeviceInfo)

        #Connecting signals from device control to functions (slots)
        self.device_interface.depth_data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.depth_data_signal.connect(self.plot_window.receiveDepthData)
        self.device_interface.color_data_signal.connect(self.plot_window_color.receiveColorData)
        self.device_interface.info_signal.connect(self.info_window.receiveData)

        self.plot_window_color.resize_signal.connect(self.adjustSize)
 

        


"""
applicationAK = QApplication(sys.argv)
window = IntelRealSenseWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop
"""

"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
