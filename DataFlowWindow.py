from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QTextFormat, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import sys

class DataFlowWindow(QWidget):
    info_text = """
    \n
    Control dataflow to individual sub windows of the Device Window (e.g. Plot Window, Terminal Window, etc.)\n
    Check the checkbox of the dataflow od desired window if you want data to be displayed at that window and press 'OK'.\n
    Please be aware that allowing dataflow to too many sub windows can cause freezing or even crash of the application.\n
    Be careful especially with graphical windows.\n
    Two graphical windows and one terminal window should work fine.\n
    """
    data_signal = pyqtSignal(dict) #signal to emit data


    def __init__ (self, parent = None):
        super().__init__()

        self.createGUI()
        self.connectGUI()
        self.presetElements()
        
    def createGUI(self):
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #Properties of the window
        self.setWindowTitle("Control Dataflow")
        self.move(300, 150)
        self.setFixedSize(600, 600)

        #creating content
        self.createCheckBoxArea()
        self.createDescriptionArea()
        self.createConfirmGUI()

        #addinf elements to main layout
        self.layout.addWidget(self.heading, alignment = Qt.AlignLeft)
        self.layout.addWidget(self.textlabel, alignment = Qt.AlignLeft )
        self.layout.addWidget(self.checkbox_area, alignment = Qt.AlignLeft)
        self.layout.addWidget(self.ok_widget)

    def createCheckBoxArea(self):

        self.plot_dataflow_chbox = QCheckBox("Plot window")
        self.terminal_dataflow_chbox = QCheckBox("Terminal window")
        self.camera_dataflow_chbox = QCheckBox("Camera window")
        self.point_cloud_dataflow_chbox = QCheckBox("Point Cloud window")
        self.plot_dataflow_chbox.adjustSize()
        self.terminal_dataflow_chbox.adjustSize()
        self.camera_dataflow_chbox.adjustSize()
        self.point_cloud_dataflow_chbox.adjustSize()

        self.checkbox_area = QGroupBox("Control Dataflow")
        self.checkbox_area.adjustSize()
        self.checkbox_area.showMaximized()
        self.checkbox_area_layout = QVBoxLayout()
        self.checkbox_area.setLayout(self.checkbox_area_layout)
        self.checkbox_area_layout.addWidget(self.plot_dataflow_chbox)
        self.checkbox_area_layout.addWidget(self.terminal_dataflow_chbox)
        self.checkbox_area_layout.addWidget(self.camera_dataflow_chbox)
        self.checkbox_area_layout.addWidget(self.point_cloud_dataflow_chbox)


    def createDescriptionArea(self):
        self.heading = QLabel("Dataflow control")
        self.heading.setFont(QFont('Times', 10))
        self.heading.setStatusTip('Bold')
        self.textlabel  = QLabel()
        self.textlabel.setWordWrap(True)
        self.textlabel.setText(self.info_text)

    def createConfirmGUI(self):
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

    def presetElements(self):
        """
        Function presets elements to the default value.
        """
        self.point_cloud_dataflow_chbox.setEnabled(False)
        self.camera_dataflow_chbox.setEnabled(False)


    def adjustGUI(self):
        pass

    
    def connectGUI(self):
        self.ok_button.clicked.connect(self.give_settings)
        self.ok_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.close)

    def give_settings(self):
        """
        Function checks the state of checkboxes and emits them with the help of data_signal.
        """
        self.set_values= {
            "plot": self.plot_dataflow_chbox.isChecked(),
            "terminal": self.terminal_dataflow_chbox.isChecked(),
            "camera": self.camera_dataflow_chbox.isChecked(),
            "point cloud": self.point_cloud_dataflow_chbox.isChecked()

        }
        self.data_signal.emit(self.set_values)

    


""" applicationAK = QApplication(sys.argv)
window = DataFlowWindow()
window.show() #windows are hidden by default
applicationAK.exec() # exec() function starts the event loop """