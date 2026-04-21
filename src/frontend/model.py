from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ModelResult:
    ok: bool
    status_code: int
    data: dict[str, Any] | None
    error: str | None


class Model:
    def __init__(self, base_url: str = "http://127.0.0.1:5000") -> None:
        self._base_url = base_url

    def _request(self, method: str, path: str, **kwargs: Any) -> ModelResult:
        try:
            response = requests.request(method, f"{self._base_url}{path}", timeout=5, **kwargs)
            payload = response.json() if response.content else None
            if response.ok:
                return ModelResult(True, response.status_code, payload, None)
            error = "Unbekannter Fehler"
            if isinstance(payload, dict):
                error = str(payload.get("error", error))
            return ModelResult(False, response.status_code, payload, error)
        except requests.RequestException as exc:
            return ModelResult(False, 0, None, f"Webservice nicht erreichbar: {exc}")

    def get(self, verkehrsmittel: str, monat: int | None = None) -> ModelResult:
        params = {"monat": monat} if monat is not None else None
        return self._request("GET", f"/verkehr/{verkehrsmittel}", params=params)

    def post(self, verkehrsmittel: str, monat: int, anzahl: int) -> ModelResult:
        return self._request(
            "POST", f"/verkehr/{verkehrsmittel}", json={"monat": monat, "anzahl": anzahl}
        )

    def put(self, verkehrsmittel: str, monat: int, anzahl: int) -> ModelResult:
        return self._request(
            "PUT", f"/verkehr/{verkehrsmittel}", json={"monat": monat, "anzahl": anzahl}
        )

    def patch(self, verkehrsmittel: str, monat: int, anzahl: int) -> ModelResult:
        return self._request(
            "PATCH", f"/verkehr/{verkehrsmittel}", json={"monat": monat, "anzahl": anzahl}
        )

    def delete(self, verkehrsmittel: str, monat: int) -> ModelResult:
        return self._request("DELETE", f"/verkehr/{verkehrsmittel}", json={"monat": monat})


if __name__ == "__main__":
    model = Model()
    test_result = model.get("bus")
    print("MODEL SELF-TEST:", "OK" if test_result.ok else test_result.error)
