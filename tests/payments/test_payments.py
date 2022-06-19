import datetime

from fastapi.testclient import TestClient
from pytest_fastapi_deps import DependencyOverrider

from app.authorization import get_current_active_user
from app.database.database import Database
from app.main import app

client = TestClient(app)


def get_mock_database(mock_data):
    def mock_run_query(*args, **kwargs):
        return mock_data

    return type(
        "Database",
        (object,),
        {"run_query": mock_run_query, "run_query_with_params": mock_run_query},
    )


def skip_auth():
    pass


def test_get_ages():
    mock_data = [
        {"p_age": "<=24"},
        {"p_age": "25-34"},
        {"p_age": "35-44"},
        {"p_age": "45-54"},
        {"p_age": "55-64"},
        {"p_age": ">=65"},
    ]
    mock_database = get_mock_database(mock_data)
    with DependencyOverrider(
        app, overrides={get_current_active_user: skip_auth, Database: mock_database}
    ):
        response = client.get("/payments/ages")
        assert response.status_code == 200
        assert type(response.json()) == list
        assert response.json()


def test_get_aggregation():
    mock_data = [{"amount": 89024.69868}]
    mock_database = get_mock_database(mock_data)

    with DependencyOverrider(
        app, overrides={get_current_active_user: skip_auth, Database: mock_database}
    ):
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
    mock_data = [{"code": "28019", "amount": 89024.69868}]
    mock_database = get_mock_database(mock_data)

    with DependencyOverrider(
        app, overrides={get_current_active_user: skip_auth, Database: mock_database}
    ):
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
    mock_data = [{"p_month": datetime.date(2015, 9, 1), "amount": 89024.69868}]
    mock_database = get_mock_database(mock_data)

    with DependencyOverrider(
        app, overrides={get_current_active_user: skip_auth, Database: mock_database}
    ):
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
                datetime.datetime.strptime(row["p_month"], "%Y-%m-%d").date()
                >= start_date
            )
            assert (
                datetime.datetime.strptime(row["p_month"], "%Y-%m-%d").date()
                <= end_date
            )
