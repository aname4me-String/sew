from __future__ import annotations

import unittest

from main import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_app().test_client()

    def test_overview(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_put_get_patch_delete_flow(self) -> None:
        self.assertEqual(
            self.client.put("/verkehr/bus", json={"monat": 1, "anzahl": 10}).status_code,
            200,
        )
        self.assertEqual(
            self.client.get("/verkehr/bus", query_string={"monat": 1}).get_json(),
            {"1": 10},
        )
        self.assertEqual(
            self.client.patch("/verkehr/bus", json={"monat": 1, "anzahl": 5}).get_json(),
            {"monat": 1, "anzahl": 15},
        )
        self.assertEqual(
            self.client.delete("/verkehr/bus", json={"monat": 1}).status_code,
            204,
        )

    def test_post_conflict(self) -> None:
        self.assertEqual(
            self.client.post("/verkehr/tram", json={"monat": 2, "anzahl": 20}).status_code,
            201,
        )
        self.assertEqual(
            self.client.post("/verkehr/tram", json={"monat": 2, "anzahl": 20}).status_code,
            409,
        )

    def test_errors(self) -> None:
        self.assertEqual(self.client.get("/verkehr/ship").status_code, 404)
        self.assertEqual(
            self.client.get("/verkehr/bus", query_string={"monat": 13}).status_code,
            400,
        )
        self.assertEqual(
            self.client.post("/verkehr/bus", json={"monat": "x", "anzahl": 1}).status_code,
            400,
        )
        self.assertEqual(self.client.delete("/verkehr/bus", json={}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
