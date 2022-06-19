from functools import lru_cache

from fastapi import APIRouter, Depends, Query, Security

from app.authorization import get_current_active_user
from app.service.models import Geometry, PostalCode
from app.service.postal_codes import PostalCodesService

router = APIRouter(
    prefix="/postal-codes",
    tags=["Postal Codes"],
)


@lru_cache
@router.get(
    "/", dependencies=[Security(get_current_active_user, scopes=["postal-codes"])]
)
async def get_postal_codes(
    postal_codes_service: PostalCodesService = Depends(),
) -> [PostalCode]:
    return postal_codes_service.get_postal_codes()


@lru_cache
@router.get(
    "/find", dependencies=[Security(get_current_active_user, scopes=["postal-codes"])]
)
async def find_postal_codes(
    postal_codes: list[str] | None = Query(default=None),
    postal_codes_service: PostalCodesService = Depends(),
) -> [PostalCode]:
    return postal_codes_service.find_postal_codes(postal_codes)


@lru_cache
@router.get(
    "/union", dependencies=[Security(get_current_active_user, scopes=["postal-codes"])]
)
async def get_postal_codes_union(
    postal_codes: list[str] | None = Query(default=None),
    postal_codes_service: PostalCodesService = Depends(),
) -> Geometry:
    return postal_codes_service.get_postal_codes_union(postal_codes)
