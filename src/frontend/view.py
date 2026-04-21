from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow


class View(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        loader = QUiLoader()
        ui_path = Path(__file__).resolve().parent / "ui.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QIODevice.OpenModeFlag.ReadOnly)
        self._ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(self._ui.centralwidget)
        self.setWindowTitle("Wiener Verkehrsdaten – Mitarbeiterverwaltung")
        self._status = self.statusBar()

        if self._ui.rest.findText("Put") == -1:
            self._ui.rest.insertItem(0, "Put")

    def bind_main_start(self, callback) -> None:
        self._ui.start.clicked.connect(callback)

    def bind_main_reset(self, callback) -> None:
        self._ui.reset.clicked.connect(callback)

    def bind_main_exit(self, callback) -> None:
        self._ui.exit.clicked.connect(callback)

    def bind_admin_start(self, callback) -> None:
        self._ui.admin_start.clicked.connect(callback)

    def bind_admin_reset(self, callback) -> None:
        self._ui.admin_reset.clicked.connect(callback)

    def bind_admin_exit(self, callback) -> None:
        self._ui.admin_exit.clicked.connect(callback)

    def get_main_transport(self) -> str:
        return self._ui.verkehrsmittel.currentText().strip().lower()

    def set_main_transport(self, value: str) -> None:
        index = self._ui.verkehrsmittel.findText(value)
        if index >= 0:
            self._ui.verkehrsmittel.setCurrentIndex(index)

    def get_main_month(self) -> int:
        return int(self._ui.monat.value())

    def set_main_month(self, value: int) -> None:
        self._ui.monat.setValue(value)

    def get_main_year(self) -> bool:
        return self._ui.jahr.isChecked()

    def set_main_year(self, value: bool) -> None:
        self._ui.jahr.setChecked(value)

    def set_main_output(self, value: str) -> None:
        self._ui.text.setText(value)

    def clear_main_output(self) -> None:
        self._ui.text.clear()

    def get_admin_transport(self) -> str:
        return self._ui.type.currentText().strip().lower()

    def set_admin_transport(self, value: str) -> None:
        index = self._ui.type.findText(value)
        if index >= 0:
            self._ui.type.setCurrentIndex(index)

    def get_admin_month(self) -> int:
        return int(self._ui.admin_month.value())

    def set_admin_month(self, value: int) -> None:
        self._ui.admin_month.setValue(value)

    def get_admin_action(self) -> str:
        return self._ui.rest.currentText().strip().lower()

    def set_admin_action(self, value: str) -> None:
        index = self._ui.rest.findText(value.capitalize())
        if index >= 0:
            self._ui.rest.setCurrentIndex(index)

    def get_admin_value(self) -> int:
        return int(self._ui.new_value.value())

    def set_admin_value(self, value: int) -> None:
        self._ui.new_value.setValue(value)

    def set_admin_output(self, index: int, value: str) -> None:
        outputs = [self._ui.admin_text_1, self._ui.admin_text_2, self._ui.admin_text_3]
        if 0 <= index < len(outputs):
            outputs[index].setText(value)

    def clear_admin_outputs(self) -> None:
        self._ui.admin_text_1.clear()
        self._ui.admin_text_2.clear()
        self._ui.admin_text_3.clear()

    def set_status(self, text: str, timeout: int = 3000) -> None:
        self._status.showMessage(text, timeout)

    def close_app(self) -> None:
        self.close()
