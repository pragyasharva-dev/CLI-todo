import requests
from packaging import version

CURRENT_VERSION = "2.0.7"
latest = "https://api.github.com/repos/pragyasharva-dev/CLI-todo/releases/latest"

def check_for_updates():
    try:
        response = requests.get(latest, timeout=5)
        if response.status_code == 200:
            release = response.json()
            latest_version = release.get("tag_name", "").replace("v", "")
            
            if latest_version and version.parse(latest_version) > version.parse(CURRENT_VERSION):
                return True, latest_version
    except Exception as e:
        print(f"Update check failed: {e}")
        
    return False, CURRENT_VERSION
