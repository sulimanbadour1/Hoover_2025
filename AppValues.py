from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, QTimer
from PyQt5.QtWidgets import  (QApplication, 
                        QWidget )

class  AppValues(QObject):
    """
    Class representing current settings and saved data
    """
    update_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.settings_data= {
                "Device": "No Device",
                "Port 1": "No Port",
                "Port 2": "No port",
                "Device specification": "No specification",
                "Serial number": "No serial number"
                } 
        self.name = "Nm"#dictionary to save current settings when settings window is closed 
    
    
    @pyqtSlot(dict)
    def receiveSettingsData(self, data):
        """
        Function receive settings data from 'Settings Window' after confirmation by 'OK' in Settings window
        
        """
        self.settings_data = data
        self.updateSettingsData()

    def updateSettingsData(self):
        """
        Function sends signal with updates values to every Slot connected to it.
        """
        self.update_signal.emit(self.settings_data)
    
    def giveSettingsData(self):
        return self.settings_data
    
    

