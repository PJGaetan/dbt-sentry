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
