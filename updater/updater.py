import requests
import time
import os
import subprocess
from version import latest


def get_download_url():
    response = requests.get(latest)
    release = response.json()

    assets = release.get("assets")

    if not assets:
        raise Exception("No release assets found")

    return assets[0]["browser_download_url"]


def download_update(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise Exception("Download failed")

    with open("TodoApp_new.exe", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


download_url = get_download_url()
print("Downloading:", download_url)

download_update(download_url)

if not os.path.exists("TodoApp_new.exe"):
    print("Download failed")
    exit()

print("Download finished")

time.sleep(2)

if os.path.exists("TodoApp.exe"):
    os.replace("TodoApp.exe", "TodoApp_backup.exe")

os.replace("TodoApp_new.exe", "TodoApp.exe")

print("Update installed")

subprocess.Popen(["TodoApp.exe"])