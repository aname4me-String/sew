from model.api_client import ApiClient


class MainController:
    def __init__(self, view):
        self.view = view
        self.api = ApiClient()

        self.view.btn_get.clicked.connect(self.get_data)
        self.view.btn_reset.clicked.connect(self.reset_mitarbeiter)
        self.view.btn_exit.clicked.connect(self.view.close)

        self.view.btn_admin_start.clicked.connect(self.execute_admin_action)
        self.view.btn_admin_reset.clicked.connect(self.reset_admin)
        self.view.btn_admin_exit.clicked.connect(self.view.close)

    def format_yearly_data(self, data, transport_name):
        output = f"{transport_name.upper()}\n\n"
        for month in range(1, 13):
            value = data.get(str(month), "-")
            output += f"Monat {month:02d}: {value}\n"
        return output

    def refresh_all_admin_yearly(self):
        transports = ["ubahn", "tram", "bus"]
        outputs = [
            self.view.admin_text_1,
            self.view.admin_text_2,
            self.view.admin_text_3,
        ]

        for transport, output_widget in zip(transports, outputs):
            r = self.api.get(transport)
            if r.ok:
                data = r.json()
                output_widget.setText(self.format_yearly_data(data, transport))
            else:
                output_widget.setText(f"{transport.upper()}\n\nFehler: {r.status_code}")

    def show_response(self, text_widget, r):
        if r.ok:
            text_widget.setText(str(r.json()) if r.content else "OK")
            self.view.status.showMessage("Erfolgreich", 3000)
        else:
            text_widget.setText(str(r.json()))
            self.view.status.showMessage("Fehler", 3000)

    def get_data(self):
        verkehr = self.view.transport.currentText()

        if self.view.year_view.isChecked():
            r = self.api.get(verkehr)
            if not r.ok:
                self.show_response(self.view.output, r)
                return

            data = r.json()
            output = "Jahresübersicht\n\n"

            for month in range(1, 13):
                value = data.get(str(month), "-")
                output += f"Monat {month:02d}: {value}\n"

            self.view.output.setText(output)
            self.view.status.showMessage("Jahresübersicht geladen", 3000)

            self.refresh_all_admin_yearly()
            return

        r = self.api.get(verkehr, self.view.month.value())
        self.show_response(self.view.output, r)

        self.refresh_all_admin_yearly()

    def execute_admin_action(self):
        action = self.view.admin_action.currentText().lower()
        selected_transport = self.view.admin_transport.currentText()
        month = self.view.admin_month.value()
        value = self.view.admin_value.value()

        if action == "get":
            self.refresh_all_admin_yearly()
        elif action == "post":
            r = self.api.post(selected_transport, month, value)
            if not r.ok and r.status_code == 409:
                self.api.delete(selected_transport, month)
                r = self.api.post(selected_transport, month, value)
            self.show_response(self.view.output, r)
            self.refresh_all_admin_yearly()
        elif action == "put":
            r = self.api.put(selected_transport, month, value)
            self.show_response(self.view.output, r)
            self.refresh_all_admin_yearly()
        elif action == "patch":
            r = self.api.patch(selected_transport, month, value)
            self.show_response(self.view.output, r)
            self.refresh_all_admin_yearly()
        elif action == "delete":
            r = self.api.delete(selected_transport, month)
            self.show_response(self.view.output, r)
            self.refresh_all_admin_yearly()

    def reset_mitarbeiter(self):
        self.view.transport.setCurrentIndex(0)
        self.view.month.setValue(1)
        self.view.year_view.setChecked(False)
        self.view.output.clear()
        self.view.status.showMessage("Zurückgesetzt", 2000)

    def reset_admin(self):
        self.view.admin_transport.setCurrentIndex(0)
        self.view.admin_month.setValue(1)
        self.view.admin_action.setCurrentIndex(0)
        self.view.admin_value.setValue(0)
        self.view.admin_text_1.clear()
        self.view.admin_text_2.clear()
        self.view.admin_text_3.clear()
        self.view.status.showMessage("Admin zurückgesetzt", 2000)
