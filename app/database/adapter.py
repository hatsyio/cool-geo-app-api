import datetime


class PostalCodeAdapter:
    ID_COLUMN = "id"
    POSTAL_CODE_COLUMN = "code"
    GEOMETRY_COLUMN = "the_geom"

    @staticmethod
    def get_postal_code_filter(postal_codes: list[str] | None) -> tuple[tuple, str]:
        if postal_codes:
            params = tuple(postal_codes)
            placeholders = ",".join(["%s"] * len(postal_codes))
            postal_codes_filter = (
                " and "
                + PostalCodeAdapter.POSTAL_CODE_COLUMN
                + " in ("
                + placeholders
                + ") "
            )
            return params, postal_codes_filter
        return tuple(), ""


class PaymentsAdapter:
    ID_COLUMN = "id"
    POSTAL_CODE_ID_COLUMN = "postal_code_id"
    GENDER_COLUMN = "p_gender"
    AGE_COLUMN = "p_age"
    POSTAL_CODE_COLUMN = PostalCodeAdapter.POSTAL_CODE_COLUMN
    AMOUNT_COLUMN = "amount"
    MONTH_COLUMN = "p_month"

    @staticmethod
    def get_select_statement(columns: [str]) -> str:
        if columns:
            select_fields = ",".join(columns) + ", coalesce(sum(amount), 0) as amount"
            return "select " + select_fields
        return "select coalesce(sum(amount), 0) as amount"

    @staticmethod
    def get_genders_filter(genders: [str]) -> tuple[tuple, str]:
        params = tuple(genders)
        placeholders = ",".join(["%s"] * len(genders))
        gender_filter = (
            " and " + PaymentsAdapter.GENDER_COLUMN + " in (" + placeholders + ") "
        )
        return params, gender_filter

    @staticmethod
    def get_ages_filter(ages: [str]) -> tuple[tuple, str]:
        params = tuple(ages)
        placeholders = ",".join(["%s"] * len(ages))
        ages_filter = (
            " and " + PaymentsAdapter.AGE_COLUMN + " in (" + placeholders + ") "
        )
        return params, ages_filter

    @staticmethod
    def get_start_date_filter(start_date: datetime.date) -> tuple[tuple, str]:
        return (start_date,), " and " + PaymentsAdapter.MONTH_COLUMN + " >= %s "

    @staticmethod
    def get_end_date_filter(end_date: datetime.date) -> tuple[tuple, str]:
        return (end_date,), " and " + PaymentsAdapter.MONTH_COLUMN + " <= %s "

    @staticmethod
    def get_postal_codes_filter(postal_codes: [str]) -> tuple[tuple, str]:
        params = tuple(postal_codes)
        placeholders = ",".join(["%s"] * len(postal_codes))
        postal_codes_filter = (
            " and " + PaymentsAdapter.POSTAL_CODE_COLUMN + " in (" + placeholders + ") "
        )
        return params, postal_codes_filter

    @staticmethod
    def get_group_by_statement(columns: [str]) -> str:
        if columns:
            group_by_fields = ",".join(columns)
            return "group by " + group_by_fields
        return ""
