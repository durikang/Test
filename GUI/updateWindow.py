# GUI/updateWindow.py
import requests
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from config.config_manager import load_version  # load_version 함수 불러오기

class UpdateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.current_version = load_version()  # JSON에서 불러온 버전 사용

        # 업데이트 창 설정
        self.setWindowTitle(f"업데이트 확인 - {self.current_version}")
        self.setGeometry(150, 150, 300, 200)

        # 라벨 설정
        self.version_label = QLabel(f"현재 버전: {self.current_version}")
        self.status_label = QLabel("버전을 확인하세요")

        # 버튼 설정
        self.check_update_button = QPushButton("최신 버전 확인하기")
        self.check_update_button.clicked.connect(self.check_for_update)

        self.update_button = QPushButton("업데이트 하기")
        self.update_button.setEnabled(False)  # 최신 버전일 경우 비활성화
        self.update_button.clicked.connect(self.perform_update)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.check_update_button)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def check_for_update(self):
        # GitHub API에서 최신 릴리스 버전을 확인
        try:
            response = requests.get("https://api.github.com/repos/durikang/Test/releases/latest")
            latest_version = response.json().get("tag_name", "N/A")

            if latest_version > self.current_version:
                self.status_label.setText(f"새로운 버전 {latest_version}을 사용할 수 있습니다.")
                self.update_button.setEnabled(True)  # 업데이트 버튼 활성화
            else:
                self.status_label.setText("최신 버전입니다.")
        except Exception as e:
            QMessageBox.warning(self, "오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")

    def perform_update(self):
        # 업데이트 로직
        try:
            QMessageBox.information(self, "업데이트", "업데이트가 성공적으로 완료되었습니다!")
            self.status_label.setText("최신 버전으로 업데이트되었습니다.")
            self.update_button.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"업데이트 중 오류가 발생했습니다: {e}")
