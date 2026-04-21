from __future__ import annotations

from model import Model, ModelResult


class Controller:
    def __init__(self, model: Model, view) -> None:
        self._model = model
        self._view = view

        self._view.bind_main_start(self.get_data)
        self._view.bind_main_reset(self.reset_main)
        self._view.bind_main_exit(self._view.close_app)

        self._view.bind_admin_start(self.execute_admin_action)
        self._view.bind_admin_reset(self.reset_admin)
        self._view.bind_admin_exit(self._view.close_app)

        self.reset_main()
        self.reset_admin()

    @staticmethod
    def _format_yearly(data: dict[str, int], transport: str) -> str:
        lines = [transport.upper(), ""]
        for month in range(1, 13):
            lines.append(f"Monat {month:02d}: {data.get(str(month), '-')}")
        return "\n".join(lines)

    def _show_result(self, result: ModelResult) -> None:
        if result.ok:
            self._view.set_main_output(str(result.data) if result.data is not None else "OK")
            self._view.set_status("Erfolgreich", 3000)
            return
        self._view.set_main_output(str(result.data) if result.data is not None else (result.error or "Fehler"))
        self._view.set_status(result.error or "Fehler", 4000)

    def _refresh_admin(self) -> None:
        for idx, transport in enumerate(["bus", "tram", "ubahn"]):
            result = self._model.get(transport)
            if result.ok and isinstance(result.data, dict):
                self._view.set_admin_output(idx, self._format_yearly(result.data, transport))
            else:
                self._view.set_admin_output(idx, f"{transport.upper()}\n\nFehler")

    def get_data(self) -> None:
        transport = self._view.get_main_transport()
        month = self._view.get_main_month()

        self._view.set_status(
            f"Abfrage: Verkehrsmittel={transport}, Monat={month}, Jahr={self._view.get_main_year()}"
        )

        if self._view.get_main_year():
            result = self._model.get(transport)
            if result.ok and isinstance(result.data, dict):
                self._view.set_main_output(self._format_yearly(result.data, transport))
                self._view.set_status("Jahresübersicht geladen", 3000)
            else:
                self._show_result(result)
            self._refresh_admin()
            return

        result = self._model.get(transport, month)
        self._show_result(result)
        self._refresh_admin()

    def execute_admin_action(self) -> None:
        action = self._view.get_admin_action()
        transport = self._view.get_admin_transport()
        month = self._view.get_admin_month()
        value = self._view.get_admin_value()

        if action == "get":
            self._refresh_admin()
            self._view.set_status("Admin Jahressicht geladen", 3000)
            return

        action_map = {
            "post": lambda: self._model.post(transport, month, value),
            "put": lambda: self._model.put(transport, month, value),
            "patch": lambda: self._model.patch(transport, month, value),
            "delete": lambda: self._model.delete(transport, month),
        }

        if action not in action_map:
            self._view.set_status("Ungültige Aktion", 3000)
            return

        result = action_map[action]()
        self._show_result(result)
        self._refresh_admin()

    def reset_main(self) -> None:
        self._view.set_main_transport("bus")
        self._view.set_main_month(1)
        self._view.set_main_year(False)
        self._view.clear_main_output()
        self._view.set_status("Mitarbeiteransicht zurückgesetzt", 2000)

    def reset_admin(self) -> None:
        self._view.set_admin_transport("bus")
        self._view.set_admin_month(1)
        self._view.set_admin_action("put")
        self._view.set_admin_value(0)
        self._view.clear_admin_outputs()
        self._view.set_status("Adminansicht zurückgesetzt", 2000)
