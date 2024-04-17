from click.testing import CliRunner
from dbt_sentry.ci import ci


def test_generate():
    runner = CliRunner()
    result = runner.invoke(
        ci,
        [
            "generate",
            "--target-compare",
            "prd",
            "--compare-branch",
            "test-ci-branch",
            "--dbt-path",
            "jaffle_shop",
        ],
    )
    assert result.exit_code == 0
    with open("jaffle_shop/dbts-artefact/audit.md", "r") as f:
        result = f.read()
    assert "Head: dbt.main.orders" in result
    assert "Compare: dbt.prd.orders" in result
    assert (
        "| column_name          | data_type | row_count | not_null_proportion | distinct_proportion | distinct_count | is_unique | min        | max        |     avg | median | std_dev_population | std_dev_sample | profiled_at          |"
        in result
    )
