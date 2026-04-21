from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from service import Service


class Controller:
    def __init__(self, service: Service) -> None:
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

    @staticmethod
    def _error_response(message: str, status_code: int) -> tuple[Any, int]:
        return jsonify({"error": message}), status_code

    def _extract_set_body(self) -> tuple[tuple[int, int] | None, tuple[Any, int] | None]:
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or "monat" not in body or "anzahl" not in body:
            return None, self._error_response("Ungültige Eingabe", 400)
        try:
            return (int(body["monat"]), int(body["anzahl"])), None
        except (TypeError, ValueError):
            return None, self._error_response("Ungültige Eingabe", 400)

    def _extract_delete_body(self) -> tuple[int | None, tuple[Any, int] | None]:
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or "monat" not in body:
            return None, self._error_response("Ungültige Eingabe", 400)
        try:
            return int(body["monat"]), None
        except (TypeError, ValueError):
            return None, self._error_response("Ungültige Eingabe", 400)

    def _validate_transport(self, verkehrsmittel: str) -> tuple[bool, tuple[Any, int] | None]:
        if not self._service.has_transport(verkehrsmittel):
            return False, self._error_response("Verkehrsmittel nicht gefunden", 404)
        return True, None

    def get_overview(self) -> tuple[Any, int]:
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

    def get_data(self, verkehrsmittel: str) -> tuple[Any, int]:
        ok, error_response = self._validate_transport(verkehrsmittel)
        if not ok:
            return error_response

        monat = request.args.get("monat")
        if monat is None:
            return jsonify(self._service.get_all(verkehrsmittel)), 200
        try:
            return jsonify(self._service.get_monat(verkehrsmittel, int(monat))), 200
        except ValueError:
            return self._error_response("Ungültiger Monat", 400)
        except KeyError:
            return self._error_response("Monat nicht gefunden", 404)

    def post_data(self, verkehrsmittel: str) -> tuple[Any, int]:
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
            return self._error_response("Ungültige Eingabe", 400)
        except FileExistsError:
            return self._error_response("Monat bereits vorhanden", 409)

    def put_data(self, verkehrsmittel: str) -> tuple[Any, int]:
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
            return self._error_response("Ungültige Eingabe", 400)

    def patch_data(self, verkehrsmittel: str) -> tuple[Any, int]:
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
            return self._error_response("Ungültige Eingabe", 400)
        except KeyError:
            return self._error_response("Monat nicht gefunden", 404)

    def delete_data(self, verkehrsmittel: str) -> tuple[Any, int]:
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
            return self._error_response("Ungültige Eingabe", 400)
        except KeyError:
            return self._error_response("Monat nicht gefunden", 404)
