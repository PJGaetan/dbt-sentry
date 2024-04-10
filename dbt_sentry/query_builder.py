from .template_query import (
    PROFILE_QUERY,
    COMPARE_COLUMNS_QUERY,
    COLUMNS_PROFILE_QUERY,
    COMPARE_RELATION_QUERY,
    TEMPLATED_METRICS_JINJA_QUERY,
)


class QueryBuilder:
    def __init__(self, model: str, model_to_compare: str):
        self.model = model
        self.model_to_compare = model_to_compare

    def profile_query(self) -> str:
        query = PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", self.model)
        return query

    def compare_columns_query(self) -> str:
        query = COLUMNS_PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", self.model).replace(
            "RELATION_TO_REPLACE", self.model_to_compare
        )
        return query

    def compare_model_query(self, not_in_both_columns: list) -> str:
        # Filter missing columns
        excluded_columns = "" if len(not_in_both_columns) == 0 else f"""'{"','".join(not_in_both_columns)}'"""
        query = (
            COMPARE_COLUMNS_QUERY.replace("PLACEHOLDER_MODEL_NAME", self.model)
            .replace("RELATION_TO_REPLACE", self.model_to_compare)
            .replace("EXCLUDED_COLUMNS", excluded_columns)
        )
        return query

    def compare_rows_query(self, not_in_both_columns: list) -> str:
        # Filter missing columns
        excluded_columns = "" if len(not_in_both_columns) == 0 else f"""'{"','".join(not_in_both_columns)}'"""
        query = (
            COMPARE_RELATION_QUERY.replace("PLACEHOLDER_MODEL_NAME", self.model)
            .replace("RELATION_TO_REPLACE", self.model_to_compare)
            .replace("EXCLUDED_COLUMNS", excluded_columns)
        )
        return query

    def metrics_query(self, dimensions: list, metric: str) -> str:
        columns_to_replace = f"""'{"','".join(dimensions)}'"""
        metric_to_replace = f"'{metric}'"

        # Filter missing columns
        query = (
            TEMPLATED_METRICS_JINJA_QUERY.replace("PLACEHOLDER_MODEL_NAME", self.model)
            .replace("COLUMNS_TO_REPLACE", columns_to_replace)
            .replace("METRICS_TO_REPLACE", metric_to_replace)
            .replace("RELATION_TO_REPLACE", self.model_to_compare)
        )
        return query
