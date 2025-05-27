import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtGui import QFont
from IntelRealSenseData import IntelRealSenseData
from Info import Info

class SettingsWindow(QWidget):
        
        settings_signal = pyqtSignal(dict) #dictionary containing settings information


        def __init__(self):
            super().__init__()
            
            self.device_list = ["No device","RP Lidar", "TI Radar", "Intel Real Sense"]
            #self.device_list = ["No device","RP Lidar", "TI Radar", "Time of Flight", "Intel Real Sense",  "Sensor"]
            self.inter_real_sense_devices =  ["No Intel device", "Lidar L500", "Depth Camera D435i Dev 1 (Front)", "Depth Camera D435i Dev 2 (Back)"]
            self.rs_serial_numbers = ["", "f1320623", "241122074115", "241222076731"]
            self.data = IntelRealSenseData()

            self.port_list = ["No port"]
            self.createGUI()
            self.connectGUI()
            
        def ListRSDevices(self):
             return self.inter_real_sense_devices, self.rs_serial_numbers

        def createGUI(self):

            #Creating major layout
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)

            #Properties of the SettingsWindow GUI
            self.move(300, 150)
            self.setBaseSize(1200, 800)
            self.setMaximumSize(1200, 800)
            self.setWindowTitle('Settings Window') 

            #Calling function creating minor layouts
            self.createDeviceSettingsGUI()
            self.createPortSettingsGUI()
            self.createDeviceSpecifyGUI()
            self.createSettingsGUI()

            self.info_line1CZ = QLabel(Info.SettingsTextCZ)
            self.info_line1CZ.setFont(QFont('Times', 10))
            self.info_line1CZ.setWordWrap(True)
            self.info_line1EN = QLabel(Info.SettingsTextEN)
            self.info_line1EN.setFont(QFont('Times', 8))
            self.info_line1EN.setWordWrap(True)
            #Adding minor layouts to the major layout
            self.layout.addWidget(self.info_line1CZ)
            self.layout.addWidget(self.info_line1EN)
            self.layout.addWidget(self.device_settings)
            self.layout.addWidget(self.port_settings)
            self.layout.addWidget(self.search_ports_infoCZ)
            self.layout.addWidget(self.search_ports_infoEN)
            self.layout.addWidget(self.spec_device_settings)
            self.layout.addWidget(self.ok_widget)

            #Hiding window by default 
            self.hide()

         

        def createSettingsGUI(self):
            
            #Confirm/close section
            self.ok_widget = QWidget()
            self.ok_widget_layout = QHBoxLayout()
            self.ok_widget.setLayout(self.ok_widget_layout)

            self.ok_button = QPushButton("OK")
            self.ok_button.setFixedSize(150, 30)
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.setFixedSize(150, 30)
            

            self.ok_widget_layout.addWidget(self.ok_button)
            self.ok_widget_layout.insertSpacing(1, 100)
            self.ok_widget_layout.addWidget(self.cancel_button)



        def createDeviceSettingsGUI(self):

            #Creating Layout of the section
            self.device_settings = QGroupBox("Select Device")
            self.device_settings_layout = QGridLayout()
            self.device_settings.setLayout(self.device_settings_layout)

            #Creating elements of the layout
            self.device_label = QLabel("Device: ")
            self.device_combo_box = QComboBox()
            self.device_combo_box.setFixedSize(200, 30)

            #Adding elements to the layout
            self.device_settings_layout.addWidget(self.device_label, 0, 0)
            self.device_settings_layout.addWidget(self.device_combo_box, 0, 1)



        def createPortSettingsGUI(self):

            #Creating section layout
            self.port_settings = QGroupBox('Specify port(s)')
            self.port_settings_layout = QGridLayout()
            self.port_settings.setLayout(self.port_settings_layout)

            #Creating section elements
            self.port1_label = QLabel("Port 1: ") 
            self.port2_label = QLabel("Port 2: ")
            self.search_ports_button = QPushButton("Search ports")
            self.search_ports_infoCZ = QLabel(Info.SettingsSearchPortsInfoCZ)
            self.search_ports_infoEN = QLabel(Info.SettingsSearchPortsInfoEN)
            self.port1_combo_box = QComboBox()
            self.port2_combo_box = QComboBox()
            self.port2_combo_box.setEnabled(False)
            self.port1_combo_box.setFixedSize(200, 30)
            self.port2_combo_box.setFixedSize(200, 30)
            self.search_ports_button.setFixedSize(150, 30)

            #Adding elements to section layout
            self.port_settings_layout.addWidget(self.port1_label, 0, 0)
            self.port_settings_layout.addWidget(self.port2_label, 1, 0)
            self.port_settings_layout.addWidget(self.port1_combo_box, 0, 1)
            self.port_settings_layout.addWidget(self.port2_combo_box, 1, 1)
            self.port_settings_layout.addWidget(self.search_ports_button, 2, 1)

            


        def createDeviceSpecifyGUI(self):
             
            #Creating Layout of the section
            self.spec_device_settings = QGroupBox("Specify device")
            self.spec_device_settings_layout = QGridLayout()
            self.spec_device_settings.setLayout(self.spec_device_settings_layout)

            #Creating elements of section 
            self.spec_device_label = QLabel("Specify device: ")
            self.spec_device_settings_combo_box = QComboBox()
            self.spec_device_settings_combo_box.setFixedSize(200, 30)

            #Adding elements to section layout
            self.spec_device_settings_layout.addWidget(self.spec_device_label, 0, 0)
            self.spec_device_settings_layout.addWidget(self.spec_device_settings_combo_box, 0, 1)



        def connectGUI(self):

            #Adding content to the combo_boxes
            self.device_combo_box.addItems(self.device_list)
            self.spec_device_settings_combo_box.addItems(self.inter_real_sense_devices)
            self.port1_combo_box.addItems(self.port_list)
            self.port2_combo_box.addItems(self.port_list)

            #Disabling elements by default
            self.port1_combo_box.setEnabled(False)
            self.port2_combo_box.setEnabled(False)
            self.search_ports_button.setEnabled(False)
            self.spec_device_settings_combo_box.setEnabled(False)

            #Connecting other elements
            self.search_ports_button.clicked.connect(self.searchPorts) 
            self.device_combo_box.activated[str].connect(self.controlPortCombos)   
            self.ok_button.clicked.connect(self.okClicked)
            self.cancel_button.clicked.connect(self.cancelClicked)

        def okClicked(self):

            dev_name = self.device_combo_box.currentText()
            if dev_name == "Intel Real Sense":
                 serial_num  = self.data.matchSerialNumber(self.spec_device_settings_combo_box.currentText())
            else:
                 serial_num = "No serial number set"
        
            settings_dictionary= {
                "Device": self.device_combo_box.currentText(),
                "Port 1": self.port1_combo_box.currentText(),
                "Port 2": self.port2_combo_box.currentText(),
                "Device specification": self.spec_device_settings_combo_box.currentText(),
                "Serial number": serial_num
                }
            self.settings_signal.emit(settings_dictionary)
            self.close()

        def cancelClicked(self):
             self.close()
    
        def searchPorts(self):
            self.port1_combo_box.clear()
            self.port2_combo_box.clear()
            port_list = QSerialPortInfo.availablePorts()
            port_names = []

            if port_list:
                #Checks if port list of available ports is not empty and adds the available ports to the attribute
                for port in port_list:
                    port_names.append(port.portName())
                self.port_list = port_names
            self.port1_combo_box.clear()
            self.port1_combo_box.addItems(self.port_list)
            if self.device_combo_box.currentText() == "TI Radar":
                self.port2_combo_box.clear()
                self.port2_combo_box.addItems(self.port_list)
                self.port1_combo_box.setCurrentText(self.port_list[1])
                self.port2_combo_box.setCurrentText(self.port_list[0])
        
                

        def controlPortCombos(self, device_name):
            if device_name == "RP Lidar" or device_name == "Time of Flight":
                self.port1_combo_box.setEnabled(True)
                self.search_ports_button.setEnabled(True)
                self.spec_device_settings_combo_box.setEnabled(False)
            elif device_name == "TI Radar":
                self.port1_combo_box.setEnabled(True)
                self.port2_combo_box.setEnabled(True)
                self.search_ports_button.setEnabled(True)
                self.spec_device_settings_combo_box.setEnabled(False)
            elif device_name == "Intel Real Sense":
                self.spec_device_settings_combo_box.setEnabled(True)
                self.port1_combo_box.setEnabled(False)
                self.port2_combo_box.setEnabled(False)
                self.search_ports_button.setEnabled(False)
            else:
                self.port1_combo_box.setEnabled(False)
                self.port2_combo_box.setEnabled(False)
                self.search_ports_button.setEnabled(False)
                self.spec_device_settings_combo_box.setEnabled(False)
                    
                    
        def changeLabel(self, checked):
                if checked == True:
                        self.label.setText("Button of another window checked.")
                else:
                        self.label.setText("Button of another window unchecked.")

        


""" applicationAK = QApplication(sys.argv)
window = SettingsWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
 """

