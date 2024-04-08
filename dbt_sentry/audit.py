import click
from agate import Table
from .options import global_test_options, GlobalTestOptions
from .template_query import (
    PROFILE_QUERY,
    COMPARE_COLUMNS_QUERY,
    COLUMNS_PROFILE_QUERY,
    COMPARE_RELATION_QUERY,
    COMPARE_METRICS_QUERY,
    TEMPLATED_METRICS_JINJA_QUERY,
)
from .utils import walk_dbt_project, grouper, get_files, File
import os
from .query_runner import QueryRunner


def print_agate_table(table: Table):
    columns = table.column_names
    col_grouped = grouper(columns[1:], 5)
    for col in col_grouped:
        t = table.select([columns[0], *[c for c in col if c is not None]])
        t.print_table(max_rows=None, max_columns=6)
        print("\n")


@click.group()
def audit():
    """Audit a specific piece of your dbt project."""
    pass


@audit.command()
@click.argument("model", nargs=1)
@global_test_options
def profile(model, target, profile, dbt_path, debug):
    """Generate the profile of a dbt model.

    Depends on dbt package data-mie/dbt-profiler.
    """
    profile_query = PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", model)

    walk_dbt_project(dbt_path, debug)
    qr = QueryRunner(debug, target, profile)
    table = qr.run_query(profile_query)
    print_agate_table(table)


@audit.command()
@click.argument("model", nargs=1)
@global_test_options
def compare_model(model, target, profile, dbt_path, debug):
    """Compare columns and relations of a model."""
    walk_dbt_project(dbt_path, debug)

    qr = QueryRunner(debug, target, profile)

    # TODO: only print
    # Better would be to go for added and removed
    # a: table_name_one && b: table_name_two
    # Column(s) not in a: [list of columns]
    # Column(s) not in b: [list of columns]
    query = COLUMNS_PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", model)
    table = qr.run_query(query)
    print_agate_table(table)
    not_in_both_columns = []
    for row in table.rows:
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))

    # Filter missing columns
    excluded_columns = "" if len(not_in_both_columns) == 0 else f"""'{"','".join(not_in_both_columns)}'"""
    query = COMPARE_COLUMNS_QUERY.replace("PLACEHOLDER_MODEL_NAME", model).replace("EXCLUDED_COLUMNS", excluded_columns)
    table = qr.run_query(query)
    table.print_table(max_rows=None, max_columns=7)


@audit.command()
@click.argument("model", nargs=1)
@global_test_options
def compare_rows(target, profile, dbt_path, model, debug):
    """Compare the rows difference a model."""
    walk_dbt_project(dbt_path, debug)
    qr = QueryRunner(debug, target, profile)

    query = COLUMNS_PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", model)
    table = qr.run_query(query)
    not_in_both_columns = []
    for row in table.rows:
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))
    click.echo("Excluded column(s): " + ", ".join(not_in_both_columns))

    # Filter missing columns
    excluded_columns = "" if len(not_in_both_columns) == 0 else f"""'{"','".join(not_in_both_columns)}'"""
    query = COMPARE_RELATION_QUERY.replace("PLACEHOLDER_MODEL_NAME", model).replace(
        "EXCLUDED_COLUMNS", excluded_columns
    )
    table = qr.run_query(query)
    table.print_table(max_rows=None, max_columns=7)


@audit.command()
@click.argument("model", nargs=1)
@click.argument("metric", nargs=1)
@click.argument("dimensions", nargs=-1)
@global_test_options
def metric(target, profile, dbt_path, debug, model, metric, dimensions):
    """Audit the trend of a specific metrics in dbt."""
    walk_dbt_project(dbt_path, debug)
    qr = QueryRunner(debug, target, profile)

    # Filter missing columns
    columns_to_replace = f"""'{"','".join(dimensions)}'"""
    metric_to_replace = f"'{metric}'"
    query = (
        TEMPLATED_METRICS_JINJA_QUERY.replace("PLACEHOLDER_MODEL_NAME", model)
        .replace("COLUMNS_TO_REPLACE", columns_to_replace)
        .replace("METRICS_TO_REPLACE", metric_to_replace)
    )
    table = qr.run_query(query)
    table.print_table(max_rows=None, max_columns=7)


@audit.command()
@click.argument("path", nargs=1)
@click.option("-R", "--recursive", is_flag=True, help="Recursively search for dbt files")
@global_test_options
def custom(target, profile, dbt_path, debug, path, recursive):
    """Run custom queries on a dbt project."""
    if recursive and os.path.isdir(path):
        files = get_files(path)
    elif os.path.isdir(path) and not recursive:
        raise click.ClickException(f"Directory {path} is not a file.")
    elif not os.path.exists(path) or not os.path.isfile(path):
        raise click.ClickException(f"File {path} does not exist")
    else:
        files = [File(content=open(path, "r").read(), name=path)]
    walk_dbt_project(dbt_path, debug)
    qr = QueryRunner(debug, target, profile)
    for f in files:
        table = qr.run_query(f.content)
        print_agate_table(table)
