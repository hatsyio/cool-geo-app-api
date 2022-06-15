from fastapi import Depends
from jinja2 import Template

from app.database.adapter import PostalCodeAdapter
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
        params, postal_codes_filter = PostalCodeAdapter.get_postal_code_filter(
            postal_codes
        )
        query = template.render(postal_codes_filter=postal_codes_filter)
        data = self.database.run_query_with_params(query, params)
        return [PostalCode(**row) for row in data]

    def get_postal_codes_union(self, postal_codes: list[str] | None) -> Geometry:
        template: Template = self.template_loader.load_template(
            "select_postal_codes_union.jinja"
        )
        params, postal_codes_filter = PostalCodeAdapter.get_postal_code_filter(
            postal_codes
        )
        query = template.render(postal_codes_filter=postal_codes_filter)
        data = self.database.run_query_with_params(query, params)
        return Geometry(**data[0])
