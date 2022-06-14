import datetime

from fastapi.testclient import TestClient

from app.database.database import Database
from app.main import app

client = TestClient(app)


def mock_database(mock_data):
    def mock_run_query(*args, **kwargs):
        return mock_data

    app.dependency_overrides[Database] = type(
        "Database",
        (object,),
        {"run_query": mock_run_query, "run_query_with_params": mock_run_query},
    )


def test_get_postal_codes():
    mock_data = [
        ("28019", 0xDEADBEEF0),
        ("28018", 0xDEADBEEF1),
        ("28017", 0xDEADBEEF2),
        ("28016", 0xDEADBEEF3),
        ("28015", 0xDEADBEEF4),
    ]
    mock_database(mock_data)

    response = client.get("/postal-codes/")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()
    for row in response.json():
        assert row.keys() == {"code", "the_geom"}


