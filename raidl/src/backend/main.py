from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Verkehrsdaten Wien API",
    version="1.0.0",
    description="API zur Abfrage und Bearbeitung von Mitarbeiterzahlen",
)

data: Dict[str, Dict[int, int]] = {"bus": {}, "tram": {}, "ubahn": {}}

VALID_TRANSPORTS = {"bus", "tram", "ubahn"}


class SetData(BaseModel):
    """
    Request body model used to create or update a monthly value
    for a specific transport type.

    Attributes:
        monat (int): Month number (1–12).
        anzahl (int): Number of employees.
    """

    monat: int = Field(ge=1, le=12)
    anzahl: int


class DeleteData(BaseModel):
    """
    Request body model used to delete a monthly record.

    Attributes:
        monat (int): Month number (1–12) to be removed.
    """

    monat: int = Field(ge=1, le=12)


class Error(BaseModel):
    """
    Standard error response model.

    Attributes:
        error (str): Human-readable error description.
    """

    error: str


def validate_transport(verkehrsmittel: str):
    """
    Validates whether the given transport type is supported.

    Args:
        verkehrsmittel (str): Name of the transport type.

    Raises:
        HTTPException:
            - 404 if the transport type is not recognized.
    """
    if verkehrsmittel not in VALID_TRANSPORTS:
        raise HTTPException(
            status_code=404, detail={"error": "Verkehrsmittel nicht gefunden"}
        )


def validate_range(value: int):
    """
    Validates that a numeric value is within the allowed range.

    Args:
        value (int): Value to validate.

    Raises:
        HTTPException:
            - 400 if the value is outside the range 0–250.
    """
    if not 0 <= value <= 250:
        raise HTTPException(
            status_code=400, detail={"error": "Anzahl muss zwischen 0 und 250 liegen"}
        )


@app.get("/")
def api_guide():
    """
    Returns an overview of available API endpoints.

    Returns:
        dict: Mapping of HTTP methods to endpoint paths.
    """
    return {
        "endpoints": {
            "GET": "/verkehr/{verkehrsmittel}?monat=1",
            "POST": "/verkehr/{verkehrsmittel}",
            "PUT": "/verkehr/{verkehrsmittel}",
            "PATCH": "/verkehr/{verkehrsmittel}",
            "DELETE": "/verkehr/{verkehrsmittel}",
        }
    }


@app.get("/verkehr/{verkehrsmittel}")
def get_data(verkehrsmittel: str, monat: Optional[int] = None):
    """
    Retrieves stored monthly data for a given transport type.

    If a specific month is provided, only that month's value
    is returned. Otherwise, all stored months are returned.

    Args:
        verkehrsmittel (str): Name of the transport type.
        monat (Optional[int]): Month number (1–12).

    Returns:
        dict: Either a single month entry or all stored data
        for the transport type.

    Raises:
        HTTPException:
            - 400 if the month is invalid.
            - 404 if the transport type or month is not found.
    """
    validate_transport(verkehrsmittel)

    if monat is not None:
        if monat < 1 or monat > 12:
            raise HTTPException(status_code=400, detail={"error": "Ungültiger Monat"})
        if monat not in data[verkehrsmittel]:
            raise HTTPException(
                status_code=404, detail={"error": "Monat nicht gefunden"}
            )
        return {monat: data[verkehrsmittel][monat]}

    return data[verkehrsmittel]


@app.post("/verkehr/{verkehrsmittel}", status_code=status.HTTP_201_CREATED)
def create_data(verkehrsmittel: str, body: SetData):
    """
    Creates a new monthly record for a transport type.

    Args:
        verkehrsmittel (str): Name of the transport type.
        body (SetData): Month and employee count.

    Returns:
        SetData: The created record.

    Raises:
        HTTPException:
            - 404 if the transport type is invalid.
            - 400 if the value is outside the allowed range.
            - 409 if the month already exists.
    """
    validate_transport(verkehrsmittel)
    validate_range(body.anzahl)

    if body.monat in data[verkehrsmittel]:
        raise HTTPException(
            status_code=409, detail={"error": "Monat bereits vorhanden"}
        )

    data[verkehrsmittel][body.monat] = body.anzahl
    return body


@app.put("/verkehr/{verkehrsmittel}")
def set_data(verkehrsmittel: str, body: SetData):
    """
    Sets (creates or replaces) a monthly record for a transport type.

    If the month already exists, the value is overwritten.
    If it does not exist, a new entry is created.

    Args:
        verkehrsmittel (str): Name of the transport type.
        body (SetData): Month and employee count.

    Returns:
        SetData: The updated record.

    Raises:
        HTTPException:
            - 404 if the transport type is invalid.
            - 400 if the value is outside the allowed range.
    """
    validate_transport(verkehrsmittel)
    validate_range(body.anzahl)

    data[verkehrsmittel][body.monat] = body.anzahl
    return body


@app.patch("/verkehr/{verkehrsmittel}")
def patch_data(verkehrsmittel: str, body: SetData):
    """
    Incrementally updates an existing monthly record.

    The provided value is added to the current stored value.

    Args:
        verkehrsmittel (str): Name of the transport type.
        body (SetData): Month and increment/decrement value.

    Returns:
        SetData: The updated record with the new total value.

    Raises:
        HTTPException:
            - 404 if the transport type or month does not exist.
            - 400 if the resulting value is outside the range 0–250.
    """
    validate_transport(verkehrsmittel)

    if body.monat not in data[verkehrsmittel]:
        raise HTTPException(status_code=404, detail={"error": "Monat nicht gefunden"})

    new_value = data[verkehrsmittel][body.monat] + body.anzahl
    validate_range(new_value)

    data[verkehrsmittel][body.monat] = new_value
    return SetData(monat=body.monat, anzahl=new_value)


@app.delete("/verkehr/{verkehrsmittel}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data(verkehrsmittel: str, body: DeleteData):
    """
    Deletes a monthly record for a transport type.

    Args:
        verkehrsmittel (str): Name of the transport type.
        body (DeleteData): Month to be deleted.

    Raises:
        HTTPException:
            - 404 if the transport type or month does not exist.
    """
    validate_transport(verkehrsmittel)

    if body.monat not in data[verkehrsmittel]:
        raise HTTPException(status_code=404, detail={"error": "Monat nicht gefunden"})

    del data[verkehrsmittel][body.monat]
