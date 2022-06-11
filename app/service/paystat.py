from datetime import datetime
from typing import List, Optional

from fastapi import Depends

from app.database.database import Database
from app.database.dynamic_query_builder import DynamicQueryBuilder
from app.database.query_loader import QueryLoader
from app.service.models import PaystatAggregation


class PaystatService:
    def __init__(self, database=Depends(Database), query_loader=Depends(QueryLoader)):
        self.database = database
        self.query_loader = query_loader

    def get_ages(self) -> list[str]:
        query = self.query_loader.load_query("get_ages.sql")
        data = self.database.run_query(query)
        return [str(row[0]) for row in data]

    def get_genders(self) -> list[str]:
        query = self.query_loader.load_query("get_genders.sql")
        data = self.database.run_query(query)
        return [str(row[0]) for row in data]

    def get_months(self) -> list[str]:
        query = self.query_loader.load_query("get_months.sql")
        data = self.database.run_query(query)
        return [str(row[0]) for row in data]

    def get_aggregation(
        self,
        ages: Optional[List[str]] = None,
        genders: Optional[List[str]] = None,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        postal_code: Optional[str] = None,
        add_postal_code: bool = False,
        add_month: bool = False,
    ) -> [PaystatAggregation]:

        columns = ["p_age", "p_gender"]

        if add_postal_code:
            columns.append("code")
        if add_month:
            columns.append("p_month")

        aggregation = ["sum(amount)"]
        select_columns = columns + aggregation
        group_by_columns = columns

        query_builder = DynamicQueryBuilder(
            "paystats", select_columns, group_by_columns
        )

        filters = []
        params = tuple()
        if genders:
            params += tuple(genders)
            placeholders = ["%s" for i in range(len(genders))]
            filters.append(" p_gender in (" + ",".join(placeholders) + ") ")
        if ages:
            params += tuple(ages)
            placeholders = ["%s" for i in range(len(ages))]
            filters.append(" p_age in (" + ",".join(placeholders) + ") ")
        if start_date:
            params += (start_date,)
            filters.append(" p_month >= %s ")
        if end_date:
            params += (end_date,)
            filters.append(" p_month <= %s ")
        if postal_code or add_postal_code:
            query_builder.add_with()
            if postal_code:
                params = (postal_code,) + params
                query_builder.restrict_with()

        query = query_builder.build_query(filters)
        data = self.database.run_query_with_params(query, params)

        result = []
        for row in data:
            d = {}
            for i in range(len(columns)):
                d[columns[i]] = row[i]
            d["amount"] = row[-1]
            result.append(PaystatAggregation(**d))

        return result
