#This script contains info texts for 'Help Window' of Sensor Application


class Info():

    MainWindowInfoCZ = """
    Vyberte zařízení v nastavení (tlačítko 'Settings') a spusťte okno pro ovládání zařízení (tlačítko 'RUN').
    
    """
    MainWindowInfoEN = """
    Choose the device in 'Settings' and Press 'RUN' to control the device outputs.
    """

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
    SettingsTextEN= """
    Select the desired device.
    The other necessary settings will activate dynamically according to the selected device (each device requires different settings).
   
"""

    SettingsTextCZ = """
    Zvolte zařízení. Ostatní parametry nutná pro nastavení zařízení se zpřístupní dynamicky v závislosti na zařízení.
    (Každé zařízení vyžaduje jiné nastavení).
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
    IntelRealSenseInfoCZ = """
    Spusťte zařízení kliknutím na tlačítko 'Start' a začnětě měřit kliknutím na tlačítko 'Measure'.

    Zastavte měření kliknutím na tlačítko 'Stop'.

    Vyhodnoťte data kliknutím na tlačítko 'Evaluate'.

    Pro volbu vlastních výstupních oken zvolte v horní liště 'Window' a zvolte vybrané výstupy. 
    Optimální je zobrazit 'Terminal Window' a 'Graphical window'.
    """
    
    IntelRealSenseInfoEN = """
    Press 'Start' button to start the device and 'Measure' to start receiving data. 

    Press 'Stop' to stop measuring.

    Click on 'Evaluate' to process data.

    Press 'Window' in Menu bar and display desired window to show window with desired output.
    Optimal windows are 'Terminal Window' and 'Graphical window'. 

"""

    IntelDragDrawInfoCZ = """
    Vyberte oblast (tahněte levým tlačítkem myši přes žádanou oblast v obrázku níže).
    Poté zavřete okno kliknutím na 'x'. 
"""
    IntelDragDrawInfoEN = """
    Select area (drag with left button of mouse over the area in picture below).
    Close the window by clicking on 'x' after selecting wanted area.
"""

    IntelSelectAreaInfoCZ = """
    Tip:    Jaksprávně vybrat oblast?

    V případě, že měříte vzdálenost objektu, vybraná oblast by měla být uvnitř plochy objektu (Velký rozsah vzdáleností z okolí snižuje rozlišení).
    Oblast by měla být malá kvůli lepšímu čtení výstupní matice ve TerminalWindow. (Velká oblast znamená velkou matici o mnoha sloupcích a řádcích a znesnadňuje se tak orientace v ní)

"""
    IntelSelectAreaInfoEN = """
    Tip:    How to choose area in correct way?

    If measuring the distance of certain object selected area should be inside the object (Large distance range can lower the resolution of depth image).
    The area should be small for better reading of output matrix in Terminal Window (Large area can make the reading of the matrix distances more difficult because of too many columns and rows).
"""


    SettingsSearchPortsInfoCZ = """Přiřazené porty k zařízení je potřeba najít ve 'Správce zařízení' (Start -> Správce zařízení)."""

    SettingsSearchPortsInfoEN = """Please look to 'Device  Manager' (Start -> Device Manager) to find what ports are assigned to your device"""

    TIRadarInfoCZ = """
    Spusťte zařízení kliknutím na tlačítko 'Start' a začnětě měřit kliknutím na tlačítko 'Measure'.

    Zastavte měření kliknutím na tlačítko 'Stop'.

    Pro volbu vlastních výstupních oken zvolte v horní liště 'Window' a zvolte vybrané výstupy. 
    Optimální je zobrazit 'Terminal Window' a 'Graphical window'.
    """
    
    TIRadarInfoEN = """
    Press 'Start' button to start the device and 'Measure' to start receiving data. 

    Press 'Stop' to stop measuring.

    Press 'Window' in Menu bar and display desired window to show window with desired output.
    Optimal windows are 'Terminal Window' and 'Graphical window'. 

"""