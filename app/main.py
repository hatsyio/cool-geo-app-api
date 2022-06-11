from datetime import datetime

from fastapi import Depends, FastAPI, Path, Query

from app.service.models import PaystatAggregation, PostalCode
from app.service.paystat import PaystatService
from app.service.postal_code import PostalCodeService

app = FastAPI()


@app.get("/ages")
async def get_ages(paystat_service: PaystatService = Depends()) -> [str]:
    return paystat_service.get_ages()


@app.get("/genders")
async def get_genders(paystat_service: PaystatService = Depends()) -> [str]:
    return paystat_service.get_genders()


@app.get("/months")
async def get_months(paystat_service: PaystatService = Depends()) -> [str]:
    return paystat_service.get_months()


@app.get("/paystat/")
async def get_paystat_aggregation(
    ages: list[str] | None = Query(default=None),
    genders: list[str] | None = Query(default=None),
    start_date: str | None = Query(default=None, regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str | None = Query(default=None, regex="^\d{4}-\d{2}-\d{2}$"),
    postal_code: str | None = Query(default=None),
    add_postal_code: bool = False,
    add_month: bool = False,
    paystat_service: PaystatService = Depends(),
) -> [PaystatAggregation]:
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return paystat_service.get_aggregation(
        ages=ages,
        genders=genders,
        start_date=start_date,
        end_date=end_date,
        postal_code=postal_code,
        add_postal_code=add_postal_code,
        add_month=add_month,
    )


@app.get("/paystat/postal-codes/{postal_code}")
async def get_paystat_aggregation_by_postal_code(
    postal_code: str,
    ages: list[str] | None = Query(default=None),
    genders: list[str] | None = Query(default=None),
    start_date: str | None = Query(default=None, regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str | None = Query(default=None, regex="^\d{4}-\d{2}-\d{2}$"),
    add_month: bool = False,
    paystat_service: PaystatService = Depends(),
) -> [PaystatAggregation]:
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return paystat_service.get_aggregation(
        ages=ages,
        genders=genders,
        start_date=start_date,
        end_date=end_date,
        postal_code=postal_code,
        add_postal_code=True,
        add_month=add_month,
    )


@app.get("/paystat/time-series/{start_date}/{end_date}")
async def get_paystat_aggregation_with_time_series(
    start_date: str = Path(regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Path(regex="^\d{4}-\d{2}-\d{2}$"),
    ages: list[str] | None = Query(default=None),
    genders: list[str] | None = Query(default=None),
    postal_code: str | None = Query(default=None),
    add_postal_code: bool = False,
    paystat_service: PaystatService = Depends(),
) -> [PaystatAggregation]:
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return paystat_service.get_aggregation(
        ages=ages,
        genders=genders,
        start_date=start_date,
        end_date=end_date,
        postal_code=postal_code,
        add_postal_code=add_postal_code,
        add_month=True,
    )


@app.get("/postal-codes")
async def get_postal_codes(
    postal_code_service: PostalCodeService = Depends(),
) -> [PostalCode]:
    return postal_code_service.get_postal_codes()
