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


class DeviceWindowTemplate(QMainWindow):

    #
    #
    #
    #Functions needed for initialization

    def __init__(self):
        super().__init__()
        
        #creating Windows from their Templates
        self.control_window = None
        self.terminal_window = None
        self.plot_window = None
        self.info_window = None
        self.device_interface = None
        self.device_thread = QThread(self)

        #uncomment only if testing 
        #and all attributes (control_window, terminal_window, plot_window, info_window and device_thread) are non None
        #self.createGUI()   
        #self.connectGUI()

    def createThreadCommunication(self):
        """
        Function moves the object self.device_control into this thread and starts the thread.
        """
        if self.device_interface is not None:
            #Deploying device to thread
            self.device_interface.moveToThread(self.device_thread)

            #Starting the thread
            self.device_thread.start()
    
    def reinitializeThread(self, state):
        """
        Function terminates the thread and starts it again.
        """
        if state == True:
            self.device_thread.terminate()
            self.createThreadCommunication()

    def destroyThread(self):
        self.device_thread.quit()
        self.device_thread.wait()
    

    #
    #
    #
    #Functions connecting GUI of main device window


    def createGUI(self):
        """
        Function Creates GUI of Main Device Window
        """
        self.setWindowTitle("Device window")
        #self.setGeometry(100, 100, 300, 500)
        self.resize(1920, 1080)
        self.showMaximized()        
    
        #self.layout = QVBoxLayout(self)
        self.createMenu()
        self.createStatusBar()
        self.createWindows()
        self.adjustGUI()

        #Hiding this window by default (since it is not main window of the app but main window for device control)
        self.hide()
        
    
    def createMenu(self):
        """
        Function creates menu bar at the top of the main device window.
        """
        
        #Basic properties of menu bar
        self.menu_bar = QMenuBar(self)
        self.menu_bar.move(0, 0)
        self.menu_bar.setMaximumHeight(30)
        self.menu_bar.adjustSize()
        
        #Creating main menu cards
        # self.device_menu = self.menu_bar.addMenu("&Connection/Device")
        self.window_menu = self.menu_bar.addMenu("&View")
        # self.data_menu = self.menu_bar.addMenu("&Data")
        # self.help_menu = self.menu_bar.addMenu("&Help")
      
        #Creating subcards - actions
        self.show_control = QAction("&Control Panel")
        self.show_terminal = QAction("&Terminal window")
        self.show_graphics = QAction("&Plot")
        self.show_info = QAction("&Info Terminal")
        self.device_info = QAction("&Device Info")
        self.connection_info = QAction("&Connection Info")


        #Adding subcards to proper cards of menu
        self.window_menu_actions = [self.show_control, self.show_graphics, self.show_terminal] 
        self.window_menu.addActions(self.window_menu_actions)

        # self.device_menu_actions = [self.device_info, self.connection_info]
        # self.device_menu.addActions(self.device_menu_actions)


        #Adding menu bar to the window
        self.setMenuBar(self.menu_bar)

    def createStatusBar(self):
        self.status_bar = QStatusBar()  
        self.setStatusBar(self.status_bar)  
        self.status_bar.showMaximized()

    def createWindows(self):
        """
        Function creates windows as a part of main device window
        """

        #Creating dockerizing areas
        self.control_window_area = QDockWidget('Control Panel')
        self.terminal_window_area = QDockWidget('Terminal Window Area')
        self.plot_window_area = QDockWidget('Plot Window')
        self.info_window_area = QDockWidget('Info Window Area')

        self.control_window_area.setGeometry(0,0, 200, 300)
        self.control_window_area.setMinimumSize(100, 200)
        self.terminal_window_area.setMinimumSize(100, 25)
        self.plot_window_area.setMinimumSize(100, 25)
        self.info_window_area.setMinimumSize(100, 25)
        #self.terminal_window_area.size(800,400)

        #self.plot_window_area.showMaximized()

        #Adding widgets to the areas
        self.control_window_area.setWidget(self.control_window)
        self.plot_window_area.setWidget(self.plot_window)
        self.terminal_window_area.setWidget(self.terminal_window)
        self.info_window_area.setWidget(self.info_window)
        #Properties of the areas
        self.control_window_area.setMaximumWidth(500)
        self.control_window_area.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.plot_window_area.setAllowedAreas(Qt.RightDockWidgetArea)
        self.info_window_area.setAllowedAreas(Qt.BottomDockWidgetArea)
        #Default setting of window areas
        self.terminal_window_area.hide()
        self.plot_window_area.hide()
        self.info_window_area.hide()
        
        #Adding Areas to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.control_window_area)
        self.addDockWidget(Qt.RightDockWidgetArea, self.plot_window_area)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.info_window_area)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.terminal_window_area)
    
    
    def adjustGUI(self):

        """Function to implement GUI changes if necessary"""
        
        #implemet changes of gui here

        pass 

    #
    #
    #
    #Functions connecting GUI of



    def connectGUI(self):
        self.connectShowMenu()
        self.connectElements()
        self.connectAdjustedGUI()

    def connectShowMenu(self):
        """Fuction connects windows to menu card 'self.show_menu'. 
            Enables to """
        self.show_control.triggered.connect(self.control_window_area.showNormal)
        self.show_terminal.triggered.connect(self.terminal_window_area.showFullScreen)
        self.show_graphics.triggered.connect(self.plot_window_area.showMaximized)
        self.show_info.triggered.connect(self.info_window_area.show)

    def connectElements(self):
        """
        Function connects the elements, events and threads.
        """
        #Implement connection according to device.
        pass

    def connectAdjustedGUI(self):
        """
        Function connects the elements and events of adjusted GUI.
        """
        #Implement connection according to adjusted window.
        pass
    
    def setElements(self):
        """
        Function enables or disables elements from window or subwindows
        """
        pass
    #
    #
    #Other functionns
    @pyqtSlot(str)
    def setStatusBarText(self, text: str):
        self.status_bar.showMessage(text)

    @pyqtSlot(dict)
    def controlDataFlow(self, dataflow_settings: dict):
        """
        Function enables to control dataflow to subwindows. 
        It receives data from DataFlowWindow.give_settings()
        """
    


