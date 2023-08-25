#Templates for windows of SensorApplication
#Only GUIs - menu bar, status bar and layout are created
#No buttons or other elements are added (will be added in implementation)
#Also slots are created but not connected  


import sys
import time

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from pyqtgraph import  plot, mkPen, PlotItem, ScatterPlotWidget, ScatterPlotItem, mkBrush
import pyqtgraph as pg


class ControlTemplate(QWidget):
    trigger_measure_signal = pyqtSignal(bool)
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel - Sensor")
        self.setGeometry(100, 100, 300, 500)
        self.device_control = None
        #self.communication_thread = QThread(self)
        self.terminal = None #use child 'TerminalWindow(self)' inherited from 'TerminalTemplate'
        self.plot_window = None #iuse child 'PlotWindow(self)' inherited from 'PlotTemplate'
        #self.create_thread_communication() #uncomment after creating Thread
        
    def createMenu(self):
        #Creating menu
        self.menu_bar = QMenuBar(self)
        self.menu_bar.move(0, 0)
        self.menu_bar.setMaximumHeight(30)

        #Creating main menu cards
        self.device_menu = self.menu_bar.addMenu("&Connection/Device")
        self.show_menu = self.menu_bar.addMenu("&Show")
        self.data_menu = self.menu_bar.addMenu("&Data")
        self.data_menu = self.menu_bar.addMenu("&Help")
      
        #Creating subcards - actions
        self.show_terminal = QAction("&Terminal window")
        self.show_graphics = QAction("&Graphical window")
        self.device_connection= QAction("&Connection")
        self.device_info = QAction("&Device Info")
        self.connection_info = QAction("&Connection Info")

        #Adding subcards to proper cards of menu
        self.show_menu.addAction(self.show_terminal)
        self.show_menu.addAction(self.show_graphics)
        self.device_menu.addAction(self.device_info)
        self.device_menu.addAction(self.connection_info)
        

    def createGUI(self):
        """
        Function creates graphical user interface GUI
        """


        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def createStatusBar(self):
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

    def adjustGUI(self):
        """
        Implement other elements (buttons, texts, sliders, etc.) according to the necessity of particular device

        Use 'self.layout.addWidget(element)' to add your element to the layout

        Use function after self.createGUI or super().__init__() if your class is inherited from this class.
        Attribute 'self.layout' will be created when inheriting from this calss 
        therefore it must be created before  element can be added to the layout


        """

        #Creating element  - example:

        #self.button = QPushButton(self)
        #self.button.setGeometry(50, 50, 200, 25)
        #self.layout.addWidget(self.start_button)

        pass
    
    def connectGUI(self):
        """
        Function creates connection between elements in the GUI.
        """
        pass

    
    
    def showTerminalWindow(self):

        #Uncomment after creating proper  object of type PlotWindow inherited from (TerminalTemplate)

        #self.terminal.show()
        pass
    
    def showGraphicWindow(self):

        #Uncomment after creating proper object of type PlotWindow inherited from (PlotTemplate)
        
        #self.plot_window.createPlot()
        #self.plot_window.show()

        pass




    def createThreadCommunication(self):
        """
        Function moves the object self.device_control into this thread and starts the thread.
        """
        
        #Uncomment after creating proper child and ints object of type QThread

        #self.device_control.moveToThread(self.communication_thread)
        #self.communication_thread.start()
        pass
    
    def reinitializeThread(self, state):
        """
        Function terminates the thread and starts it again.
        """

        #Uncomment after creating proper child and ints object of type QThread
        #if state == True:
        #    self.communication_thread.terminate()
        #    self.create_thread_communication()
        pass

    @pyqtSlot(str)
    def receiveMessage(self, message: str):
        """
        Function receives messages e.g. from data receiving thread (thread connected to device)
        and displays them in status bar.
        """
        self.status_bar.showMessage(message)
    


