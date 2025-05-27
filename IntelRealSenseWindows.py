import sys
import time
import typing

from PyQt5 import QtCore, QtGui
from WindowsTemplates import *
from device_interfaces.IntelRealSenseInterface import Device
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QObject, QPoint, QRect, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cv2

from HelpWindows import HelpWindow
from Info import Info
from app_functions.app_functions import Converter, Cutter


class IntelRealSenseWindow(DeviceWindowTemplate):
    resize_signal = pyqtSignal(bool)
    depth_fig_showed = False
    def __init__(self, serial_number = "f1320623"):
        super().__init__()

        self.serial_number = serial_number
        
        #Creating subwindows
        self.control_window = ControlPanelWindow(self)
        self.terminal_window = TerminalWindow()
        self.plot_window_color = PlotWindowColor(self) #color camera of Intel Real Sense Device
        self.plot_window = PlotWindow(self) #depth camera or Intel Real Sense Device
        self.info_window = InfoWindow()
        self.central_widget = CentralWidgetWindow()
        self.process_window = ProcessWindow()
        self.process_window_area = ProcessWindowArea()

        #creating objects helping with data processing and information
        self.info_provider = Info()
        self.converter = Converter()
        self.cutter = Cutter()
        

        self.device_interface  = Device(serial_number = self.serial_number)

        self.serial_number = serial_number
        self.createGUI()
        self.adjustGUI()
        self.connectGUI()
        self.connectAdjustedGUI()
        self.setElements()
        self.createThreadCommunication()

        #Running functions necessary to complete initialization of the Main Window 
        self.device_interface.getDeviceInfo()

        #Showing graphical (self.plot_window) and camera window (self.plot_window_color) by default
        self.showDefaultWindows()

    def moveTerminalToThread(self):
        self.terminal_thread = QThread()
        self.terminal_window_thread.moveToThread(self.terminal_thread)
        self.terminal_thread.start()

    def adjustGUI(self):
        self.setWindowTitle("IntelRealSenseWindow")
        #Creating Widget Window for color camera
        self.camera_window_area = QDockWidget("Camera Window")
        self.camera_window_area.setWidget(self.plot_window_color)
        self.camera_window_area.setAllowedAreas(Qt.RightDockWidgetArea)
        self.camera_window_area.hide()
        self.addDockWidget(Qt.RightDockWidgetArea, self.camera_window_area)

        

        #Creating menu subcard action for opening color camera
        self.show_graphics_color  = QAction("&Camera")
        self.window_menu.addAction(self.show_graphics_color)

        self.depth_evaluation  = QAction("&Evaluate Depth Image")
        # self.data_menu.addAction(self.depth_evaluation)

        #Setting central window with info
        self.central_widget.setInfoText(Info.IntelRealSenseInfoCZ, 'CZ' )
        self.central_widget.setInfoText(Info.IntelRealSenseInfoEN, 'EN' )
        self.setCentralWidget(self.central_widget)


    def connectAdjustedGUI(self):
        self.show_graphics_color.triggered.connect(self.camera_window_area.show)
        self.control_window.evaluate_button.clicked.connect(self.processDepthImage)



    def createGUI(self):
        super().createGUI()
    
    def connectGUI(self):
        return super().connectGUI()
    
    def connectElements(self):

        #Data thread initialization
        self.device_interface.end_thread_signal.connect(self.reinitializeThread)

        #Connecting buttons to functions
        self.control_window.start_button.clicked.connect(self.device_interface.measureData)
        self.control_window.stop_button.clicked.connect(self.device_interface.stopDevice)
        # self.control_window.start_measure_button.clicked.connect(self.device_interface.measureData)
        self.device_info.triggered.connect(self.device_interface.getDeviceInfo)
        self.depth_evaluation.triggered.connect(self.processDepthImage)

        #Connecting signals from device control to functions (slots)
        self.device_interface.depth_data_signal.connect(self.terminal_window.receiveData)
        self.device_interface.depth_data_signal.connect(self.plot_window.receiveDepthData)
        self.device_interface.depth_data_signal.connect(self.storeDepthData)
        self.device_interface.color_data_signal.connect(self.plot_window_color.receiveColorData)
        self.process_window_area.process_window.coords_signal.connect(self.cropDepthImage)
        self.device_interface.info_signal.connect(self.info_window.receiveData)
        self.device_interface.info_signal.connect(self.plot_window_color.setColorImageSize)
        self.device_interface.message_signal.connect(self.setStatusBarText)
        self.plot_window_color.resize_signal.connect(self.adjustSize)  
        



    @pyqtSlot(np.ndarray)
    def storeDepthData(self, data):
        """
        Stores data from depth image.
        """
        self.depth_data = data


    def processDepthImage(self):
        IntelRealSenseWindow.depth_fig_showed = False
        print("fales")
        self.process_window_area.process_window.setPixmap(self.plot_window.pix_map)
        self.process_window_area.show()
        self.process_window_area.process_window.show()

    

    @pyqtSlot(tuple)
    def cropDepthImage(self, border_coords):
    
        data_raw = self.depth_data

        #Getting coordinates of selected area to crop
        border = border_coords
        row_begin = border[0][1] #begin of row to crop from (y coordinate)
        row_end = border[1][1] #end of row to crop to (y coordinate)
        column_begin = border[0][0] #begin of xolumn to crop from (x coordinate)
        column_end = border[1][0] #end of column to crop to (x coordinate)

        #Cropping the array
        cropped_image = self.cutter.cutArray(data_raw, row_begin, row_end, column_begin, column_end)


        #Printing cropped imag in terminal window
        self.terminal_window.printMatrix(cropped_image)
        plt.subplot(1,1,1)
        plt.imshow(cropped_image)
        plt.title("Depth value [mm]")

        # cmap = plt.get_cmap('jet', 10) 
        # norm = mpl.colors.Normalize(vmin=0, vmax=2) 
        # sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm) 
        # sm.set_array([]) 
        # plt.colorbar(sm, ticks=np.linspace(0, 2, 10)) 

        plt.colorbar() 

        #Adding scale to image 
        plt.show()



    def closeEvent(self, event) -> None:
        
        #closing subwindows when main window is closed
        self.destroyThread()
        self.control_window.close()
        self.terminal_window.close()
        self.plot_window_color.close()
        self.plot_window.close()
        self.info_window.close()
        self.central_widget.close()
        #self.process_window = ProcessWindow()
        self.process_window_area.close()
        plt.close()



    def showDefaultWindows(self):
        """
        Function shows default output windows in main window.
        """
        # self.terminal_window_area.show()
        self.plot_window_area.show()
        self.camera_window_area.show()




