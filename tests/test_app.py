import io
import unittest

from smartanalytics import create_app


class DashboardApiTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app({"TESTING": True})
        self.client = app.test_client()

    def _upload_sample(self):
        csv_data = """customer_id,signup_date,last_activity_date,status,plan,location
1,2024-01-01,2024-04-01,active,Basic,NY
2,2024-01-10,2024-04-02,cancelled,Premium,CA
3,2024-02-01,2024-04-12,active,Basic,TX
"""
        return self.client.post(
            "/api/upload",
            data={"file": (io.BytesIO(csv_data.encode("utf-8")), "customers.csv")},
            content_type="multipart/form-data",
        )

    def test_upload_and_summary(self):
        response = self._upload_sample()
        self.assertEqual(response.status_code, 200)

        summary = self.client.get("/api/summary")
        payload = summary.get_json()
        self.assertEqual(payload["total_customers"], 3)
        self.assertEqual(payload["churned_customers"], 1)
        self.assertEqual(payload["retained_customers"], 2)
        self.assertAlmostEqual(payload["churn_rate"], 33.33, places=2)

    def test_upload_rejects_missing_columns(self):
        csv_data = "customer_id,signup_date,status\n1,2024-01-01,active\n"
        response = self.client.post(
            "/api/upload",
            data={"file": (io.BytesIO(csv_data.encode("utf-8")), "customers.csv")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid CSV format", response.get_json()["error"])

    def test_export_returns_csv(self):
        self._upload_sample()
        response = self.client.get("/api/export/summary.csv")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response.content_type)
        self.assertIn("total_customers", response.data.decode("utf-8"))

    def test_cohorts_trends_segments_endpoints(self):
        self._upload_sample()

        cohorts = self.client.get("/api/cohorts")
        self.assertEqual(cohorts.status_code, 200)
        self.assertTrue(len(cohorts.get_json()) >= 1)

        trends = self.client.get("/api/trends")
        self.assertEqual(trends.status_code, 200)
        self.assertTrue(len(trends.get_json()) >= 1)

        segments = self.client.get("/api/segments")
        self.assertEqual(segments.status_code, 200)
        payload = segments.get_json()
        self.assertIn("plan", payload)


if __name__ == "__main__":
    unittest.main()
