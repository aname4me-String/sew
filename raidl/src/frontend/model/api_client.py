import requests

BASE_URL = "http://127.0.0.1:5000"


class ApiClient:
    def __init__(self):
        self.base = BASE_URL

    def get(self, verkehrsmittel, monat=None):
        params = {"monat": monat} if monat else {}
        r = requests.get(f"{self.base}/verkehr/{verkehrsmittel}", params=params)
        return r

    def post(self, verkehrsmittel, monat, anzahl):
        return requests.post(
            f"{self.base}/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": anzahl},
        )

    def put(self, verkehrsmittel, monat, anzahl):
        return requests.put(
            f"{self.base}/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": anzahl},
        )

    def patch(self, verkehrsmittel, monat, delta):
        return requests.patch(
            f"{self.base}/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": delta},
        )

    def delete(self, verkehrsmittel, monat):
        return requests.delete(
            f"{self.base}/verkehr/{verkehrsmittel}",
            json={"monat": monat},
        )