class ControlTemplate(QWidget):
    trigger_measure_signal = pyqtSignal(bool)
    

    def __init__(self, parent = None):
        super().__init__()
        #call createGUI function in the implementation 
        
    def createGUI(self):
        """
        Function creates graphical user interface GUI
        """

        pass
        


class TerminalTemplate(QWidget):

    def __init__(self, parent = None):
        """
        parent - superior object (e.g superior window)
        
        If superior object is destroyed the object of this class will be destroyed as well. 
        """
        super().__init__()
        
        #call createGUI in the implementation
    
    def createGUI(self):
        self.setWindowTitle("Terminal Name") #Change 'Terminal name to proper terminal name'
        self.setGeometry(700, 100, 1000, 300) #Change position of terminal if needed

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

    def clearOutputBox(self):
        """
        Function cleaning the terminal
        """
        self.output_box.clear()


class PlotTemplate(QWidget):

    def __init__(self, parent = None):
        """
        parent - superior object (e.g superior window)
        
        If superior object is destroyed the object of this class will be destroyed as well. 
        """

        super().__init__()

        
        #self.setGeometry(700, 100, 1000, 600)
        
    def createGUI(self):
        #Window properties
        self.setWindowTitle("Plot")
        self.createPlot()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.adjustGUI()
        self.setLayout(self.layout)

    def adjustGUI(self):
        """
        Function enables to adjust GUI of plot template.
        """
        pass

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
        self.graph.setLabel('left','Y [mm]')
        self.graph.setLabel('bottom','X [mm]')

    @pyqtSlot(type)
    def updatePlot(self, data):
        """
        Function to receive data from sensor and display in the plot.

        Replace 'type' at he pyqtSlotDecorator with proper data type received from device 
        (nd.array, int, list, dict, etc.)
        
        Extract x_values and y_values from received data  Uncomment self.plot_data 
        """


        self.sensor_position = self.graph_scatter.addPoints([0], [0], brush=pg.mkBrush('r'))
        #Extracting  values 
        #x_values = data[0]
        #y_values = data[1]

        self.graph_scatter.clear() #clearing plot before the update by plotting new position

        #   self.plot_data = self.graph_scatter.addPoints(self.x_values, self.y_values )
        pass



