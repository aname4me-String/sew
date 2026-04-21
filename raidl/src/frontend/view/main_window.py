from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("ui.ui")
        ui_file.open(QIODevice.OpenModeFlag.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(self.ui.centralwidget)
        self.setWindowTitle("Wiener Verkehrsbetriebe – Mitarbeiter")

        self.transport = self.ui.verkehrsmittel
        self.month = self.ui.monat
        self.year_view = self.ui.jahr
        self.output = self.ui.text
        self.btn_get = self.ui.start
        self.btn_reset = self.ui.reset
        self.btn_exit = self.ui.exit

        self.admin_transport = self.ui.type
        self.admin_month = self.ui.admin_month
        self.admin_action = self.ui.rest
        self.admin_value = self.ui.new_value
        self.admin_text_1 = self.ui.admin_text_1
        self.admin_text_2 = self.ui.admin_text_2
        self.admin_text_3 = self.ui.admin_text_3
        self.btn_admin_start = self.ui.admin_start
        self.btn_admin_reset = self.ui.admin_reset
        self.btn_admin_exit = self.ui.admin_exit

        self.status = self.statusBar()
