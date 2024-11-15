import requests
import os
import sys
import zipfile
import subprocess
import traceback
import json
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from config.config_manager import load_version, is_newer_version

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 환경 변수로 GitHub 토큰을 가져옴


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
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "User-Agent": "MyApp"
            }
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

                # assets가 비어 있지 않은지 확인하고 다운로드 URL 가져오기
                if data.get("assets"):
                    for asset in data["assets"]:
                        if asset["name"].endswith(".zip"):  # 필요한 파일 형식 선택
                            self.latest_asset_url = asset["browser_download_url"]

                # 최신 버전을 version.json 파일에 업데이트
                from config.update_version_json import update_version_json
                update_version_json(latest_version)  # 최신 버전으로 버전 파일 업데이트

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
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            response = requests.get(self.latest_asset_url, headers=headers, stream=True)
            response.raise_for_status()

            # 다운로드한 zip 파일을 임시 위치에 저장
            with open("latest_release.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 다운로드되었습니다! 압축을 해제하고 프로그램을 재시작합니다.")

            # 압축 해제 및 실행 파일 대체
            with zipfile.ZipFile("latest_release.zip", "r") as zip_ref:
                zip_ref.extractall(os.path.dirname(sys.argv[0]))

            # 프로그램 재시작
            subprocess.Popen([sys.executable] + sys.argv)  # 새로 업데이트된 프로그램 재실행
            sys.exit(0)  # 기존 프로그램 종료

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")
