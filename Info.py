#This script contains info texts for 'Help Window' of Sensor Application


class Info():

    windows_port_names = {
        "RP Lidar": "Silicon Labs CP210x USB to UART Bridge (COM N)"


    }

    About_text= """
    The app is designed to control various sensors and display the output of the sensors.
"""

    Introduction_text = """
    The Sensor Application is controlling software which enables you to control various sensors and their output.
    It also enables you to observe the graphical representation of the data.\n
    After opening the app you are in main window. Click on 'Settings' and select desired sensor in combo box 'Device'.
    (note: please be sure your device is connected otherwise you won't be able to find it).\n
    After selection of desired device the settings varies according the type of the device. 
    Some devices need to set on or more ports some don't.
    The settings enables automatically othe proper settings according the selected device.\n 
    In case your device needs to set the port you probably will need to check it in the Device Manager on Windows or in similar place where you can check connceted ports and infos about them 
    in other OS.\n
    

"""
    Settings_text= """
    Settings:

    \n\nPlease select device in device list. After that proper port settings gets enabled. Choose right port (check in Device Manger if necessary). 
    Press 'OK' and close the SettingsWindow.
    \nSome devices use only one port, some use two ports while the others don't need to set the port (the settings is done automatically).
    \nWindows ports can be found under Start -> Device Manager -> COM Ports.
   
"""
    windows_use = """
    After opening the application click on 'Settings' in the main window. 
    After proper settings (see 'Settings' below) close 'SettingsWindow' and click 'Run Device'.
    If the settings has been made properly and the device is connected the window for device control opens.
    \n\n
    If you want to change the device, close window with the current device and repeat the setting process. 
"""
    RPLidarSettings_text = f"""
    RP Lidar uses one port. \n
    
    \nWindows OS
    In Device Manger in Windows the device is under the name: {windows_port_names["RP Lidar"]}. 
    Select 'Port N' (N - Number of port) in the 'Settings'
    
    
    """

    IntelRealSenseSettings_text = f"""
    Intel Real Sense devices do not need to configure port. Their control library does it automatically.
    It only needs to specify the serial number in the case that more Intel Real Sense devices are connected.
    """
     
    SensorSettings_text = """
    'Sensor' is software simulation of device. It can be used when no device is connected. Therefore it does not require to select ports or other extra settings.\n 
    'Sensor' contains algorithm to generate dummy data of time and some value. The value can  be e.g. simualation of distance or whatever else.
""" 