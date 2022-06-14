from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from jinja2 import Template

from app.database.adapter import PaymentsAdapter
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
        return self._run_select_distinct(PaymentsAdapter.AGE_COLUMN)

    def get_genders(self) -> list[str]:
        return self._run_select_distinct(PaymentsAdapter.GENDER_COLUMN)

    def get_months(self) -> list[str]:
        return self._run_select_distinct(PaymentsAdapter.MONTH_COLUMN)

    def _run_select_distinct(self, column) -> list[str]:
        template: Template = self.template_loader.load_template(
            "select_distinct_from_paystats.jinja"
        )
        query = template.render(column=column)
        data = self.database.run_query(query)
        return [str(row[column]) for row in data]

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

        if add_ages:
            columns.append(PaymentsAdapter.AGE_COLUMN)
        if add_genders:
            columns.append(PaymentsAdapter.GENDER_COLUMN)
        if add_postal_code:
            columns.append(PaymentsAdapter.POSTAL_CODE_COLUMN)
        if add_month:
            columns.append(PaymentsAdapter.MONTH_COLUMN)

        select_statement = PaymentsAdapter.get_select_statement(columns)

        filters = []
        params = tuple()
        if genders:
            gender_params, gender_filter = PaymentsAdapter.get_genders_filter(genders)
            params += gender_params
            filters.append(gender_filter)
        if ages:
            ages_params, ages_filter = PaymentsAdapter.get_ages_filter(ages)
            params += ages_params
            filters.append(ages_filter)
        if start_date:
            (
                start_date_params,
                start_date_filter,
            ) = PaymentsAdapter.get_start_date_filter(start_date)
            params += start_date_params
            filters.append(start_date_filter)
        if end_date:
            end_date_params, end_date_filter = PaymentsAdapter.get_end_date_filter(
                end_date
            )
            params += end_date_params
            filters.append(end_date_filter)
        if postal_codes:
            (
                postal_codes_params,
                postal_codes_filter,
            ) = PaymentsAdapter.get_postal_codes_filter(postal_codes)
            params += postal_codes_params
            filters.append(postal_codes_filter)

        where_clause = "".join(filters)

        group_by_statement = PaymentsAdapter.get_group_by_statement(columns)

        template: Template = self.template_loader.load_template(
            "select_aggregation_from_paystats.jinja"
        )
        query = template.render(
            select_statement=select_statement,
            where_clause=where_clause,
            group_by_statement=group_by_statement,
        )

        data = self.database.run_query_with_params(query, params)

        return [PaymentAggregation(**row) for row in data]
