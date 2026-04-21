from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

BASE_URL = "http://127.0.0.1:5000"


@dataclass
class ApiResult:
    ok: bool
    status_code: int
    data: dict[str, Any] | None
    error: str | None


class ApiClient:
    def __init__(self) -> None:
        self._base = BASE_URL

    def _request(self, method: str, path: str, **kwargs: Any) -> ApiResult:
        try:
            response = requests.request(method, f"{self._base}{path}", timeout=5, **kwargs)
            if response.content:
                payload = response.json()
            else:
                payload = None
            if response.ok:
                return ApiResult(True, response.status_code, payload, None)
            error_text = "Unbekannter Fehler"
            if isinstance(payload, dict) and "error" in payload:
                error_text = str(payload["error"])
            return ApiResult(False, response.status_code, payload, error_text)
        except requests.RequestException as exc:
            return ApiResult(False, 0, None, f"Webservice nicht erreichbar: {exc}")

    def get(self, verkehrsmittel: str, monat: int | None = None) -> ApiResult:
        params = {"monat": monat} if monat is not None else None
        return self._request("GET", f"/verkehr/{verkehrsmittel}", params=params)

    def post(self, verkehrsmittel: str, monat: int, anzahl: int) -> ApiResult:
        return self._request(
            "POST",
            f"/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": anzahl},
        )

    def put(self, verkehrsmittel: str, monat: int, anzahl: int) -> ApiResult:
        return self._request(
            "PUT",
            f"/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": anzahl},
        )

    def patch(self, verkehrsmittel: str, monat: int, anzahl: int) -> ApiResult:
        return self._request(
            "PATCH",
            f"/verkehr/{verkehrsmittel}",
            json={"monat": monat, "anzahl": anzahl},
        )

    def delete(self, verkehrsmittel: str, monat: int) -> ApiResult:
        return self._request(
            "DELETE",
            f"/verkehr/{verkehrsmittel}",
            json={"monat": monat},
        )
