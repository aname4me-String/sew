from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from controller import Controller
from model import Model
from view import View


def main() -> int:
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    Controller(model, view)
    view.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
