from __future__ import annotations

from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from service import VerkehrService


class VerkehrController:
    def __init__(self, service: VerkehrService) -> None:
        self._service = service
        self.blueprint = Blueprint("verkehr", __name__)
        self._register_routes()

    def _register_routes(self) -> None:
        self.blueprint.get("/")(self.get_overview)
        self.blueprint.get("/verkehr/<verkehrsmittel>")(self.get_data)
        self.blueprint.post("/verkehr/<verkehrsmittel>")(self.post_data)
        self.blueprint.put("/verkehr/<verkehrsmittel>")(self.put_data)
        self.blueprint.patch("/verkehr/<verkehrsmittel>")(self.patch_data)
        self.blueprint.delete("/verkehr/<verkehrsmittel>")(self.delete_data)

    def _error(self, message: str, status_code: int) -> Tuple[Any, int]:
        return jsonify({"error": message}), status_code

    def _validate_transport(self, verkehrsmittel: str) -> Tuple[bool, Tuple[Any, int] | None]:
        if not self._service.has_transport(verkehrsmittel):
            return False, self._error("Verkehrsmittel nicht gefunden", 404)
        return True, None

    def _extract_monat_query(self) -> Tuple[int | None, Tuple[Any, int] | None]:
        raw_monat = request.args.get("monat")
        if raw_monat is None:
            return None, None
        try:
            monat = int(raw_monat)
        except ValueError:
            return None, self._error("Ungültiger Monat", 400)
        return monat, None

    def _extract_set_body(self) -> Tuple[tuple[int, int] | None, Tuple[Any, int] | None]:
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return None, self._error("Ungültige Eingabe", 400)
        if "monat" not in body or "anzahl" not in body:
            return None, self._error("Ungültige Eingabe", 400)
        try:
            monat = int(body["monat"])
            anzahl = int(body["anzahl"])
        except (TypeError, ValueError):
            return None, self._error("Ungültige Eingabe", 400)
        return (monat, anzahl), None

    def _extract_delete_body(self) -> Tuple[int | None, Tuple[Any, int] | None]:
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or "monat" not in body:
            return None, self._error("Ungültige Eingabe", 400)
        try:
            monat = int(body["monat"])
        except (TypeError, ValueError):
            return None, self._error("Ungültige Eingabe", 400)
        return monat, None

    def get_overview(self) -> Tuple[Any, int]:
        return (
            jsonify(
                {
                    "title": "Verkehrsdaten Wien API",
                    "endpoints": {
                        "GET": "/verkehr/{verkehrsmittel}?monat=1",
                        "POST": "/verkehr/{verkehrsmittel}",
                        "PUT": "/verkehr/{verkehrsmittel}",
                        "PATCH": "/verkehr/{verkehrsmittel}",
                        "DELETE": "/verkehr/{verkehrsmittel}",
                    },
                }
            ),
            200,
        )

    def get_data(self, verkehrsmittel: str) -> Tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        monat, query_error = self._extract_monat_query()
        if query_error is not None:
            return query_error

        try:
            if monat is None:
                return jsonify(self._service.get_all(verkehrsmittel)), 200
            return jsonify(self._service.get_monat(verkehrsmittel, monat)), 200
        except ValueError:
            return self._error("Ungültiger Monat", 400)
        except KeyError:
            return self._error("Monat nicht gefunden", 404)

    def post_data(self, verkehrsmittel: str) -> Tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        payload, payload_error = self._extract_set_body()
        if payload_error is not None:
            return payload_error

        monat, anzahl = payload
        try:
            return jsonify(self._service.create(verkehrsmittel, monat, anzahl)), 201
        except ValueError:
            return self._error("Ungültige Eingabe", 400)
        except FileExistsError:
            return self._error("Monat bereits vorhanden", 409)

    def put_data(self, verkehrsmittel: str) -> Tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        payload, payload_error = self._extract_set_body()
        if payload_error is not None:
            return payload_error

        monat, anzahl = payload
        try:
            return jsonify(self._service.set(verkehrsmittel, monat, anzahl)), 200
        except ValueError:
            return self._error("Ungültige Eingabe", 400)

    def patch_data(self, verkehrsmittel: str) -> Tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        payload, payload_error = self._extract_set_body()
        if payload_error is not None:
            return payload_error

        monat, anzahl = payload
        try:
            return jsonify(self._service.increase(verkehrsmittel, monat, anzahl)), 200
        except ValueError:
            return self._error("Ungültige Eingabe", 400)
        except KeyError:
            return self._error("Monat nicht gefunden", 404)

    def delete_data(self, verkehrsmittel: str) -> Tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        monat, payload_error = self._extract_delete_body()
        if payload_error is not None:
            return payload_error

        try:
            self._service.delete(verkehrsmittel, monat)
            return "", 204
        except ValueError:
            return self._error("Ungültige Eingabe", 400)
        except KeyError:
            return self._error("Monat nicht gefunden", 404)
