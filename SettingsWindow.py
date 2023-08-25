import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject

class SettingsWindow(QWidget):
        
        settings_signal = pyqtSignal(dict) #dictionary containing settings information


        def __init__(self):
            super().__init__()
            
            self.device_list = ["No device","RP Lidar", "TI Radar", "Time of Flight", "Intel Real Sense L500", "Intel Real Sense  D435i Dev 1", "Intel Real Sense S435i Dev 2", "Sensor"]
            self.port_list = ["No port"]
            self.createGUI()
            self.connectGUI()
            

        def createGUI(self):
            #Button to search available ports
            self.ok_button = QPushButton("OK")
            self.ok_button.setMaximumWidth(150)
            self.search_ports_button = QPushButton("Search ports")
            self.search_ports_button.setMaximumHeight(30)
            self.search_ports_button.setMaximumWidth(150)

            self.device_combo_box = QComboBox()
            self.device_combo_box.setMaximumWidth(200)

            self.port1_combo_box = QComboBox()
            self.port1_combo_box.setEnabled(False)
            self.port1_combo_box.setMaximumWidth(200)
            self.port2_combo_box = QComboBox()
            self.port2_combo_box.setEnabled(False)
            self.port2_combo_box.setMaximumWidth(200)
            self.device_label = QLabel("Device: ")
            self.port1_label = QLabel("Port 1: ") 
            self.port2_label = QLabel("Port 2: ")

            self.layout = QGridLayout()
            self.setLayout(self.layout)
            self.setGeometry(50, 50, 800, 600)
            
            self.layout.addWidget(self.device_label, 0, 0, 4, 4)
            self.layout.addWidget(self.port1_label,  1, 0, 4, 4)
            self.layout.addWidget(self.port2_label,  2, 0, 4, 4)

            self.layout.addWidget(self.device_combo_box, 0, 1, 4, 4)
            self.layout.addWidget(self.port1_combo_box,  1, 1, 4, 4)
            self.layout.addWidget(self.port2_combo_box,  2, 1, 4, 4)

            self.layout.addWidget(self.ok_button,  3, 3, 4, 4)
            self.layout.addWidget(self.search_ports_button, 1, 3, 4, 4)
            

            self.device_combo_box.addItems(self.device_list)
            self.port1_combo_box.addItems(self.port_list)
            self.port2_combo_box.addItems(self.port_list)
            self.move(300, 150)
            self.setWindowTitle('Settings Window')  


        def connectGUI(self):
            self.search_ports_button.clicked.connect(self.searchPorts) 
            self.device_combo_box.activated[str].connect(self.controlPortCombos)   
            self.ok_button.clicked.connect(self.okClicked)

        def okClicked(self):
            settings_dictionary= {
                "Device": self.device_combo_box.currentText(),
                "Port 1": self.port1_combo_box.currentText(),
                "Port 2": self.port2_combo_box.currentText()
                }
            self.settings_signal.emit(settings_dictionary)

    
        def searchPorts(self):
            self.port1_combo_box.clear()
            self.port2_combo_box.clear()
            port_list = QSerialPortInfo.availablePorts()
            port_names = []
            for port in port_list:
                port_names.append(port.portName())

            self.port1_combo_box.addItems(port_names) 
            self.port2_combo_box.addItems(port_names) 

        def controlPortCombos(self, device_name):
              if device_name == "RP Lidar" or device_name == "Time of Flight":
                    self.port1_combo_box.setEnabled(True)
              elif device_name == "TI Radar":
                    self.port1_combo_box.setEnabled(True)
                    self.port2_combo_box.setEnabled(True)
              else:
                    self.port1_combo_box.setEnabled(False)
                    self.port2_combo_box.setEnabled(False)
                    
                    
        def changeLabel(self, checked):
                if checked == True:
                        self.label.setText("Button of another window checked.")
                else:
                        self.label.setText("Button of another window unchecked.")

        

"""

applicationAK = QApplication(sys.argv)
window = SettingsWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop

""" 
