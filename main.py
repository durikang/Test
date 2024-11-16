# main.py
import logging
import sys
from PyQt5.QtWidgets import QApplication
from GUI.mainWindow import MainWindow

# 로깅 설정
logging.basicConfig(filename='app_error.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.exception("Unhandled exception occurred")  # 발생한 예외 기록
