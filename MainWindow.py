import sys
from PyQt5.QtWidgets import  (QApplication, 
                        QMainWindow, 
                        QMenuBar,
                        QAction)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from serial.tools.list_ports import comports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from SettingsWindow import SettingsWindow
from AppValues import AppValues
from sens_app.WindowsTemplates import ConnectionInfoWindow, MainWindowContent
from RPLidarWindows import RPLidarWindow
from TIRadarWindows import TIRadarWindow
from HelpWindows import HelpWindow
#from TOFWindows import TOFWindow
#from IntelRealSenseWindows import IntelRealSenseWindow


class MainWindow(QMainWindow):

        def __init__(self):
            super().__init__()
            
            self.setWindowTitle("Sensor Application")
            self.setGeometry(50, 50, 1000, 800)

            self.application_values = AppValues()
            self.settings_window = SettingsWindow()
            self.settings_running = False
            self.sensor_window = None
            self.info_window = None
            self.help_window = HelpWindow()
         
            self.connection_info_window = ConnectionInfoWindow() 
            
            self.createMenu()
            self.createStatusBar()
            self.createGUI()
            self.connectGUI()
       
        def createMenu(self):
                self.menu_bar = QMenuBar(self)
                self.menu_bar.move(0, 0)
                self.menu_bar.setMaximumHeight(30)
                self.device_menu = self.menu_bar.addMenu("&Connection/Device")
                self.data_menu = self.menu_bar.addMenu("&Data")
                self.help_menu = self.menu_bar.addMenu("&Help")


                self.show_terminal = QAction("&Terminal window")
                self.show_graphics = QAction("&Graphical window")
                self.device_connection= QAction("&Connection")
                self.device_info = QAction("&Device Info")
                self.connection_info = QAction("&Connection Info")

                self.intro_help = QAction("&Introduction")
                self.window_help = QAction("&Window use")
                self.general_help = QAction("&Open Help")
                self.about_help = QAction("&About")

                self.device_menu.addAction(self.device_info)
                self.device_menu.addAction(self.connection_info)
                self.help_menu.addAction(self.intro_help)
                self.help_menu.addAction(self.window_help)
                self.help_menu.addAction(self.general_help)
                self.help_menu.addAction(self.about_help)
             
                self.setMenuBar(self.menu_bar)

        def createStatusBar(self):
              self.status_bar = self.statusBar()

        def createGUI(self):
                self.window_layout = MainWindowContent()
                self.setCentralWidget(self.window_layout)

        def connectGUI(self):
               self.window_layout.run_button.clicked.connect(self.runDeviceWindow)
               self.window_layout.settings_button.clicked.connect(self.runSettingsWindow)
               self.settings_window.settings_signal.connect(self.application_values.receiveSettingsData)
               self.connection_info.triggered.connect(self.application_values.updateSettingsData) #connection similar to previous one in case no data are received by aplication_values from settings window
               self.application_values.update_signal.connect(self.connection_info_window.createInfo) 
               self.connection_info.triggered.connect(self.showConnectionInfoWindow)
               self.intro_help.triggered.connect(self.showHelpWindow)
               

               if self.sensor_window is not None:

                #connecting menu buttons from sensor window to app values
                self.sensor_window.connection_info.triggered.connect(self.application_values.updateSettingsData)
                self.connection_info.triggered.connect(self.showConnectionInfoWindow)
        
        def runSettingsWindow(self): 
               self.settings_running = True
               self.settings_window.show()

        def showConnectionInfoWindow(self):
               self.connection_info_window.show()
        
        def showHelpWindow(self):
               self.help_window.show()

        def runDeviceWindow(self):
               settings_values = self.application_values.giveSettingsData()
               verification = self.verify_connection(settings_values) #veryfying proper settings
               if self.sensor_window is None and verification == True:
                        if settings_values["Device"] == "RP Lidar":
                                self.sensor_window = RPLidarWindow()
                        elif settings_values["Device"] == "Time Of Flight":
                                self.sensor_window = TOFWindow()
                        elif settings_values["Device"] == "TI Radar":
                                self.sensor_window = TIRadarWindow()
                        elif settings_values["Device"] == ("Intel Real Sense L500" or "Intel Real Sense  D435 Dev 1" or "Intel Real Sense D435 Dev 2"):
                                #self.sensor_window = IntelRealSenseWindow()
                                print("Intel realsense")
              
        def verify_connection(self, settings_data: dict):
                device = settings_data["Device"]
                port1 = settings_data["Port 1"]
                port2 = settings_data["Port 2"]
                specification = settings_data["Specification"]

                verification_value = False
                if device == "No device":
                        self.status_bar.showMessage("Select device and  make proper settings of ports by clicking on 'Settings' button.")
                elif device == ("RP Lidar" or "Time of Flight"):
                        if port1 == "No port":
                                self.status_bar.showMessage(f"{device} requires setting the port. Make proper setting by clicking on 'Settings' button") 
                elif device == "TI Radar":
                        if (port1 == "No port" or port2 == "No port"):
                                self.status_bar.showMessage(f"{device} requires setting two ports. Make proper setting by clicking on 'Settings' button") 
                elif device == ("Intel Real Sense L500" or "Intel Real Sense  D435 Dev 1" or "Intel Real Sense D435 Dev 2"):
                        if specification == "No specification":
                                self.status_bar.showMessage(f"{device} requires specification. Make proper setting by clicking on 'Settings' button")
                else:
                        verification_value = True

                return verification_value
                        

        

        
        
        
        
  

applicationAK = QApplication(sys.argv)
window = MainWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop