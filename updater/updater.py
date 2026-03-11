import os
import subprocess
import requests
import sys
from version import latest

APP_NAME = "TodoApp.exe"
NEW_APP = "TodoApp_new.exe"


def get_latest_release():
    r = requests.get(latest, timeout=10)
    r.raise_for_status()
    return r.json()


def get_download_url(release):
    assets = release.get("assets", [])

    if not assets:
        raise RuntimeError("No release assets found")

    # Find the executable asset, not the zip
    for asset in assets:
        if asset["name"] == "TodoApp.exe":
            return asset["browser_download_url"]

    # Fallback to the first asset if not found
    return assets[0]["browser_download_url"]


def download_file(url, dest):
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()

        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def install_update():
    release = get_latest_release()
    url = get_download_url(release)
    version_tag = release.get("tag_name", "unknown").replace("v", "")
    
    # We are running from versions/app-vX.X.X/ backend, so we need to go up two directories
    # to find the main versions folder if running compiled, or use local dir for dev.
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
    else:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        
    versions_dir = os.path.join(base_dir, "versions")
    os.makedirs(versions_dir, exist_ok=True)
    
    new_version_dir = os.path.join(versions_dir, f"app-v{version_tag}")
    if os.path.exists(new_version_dir):
        print(f"Version {version_tag} is already downloaded.")
        return

    os.makedirs(new_version_dir, exist_ok=True)
    new_app_path = os.path.join(new_version_dir, APP_NAME)

    print(f"Downloading update {version_tag} to {new_version_dir}...")
    download_file(url, new_app_path)

    if not os.path.exists(new_app_path):
        raise RuntimeError("Download failed")

    print(f"Update installed to {new_app_path}. Please restart the launcher to run it.")


def main():
    try:
        install_update()
    except Exception as e:
        print("Update skipped:", e)


if __name__ == "__main__":
    main()