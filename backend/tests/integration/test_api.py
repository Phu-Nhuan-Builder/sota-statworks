"""
Integration tests for API endpoints.
Uses httpx AsyncClient with full app.
"""
import io
import pytest
import pytest_asyncio
import httpx
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Synchronous test client for simple tests."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_csv_bytes():
    """Sample CSV file content."""
    content = """id,age,gender,score,group
1,22,1,78.5,1
2,25,2,82.3,1
3,21,1,65.4,2
4,28,2,90.1,1
5,23,1,71.2,2
6,30,2,88.7,1
7,24,1,79.8,2
8,26,2,84.5,1
9,22,1,68.3,2
10,29,2,92.1,1
11,21,1,75.6,2
12,27,2,81.4,1
13,23,1,70.2,2
14,25,2,86.3,1
15,22,1,73.8,2
"""
    return content.encode("utf-8")


class TestHealth:
    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "sessions" in data


class TestFileUpload:
    def test_upload_csv(self, client, sample_csv_bytes):
        response = client.post(
            "/files/upload",
            files={"file": ("test.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["meta"]["n_cases"] == 15
        assert data["meta"]["n_vars"] == 5
        # Cleanup
        client.delete(f"/files/{data['session_id']}")

    def test_upload_returns_variable_metadata(self, client, sample_csv_bytes):
        response = client.post(
            "/files/upload",
            files={"file": ("test.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
        )
        data = response.json()
        assert len(data["meta"]["variables"]) == 5
        var_names = [v["name"] for v in data["meta"]["variables"]]
        assert "age" in var_names
        assert "score" in var_names
        client.delete(f"/files/{data['session_id']}")

    def test_upload_unsupported_format(self, client):
        response = client.post(
            "/files/upload",
            files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
        )
        assert response.status_code == 400

    def test_get_data_paginated(self, client, sample_csv_bytes):
        upload_resp = client.post(
            "/files/upload",
            files={"file": ("test.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
        )
        session_id = upload_resp.json()["session_id"]
        response = client.get(f"/files/{session_id}/data?page=1&page_size=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 5
        assert data["total"] == 15
        client.delete(f"/files/{session_id}")


class TestDescriptives:
    @pytest.fixture
    def session_id(self, client, sample_csv_bytes):
        resp = client.post(
            "/files/upload",
            files={"file": ("test.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
        )
        sid = resp.json()["session_id"]
        yield sid
        client.delete(f"/files/{sid}")

    def test_frequencies(self, client, session_id):
        response = client.post("/descriptives/frequencies", json={
            "session_id": session_id,
            "variable": "gender",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["n_valid"] == 15
        assert len(data["rows"]) >= 2

    def test_descriptives(self, client, session_id):
        response = client.post("/descriptives/descriptives", json={
            "session_id": session_id,
            "variables": ["score", "age"],
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["rows"]) == 2

    def test_crosstabs(self, client, session_id):
        response = client.post("/descriptives/crosstabs", json={
            "session_id": session_id,
            "row_var": "gender",
            "col_var": "group",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["chi2"] is not None


class TestTTests:
    @pytest.fixture
    def session_id(self, client, sample_csv_bytes):
        resp = client.post(
            "/files/upload",
            files={"file": ("test.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
        )
        sid = resp.json()["session_id"]
        yield sid
        client.delete(f"/files/{sid}")

    def test_independent_ttest(self, client, session_id):
        response = client.post("/tests/ttest/independent", json={
            "session_id": session_id,
            "group_var": "gender",
            "test_var": "score",
            "equal_var": True,
            "alternative": "two-sided",
        })
        assert response.status_code == 200
        data = response.json()
        assert "statistic" in data
        assert "pvalue" in data
        assert 0.0 <= data["pvalue"] <= 1.0

    def test_one_sample_ttest(self, client, session_id):
        response = client.post("/tests/ttest/one-sample", json={
            "session_id": session_id,
            "variable": "score",
            "test_value": 75.0,
        })
        assert response.status_code == 200
        data = response.json()
        assert "statistic" in data
        assert "mean_diff" in data
