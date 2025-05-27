# Hoover_2025
# Sensor Control Application

A comprehensive desktop application for controlling and visualizing data from various sensors, built with PyQt5. The application provides a user-friendly interface for managing multiple types of sensors and viewing their data in real-time.

## Supported Sensors

- RP Lidar
- TI Radar
- Intel RealSense Devices
  - Intel Lidar L515
  - Intel DepthCamera D435 (Front and Back)
- Time of Flight (TOF) Sensors
- Generic Sensor Simulation

## Features

- **Multi-Sensor Support**: Control and monitor multiple types of sensors through a unified interface
- **Real-time Visualization**: View sensor data through various visualization windows
  - Terminal Window for raw data
  - Plot Window for graphical representation
  - Control Panel for device management
  - Info Terminal for device status
- **Device Management**: Easy device selection and configuration through the Settings window
- **Bilingual Interface**: Support for both English and Czech languages
- **Help System**: Comprehensive help documentation accessible through the Help window

## Requirements

- Python 3.8 or higher
- PyQt5
- NumPy
- Matplotlib
- OpenCV (for Intel RealSense support)
- pyrealsense2 (for Intel RealSense devices)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd SensorControlApp_Jetson
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the application:
```bash
python MainWindow.py
```

2. In the main window:
   - Click "Settings" to configure your sensor
   - Select the desired device from the available options
   - Configure any necessary ports or device-specific settings
   - Click "RUN" to start the sensor control window

3. In the sensor control window:
   - Use the Control Panel to manage device operations
   - View real-time data in the Terminal window
   - Monitor graphical representations in the Plot window
   - Access device information through the Info Terminal

## Device-Specific Notes

### RP Lidar
- Requires COM port configuration
- Appears as "Silicon Labs CP210x USB to UART Bridge" in Device Manager

### Intel RealSense Devices
- Automatic port detection
- Serial number required when multiple devices are connected
- Supports both L515 Lidar and D435 Depth Camera models

### TI Radar
- Requires two COM ports for operation

### Time of Flight (TOF)
- Requires COM port configuration

## Project Structure

```    
source/
├── MainWindow.py # Main application window
├── SettingsWindow.py # Device configuration window
├── HelpWindows.py # Help documentation interface
├── device_interfaces/ # Device-specific interface implementations
├── device_scripts/ # Device control scripts
├── app_functions/ # Utility functions
├── app_info/ # Application information
└── source_rp/ # RP Lidar specific code

```

