from __future__ import annotations


class Service:
    def __init__(self) -> None:
        self._data: dict[str, dict[int, int]] = {"bus": {}, "tram": {}, "ubahn": {}}

    @staticmethod
    def _validate_monat(monat: int) -> None:
        if monat < 1 or monat > 12:
            raise ValueError("Ungültiger Monat")

    def has_transport(self, verkehrsmittel: str) -> bool:
        return verkehrsmittel in self._data

    def get_all(self, verkehrsmittel: str) -> dict[str, int]:
        return {str(monat): anzahl for monat, anzahl in self._data[verkehrsmittel].items()}

    def get_monat(self, verkehrsmittel: str, monat: int) -> dict[str, int]:
        self._validate_monat(monat)
        if monat not in self._data[verkehrsmittel]:
            raise KeyError("Monat nicht gefunden")
        return {str(monat): self._data[verkehrsmittel][monat]}

    def create(self, verkehrsmittel: str, monat: int, anzahl: int) -> dict[str, int]:
        self._validate_monat(monat)
        if monat in self._data[verkehrsmittel]:
            raise FileExistsError("Monat bereits vorhanden")
        self._data[verkehrsmittel][monat] = anzahl
        return {"monat": monat, "anzahl": anzahl}

    def set(self, verkehrsmittel: str, monat: int, anzahl: int) -> dict[str, int]:
        self._validate_monat(monat)
        self._data[verkehrsmittel][monat] = anzahl
        return {"monat": monat, "anzahl": anzahl}

    def increase(self, verkehrsmittel: str, monat: int, anzahl: int) -> dict[str, int]:
        self._validate_monat(monat)
        if monat not in self._data[verkehrsmittel]:
            raise KeyError("Monat nicht gefunden")
        self._data[verkehrsmittel][monat] += anzahl
        return {"monat": monat, "anzahl": self._data[verkehrsmittel][monat]}

    def delete(self, verkehrsmittel: str, monat: int) -> None:
        self._validate_monat(monat)
        if monat not in self._data[verkehrsmittel]:
            raise KeyError("Monat nicht gefunden")
        del self._data[verkehrsmittel][monat]
