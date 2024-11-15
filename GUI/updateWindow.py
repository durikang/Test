import requests
import os
import sys
import zipfile
import subprocess
from io import BytesIO
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from config.config_manager import load_version, is_newer_version
import traceback

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub 액세스 토큰 환경 변수


class UpdateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.current_version = load_version()

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
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "User-Agent": "MyApp"
            }
            response = requests.get("https://api.github.com/repos/durikang/Test/releases/latest", headers=headers)

            latest_version = response.json().get("tag_name", "N/A")

            if latest_version == "N/A":
                self.status_label.setText("최신 버전 정보를 불러올 수 없습니다.")
                return

            if is_newer_version(latest_version, self.current_version):
                self.status_label.setText(f"새로운 버전 {latest_version}을 사용할 수 있습니다.")
                self.update_button.setEnabled(True)
                self.latest_asset_url = response.json()["assets"][0]["browser_download_url"]  # 최신 릴리스 exe 파일 URL 저장
            else:
                self.status_label.setText("최신 버전입니다.")
        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self, "오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")

    def perform_update(self):
        try:
            # 최신 exe 파일 다운로드
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            response = requests.get(self.latest_asset_url, headers=headers, stream=True)
            response.raise_for_status()

            # 다운로드한 exe 파일을 임시 위치에 저장
            with open("update_temp.exe", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # 기존 exe 파일 위치 가져오기
            current_exe_path = sys.argv[0]  # 현재 실행 중인 exe 경로

            # 다운로드한 파일을 기존 exe에 덮어쓰기
            os.replace("update_temp.exe", current_exe_path)

            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 완료되었습니다! 프로그램을 재시작합니다.")

            # 프로그램 재시작
            subprocess.Popen([current_exe_path])  # 새로 업데이트된 exe 파일 실행
            sys.exit(0)  # 기존 프로그램 종료

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")