class TerminalTemplate(QWidget):

    def __init__(self, parent):
        """
        parent - superior object (e.g superior window)
        
        If superior object is destroyed the object of this class will be destroyed as well. 
        """
        super().__init__()
        self.setWindowTitle("Terminal Name") #Change 'Terminal name to proper terminal name'
        self.setGeometry(700, 100, 500, 300) #Change position of terminal if needed
        self.createGUI()
    
    def createGUI(self):
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.output_box)
        self.setLayout(self.layout)
    
    @pyqtSlot(type)
    def receiveData(self, data):
        """
        Function to receive data from sensor and display them in the text window.

        Replace type with proper data type received from device (nd.array, int, list, dict, etc.)
        """
        pass

class PlotTemplate(QWidget):

    def __init__(self, parent):
        """
        parent - superior object (e.g superior window)
        
        If superior object is destroyed the object of this class will be destroyed as well. 
        """

        super().__init__()

        self.setWindowTitle("Plot")
        self.setGeometry(700, 100, 800, 600)
        
    def createGUI(self):
        self.createPlot()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)

    def createPlot(self):
        """
        Separate function to create the plot. 
        If the plot is created in self.createGUI which is called only when object is created, 
        than the plot is not going to show when the window is closed and reopened therefore the separate function.

        Function must be called always before self.show() function.
        """
        self.graph = plot()
        self.graph.setBackground('w')
        self.graph_scatter = ScatterPlotItem(size = 10, brush=pg.mkBrush(30, 255, 0, 255) )
        self.graph.addItem(self.graph_scatter)
        #self.graph.addItem(self.center_scatter)
        self.graph.setXRange(-3, 3)
        self.graph.setYRange(-3,3)

    @pyqtSlot(type)
    def updatePlot(self, data):
        """
        Function to receive data from sensor and display in the plot.

        Replace 'type' at he pyqtSlotDecorator with proper data type received from device 
        (nd.array, int, list, dict, etc.)
        
        Extract x_values and y_values from received data  Uncomment self.plot_data 
        """

        #Extracting  values 
        #x_values = data[0]
        #y_values = data[1]

        self.graph_scatter.clear() #clearing plot before the update by plotting new position

        #   self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values )
        pass



class ConnectionInfoWindow(QWidget):
    

    def __init__(self):
        super().__init__()
        self.x = 11
        self.createGUI( )

        
    @pyqtSlot(dict)    
    def createInfo(self,data):
        self.settings_data = data
        self.info_text = f"""
        Device: {self.settings_data["Device"]}\n
        Port 1: {self.settings_data["Port 1"]}\n
        Port 2: {self.settings_data["Port 2"]}\n
        """
        self.info_label.setText(self.info_text)

    def createGUI(self):
        self.setGeometry(200, 100, 300, 300)

        self.info_label = QLabel()
        self.info_label.setFont(QFont('Ms Shell Dlg 2', 8))
        self.info_label.setText("")

        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.info_label)
        self.setLayout(self.layout)

class SettingsInfoWindo(QWidget):

    def __init__(self):
        super().__init__()
        self.x = 11
        self.createGUI( )

    def createGUI(self):
        self.setGeometry(200, 100, 300, 300)

        self.info_label = QLabel("Settings Info")
        

    @pyqtSlot(dict)    
    def createInfo(self,data):
        self.settings_data = data

    
class MainWindowContent(QWidget):

        
        def __init__(self):
            super().__init__()
            self.createGUI()
            
            self.show()
        
            #self.connectAdjustedGUI()

        def createGUI(self):
                self.layout = QGridLayout()
                

                self.label = QLabel("Sensor Application")
                self.label.setFont(QFont('Times', 18))
                #Settings Window Button            
                self.settings_button = QPushButton(self)
                self.settings_button.setFixedSize(300, 100)
                self.settings_button.setText("Settings")


                #Sensor Window Button            
                self.run_button = QPushButton(self)
                self.run_button.setText("Run")
                self.run_button.setFixedSize(300, 100)
                self.layout.addWidget(self.settings_button, 1, 1)
                self.layout.addWidget(self.run_button,2,1)

                self.setLayout(self.layout)

        
"""
applicationAK = QApplication(sys.argv)
data = AppValues()

window = ConnectionInfoWindow()
window.createInfo(data.giveSettingsData())
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
"""