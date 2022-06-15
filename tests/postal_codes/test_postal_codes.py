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
        {"code": "28019", "the_geom": 0xDEADBEEF0},
        {"code": "28018", "the_geom": 0xDEADBEEF1},
        {"code": "28017", "the_geom": 0xDEADBEEF2},
        {"code": "28016", "the_geom": 0xDEADBEEF3},
        {"code": "28015", "the_geom": 0xDEADBEEF4},
    ]
    mock_database(mock_data)

    response = client.get("/postal-codes/")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()
    for row in response.json():
        assert row.keys() == {"code", "the_geom"}
