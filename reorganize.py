#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path


class ProjectReorganizer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.new_structure = {
            "docs": ["README.md", "l515.md"],
            "src": {
                "config": ["konfigurace.cfg", "AppValues.py"],
                "core": ["main.py"],
                "gui": {
                    "windows": {
                        "device_windows": [
                            "IntelRealSenseWindows.py",
                            "TIRadarWindows.py",
                            "RPLidarWindows.py",
                            "TOFWindows.py",
                            "SensorWindows.py",
                        ],
                        "": [
                            "MainWindow.py",
                            "SettingsWindow.py",
                            "HelpWindows.py",
                            "WindowsTemplates.py",
                            "PointCloudWindow.py",
                            "DataFlowWindow.py",
                        ],
                    }
                },
                "devices": {
                    "interfaces": ["device_interfaces/*"],
                    "scripts": ["device_scripts/*", "source_rp/*"],
                },
                "utils": ["app_functions/*"],
                "resources": {"": ["Info.py"], "strings": [], "icons": []},
            },
        }

        # Create backup
        self.backup_dir = self.source_dir.parent / f"{self.source_dir.name}_backup"
        self.create_backup()

    def create_backup(self):
        """Create a backup of the current directory"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.source_dir, self.backup_dir)
        print(f"Created backup at {self.backup_dir}")

    def create_directory_structure(self):
        """Create the new directory structure"""

        def create_dirs(base_path, structure):
            if isinstance(structure, dict):
                for dir_name, content in structure.items():
                    dir_path = base_path / dir_name
                    dir_path.mkdir(parents=True, exist_ok=True)
                    create_dirs(dir_path, content)
            elif isinstance(structure, list):
                for item in structure:
                    if "*" in item:
                        # Handle wildcard patterns
                        pattern = item.split("/")[-1]
                        source_dir = self.source_dir / "/".join(item.split("/")[:-1])
                        if source_dir.exists():
                            for file in source_dir.glob(pattern):
                                if file.is_file():
                                    shutil.copy2(file, base_path)
                    else:
                        # Handle specific files
                        source_file = self.source_dir / item
                        if source_file.exists():
                            shutil.copy2(source_file, base_path)

        # Create new structure
        new_base = self.source_dir.parent / f"{self.source_dir.name}_new"
        if new_base.exists():
            shutil.rmtree(new_base)
        new_base.mkdir(parents=True)
        create_dirs(new_base, self.new_structure)

    def update_imports(self):
        """Update import statements in Python files"""

        def update_file_imports(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Update relative imports
            import_patterns = [
                (
                    r"from (WindowsTemplates|MainWindow|SettingsWindow|HelpWindows|IntelRealSenseWindows|TIRadarWindows|RPLidarWindows|TOFWindows|SensorWindows|PointCloudWindow|DataFlowWindow) import",
                    r"from src.gui.windows.\1 import",
                ),
                (
                    r"from (device_interfaces\.[^.]+) import",
                    r"from src.devices.interfaces.\1 import",
                ),
                (r"from (app_functions\.[^.]+) import", r"from src.utils.\1 import"),
                (r"from (Info) import", r"from src.resources.\1 import"),
                (r"from (AppValues) import", r"from src.config.\1 import"),
            ]

            for pattern, replacement in import_patterns:
                content = re.sub(pattern, replacement, content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        # Update imports in all Python files
        for root, _, files in os.walk(
            self.source_dir.parent / f"{self.source_dir.name}_new"
        ):
            for file in files:
                if file.endswith(".py"):
                    update_file_imports(Path(root) / file)

    def create_init_files(self):
        """Create __init__.py files in all Python packages"""

        def create_inits(base_path):
            for root, dirs, _ in os.walk(base_path):
                if any(f.endswith(".py") for f in os.listdir(root)):
                    init_file = Path(root) / "__init__.py"
                    if not init_file.exists():
                        init_file.touch()

        create_inits(self.source_dir.parent / f"{self.source_dir.name}_new")

    def create_requirements(self):
        """Create requirements files"""
        requirements_dir = (
            self.source_dir.parent / f"{self.source_dir.name}_new" / "requirements"
        )
        requirements_dir.mkdir(exist_ok=True)

        # Main requirements
        with open(requirements_dir / "requirements.txt", "w") as f:
            f.write(
                """PyQt5
numpy
matplotlib
opencv-python
pyrealsense2
pyqtgraph
adafruit-circuitpython-rplidar
"""
            )

        # Ubuntu-specific requirements
        with open(requirements_dir / "requirements-ubuntu.txt", "w") as f:
            f.write(
                """# Ubuntu-specific requirements
librealsense2-dkms
librealsense2-utils
librealsense2-dev
librealsense2-dbg
"""
            )

    def create_setup_scripts(self):
        """Create setup and installation scripts"""
        scripts_dir = self.source_dir.parent / f"{self.source_dir.name}_new" / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # Create install.sh
        with open(scripts_dir / "install.sh", "w") as f:
            f.write(
                """#!/bin/bash
# Installation script for Sensor Control Application

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements/requirements.txt

# Install Ubuntu-specific requirements if on Ubuntu
if [ -f /etc/lsb-release ]; then
    sudo apt-get update
    sudo apt-get install -y $(cat requirements/requirements-ubuntu.txt | grep -v '^#')
fi

# Create necessary directories
mkdir -p logs
mkdir -p data

echo "Installation complete!"
"""
            )

        # Make script executable
        os.chmod(scripts_dir / "install.sh", 0o755)

    def reorganize(self):
        """Execute the complete reorganization process"""
        try:
            print("Starting project reorganization...")
            self.create_directory_structure()
            print("Created new directory structure")

            self.update_imports()
            print("Updated import statements")

            self.create_init_files()
            print("Created __init__.py files")

            self.create_requirements()
            print("Created requirements files")

            self.create_setup_scripts()
            print("Created setup scripts")

            print("\nReorganization complete!")
            print(
                f"New structure created at: {self.source_dir.parent}/{self.source_dir.name}_new"
            )
            print(f"Backup created at: {self.backup_dir}")
            print("\nTo complete the reorganization:")
            print("1. Review the new structure")
            print("2. Test the application in the new structure")
            print("3. If everything works, replace the old structure with the new one")

        except Exception as e:
            print(f"Error during reorganization: {str(e)}")
            print("Restoring from backup...")
            if self.backup_dir.exists():
                shutil.rmtree(self.source_dir)
                shutil.copytree(self.backup_dir, self.source_dir)
            raise


if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create and run the reorganizer
    reorganizer = ProjectReorganizer(current_dir)
    reorganizer.reorganize()
