import sys
import time
from WindowsTemplates import TerminalTemplate, ControlTemplate, PlotTemplate
from DeviceTemplate import DeviceTemplate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QAction, QMenuBar, QMenu
from adafruit_rplidar_AK import RPLidar, RPLidarException
from pyqtgraph import PlotWidget, plot
import pyrealsense2 as rs
import numpy as np
import cv2


class Device(DeviceTemplate):
    depth_data_signal =pyqtSignal(np.ndarray)
    color_data_signal = pyqtSignal(np.ndarray)
    info_signal = pyqtSignal(dict)
    end_thread_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__(self)
        self.device_running = False 
        self.depth_mesure_running = False
        self.color_running = False
        self.depth_image_running = True
        self.initDevice()

    def initDevice(self): 
        self.pipeline = rs.pipeline() #dataflow of all connected Intel Real Sense Devices
        self.config = rs.config() #object able to control dataflow
        self.pipeline_profile = self.config.resolve(self.pipeline) #configuration of dataflow
        self.device = self.pipeline_profile.get_device() 
        self.data_array = np.zeros((480, 640+640,3))
        self.config.enable_stream(rs.stream.depth,640, 480, rs.format.z16, 30) #Enabling depth camera and distance flow
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    def startDevice(self):
        self.pipeline.start(self.config)
        self.device_running = True
        self.depth_mesure_running = True

    def stopDevice(self):
        self.pipeline.stop()
        self.depth_mesure_running = False
        self.device_running = False
        

    @pyqtSlot()
    def measureData(self):
        """
        Function for data receive.
        Function generates signal emiting the tuple 'data'. 
        In case termination of function is required it is necessary to terminate the whole thread (use 'end_thread_signal').
        """

        if self.device_running == False or self.measuring_running == False:
            self.startDevice()

        while self.depth_mesure_running == True:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_data = depth_image
            color_data = color_image

            self.depth_data_signal.emit(depth_data)
            self.color_data_signal.emit(color_image)
            time.sleep(0.1)

    def getDeviceInfo(self):
        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        device_port = str(self.device.get_info(rs.camera_info.physical_port))
        device_name=str(self.device.get_info(rs.camera_info.name))
        device_product_id= str(self.device.get_info(rs.camera_info.product_id))
        device_serial_number = str(self.device.get_info(rs.camera_info.serial_number))
        device_recommended_firmware_version = str(self.device.get_info(rs.camera_info.recommended_firmware_version))
        device_type = str(self.device.get_info(rs.camera_info.name))
        info_dict = {
            "device product line": device_product_line,
            "device type": device_type,
            "device port": device_port,
            "device name": device_name,
            "device product id": device_product_id,
            "device serial number": device_serial_number,
            "device recommended firmware version": device_recommended_firmware_version
        } 

        self.info_signal.emit(info_dict)

        #241122074115



class IntelRealSenseWindow(QWidget):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel - Intel Real Sense L500")
        self.setGeometry(100, 100, 300, 500)
        self.createGUI()
        self.device_control = Device()
        self.communication_thread = QThread()
        self.terminal = TerminalWindow(self)
        self.camera = CameraWindow(self)
        self.info_terminal = InfoTerminal(self)
        self.connectGUI()
        self.createThreadCommunication()
        

    def createGUI(self):
        """
        Function creates graphical user interface GUI
        """
        self.menu_bar = QMenuBar()
        self.menu_bar.move(0, 0)
        self.menu_bar.setMaximumHeight(30)
        self.control_menu = self.menu_bar.addMenu("&Device")
        self.show_menu = self.menu_bar.addMenu("&Show")
        self.data_menu = self.menu_bar.addMenu("&Data")
        self.data_menu = self.menu_bar.addMenu("&Help")
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_measure_button = QPushButton("Measure", self)

        self.start_button.setGeometry(50, 50, 200, 25)
        self.stop_button.setGeometry(50, 100, 200, 25)

        self.show_terminal = QAction("&Terminal window")
        self.show_camera = QAction("&Camera window")
        self.device_connection= QAction("&Connection")
        self.device_info = QAction("&Device Info")

        self.show_menu.addAction(self.show_terminal)
        self.show_menu.addAction(self.show_camera)

        self.control_menu.addAction(self.device_info)

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

        #Connecting menu 
        self.show_terminal.triggered.connect(self.showTerminalWindow)
        self.show_camera.triggered.connect(self.showCameraWindow)
        self.device_info.triggered.connect(self.showDeviceInfoWindow)

        #Data thread initialization
        self.device_control.end_thread_signal.connect(self.reinitializeThread)

        #Connecting buttons to functions
        self.start_button.clicked.connect(self.device_control.startDevice)
        self.stop_button.clicked.connect(self.device_control.stopDevice)

        #Connecting signals from device control to functions (slots)
        self.device_control.depth_data_signal.connect(self.terminal.receiveData)
        self.device_control.depth_data_signal.connect(self.camera.receiveDepthData)
        self.device_control.color_data_signal.connect(self.camera.receiveColorData)
        self.start_measure_button.clicked.connect(self.device_control.measureData)
        self.device_control.info_signal.connect(self.info_terminal.receiveData)

    
    def showTerminalWindow(self):
        self.terminal.show()

    def showCameraWindow(self):
        self.camera.show()
    
    def showDeviceInfoWindow(self):
        self.device_control.getDeviceInfo()
        self.info_terminal.show()
    
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
    
    @pyqtSlot(np.ndarray)
    def receiveData(self, data):
        array = str(data)
        self.output_box.insertPlainText(array)
        rows_number = np.size(data, 0)
        columns_number = np.size(data, 1)
        print(f"Size: {rows_number} x {columns_number}")


class CameraWindow(PlotTemplate):

    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Camera")
        self.camera_running = False
        self.setGeometry(700, 100, 500, 300)
        self.createGUI()

    def createGUI(self):
        self.layout = QVBoxLayout(self)
   
    
    @pyqtSlot(np.ndarray)
    def receiveDepthData(self, data):
        array = data #depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
        depth_colormap_dim = depth_colormap.shape 


        #Displaying window
        
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', depth_colormap)

    @pyqtSlot(np.ndarray)
    def receiveColorData(self, data):
        array = data #depth image
        image_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
        image_colormap_dim = image_colormap.shape 


        #Displaying window
        
        cv2.namedWindow('RealSense Image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense Image', data)


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
window = ControlPanelWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop
"""

"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
