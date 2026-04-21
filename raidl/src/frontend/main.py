import sys

from controller.main_controller import MainController
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
controller = MainController(window)

window.show()
sys.exit(app.exec())
