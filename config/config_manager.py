# config_manager.py
import json
import os
import sys


# JSON 파일에서 버전 정보 불러오기
def load_version():
    # PyInstaller로 빌드된 환경인지 확인하여 경로 설정
    if getattr(sys, 'frozen', False):
        # 빌드된 환경에서는 sys._MEIPASS 경로 사용
        config_path = os.path.join(sys._MEIPASS, "config", "metadata.json")
    else:
        # 개발 환경에서는 현재 디렉토리를 기준으로 경로 설정
        config_path = os.path.join("config", "metadata.json")

    # 파일이 존재하면 JSON 데이터 읽어오기
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            data = json.load(file)
            return data.get("version", "N/A")
    return "N/A"