class ConnectionInfoWindow(QWidget):
    

    def __init__(self, parent = None):
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

class InfoWindowTemplate(TerminalTemplate):
    #Note: used in SensorWindows

    def __init__(self, parent = None):
        super().__init__() 

    @pyqtSlot(dict)    
    def createInfo(self,data):
        self.clearOutputBox()
        self.settings_data = data

    
class MainWindow(QMainWindow):

        
        def __init__(self):
            super().__init__()
        
            #self.connectAdjustedGUI()

        def createGUI(self):
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)

                self.adjustGUI()
                self.createMenu()
                self.createStatusBar()

        def adjustGUI(self):
                self.label = QLabel("Sensor Application")
                self.label.setFont(QFont('Times', 18))
                #Settings Window Button            
                self.settings_button = QPushButton("Settings")
                self.settings_button.setFixedSize(200, 50)


                #Sensor Window Button            
                self.run_button = QPushButton("RUN")
                self.run_button.setFixedSize(200, 50)


                #Cancel Window Button
                self.cancel_button = QPushButton("Cancel")
                self.cancel_button.setFixedSize(200, 50)

                #Adding elements to the layout
                self.layout.addWidget(self.run_button, alignment = Qt.AlignCenter )
                self.layout.addWidget(self.settings_button, alignment = Qt.AlignCenter)
                self.layout.addWidget(self.cancel_button, alignment = Qt.AlignCenter )


        def createMenu(self):
            """
            Function creates menu bar at the top of the main device window.
            """
            
            #Basic properties of menu bar
            self.menu_bar = QMenuBar(self)
            self.menu_bar.move(0, 0)
            self.menu_bar.setMaximumHeight(30)
            self.menu_bar.adjustSize()
            
            #Creating main menu cards
            self.device_menu = self.menu_bar.addMenu("&Connection")
            self.help_menu = self.menu_bar.addMenu("&Help")

            #Creating subcards
            self.connection_info = QAction("&Connection Info")
            
            #Adding subcards to proper cards of menu
            self.device_menu.addActions(self.device_menu_actions)

            #Adding menu bar to the window
            self.setMenuBar(self.menu_bar)

        def createStatusBar(self):
            self.status_bar = QStatusBar()  
            self.setStatusBar(self.status_bar)  
            self.status_bar.showMaximized()


class CentralWidgetWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.createGUI()

    def createGUI(self):
        #Creating central widget with info
        self.central_widget = QWidget(self)
        self.central_widget.setMaximumSize(2000, 600)
        self.central_widget.setBaseSize(2000, 600)

        self.info_labelCZ = QLabel()
        self.info_labelCZ.setWordWrap(True)
        self.info_labelCZ.showMaximized()

        self.info_labelEN = QLabel()
        self.info_labelEN.setWordWrap(True)
        self.info_labelEN.showMaximized()

        self.central_widget_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_widget_layout)
        self.central_widget_layout.addWidget(self.info_labelCZ)
        self.central_widget_layout.addWidget(self.info_labelEN)

    def setInfoText(self, text: str, language = 'CZ'):
        """
        Function sets information text in central widget.
        """
        if language == 'CZ':
            self.info_labelCZ.setText(text)
            self.info_labelCZ.setFont(QFont('Times', 10))
        elif language == 'EN':
            self.info_labelEN.setText(text)
            self.info_labelEN.setFont(QFont('Times', 8))

        
        
"""
applicationAK = QApplication(sys.argv)
data = AppValues()

window = ConnectionInfoWindow()
window.createInfo(data.giveSettingsData())
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop
"""

"""
application = QApplication(sys.argv)
window = DeviceWindowTemplate()

window.show()
application.exec()
"""


"""
Sources:

https://www.geeksforgeeks.org/pyqt5-qdockwidget/
https://www.tutorialspoint.com/pyqt/pyqt_qdockwidget.htm 
https://www.pythonguis.com/tutorials/creating-multiple-windows/
https://www.pythonguis.com/tutorials/pyqt-actions-toolbars-menus/
https://www.pythontutorial.net/pyqt/pyqt-qdockwidget/
https://doc.qt.io/qt-6/qdockwidget.html
https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDockWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QDockWidget.setFloating

"""