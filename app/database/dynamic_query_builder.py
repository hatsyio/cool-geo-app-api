class DynamicQueryBuilder:
    def __init__(self, table_name, select_columns, group_by_columns):
        self.table_name = table_name
        self.select_columns = select_columns
        self.group_by_columns = group_by_columns
        self.with_clause = (
            "WITH postal_codes as (SELECT id, code FROM postal_codes {where})"
        )
        self.with_clause_where = ""
        self.with_clause_enabled = False

    def add_with(self):
        self.with_clause_enabled = True

    def restrict_with(self):
        self.with_clause_where = "WHERE code = %s"

    def build_query(self, filters):
        query = "SELECT "
        query += ", ".join(self.select_columns)
        query += " FROM " + self.table_name
        if self.with_clause_enabled:
            query = self.with_clause.format(where=self.with_clause_where) + query
            query += (
                " INNER JOIN postal_codes pc ON pc.id = "
                + self.table_name
                + ".postal_code_id"
            )
        query += " WHERE 1=1 "
        query += self._build_where_clause(filters)
        query += " GROUP BY "
        query += ", ".join(self.group_by_columns)
        query += ";"
        return query

    @staticmethod
    def _build_where_clause(filters):
        where_clause = ""
        for filter in filters:
            where_clause += " AND " + filter
        return where_clause