class ControlPanelWindow(ControlTemplate):
    trigger_measure_signal = pyqtSignal(bool)

    def __init__(self,parent):
        super().__init__(parent)
        self.createGUI()

        

    def createGUI(self):
        """
        Function creates user control GUI
        """
        self.setWindowTitle("Control Panel - Intel Real Sense L500")
        self.setGeometry(100, 100, 300, 500)

        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        # self.start_measure_button = QPushButton("Measure", self)
        self.evaluate_button = QPushButton("Evaluate", self)

        self.start_button.setMinimumSize(100, 25)
        self.start_button.move(10, 50)

        self.stop_button.setMinimumSize(100, 25)
        self.stop_button.move(10, 100)

        # self.start_measure_button.setMinimumSize(100, 25)
        # self.start_measure_button.move(10, 150)

        self.evaluate_button.setMinimumSize(100, 25)
        
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.start_button, 0 , 0)
        self.layout.addWidget(self.stop_button, 1, 0)
        # self.layout.addWidget(self.start_measure_button, 2, 0)
        self.layout.addWidget(self.evaluate_button, 2, 0)
        self.setLayout(self.layout)




class TerminalWindow(TerminalTemplate):
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Terminal")
        self.setGeometry(0, 100, 200, 100)
        self.createGUI()
        self.data_flow = False

    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)

        #np.set_printoptions(threshold=np.inf)
    
    @pyqtSlot(np.ndarray)
    def receiveData(self, data):
        

        self.output_box.clear()
        array = str(data)
        self.output_box.insertPlainText("\nDepth Matrix: \n")
        self.output_box.insertPlainText(array)
        

    def printMatrix(self, data):

        np.set_printoptions(threshold=sys.maxsize)
        self.output_box.clear()
        array = str(data)
        self.output_box.insertPlainText("\nDepth Matrix of selected area: \n")
        self.output_box.insertPlainText(array)
        np.set_printoptions(threshold = None)


