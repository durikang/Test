import requests
import sys
import zipfile
import subprocess
import traceback
import shutil
import os
import time
import json
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox, QApplication
from config.config_manager import load_version, is_newer_version
import logging

# 로그 설정
logging.basicConfig(filename='update_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class UpdateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.current_version = load_version()
        self.latest_asset_url = None
        self.latest_version_data = None
        self.target_path = os.getcwd()
        self.program_path = os.path.join(self.target_path, "main.exe")
        self.temp_extract_path = os.path.join(self.target_path, "temp_update")

        self.setWindowTitle(f"업데이트 확인 - {self.current_version}")
        self.setGeometry(150, 150, 300, 200)

        self.version_label = QLabel(f"현재 버전: {self.current_version}")
        self.status_label = QLabel("버전을 확인하세요")

        self.check_update_button = QPushButton("최신 버전 확인하기")
        self.check_update_button.clicked.connect(self.check_for_update)

        self.update_button = QPushButton("업데이트 하기")
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.prepare_for_update)

        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.check_update_button)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def check_for_update(self):
        try:
            logging.debug("Checking for updates.")
            headers = {"User-Agent": "MyApp"}
            response = requests.get("https://api.github.com/repos/durikang/Test/releases/latest", headers=headers)
            response.raise_for_status()

            data = response.json()
            self.latest_version_data = data
            latest_version = data.get("tag_name", "N/A")
            logging.debug(f"Latest version fetched: {latest_version}")

            if latest_version == "N/A":
                self.status_label.setText("최신 버전 정보를 불러올 수 없습니다.")
                return

            if is_newer_version(latest_version, self.current_version):
                self.status_label.setText(f"새로운 버전 {latest_version}을 사용할 수 있습니다.")
                self.update_button.setEnabled(True)

                if data.get("assets"):
                    for asset in data["assets"]:
                        if asset["name"].endswith(".zip"):
                            self.latest_asset_url = asset["browser_download_url"]
                            logging.debug(f"Latest asset URL: {self.latest_asset_url}")

            else:
                self.status_label.setText("최신 버전입니다.")
        except Exception as e:
            logging.error("Error during update check.")
            logging.error(traceback.format_exc())
            QMessageBox.warning(self, "오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")

    def prepare_for_update(self):
        try:
            if not self.latest_asset_url:
                QMessageBox.warning(self, "오류", "다운로드할 파일 URL이 없습니다.")
                return

            # 최신 zip 파일 다운로드
            zip_file_path = os.path.join(self.target_path, "latest_release.zip")
            logging.debug(f"Downloading latest release to: {zip_file_path}")
            response = requests.get(self.latest_asset_url, stream=True)
            response.raise_for_status()

            with open(zip_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logging.debug("Download completed.")
            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 다운로드되었습니다! 프로그램을 종료하고 재시작합니다.")

            # 압축 해제
            logging.debug(f"Extracting zip to: {self.temp_extract_path}")
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                if not os.path.exists(self.temp_extract_path):
                    os.makedirs(self.temp_extract_path)
                zip_ref.extractall(self.temp_extract_path)
            logging.debug("Extraction completed.")

            # 프로그램 종료를 위한 중재자 배치 파일 생성
            batch_script = os.path.join(self.target_path, "update_script.bat")
            logging.debug(f"Creating batch script at: {batch_script}")

            with open(batch_script, "w") as bat_file:
                bat_file.write(f"""
                @echo off
                timeout /t 2 /nobreak >nul

                REM 기존 main.exe 파일을 main_old.exe로 백업
                rename "{self.program_path}" "main_old.exe"
                if exist "main_old.exe" (
                    echo main.exe backed up as main_old.exe
                ) else (
                    echo Failed to backup main.exe
                )

                REM 압축 해제된 파일을 메인 프로그램 폴더로 복사
                xcopy "{self.temp_extract_path}\\*" "{self.target_path}" /s /e /y
                if %errorlevel%==0 (
                    echo Files copied successfully
                ) else (
                    echo Error copying files
                )

                REM main_old.exe 삭제
                del "main_old.exe"
                if not exist "main_old.exe" (
                    echo main_old.exe deleted successfully
                ) else (
                    echo Failed to delete main_old.exe
                )

                REM 임시 폴더와 zip 파일 삭제
                rmdir /s /q "{self.temp_extract_path}"
                del "{zip_file_path}"

                REM 업데이트된 main.exe 실행
                start "" "{self.program_path}"
                del "%~f0"
                """)

            logging.debug(f"Executing batch script: {batch_script}")
            subprocess.Popen(batch_script, shell=True)

            QApplication.quit()
            sys.exit(0)

        except Exception as e:
            logging.error("Error during update process.")
            logging.error(traceback.format_exc())
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")

    @staticmethod
    def update_version_json(version_data):
        try:
            version_json_path = os.path.join(os.getcwd(), "_internal", "config", "version.json")
            logging.debug(f"Updating version.json at: {version_json_path}")
            with open(version_json_path, "w") as version_file:
                json.dump({"version": version_data.get("tag_name", "v1.0.0")}, version_file, indent=4)
            logging.debug("Version.json updated successfully.")
        except Exception as e:
            logging.error("Error updating version.json")
            logging.error(traceback.format_exc())
