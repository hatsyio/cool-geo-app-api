from fastapi import Depends

from app.database.database import Database
from app.database.query_loader import QueryLoader
from app.service.models import PostalCode


class PostalCodeService:
    def __init__(self, database=Depends(Database), query_loader=Depends(QueryLoader)):
        self.database = database
        self.query_loader = query_loader

    def get_postal_code(self, code: str) -> PostalCode:
        query = self.query_loader.load_query("get_postal_code.sql")
        params = (code,)
        data = self.database.run_query_with_params(query, params)
        return PostalCode(code=data[0][0], the_geom=data[0][1])

    def get_postal_codes(self) -> list[PostalCode]:
        query = self.query_loader.load_query("get_postal_codes.sql")
        data = self.database.run_query(query)
        return [PostalCode(code=row[0], the_geom=row[1]) for row in data]