class PlotWindow(PlotTemplate):

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.data_flow = False
        self.camera_running = False

        
        self.createGUI()

    def createGUI(self):

        #Window parameters
        self.setWindowTitle("DepthCamera")
        self.win_width = 640
        self.win_height = 480
        
        self.setFixedSize(self.win_width, self.win_height)
        self.layout = QVBoxLayout()
        #Creating elements
        self.depth_image  = QLabel(self)
        #self.depth_image.setFixedSize(self.win_width, self.win_height)
        self.depth_image.showMaximized()
        
        #Creating layout and adding elements to it
        self.layout.addWidget(self.depth_image)

    
    
    @pyqtSlot(np.ndarray)
    def receiveDepthData(self, data):

        array = data #depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.05), cv2.COLORMAP_JET) #converting values of depth to color scale
        self.image = depth_colormap
        depth_colormap_dim = depth_colormap.shape 
        self.depth_image.setFixedHeight(depth_colormap_dim[0])
        self.depth_image.setFixedWidth(depth_colormap_dim[1])

        qt_image_processing = QImage(depth_colormap, 640, 480, 640*3, QImage.Format_RGB888 )
        #qt_image = qt_image_processing.scaled(self.size())
        self.pix_map = QPixmap.fromImage(qt_image_processing)
        
        self.depth_image.setPixmap(self.pix_map)
     


        
        


class PlotWindowColor(PlotTemplate):
    resize_signal = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.camera_running = False
        
        
        self.createGUI()

    def createGUI(self):

        self.setWindowTitle("Camera")

        #Setting size of the image and the window according device type
        self.setColorImageSize()
        # self.setFixedSize(self.window_width, self.window_height)

        #Creating layout and its elements
        self.layout = QVBoxLayout(self)
        self.color_image  = QLabel(self)
        self.layout.addWidget(self.color_image)
        self.color_image.showMaximized()
        # self.showMaximized()
    
    def connectGUI(self):
        self.resize_signal.connect()

    @pyqtSlot(np.ndarray)
    def receiveColorData(self, data):
        

        array = data #image array
        rgb_array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    

        image_colormap = cv2.applyColorMap(cv2.convertScaleAbs(data, alpha = 0.1), cv2.COLORMAP_JET) #converting values of depth to color scale

        
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
    def setColorImageSize(self, info_data = None):
        """
        Function sets size of the image according to the type of intel real sense device
        """

        if info_data:
            self.product_line  = info_data["device product line"]
        else:
            self.product_line = 'D400'

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
        """
        Function receives data from data signal from device thread.
        """
         
        #Clearing output box from previous data
        self.output_box.clear()

        #Printing data to output box
        for key, value in data.items():
            text = "{}: {}\n".format(key, value)
            self.output_box.insertPlainText(text)



