import sys
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class DeviceTemplate(QObject):
    """
    
    Class representing unified interface to control the devices and therefore easy connection with GUI interface.
    

    Class is designed to run in measuring thread independent of the GUI (except the initialization of the thread).
    Therefore the signals are used. 
    When the function has been triggered (by receiving the data from the device or e.g. by button from main GUI thread),
    the signal is emitted and connected to main thread.
    The connection must be done in main thread
    """



    #Signals ....

    """
    Implement signals which the oject of the class 'Device' will emit
    """

    #xExample
    #data_signal =pyqtSignal(tuple)
    #end_thread_signal = pyqtSignal(bool)



    def __init__(self, parent):
        super().__init__()  
        self.data_state = True
        self.device_running = False
        self.measuring_running = False
        #self.device = None     #attribute - object representing object of library able to control the device

    
    def startDevice(self):
        """
        Implement function able to start the device 
        """
        self.device_running = True
        #self.device.start()

    def stopDevice(self):
        """
        Implement function able to stop the device 
        """
        self.device_running = False
        self.measuring_running = False
        #self.device.stop()

    @pyqtSlot()
    def measureData(self):
        """
        Function for data receive.
        Function generates signal emiting the tuple 'data'. 
        In case termination of function is required it is necessary to terminate the whole thread (use 'end_thread_signal').
        
        time.sleep() enables the GUI in the main thread to update properly.
        It affects the speed of plot and camera windows as well as the terminal window
        """
        while self.device_running == True:
            time.sleep(0.05) 

            #data = self.device.receive_data()  #function of device library to receive the data from device
            #self.data_signal.emit(data)
        pass

    def getDeviceInfo(self):
        """
        Implement function able to give info about the device 
        """
        pass