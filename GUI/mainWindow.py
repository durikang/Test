# gui/mainWindow.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QDateTime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 기본 윈도우 설정
        self.setWindowTitle("Git Auto-Update Test")
        self.setGeometry(100, 100, 300, 150)

        # 레이아웃과 위젯 설정
        self.label = QLabel(self)
        self.update_label()  # 실행할 때 현재 시간 표시
        self.button = QPushButton("버튼 1", self)
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
        self.label.setText(current_time)
