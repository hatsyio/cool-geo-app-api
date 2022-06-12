from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from jinja2 import Template

from app.database.database import Database
from app.database.template_loader import TemplateLoader
from app.service.models import PaymentAggregation


class PaymentsService:
    def __init__(
        self,
        database: Database = Depends(),
        template_loader: TemplateLoader = Depends(),
    ):
        self.database = database
        self.template_loader = template_loader

    def get_ages(self) -> list[str]:
        return self._run_select_distinct("p_age")

    def get_genders(self) -> list[str]:
        return self._run_select_distinct("p_gender")

    def get_months(self) -> list[str]:
        return self._run_select_distinct("p_month")

    def _run_select_distinct(self, column) -> list[str]:
        template: Template = self.template_loader.load_template(
            "select_distinct_from_paystats.jinja"
        )
        query = template.render(column=column)
        data = self.database.run_query(query)
        return [str(row[0]) for row in data]

    def get_aggregation(
        self,
        ages: Optional[List[str]] = None,
        add_ages: bool = False,
        genders: Optional[List[str]] = None,
        add_genders: bool = False,
        postal_codes: Optional[List[str]] = None,
        add_postal_code: bool = False,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        add_month: bool = False,
    ) -> [PaymentAggregation]:

        columns = []
        select_fields: str = ""
        group_by: str = ""

        if add_ages:
            columns.append("p_age")
        if add_genders:
            columns.append("p_gender")
        if add_postal_code:
            columns.append("code")
        if add_month:
            columns.append("p_month")

        if columns:
            select_fields = ",".join(columns) + ","
            group_by = "group by " + ",".join(columns)

        filters = []
        params = tuple()
        if genders:
            params += tuple(genders)
            placeholders = ",".join(["%s"] * len(genders))
            filters.append(" and p_gender in (" + placeholders + ") ")
        if ages:
            params += tuple(ages)
            placeholders = ",".join(["%s"] * len(ages))
            filters.append(" and p_age in (" + placeholders + ") ")
        if start_date:
            params += (start_date,)
            filters.append(" and p_month >= %s ")
        if end_date:
            params += (end_date,)
            filters.append(" and p_month <= %s ")
        if postal_codes:
            params += tuple(postal_codes)
            placeholders = ",".join(["%s"] * len(postal_codes))
            filters.append(" and code in (" + placeholders + ") ")

        where_clause = "".join(filters)
        template: Template = self.template_loader.load_template(
            "select_aggregation_from_paystats.jinja"
        )
        query = template.render(
            select_fields=select_fields, where_clause=where_clause, group_by=group_by
        )

        data = self.database.run_query_with_params(query, params)

        result = []
        for row in data:
            d = {}
            for i in range(len(columns)):
                d[columns[i]] = row[i]
            d["amount"] = row[-1]
            result.append(PaymentAggregation(**d))

        return result
