# config_manager.py
import json
import os

# JSON 파일에서 버전 정보 불러오기
def load_version():
    config_path = os.path.join("config", "metadata.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            data = json.load(file)
            return data.get("version", "N/A")
    return "N/A"
