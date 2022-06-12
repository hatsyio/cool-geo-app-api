from fastapi import Depends
from jinja2 import Template

from app.database.database import Database
from app.database.template_loader import TemplateLoader
from app.service.models import Geometry, PostalCode


class PostalCodesService:
    def __init__(
        self,
        database: Database = Depends(),
        template_loader: TemplateLoader = Depends(),
    ):
        self.database = database
        self.template_loader = template_loader

    def get_postal_codes(self) -> list[PostalCode]:
        return self._select_postal_codes([])

    def find_postal_codes(self, postal_codes: list[str] | None) -> list[PostalCode]:
        return self._select_postal_codes(postal_codes)

    def _select_postal_codes(self, postal_codes: list[str] | None) -> list[PostalCode]:
        template: Template = self.template_loader.load_template(
            "select_postal_codes.jinja"
        )
        postal_codes_filter, params = self._get_postal_code_filter_and_params(
            postal_codes
        )
        query = template.render(postal_codes_filter=postal_codes_filter)
        data = self.database.run_query_with_params(query, params)
        return [PostalCode(code=row[0], the_geom=row[1]) for row in data]

    def get_postal_codes_union(self, postal_codes: list[str] | None) -> Geometry:
        template: Template = self.template_loader.load_template(
            "select_postal_codes_union.jinja"
        )
        postal_codes_filter, params = self._get_postal_code_filter_and_params(
            postal_codes
        )
        query = template.render(postal_codes_filter=postal_codes_filter)
        data = self.database.run_query_with_params(query, params)
        return Geometry(the_geom=data[0][0], the_geom_as_text=data[0][1])

    @staticmethod
    def _get_postal_code_filter_and_params(postal_codes: list[str] | None) -> tuple:
        postal_codes_filter = ""
        params = tuple()
        if postal_codes:
            params += tuple(postal_codes)
            placeholders = ",".join(["%s"] * len(postal_codes))
            postal_codes_filter += " and code in (" + placeholders + ") "
        return postal_codes_filter, params
