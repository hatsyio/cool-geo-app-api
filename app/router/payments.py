from datetime import datetime
from functools import lru_cache

from fastapi import APIRouter, Depends, Path, Query, Security

from app.authorization import get_current_active_user
from app.service.models import PaymentAggregation
from app.service.payments import PaymentsService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@lru_cache
@router.get(
    "/ages", dependencies=[Security(get_current_active_user, scopes=["payments"])]
)
async def get_payments_ages(
    payments_service: PaymentsService = Depends(),
) -> [str]:
    return payments_service.get_ages()


@lru_cache
@router.get(
    "/genders", dependencies=[Security(get_current_active_user, scopes=["payments"])]
)
async def get_payments_genders(payments_service: PaymentsService = Depends()) -> [str]:
    return payments_service.get_genders()


@lru_cache
@router.get(
    "/months", dependencies=[Security(get_current_active_user, scopes=["payments"])]
)
async def get_payments_months(payments_service: PaymentsService = Depends()) -> [str]:
    return payments_service.get_months()


@lru_cache
@router.get(
    "/aggregation",
    dependencies=[Security(get_current_active_user, scopes=["payments"])],
)
async def get_payments_aggregation(
    ages: list[str] | None = Query(default=None),
    add_ages: bool = Query(default=False),
    genders: list[str] | None = Query(default=None),
    add_genders: bool = Query(default=False),
    postal_code: list[str] | None = Query(default=None),
    add_postal_code: bool = Query(default=False),
    start_date: str | None = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: str | None = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    add_month: bool = Query(default=False),
    payments_service: PaymentsService = Depends(),
) -> [PaymentAggregation]:
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return payments_service.get_aggregation(
        ages=ages,
        add_ages=add_ages,
        genders=genders,
        add_genders=add_genders,
        postal_codes=postal_code,
        add_postal_code=add_postal_code,
        start_date=start_date,
        end_date=end_date,
        add_month=add_month,
    )


@lru_cache
@router.get(
    "/aggregation/postal-codes/{postal_code}",
    dependencies=[Security(get_current_active_user, scopes=["payments"])],
)
async def get_payments_aggregation_by_postal_code(
    postal_code: str,
    ages: list[str] | None = Query(default=None),
    add_ages: bool = Query(default=False),
    genders: list[str] | None = Query(default=None),
    add_genders: bool = Query(default=False),
    start_date: str | None = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: str | None = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    add_month: bool = Query(default=False),
    payments_service: PaymentsService = Depends(),
) -> [PaymentAggregation]:
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return payments_service.get_aggregation(
        postal_codes=[postal_code],
        add_postal_code=True,
        ages=ages,
        add_ages=add_ages,
        genders=genders,
        add_genders=add_genders,
        start_date=start_date,
        end_date=end_date,
        add_month=add_month,
    )


@lru_cache
@router.get(
    "/aggregation/time-series/{start_date}/{end_date}",
    dependencies=[Security(get_current_active_user, scopes=["payments"])],
)
async def get_payments_aggregation_with_time_series(
    start_date: str = Path(regex=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Path(regex=r"^\d{4}-\d{2}-\d{2}$"),
    ages: list[str] | None = Query(default=None),
    add_ages: bool = Query(default=False),
    genders: list[str] | None = Query(default=None),
    add_genders: bool = Query(default=False),
    postal_codes: list[str] | None = Query(default=None),
    add_postal_code: bool = Query(default=False),
    payments_service: PaymentsService = Depends(),
) -> [PaymentAggregation]:
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return payments_service.get_aggregation(
        start_date=start_date,
        end_date=end_date,
        add_month=True,
        ages=ages,
        add_ages=add_ages,
        genders=genders,
        add_genders=add_genders,
        postal_codes=postal_codes,
        add_postal_code=add_postal_code,
    )
