# GUI/mainWindow.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMenuBar, QAction
from PyQt5.QtCore import QTimer, QDateTime
from GUI.updateWindow import UpdateWindow
from config.config_manager import load_version  # load_version 함수 불러오기

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = load_version()  # 버전 정보 불러오기

        # 기본 윈도우 설정
        self.setWindowTitle(f"Git Auto-Update Test - {self.version}")
        self.setGeometry(100, 100, 400, 200)

        # 메뉴바 설정
        menubar = self.menuBar()
        update_menu = menubar.addMenu("업데이트")

        # 업데이트 메뉴 항목 추가
        update_action = QAction("업데이트 확인", self)
        update_action.triggered.connect(self.show_update_window)
        update_menu.addAction(update_action)

        # 레이아웃과 위젯 설정
        self.label = QLabel(f"현재 시간 표시 ({self.version})", self)
        self.update_label()  # 실행할 때 현재 시간 표시

        # 버튼 텍스트 업데이트
        self.button = QPushButton("업데이트 된건가?", self)
        self.button.clicked.connect(self.update_label)

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
        self.label.setText(f"현재 시간: {current_time} ({self.version})")

    def show_update_window(self):
        # 업데이트 창 열기
        update_window = UpdateWindow()
        update_window.exec_()
