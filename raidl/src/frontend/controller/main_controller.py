from __future__ import annotations

from model.api_client import ApiClient, ApiResult


class MainController:
    def __init__(self, view) -> None:
        self._view = view
        self._api = ApiClient()

        self._view.bind_main_start(self.get_data)
        self._view.bind_main_reset(self.reset_mitarbeiter)
        self._view.bind_main_exit(self._view.close_application)

        self._view.bind_admin_start(self.execute_admin_action)
        self._view.bind_admin_reset(self.reset_admin)
        self._view.bind_admin_exit(self._view.close_application)

        self.reset_mitarbeiter()
        self.reset_admin()

    def _format_yearly_data(self, data: dict[str, int], transport_name: str) -> str:
        output = [transport_name.upper(), ""]
        for month in range(1, 13):
            output.append(f"Monat {month:02d}: {data.get(str(month), '-')}")
        return "\n".join(output)

    def _show_result_on_main_output(self, result: ApiResult) -> None:
        if result.ok:
            self._view.set_main_output(str(result.data) if result.data is not None else "OK")
            self._view.show_status_message("Erfolgreich", 3000)
            return

        if result.data is not None:
            self._view.set_main_output(str(result.data))
        elif result.error is not None:
            self._view.set_main_output(result.error)
        else:
            self._view.set_main_output("Fehler")
        self._view.show_status_message(result.error or "Fehler", 4000)

    def _refresh_all_admin_yearly(self) -> None:
        transports = ["bus", "tram", "ubahn"]
        for index, transport in enumerate(transports):
            result = self._api.get(transport)
            if result.ok and isinstance(result.data, dict):
                self._view.set_admin_output(index, self._format_yearly_data(result.data, transport))
            else:
                self._view.set_admin_output(
                    index,
                    f"{transport.upper()}\n\nFehler: {result.error or result.status_code}",
                )

    def get_data(self) -> None:
        transport = self._view.get_main_transport()
        month = self._view.get_main_month()

        if month < 1 or month > 12:
            self._view.show_status_message("Ungültiger Monat", 4000)
            return

        self._view.show_status_message(
            f"Abfrage: Verkehrsmittel={transport}, Monat={month}, Jahr={self._view.get_main_yearly_enabled()}"
        )

        if self._view.get_main_yearly_enabled():
            result = self._api.get(transport)
            if result.ok and isinstance(result.data, dict):
                self._view.set_main_output(self._format_yearly_data(result.data, transport))
                self._view.show_status_message("Jahresübersicht geladen", 3000)
            else:
                self._show_result_on_main_output(result)
            self._refresh_all_admin_yearly()
            return

        result = self._api.get(transport, month)
        self._show_result_on_main_output(result)
        self._refresh_all_admin_yearly()

    def execute_admin_action(self) -> None:
        action = self._view.get_admin_action()
        selected_transport = self._view.get_admin_transport()
        month = self._view.get_admin_month()
        value = self._view.get_admin_value()

        if action == "get":
            self._refresh_all_admin_yearly()
            self._view.show_status_message("Admin Jahressicht geladen", 3000)
            return

        action_map = {
            "post": lambda: self._api.post(selected_transport, month, value),
            "put": lambda: self._api.put(selected_transport, month, value),
            "patch": lambda: self._api.patch(selected_transport, month, value),
            "delete": lambda: self._api.delete(selected_transport, month),
        }

        if action not in action_map:
            self._view.show_status_message("Ungültige Aktion", 4000)
            return

        result = action_map[action]()
        self._show_result_on_main_output(result)
        self._refresh_all_admin_yearly()

    def reset_mitarbeiter(self) -> None:
        self._view.set_main_transport("bus")
        self._view.set_main_month(1)
        self._view.set_main_yearly_enabled(False)
        self._view.clear_main_output()
        self._view.show_status_message("Mitarbeiteransicht zurückgesetzt", 2000)

    def reset_admin(self) -> None:
        self._view.set_admin_transport("bus")
        self._view.set_admin_month(1)
        self._view.set_admin_action("put")
        self._view.set_admin_value(0)
        self._view.clear_admin_outputs()
        self._view.show_status_message("Adminansicht zurückgesetzt", 2000)
