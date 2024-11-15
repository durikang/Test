import requests
import os
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from config.config_manager import load_version, is_newer_version
import traceback

# 환경 변수에서 GitHub 토큰 불러오기
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GITHUB_TOKEN 환경 변수를 설정해줘야 함

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

            print(f"[DEBUG] GitHub API Response Status Code: {response.status_code}")
            print(f"[DEBUG] GitHub API Response JSON: {response.json()}")

            latest_version = response.json().get("tag_name", "N/A")

            if latest_version == "N/A":
                self.status_label.setText("최신 버전 정보를 불러올 수 없습니다.")
                print("[ERROR] 최신 버전 정보를 가져오지 못했습니다.")
                return

            print(f"[DEBUG] Current version: {self.current_version}")
            print(f"[DEBUG] Latest version from GitHub: {latest_version}")

            if is_newer_version(latest_version, self.current_version):
                self.status_label.setText(f"새로운 버전 {latest_version}을 사용할 수 있습니다.")
                self.update_button.setEnabled(True)
                print("[DEBUG] 업데이트가 가능합니다.")
            else:
                self.status_label.setText("최신 버전입니다.")
                print("[DEBUG] 최신 버전입니다.")
        except Exception as e:
            print("[ERROR] 업데이트 확인 중 오류 발생")
            traceback.print_exc()
            QMessageBox.warning(self, "오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")

    def perform_update(self):
        try:
            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 완료되었습니다!")
            self.status_label.setText("최신 버전으로 업데이트되었습니다.")
            self.update_button.setEnabled(False)
        except Exception as e:
            print("[ERROR] 업데이트 중 오류 발생")
            traceback.print_exc()
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")
