"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client fixture."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test cases for /health endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """Test that health endpoint returns ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAddEndpoint:
    """Test cases for /add endpoint."""

    def test_add_positive_numbers(self, client: TestClient) -> None:
        """Test addition of two positive numbers."""
        response = client.post("/add", json={"a": 5, "b": 3})
        assert response.status_code == 200
        assert response.json() == {"result": 8}

    def test_add_negative_numbers(self, client: TestClient) -> None:
        """Test addition of two negative numbers."""
        response = client.post("/add", json={"a": -5, "b": -3})
        assert response.status_code == 200
        assert response.json() == {"result": -8}

    def test_add_floats(self, client: TestClient) -> None:
        """Test addition of floating point numbers."""
        response = client.post("/add", json={"a": 2.5, "b": 3.5})
        assert response.status_code == 200
        assert response.json() == {"result": 6.0}

    def test_add_missing_field(self, client: TestClient) -> None:
        """Test that missing field returns 422."""
        response = client.post("/add", json={"a": 5})
        assert response.status_code == 422


class TestSubEndpoint:
    """Test cases for /sub endpoint."""

    def test_sub_positive_numbers(self, client: TestClient) -> None:
        """Test subtraction of two positive numbers."""
        response = client.post("/sub", json={"a": 10, "b": 3})
        assert response.status_code == 200
        assert response.json() == {"result": 7}


class TestMulEndpoint:
    """Test cases for /mul endpoint."""

    def test_mul_positive_numbers(self, client: TestClient) -> None:
        """Test multiplication of two positive numbers."""
        response = client.post("/mul", json={"a": 4, "b": 5})
        assert response.status_code == 200
        assert response.json() == {"result": 20}


class TestDivEndpoint:
    """Test cases for /div endpoint."""

    def test_div_positive_numbers(self, client: TestClient) -> None:
        """Test division of two positive numbers."""
        response = client.post("/div", json={"a": 20, "b": 4})
        assert response.status_code == 200
        assert response.json() == {"result": 5}

    def test_div_floats(self, client: TestClient) -> None:
        """Test division of floating point numbers."""
        response = client.post("/div", json={"a": 7.5, "b": 2.5})
        assert response.status_code == 200
        assert response.json() == {"result": 3.0}

    def test_div_by_zero_returns_400(self, client: TestClient) -> None:
        """Test that division by zero returns HTTP 400 with message."""
        response = client.post("/div", json={"a": 10, "b": 0})
        assert response.status_code == 400
        assert response.json() == {"detail": "Division by zero is not allowed"}

    def test_div_zero_by_number(self, client: TestClient) -> None:
        """Test division of zero by a number."""
        response = client.post("/div", json={"a": 0, "b": 5})
        assert response.status_code == 200
        assert response.json() == {"result": 0}
