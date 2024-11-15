# GUI/mainWindow.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMenuBar, QAction
from PyQt5.QtCore import QTimer, QDateTime
from GUI.updateWindow import UpdateWindow  # 업데이트 창 import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 기본 윈도우 설정
        self.setWindowTitle("Git Auto-Update Test - v1.0.2")  # 버전 표시 추가
        self.setGeometry(100, 100, 400, 200)  # 창 크기 변경

        # 메뉴바 설정
        menubar = self.menuBar()
        update_menu = menubar.addMenu("업데이트")

        # 업데이트 메뉴 항목 추가
        update_action = QAction("업데이트 확인", self)
        update_action.triggered.connect(self.show_update_window)
        update_menu.addAction(update_action)

        # 레이아웃과 위젯 설정
        self.label = QLabel("현재 시간 표시 (v1.0.2)", self)  # 라벨 초기 텍스트 변경
        self.update_label()  # 실행할 때 현재 시간 표시

        # 버튼 텍스트 업데이트
        self.button = QPushButton("업데이트된 버튼 2", self)
        self.button.clicked.connect(self.update_label)  # 버튼 클릭 시 라벨 업데이트

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 타이머 설정: 1초마다 라벨 갱신
        timer = QTimer(self)
        timer.timeout.connect(self.update_label)
        timer.start(1000)

    def update_label(self):
        # 현재 시간을 년/월/일/시/분/초 형식으로 라벨에 표시
        current_time = QDateTime.currentDateTime().toString("yyyy/MM/dd hh:mm:ss")
        self.label.setText(f"현재 시간: {current_time} (v1.0.1)")

    def show_update_window(self):
        # 업데이트 창 열기
        update_window = UpdateWindow()
        update_window.exec_()