class ProcessWindow(QLabel):
    coords_signal = pyqtSignal(tuple)
    message_signal = pyqtSignal(str)
     
    def __init__(self, parent = None):
    
        QLabel.__init__(self, parent)
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.top_left_pos = QPoint()
        self.bottom_right_pos = QPoint()
    
    def mousePressEvent(self, event) -> None:

        """
        Function cathes position of the mouse when left button of mouse is clicked.
        """

        if event.button() == Qt.LeftButton:

            self.top_left_pos = QPoint(event.pos())
            self.rubber_band.setGeometry(QRect(self.top_left_pos, QSize())) #QSize gets the immediate size
            self.rubber_band.show()

    def mouseMoveEvent(self, event) -> None:
        """
        Function catches position of the mouse when left button mouse is released.
        """
        if not self.top_left_pos.isNull():
            self.rubber_band.setGeometry(QRect(self.top_left_pos, event.pos()).normalized())
            self.bottom_right_pos = QPoint(event.pos())

    def mouseReleaseEvent(self, event) -> None:
        """
        Function gives pixel coordinates of selected area 

        returns
        (top_left_coord, bott_right_coord), (tuple of tuples)

        top_left_coord (tuple) = (x,y) coordinate of top left corner
        bott_right_coord (tuple) = (x,y) coordinate of bottom right corner
        """

        top_left_coord = (self.top_left_pos.x(), self.top_left_pos.y())
        bott_right_coord = (self.bottom_right_pos.x(), self.bottom_right_pos.y())

        self.selected_area =  (top_left_coord, bott_right_coord)  

    def closeEvent(self, event) -> None: 
        if IntelRealSenseWindow.depth_fig_showed == False:
            text = "Closing window and emiting coordinates of selected area"
            print(text)
            self.message_signal.emit(text)
            IntelRealSenseWindow.depth_fig_showed = True
            self.coords_signal.emit(self.selected_area)
        else:
            print("je to zly")

class ProcessWindowArea(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.process_window = ProcessWindow()
        self.help_window = HelpWindow()

        self.createGUI()


        #hiding window by default 
        self.hide()

    def createGUI(self):
        self.setWindowTitle("Process Depth Image")
        self.layout = QVBoxLayout()
        self.setBaseSize(1200, 800)

        #Creating elements and adding them to layout
        self.createElements()
        self.layout.addWidget(self.process_window, alignment = Qt.AlignCenter)
        self.setLayout(self.layout)

    def createElements(self):
        self.info_line1CZ = QLabel(Info.IntelDragDrawInfoCZ, alignment = Qt.AlignCenter)
        self.info_line1CZ.setFont(QFont('Times', 10))

        self.info_line2CZ = QLabel(Info.IntelSelectAreaInfoCZ)
        self.info_line2CZ.setFont(QFont('Times', 8))

        self.info_line1EN = QLabel(Info.IntelDragDrawInfoEN, alignment = Qt.AlignCenter)
        self.info_line1EN.setFont(QFont('Times', 8))

        self.info_line2EN = QLabel(Info.IntelSelectAreaInfoEN)
        self.info_line2EN.setFont(QFont('Times', 8))

        self.layout.addWidget(self.info_line1CZ, alignment = Qt.AlignCenter)
        self.layout.addWidget(self.info_line2CZ, alignment = Qt.AlignCenter)
        self.layout.addWidget(self.info_line1EN, alignment = Qt.AlignCenter)
        self.layout.addWidget(self.info_line2EN, alignment = Qt.AlignCenter)
        
    def closeEvent(self, event) -> None:
        #closing subwindows when window is closed
        self.process_window.close()

    def openTip(self):
        info = Info.IntelSelectAreaInfoCZ + "\n" + Info.IntelSelectAreaInfoEN
        self.help_window.setInfo(info)

   






""" applicationAK = QApplication(sys.argv)
window = IntelRealSenseWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop """

""" applicationAK = QApplication(sys.argv)
window = IntelRealSenseWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop """


"""
Sources:
https://pythonprogramminglanguage.com/pyqt-menu/
https://pythonbasics.org/pyqt-menubar/
https://wiki.qt.io/Qt_for_Python_Signals_and_Slots 

"""
