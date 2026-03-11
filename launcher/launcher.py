"""
Launcher script for TodoApp.

This script scans the 'versions/' directory next to the executable,
finds the folder with the highest version number (e.g., 'app-v2.0.7'),
and launches the 'TodoApp.exe' from inside that folder.
"""
import os
import sys
import subprocess
from packaging import version


def main():
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    versions_dir = os.path.join(base_dir, "versions")
    
    if not os.path.exists(versions_dir):
        print(f"Error: Versions directory not found at {versions_dir}")
        sys.exit(1)

    available_versions = []
    
    for folder in os.listdir(versions_dir):
        if folder.startswith("app-v"):
            ver_str = folder.replace("app-v", "")
            try:
                parsed_ver = version.parse(ver_str)
                available_versions.append((parsed_ver, folder))
            except version.InvalidVersion:
                pass

    if not available_versions:
        print(f"Error: No valid version folders found in {versions_dir}")
        sys.exit(1)

    # Sort versions and pick the highest one
    available_versions.sort(key=lambda x: x[0], reverse=True)
    highest_version_folder = available_versions[0][1]
    
    app_path = os.path.join(versions_dir, highest_version_folder, "TodoApp.exe")
    
    if not os.path.exists(app_path):
        print(f"Error: Target executable not found at {app_path}")
        sys.exit(1)
        
    print(f"Launching version {available_versions[0][0]} from {app_path}")
    
    # Launch the target executable and exit the launcher
    subprocess.Popen([app_path])
    sys.exit(0)


if __name__ == "__main__":
    main()
