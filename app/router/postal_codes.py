from functools import lru_cache

from fastapi import APIRouter, Depends, Query

from app.service.models import Geometry, PostalCode
from app.service.postal_codes import PostalCodesService

router = APIRouter(
    prefix="/postal-codes",
    tags=["Postal Codes"],
)


@lru_cache
@router.get("/")
async def get_postal_codes(
    postal_codes_service: PostalCodesService = Depends(),
) -> [PostalCode]:
    return postal_codes_service.get_postal_codes()


@lru_cache
@router.get("/find")
async def find_postal_codes(
    postal_codes: list[str] | None = Query(default=None),
    postal_codes_service: PostalCodesService = Depends(),
) -> [PostalCode]:
    return postal_codes_service.find_postal_codes(postal_codes)


@lru_cache
@router.get("/union")
async def get_postal_codes_union(
    postal_codes: list[str] | None = Query(default=None),
    postal_codes_service: PostalCodesService = Depends(),
) -> Geometry:
    return postal_codes_service.get_postal_codes_union(postal_codes)
