import requests  # 누락된 requests 모듈을 임포트합니다.
import sys
import zipfile
import subprocess
import traceback
import os
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from config.config_manager import load_version, is_newer_version

class UpdateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.current_version = load_version()
        self.latest_asset_url = None  # 최신 자산 파일 URL

        self.setWindowTitle(f"업데이트 확인 - {self.current_version}")
        self.setGeometry(150, 150, 300, 200)

        self.version_label = QLabel(f"현재 버전: {self.current_version}")
        self.status_label = QLabel("버전을 확인하세요")

        self.check_update_button = QPushButton("최신 버전 확인하기")
        self.check_update_button.clicked.connect(self.check_for_update)

        self.update_button = QPushButton("업데이트 하기")
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.perform_update)

        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.check_update_button)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def check_for_update(self):
        try:
            headers = {"User-Agent": "MyApp"}
            response = requests.get("https://api.github.com/repos/durikang/Test/releases/latest", headers=headers)
            response.raise_for_status()

            data = response.json()
            latest_version = data.get("tag_name", "N/A")

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

            else:
                self.status_label.setText("최신 버전입니다.")
        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self, "오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")

    def perform_update(self):
        try:
            if not self.latest_asset_url:
                QMessageBox.warning(self, "오류", "다운로드할 파일 URL이 없습니다.")
                return

            # 최신 zip 파일 다운로드
            zip_file_path = os.path.join(os.getcwd(), "latest_release.zip")
            response = requests.get(self.latest_asset_url, stream=True)
            response.raise_for_status()

            with open(zip_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 다운로드되었습니다! 압축을 해제하고 프로그램을 재시작합니다.")

            # 압축 해제 및 배치 파일 작성
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                temp_extract_path = os.path.join(os.getcwd(), "temp_update")
                if not os.path.exists(temp_extract_path):
                    os.makedirs(temp_extract_path)
                zip_ref.extractall(temp_extract_path)

                # 압축 해제된 파일이 예상되는 위치에 있는지 확인
                extracted_main_file_path = os.path.join(temp_extract_path, "main.exe")

                # dist/main.exe로 압축된 파일을 찾기 위한 수정된 경로
                if not os.path.exists(extracted_main_file_path):
                    # 압축 파일 내에 dist 폴더가 있다면 dist/main.exe로 해제되었을 가능성 체크
                    extracted_main_file_path = os.path.join(temp_extract_path, "dist", "main.exe")

                if not os.path.exists(extracted_main_file_path):
                    QMessageBox.critical(self, "오류", "업데이트 파일(main.exe)을 찾을 수 없습니다. 압축 파일 내 위치를 확인하세요.")
                    return

                # 배치 파일 생성
                bat_file_path = os.path.join(os.getcwd(), "update.bat")
                with open(bat_file_path, "w") as bat_file:
                    bat_file.write(f"""
                    @echo off
                    timeout /t 1 /nobreak >nul
                    del "main.exe"
                    move "{extracted_main_file_path}" "main.exe"
                    start "" "main.exe"
                    del "%~f0"
                    """)

            # 배치 파일 실행
            subprocess.Popen(bat_file_path, shell=True)
            sys.exit(0)

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")
