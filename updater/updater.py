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

    print("Downloading update...")
    download_file(url, NEW_APP)

    if not os.path.exists(NEW_APP):
        raise RuntimeError("Download failed")

    print("Installing update...")

    old_app = APP_NAME + ".old"
    if os.path.exists(old_app):
        try:
            os.remove(old_app)
        except OSError:
            pass

    if os.path.exists(APP_NAME):
        try:
            os.rename(APP_NAME, old_app)
        except OSError as e:
            raise RuntimeError(f"Could not rename running app: {e}")

    os.rename(NEW_APP, APP_NAME)

    print("Update installed")


def run_app():
    if not os.path.exists(APP_NAME):
        print("App not found:", APP_NAME)
        sys.exit(1)

    subprocess.Popen([APP_NAME])


def main():
    try:
        install_update()
    except Exception as e:
        print("Update skipped:", e)

    run_app()


if __name__ == "__main__":
    main()