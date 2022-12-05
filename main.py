import sys
from PyQt6.QtWidgets import QApplication
from FacebookSys import FacebookSystem

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = FacebookSystem()
    sys.exit(app.exec())