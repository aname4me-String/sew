from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).resolve().parent.parent / "ui.ui"
        ui_file = QFile(str(ui_path))
        ui_file.open(QIODevice.OpenModeFlag.ReadOnly)
        self._ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(self._ui.centralwidget)
        self.setWindowTitle("Wiener Verkehrsdaten – Mitarbeiterverwaltung")
        self._status = self.statusBar()

        self._ensure_admin_put_action()

    def _ensure_admin_put_action(self) -> None:
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

    def set_main_transport(self, transport: str) -> None:
        index = self._ui.verkehrsmittel.findText(transport)
        if index >= 0:
            self._ui.verkehrsmittel.setCurrentIndex(index)

    def get_main_month(self) -> int:
        return int(self._ui.monat.value())

    def set_main_month(self, month: int) -> None:
        self._ui.monat.setValue(month)

    def get_main_yearly_enabled(self) -> bool:
        return self._ui.jahr.isChecked()

    def set_main_yearly_enabled(self, enabled: bool) -> None:
        self._ui.jahr.setChecked(enabled)

    def set_main_output(self, text: str) -> None:
        self._ui.text.setText(text)

    def clear_main_output(self) -> None:
        self._ui.text.clear()

    def get_admin_transport(self) -> str:
        return self._ui.type.currentText().strip().lower()

    def set_admin_transport(self, transport: str) -> None:
        index = self._ui.type.findText(transport)
        if index >= 0:
            self._ui.type.setCurrentIndex(index)

    def get_admin_month(self) -> int:
        return int(self._ui.admin_month.value())

    def set_admin_month(self, month: int) -> None:
        self._ui.admin_month.setValue(month)

    def get_admin_action(self) -> str:
        return self._ui.rest.currentText().strip().lower()

    def set_admin_action(self, action: str) -> None:
        index = self._ui.rest.findText(action.capitalize())
        if index >= 0:
            self._ui.rest.setCurrentIndex(index)

    def get_admin_value(self) -> int:
        return int(self._ui.new_value.value())

    def set_admin_value(self, value: int) -> None:
        self._ui.new_value.setValue(value)

    def set_admin_output(self, output_index: int, text: str) -> None:
        outputs = [self._ui.admin_text_1, self._ui.admin_text_2, self._ui.admin_text_3]
        if output_index < 0 or output_index >= len(outputs):
            return
        outputs[output_index].setText(text)

    def clear_admin_outputs(self) -> None:
        self._ui.admin_text_1.clear()
        self._ui.admin_text_2.clear()
        self._ui.admin_text_3.clear()

    def show_status_message(self, message: str, timeout_ms: int = 3000) -> None:
        self._status.showMessage(message, timeout_ms)

    def close_application(self) -> None:
        self.close()
