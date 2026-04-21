from __future__ import annotations

import unittest

from main import create_app


class VerkehrApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()

    def test_root_overview(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("endpoints", payload)

    def test_get_all_for_unknown_transport(self) -> None:
        response = self.client.get("/verkehr/ferry")
        self.assertEqual(response.status_code, 404)

    def test_put_and_get_single_month(self) -> None:
        put_response = self.client.put("/verkehr/bus", json={"monat": 1, "anzahl": 50})
        self.assertEqual(put_response.status_code, 200)

        get_response = self.client.get("/verkehr/bus?monat=1")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json(), {"1": 50})

    def test_get_invalid_month(self) -> None:
        response = self.client.get("/verkehr/bus?monat=13")
        self.assertEqual(response.status_code, 400)

    def test_post_and_conflict(self) -> None:
        first_response = self.client.post("/verkehr/tram", json={"monat": 2, "anzahl": 20})
        second_response = self.client.post("/verkehr/tram", json={"monat": 2, "anzahl": 25})

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 409)

    def test_patch_success_and_missing_month(self) -> None:
        self.client.put("/verkehr/ubahn", json={"monat": 3, "anzahl": 100})
        patch_response = self.client.patch("/verkehr/ubahn", json={"monat": 3, "anzahl": 5})
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.get_json(), {"monat": 3, "anzahl": 105})

        missing_response = self.client.patch(
            "/verkehr/ubahn", json={"monat": 4, "anzahl": 5}
        )
        self.assertEqual(missing_response.status_code, 404)

    def test_delete_success_and_missing_month(self) -> None:
        self.client.put("/verkehr/bus", json={"monat": 5, "anzahl": 12})
        delete_response = self.client.delete("/verkehr/bus", json={"monat": 5})
        self.assertEqual(delete_response.status_code, 204)

        missing_response = self.client.delete("/verkehr/bus", json={"monat": 5})
        self.assertEqual(missing_response.status_code, 404)

    def test_bad_payloads(self) -> None:
        response = self.client.post("/verkehr/bus", json={"monat": "abc", "anzahl": 4})
        self.assertEqual(response.status_code, 400)

        response = self.client.delete("/verkehr/bus", json={})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
