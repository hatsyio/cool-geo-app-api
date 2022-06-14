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


def test_get_ages():
    mock_data = [
        tuple("<=24"),
        tuple("25-34"),
        tuple("35-44"),
        tuple("45-54"),
        tuple("55-64"),
        tuple(">=65"),
    ]
    mock_database(mock_data)

    response = client.get("/payments/ages")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()


def test_get_aggregation():
    mock_data = [(89024.69868,)]
    mock_database(mock_data)

    response = client.get("/payments/aggregation")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()
    assert response.json()[0].keys() == {
        "amount",
        "p_age",
        "p_month",
        "code",
        "p_gender",
    }


def test_get_aggregation_by_postal_code():
    mock_data = [("28019", 89024.69868)]
    mock_database(mock_data)

    response = client.get("/payments/aggregation/postal-codes/28019")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()
    assert response.json()[0].keys() == {
        "amount",
        "p_age",
        "p_month",
        "code",
        "p_gender",
    }
    assert response.json()[0]["code"] == "28019"


def test_get_aggregation_with_time_series():
    mock_data = [(datetime.date(2015, 9, 1), 89024.69868)]
    mock_database(mock_data)

    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2015, 9, 1)

    response = client.get(
        f"/payments/aggregation/time-series/{start_date}/{end_date}".format(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()
    for row in response.json():
        assert row.keys() == {"amount", "p_age", "p_month", "code", "p_gender"}
    for row in response.json():
        assert (
            datetime.datetime.strptime(row["p_month"], "%Y-%m-%d").date() >= start_date
        )
        assert datetime.datetime.strptime(row["p_month"], "%Y-%m-%d").date() <= end_date
