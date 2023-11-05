import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from Info import Info
from PyQt5.QtWidgets import (QApplication, QWidget,QGridLayout, QHBoxLayout, QPushButton, QScrollArea,
                              QTextEdit, QLabel, QVBoxLayout, QTreeWidget, QTreeWidgetItem)



class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.info = Info() #class containing all info_texts
        
        self.createGUI()
        self.connectGUI()
        self.close()
        
    
    def connectGUI(self):
        self.tree.itemClicked.connect(self.setSelectedItem)


    def createTree(self):
        """
        Function creates menu in Help Window in the form of tree layout
        """
        #Creating tree object
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Sensor Application")
        self.tree.setMaximumWidth(250)

        #Creating main branches of the tree
        self.about_item = QTreeWidgetItem(self.tree)
        self.about_item.setText(0, "About")

        self.intro_item = QTreeWidgetItem(self.tree)
        self.intro_item.setText(0, "Introduction")

        self.windows_use_item = QTreeWidgetItem(self.tree)
        self.windows_use_item.setText(0, "Windows/Device Use")

        #Creating subbranches of branch 'self.windows_use_item'
        self.rplidar_use_item = QTreeWidgetItem(self.windows_use_item)
        self.rplidar_use_item.setText(0,"RP Lidar Window")
        self.tiradar_use_item = QTreeWidgetItem(self.windows_use_item)
        self.tiradar_use_item.setText(0,"TI Radar Window")
        self.intelrealsense_use_item = QTreeWidgetItem(self.windows_use_item)
        self.intelrealsense_use_item.setText(0,"Intel Real Sense Window")
        self.tof_use_item = QTreeWidgetItem(self.windows_use_item)
        self.tof_use_item.setText(0,"Time Of Flight Window")
        self.sensor_use_item = QTreeWidgetItem(self.windows_use_item)
        self.sensor_use_item.setText(0,"Sensor Window")
        self.settings_use = QTreeWidgetItem(self.windows_use_item)
        self.sensor_use_item.setText(0,"Sensor Window")
        


        #Adding branches and subbranches 

        #Adding main branches to the tree
        self.tree.addTopLevelItem(self.about_item)
        self.tree.addTopLevelItem(self.windows_use_item)

        #Adding Children to main branch 'self.windows_use_item '
        self.windows_use_item.addChild(self.rplidar_use_item)
        self.windows_use_item.addChild(self.intelrealsense_use_item)
        self.windows_use_item.addChild(self.tiradar_use_item)
        self.windows_use_item.addChild(self.tof_use_item)
        self.windows_use_item.addChild(self.sensor_use_item)

        
    def createGUI(self):
        self.setWindowTitle("Help")
        self.createTree()
        self.info_layout = QWidget()
        self.info_layout.layout = QVBoxLayout()

        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)


        #Right palette of info text
        self.info_content = QLabel("")
        self.info_content.setText(self.info.About_text)
        self.info_content.setWordWrap(True)
        self.info_layout.layout.addWidget(self.info_content)
        self.content_area.setWidget(self.info_content)
        #self.info_layout.setLayout(self.info_layout.layout)



        

        self.layout = QHBoxLayout()
        #self.layout.addWidget(self.button_layout)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.content_area)
        self.setLayout(self.layout)

    def setSelectedItem(self, item, column):
        """
        Function receives signal from tree when item is clicked.
        According to clicked item the info_content lable changes and provides info.
        Calls function showInfo which displays proper info
        
        Inputs:
        item: QTreeWidgetItem
        column: number of column in which the item was created in the tree

        """
        selected_item = item.text(column)
        self.showInfo(selected_item)
        

    def showInfo (self, selected_item_name: str):
        
        selected_item = selected_item_name

        if selected_item == "About":
            self.setInfo(Info.About_text)

        elif selected_item == "Introduction":
            self.setInfo(Info.Introduction_text)

        elif selected_item == "Settings Window":
            self.setInfo(Info.SettingsTextCZ + Info.SettingsTextEN)
        elif selected_item == "RP Lidar Window":
            self.setInfo(Info.RPLidarSettings_text)
        elif selected_item == "Intel Real Sense Window":
            self.setInfo(Info.IntelRealSenseSettings_text)
        if selected_item == "Sensor Window":
            self.setInfo(Info.SensorSettings_text)
    

    def receiveInfoRequest(self, selected_item: str):
        """
        Function receives requests in form of item names and calls self.showInfo() to show proper content.
        """
        self.showInfo(selected_item)

    def setInfo(self, info_text):
        self.info_content.setText(info_text)

    




""" 
applicationAK = QApplication(sys.argv)
window = HelpWindow()
window.show() #windows are hidden by default
applicationAK.exec_() # exec() function starts the event loop
 """

