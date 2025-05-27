import sys
print(sys.path)

from PyQt5 import QtGui
from PyQt5.QtWidgets import  (QApplication, 
                        QMainWindow, 
                        QMenuBar,
                        QAction)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from serial.tools.list_ports import comports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from SettingsWindow import SettingsWindow
from AppValues import AppValues
from Info import Info
#from sens_app.WindowsTemplates import ConnectionInfoWindow, MainWindowContent
from RPLidarWindows import RPLidarWindow
from TIRadarWindows import TIRadarWindow
from HelpWindows import HelpWindow
#from TOFWindows import TOFWindow
from IntelRealSenseWindows import IntelRealSenseWindow



class MainWindow(QMainWindow):

        def __init__(self):
            super().__init__()

            self.application_values = AppValues()
            self.settings_window = SettingsWindow()
            self.settings_running = False
            self.sensor_window = None
            self.info_window = None
            self.help_window = HelpWindow()
         
            self.connection_info_window = None 


            self.createGUI()
            self.connectGUI()

        def createMenu(self):
                self.menu_bar = QMenuBar(self)
                self.menu_bar.move(0, 0)
                self.menu_bar.setMaximumHeight(30)
                # self.device_menu = self.menu_bar.addMenu("&Connection/Device")
                #self.data_menu = self.menu_bar.addMenu("&Data")
                # self.help_menu = self.menu_bar.addMenu("&Help")


                self.connection_info = QAction("&Connection Info")

                self.intro_help = QAction("&Introduction")
                self.window_help = QAction("&Window use")
                self.general_help = QAction("&Open Help")
                self.about_help = QAction("&About")

                # self.device_menu.addAction(self.connection_info)
                # self.help_menu.addAction(self.intro_help)
                # self.help_menu.addAction(self.window_help)
                # self.help_menu.addAction(self.general_help)
                # self.help_menu.addAction(self.about_help)
             
                self.setMenuBar(self.menu_bar)

        def createStatusBar(self):
              self.status_bar = self.statusBar()

        def createGUI(self):
                """
                Function Creates GUI of Main Device Window
                """
                #self.showMaximized() 
                self.central_widget = QWidget()       
                self.layout = QVBoxLayout(self)
                self.central_widget.setLayout(self.layout)
                
                        
                self.setWindowTitle("Sensor Application")
                #self.setGeometry(50, 50, 1000, 800)
                self.showMaximized()

                self.createMenu()
                self.createStatusBar()
                self.adjustGUI()
                self.setCentralWidget(self.central_widget)

                #Hiding this window by default (since it is not main window of the app but main window for device control)

    
        
        
        def adjustGUI(self):
                self.button_height = 50
                self.button_width = 250
                self.heading_label = QLabel("Sensor Application")
                self.heading_label.setFont(QFont('Times', 18))

                self.info_line1CZ = QLabel(Info.MainWindowInfoCZ)
                self.info_line1CZ.setFont(QFont('Times', 10))
                self.info_line1EN = QLabel(Info.MainWindowInfoEN)
                self.info_line1EN.setFont(QFont('Times', 10))


                #Cancel Window Button
                self.cancel_button = QPushButton("Quit App")
                self.cancel_button.setFixedSize(self.button_width, self.button_height)

                #Sensor list
                self.rp_lidar = QPushButton("RP Lidar")
                self.rp_lidar.setFixedSize(self.button_width, self.button_height)

                self.ti_radar = QPushButton("TI Radar")
                self.ti_radar.setFixedSize(self.button_width, self.button_height)

                self.rs_515 = QPushButton("Intel Lidar L515")
                self.rs_515.setFixedSize(self.button_width, self.button_height)

                self.front_d435 = QPushButton("Front Intel DepthCamera D435")
                self.front_d435.setFixedSize(self.button_width, self.button_height)

                self.back_d435 = QPushButton("Back Intel DepthCamera D435")
                self.back_d435.setFixedSize(self.button_width, self.button_height)


                #Adding elements to the layout
                self.layout.addWidget(self.heading_label, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.info_line1CZ, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.info_line1EN, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.rp_lidar, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.ti_radar, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.rs_515, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.front_d435, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.back_d435, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.cancel_button, alignment = Qt.AlignCenter )

        def connectGUI(self):
               self.rp_lidar.clicked.connect(self.openRPLidarWindow)
               self.ti_radar.clicked.connect(self.openTIRadarWindow)
               self.rs_515.clicked.connect(self.openRS515Window)
               self.front_d435.clicked.connect(self.openFrontD435Window)
               self.back_d435.clicked.connect(self.openBackD435Window)
               self.cancel_button.clicked.connect(self.close)
               self.settings_window.settings_signal.connect(self.application_values.receiveSettingsData)
               self.connection_info.triggered.connect(self.application_values.updateSettingsData) #connection similar to previous one in case no data are received by aplication_values from settings window
               #self.application_values.update_signal.connect(self.connection_info_window.createInfo) 
               self.connection_info.triggered.connect(self.showConnectionInfoWindow)
               self.intro_help.triggered.connect(self.showHelpWindow)
               

               if self.sensor_window is not None:

                #connecting menu buttons from sensor window to app values
                self.sensor_window.connection_info.triggered.connect(self.application_values.updateSettingsData)
                self.connection_info.triggered.connect(self.showConnectionInfoWindow)
        
        def openRPLidarWindow(self):
               self.sensor_window = RPLidarWindow()
               self.sensor_window.show()

        def openTIRadarWindow(self):
               self.sensor_window = TIRadarWindow()
               self.sensor_window.show()

        def openRS515Window(self):
               self.sensor_window = IntelRealSenseWindow("f1320623")
               self.sensor_window.show()

        def openFrontD435Window(self):
               self.sensor_window = IntelRealSenseWindow("241122074115")
               self.sensor_window.show()

        def openBackD435Window(self):
               self.sensor_window = IntelRealSenseWindow("241222076731")
               self.sensor_window.show()
                      

        def runSettingsWindow(self): 
               self.settings_running = True
               self.settings_window.show()               

        def showConnectionInfoWindow(self):
               self.connection_info_window.show()
        
        def showHelpWindow(self):
               self.help_window.show()

        def runDeviceWindow(self):
               self.sensor_window = None
               settings_values = self.application_values.giveSettingsData()
               verification = self.verify_connection(settings_values) #veryfying proper settings
               realsense_devices, realsense_serials = self.settings_window.ListRSDevices() #get list of RS Devices
               
               if self.sensor_window is None and verification == True:
                        port1 = settings_values["Port 1"]
                        port1 = "/dev/" + port1
                        port2 = settings_values["Port 2"]
                        port2 = "/dev/" + port2 

                        if settings_values["Device"] == "RP Lidar":
                                self.sensor_window = RPLidarWindow(port1)
                        elif settings_values["Device"] == "Time Of Flight":
                                self.sensor_window = TOFWindow()
                        elif settings_values["Device"] == "TI Radar":
                                
                                
                                self.sensor_window = TIRadarWindow(port1, port2) #Giving port numbers
                                
                        elif settings_values["Device"] == "Intel Real Sense" and settings_values["Device specification"] != "No device":
                                print(realsense_serials)
                                for i in range(0, len(realsense_devices)):
                                        if settings_values["Device specification"] == realsense_devices[i]:
                                                self.serial_number = realsense_serials[i]
                                self.sensor_window = IntelRealSenseWindow(self.serial_number)     
                        self.sensor_window.show()
              
        def verify_connection(self, settings_data: dict):
                device = settings_data["Device"]
                port1 = settings_data["Port 1"]
                port2 = settings_data["Port 2"]
                specification = settings_data["Device specification"]
                serial_number = settings_data["Serial number"]
                verification_value = False
                if device == "No device":
                        self.status_bar.showMessage("Select device and  make proper settings of ports by clicking on 'Settings' button.")
                elif device == ("RP Lidar" or "Time of Flight") and port1 == "No port":
                        self.status_bar.showMessage(f"{device} requires setting the port. Make proper setting by clicking on 'Settings' button")
                elif device == ("Intel Real Sense L500" or "Intel Real Sense  D435 Dev 1" or "Intel Real Sense D435 Dev 2") and specification == "No specification":
                         self.status_bar.showMessage(f"{device} requires specification. Make proper setting by clicking on 'Settings' button")        
                elif device == ("TI Radar") and (port1 == "No port" or port2 == "No port") or (device == ("TI Radar") and (port1 == port2)):
                        self.status_bar.showMessage(f"{device} requires setting two ports. Make proper setting by clicking on 'Settings' button") 
                else:
                     verification_value = True                
                return verification_value
        
        def closeEvent(self, event) -> None:
               
             
                if self.sensor_window is not None:
                        self.sensor_window.close()

                if self.info_window is not None:
                        self.info_window.close()
                if self.connection_info_window is not None:
                       self.connection_info_window.close()
        
                self.settings_window.close()
                self.help_window.close()
           

        

                        

        

        
        
        
        
  

applicationAK = QApplication(sys.argv)
window = MainWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop