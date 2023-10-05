import sys
import time
import typing

from PyQt5 import QtCore, QtGui
from WindowsTemplates import TerminalTemplate, ControlTemplate, PlotTemplate, DeviceWindowTemplate
from DataFlowWindow import DataFlowWindow
from PointCloudWindow import PointCloudWindow
from device_interfaces.IntelRealSenseInterface import Device
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QObject
from PyQt5.QtWidgets import QApplication, QDockWidget, QPushButton, QTextEdit, QLabel,QWidget, QVBoxLayout, QAction, QMenuBar, QMenu
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
import numpy as np
import open3d as o3d
import cv2
from app_functions import intel_to_open3d
import pyqtgraph.opengl as gl


class IntelRealSenseWindow(DeviceWindowTemplate):
    resize_signal = pyqtSignal(bool)

    def __init__(self, serial_number = "No number"):
        super().__init__()

        self.serial_number =serial_number
        
        self.control_window = ControlPanelWindow(self)

        self.terminal_window = TerminalWindow()
        self.plot_window_color = PlotWindowColor(self) #color camera of Intel Real Sense Device
        self.plot_window = PlotWindow(self) #depth camera or Intel Real Sense Device
        self.point_cloud_window = PointCloudWindow(self)
        self.info_window = InfoWindow()
        self.data_flow_window = DataFlowWindow()

        self.terminal_window_thread = TerminalThread()


        self.device_interface  = Device(serial_number = self.serial_number)

        self.serial_number = serial_number
        self.createGUI()
        self.adjustGUI()
        self.connectGUI()
        self.connectAdjustedGUI()
        self.setElements()
        self.createThreadCommunication()
        self.moveTerminalToThread()

        #Running functions necessary to complete initialization of the Main Window 
        self.device_interface.getDeviceInfo()


    def moveTerminalToThread(self):
        self.terminal_thread = QThread()
        self.terminal_window_thread.moveToThread(self.terminal_thread)
        self.terminal_thread.start()

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

        #Creating menu subcard action for opening color camera
        self.show_graphics_color  = QAction("&Camera")
        self.window_menu.addAction(self.show_graphics_color)
        self.show_point_cloud  = QAction("&Point cloud")
        self.window_menu.addAction(self.show_point_cloud)

        #
        self.central_widget = QWidget(self)
        self.central_widget.setMaximumSize(100, 100)
        self.setCentralWidget(self.central_widget)


    def connectAdjustedGUI(self):
        self.show_graphics_color.triggered.connect(self.camera_window_area.show)
        self.show_point_cloud.triggered.connect(self.plot_window.show)


    def createGUI(self):
        super().createGUI()

    
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
        #self.device_interface.depth_data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.depth_data_signal.connect(self.plot_window.receiveDepthData)
        self.device_interface.color_data_signal.connect(self.plot_window_color.receiveColorData)
        self.device_interface.info_signal.connect(self.info_window.receiveData)
        self.device_interface.info_signal.connect(self.plot_window_color.setColorImageSize)
        self.device_interface.depth_data_signal.connect(self.terminal_window_thread.window.receiveData)
        self.device_interface.message_signal.connect(self.setStatusBarText)
        self.data_flow_window.data_signal.connect(self.point_cloud_window.setDataFlow)

        self.plot_window_color.resize_signal.connect(self.adjustSize)

        self.show_terminal.triggered.connect(self.terminal_window_thread.window.show)

        

    def setElements(self):
        self.data_flow_window.point_cloud_dataflow_chbox.setEnabled(True)
        self.data_flow_window.camera_dataflow_chbox.setEnabled(True)



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


class TerminalThread(QObject):

    def __init__(self):
        super().__init__()
        self.window = TerminalWindow()
        self.window.data_flow = True


class TerminalWindow(TerminalTemplate):
    def __init__(self, **parent):
        super().__init__()
        self.setWindowTitle("Terminal")
        self.setGeometry(700, 100, 500, 300)
        self.createGUI()
        self.data_flow = False
    
    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)

        np.set_printoptions(threshold=np.inf)
    
    @pyqtSlot(np.ndarray)
    def receiveData(self, data):
        
        
        pt_cld = o3d.geometry.PointCloud()
        pt_cld.points = o3d.utility.Vector3dVector(data)
        pt_cld_reduced = pt_cld.voxel_down_sample(voxel_size = 0.05)
        reduced_data = (np.asarray(pt_cld_reduced.points))
        if self.data_flow == True:
            self.output_box.clear()
            array = str(reduced_data)
            self.output_box.insertPlainText("\nDepth Matrix: ")
            self.output_box.insertPlainText(array)

class PlotWindow(PlotTemplate):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Camera")
        self.data_flow = False
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
        
        if self.data_flow == True:
            array = data #depth image
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
            depth_colormap_dim = depth_colormap.shape 

            qt_image_processing = QImage(depth_colormap, 640, 480, 640*3, QImage.Format_RGB888 )
            #qt_image = qt_image_processing.scaled(self.size())
            qt_image_pix_map = QPixmap.fromImage(qt_image_processing)
            self.depth_image.setPixmap(qt_image_pix_map)


class PlotWindowColor(PlotTemplate):
    resize_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        
        self.camera_running = False
        self.data_flow = True #attribute to allow data receive
        
        
        self.createGUI()

    def createGUI(self):

        self.setWindowTitle("Camera")

        #Setting size of the image and the window according device type
        self.setColorImageSize()
        self.setFixedSize(self.window_width, self.window_height)

        #Creating layout and its elements
        self.layout = QVBoxLayout(self)
        self.color_image  = QLabel(self)
        self.layout.addWidget(self.color_image)
        self.color_image.showMaximized()
        #self.showMaximized()
    
    def connectGUI(self):
        self.resize_signal.connect()

    @pyqtSlot(np.ndarray)
    def receiveColorData(self, data):
        
        if self.data_flow == True:
            array = data #image array
            rgb_array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        

            image_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
            print(image_colormap.shape)
            
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
            qt_image_processing = QImage(rgb_array, self.window_width, self.window_height, self.window_width*3, QImage.Format_RGB888 )
            #qt_image = qt_image_processing.scaled(self.size())
            qt_image_pix_map = QPixmap.fromImage(qt_image_processing)
            self.color_image.setPixmap(qt_image_pix_map)
        
    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resize_signal.emit()
        return super().resizeEvent(a0)
    
    @pyqtSlot(dict)
    def setColorImageSize(self, **info_data):
        """
        Function sets size of the image according to the type of intel real sense device
        """

        if info_data:
            self.product_line  = info_data["device product line"]
        else:
            self.product_line = 'D400'

        if self.product_line == 'L500':
            self.window_width = 960
            self.window_height = 540
        else:
            self.window_width = 640
            self.window_height = 480

    @pyqtSlot(dict)
    def setDataFlow(self, dataflow_settings: dict):
        self.data_flow = dataflow_settings["camera"]

    """
    def resizeImage(self):
        self.color_image.setFixedSize(self.size())
    """



class InfoWindow(TerminalWindow):
    def __init__(self):
        super().__init__()
    
    @pyqtSlot(dict)
    def receiveData(self, data):
         
         #Clearing output box from previous data
         self.output_box.clear()

         #Printing data to output box
         for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)




   



applicationAK = QApplication(sys.argv)
window = IntelRealSenseWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop


"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
