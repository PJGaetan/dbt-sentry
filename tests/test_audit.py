import pytest
from click.testing import CliRunner
from dbt_sentry.audit import audit


def test_profile():
    runner = CliRunner()
    result = runner.invoke(
        audit,
        [
            "profile",
            "stg_payments",
            "--dbt-path",
            "jaffle_shop",
        ],
    )
    assert result.exit_code == 0
    assert (
        "| column_name    | data_type | row_count | not_null_proportion | distinct_proportion | distinct_count |"
        in result.output
    )


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "customer_id",
            (
                "Primary key customer_id not a columns in both tables dbt.main.stg_payments && dbt.prd.stg_payments",
                1,
            ),
        ),
        ("payment_id", ("a: dbt.main.stg_payments && b: dbt.prd.stg_payments", 0)),
        (
            "payment_id",
            (
                "| column_name    | perfect_match | null_in_a | null_in_b | missing_from_a | missing_from_b | conflicting_values |",
                0,
            ),
        ),
    ],
)
def test_compare_model(test_input, expected):
    primary_key = test_input
    output, status_code = expected
    runner = CliRunner()
    result = runner.invoke(
        audit,
        [
            "compare-model",
            "stg_payments",
            "--dbt-path",
            "jaffle_shop",
            "--target-compare",
            "prd",
            "--primary-key",
            primary_key,
        ],
    )
    assert result.exit_code == status_code
    assert output in result.output


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "customer_id",
            (
                "Primary key customer_id not a columns in both tables dbt.main.stg_payments && dbt.prd.stg_payments",
                1,
            ),
        ),
        ("payment_id", ("a: dbt.main.stg_payments && b: dbt.prd.stg_payments", 0)),
        (
            "payment_id",
            (
                "| payment_id | order_id | payment_method | amount |  in_a |  in_b |",
                0,
            ),
        ),
    ],
)
def test_compare_rows(test_input, expected):
    primary_key = test_input
    output, status_code = expected
    runner = CliRunner()
    result = runner.invoke(
        audit,
        [
            "compare-rows",
            "stg_payments",
            "--dbt-path",
            "jaffle_shop",
            "--target-compare",
            "prd",
            "--primary-key",
            primary_key,
        ],
    )
    assert result.exit_code == status_code
    assert output in result.output


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            None,
            ("Please specify at least one dimension", 1),
        ),
        (
            ["last_name"],
            (
                "| last_name | a_sum(number_of_o... | b_sum(number_of_o... | sum(number_of_ord... |",
                0,
            ),
        ),
    ],
)
def test_metric(test_input, expected):
    dimensions = test_input
    output, status_code = expected
    runner = CliRunner()
    result = runner.invoke(
        audit,
        [
            "metric",
            "customers",
            "sum(number_of_orders)",
            *(dimensions or []),
            "--dbt-path",
            "jaffle_shop",
            "--target-compare",
            "prd",
        ],
    )
    assert result.exit_code == status_code
    assert output in result.output


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "tests/sql/custom_query.sql",
            (
                "| customer_id | first_name | last_name | first_order | most_recent_order | number_of_orders |",
                0,
            ),
        ),
        (
            "tests/sql/custom_query_error.sql",
            ("Error parsing inline query", 1),
        ),
    ],
)
def test_custom(test_input, expected):
    file_input = test_input
    output, status_code = expected
    runner = CliRunner()
    result = runner.invoke(
        audit,
        [
            "custom",
            file_input,
            "--dbt-path",
            "jaffle_shop",
        ],
    )
    assert result.exit_code == status_code
    assert output in result.output
