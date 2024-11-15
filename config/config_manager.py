# config/config_manager.py
import json
import os
import sys


# JSON 파일에서 버전 정보 불러오기
def load_version():
    if getattr(sys, 'frozen', False):
        config_path = os.path.join(sys._MEIPASS, "config", "version.json")
    else:
        config_path = os.path.join("config", "version.json")

    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            data = json.load(file)
            return data.get("version", "N/A")
    return "N/A"


# config_manager.py
def is_newer_version(latest_version, current_version):
    def version_tuple(v):
        return tuple(map(int, (v.lstrip("v").split("."))))

    # 버전 값이 'N/A'이거나 비어 있으면 False 반환
    if latest_version == "N/A" or current_version == "N/A":
        print("[ERROR] 버전 정보가 올바르지 않아 비교할 수 없습니다.")
        return False

    return version_tuple(latest_version) > version_tuple(current_version)
