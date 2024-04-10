import click
from .options import global_test_options, GlobalTestOptions, global_compare_options, GlobalCompareOptions
from .output_formatter import OutputFormatter
from .utils import get_files, File
import os
from .query_runner import QueryRunner
from .query_builder import QueryBuilder


@click.group()
def audit():
    """Audit a specific piece of your dbt project."""
    pass


@audit.command()
@click.argument("model", nargs=1)
@global_test_options
def profile(model, **kwargs):
    """Generate the profile of a dbt model.

    Depends on dbt package data-mie/dbt-profiler.
    """
    options = GlobalTestOptions(**kwargs)

    qr = QueryRunner(options.debug, options.target, options.profile, options.dbt_path)
    qb = QueryBuilder(model, None)
    query = qb.profile_query()
    table = qr.run_query(query)

    OutputFormatter.print_agate_table(table)


@audit.command()
@click.argument("model", nargs=1)
@global_compare_options
@global_test_options
def compare_model(model, **kwargs):
    """Compare columns and relations of a model."""
    options = GlobalTestOptions(**kwargs)
    compare_options = GlobalCompareOptions(**kwargs)
    qr = QueryRunner(options.debug, options.target, options.profile, options.dbt_path)

    relation_base, manifest_base = compare_options.get_relations_base(model, options.target, options.profile, qr)
    relation_compare, _ = compare_options.get_relations_compare(model, options.profile, qr)
    qr.manifest = manifest_base

    qb = QueryBuilder(model, relation_compare.get_dbt_relation())

    # a: table_name_one && b: table_name_two
    OutputFormatter.print_compared_relation(relation_base, relation_compare)
    query = qb.compare_columns_query()
    table = qr.run_query(query)
    not_in_both_columns = []
    not_in_a = []
    not_in_b = []
    for row in table.rows:
        if row.get("in_a") == False:
            not_in_a.append(row.get("column_name"))
        if row.get("in_b") == False:
            not_in_b.append(row.get("column_name"))
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))
    # Column(s) not in a: [list of columns]
    # Column(s) not in b: [list of columns]
    OutputFormatter.print_excluded_columns(not_in_a, not_in_b)

    query = qb.compare_model_query(not_in_both_columns)
    table = qr.run_query(query)
    OutputFormatter.print_agate_table(table, format=False)


@audit.command()
@click.argument("model", nargs=1)
@global_compare_options
@global_test_options
def compare_rows(model, **kwargs):
    """Compare the rows difference a model."""
    options = GlobalTestOptions(**kwargs)
    compare_options = GlobalCompareOptions(**kwargs)
    qr = QueryRunner(options.debug, options.target, options.profile, options.dbt_path)

    relation_base, manifest_base = compare_options.get_relations_base(model, options.target, options.profile, qr)
    relation_compare, _ = compare_options.get_relations_compare(model, options.profile, qr)
    qr.manifest = manifest_base

    qb = QueryBuilder(model, relation_compare.get_dbt_relation())

    OutputFormatter.print_compared_relation(relation_base, relation_compare)
    query = qb.compare_columns_query()
    table = qr.run_query(query)
    not_in_both_columns = []
    not_in_a = []
    not_in_b = []
    for row in table.rows:
        if row.get("in_a") == False:
            not_in_a.append(row.get("column_name"))
        if row.get("in_b") == False:
            not_in_b.append(row.get("column_name"))
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))
    # Column(s) not in a: [list of columns]
    # Column(s) not in b: [list of columns]
    OutputFormatter.print_excluded_columns(not_in_a, not_in_b)

    # Filter missing columns
    query = qb.compare_rows_query(not_in_both_columns)
    table = qr.run_query(query)
    OutputFormatter.print_agate_table(table, format=False)


@audit.command()
@click.argument("model", nargs=1)
@click.argument("metric", nargs=1)
@click.argument("dimensions", nargs=-1)
@global_compare_options
@global_test_options
def metric(model, metric, dimensions, **kwargs):
    """Audit the trend of a specific metrics in dbt."""

    options = GlobalTestOptions(**kwargs)
    compare_options = GlobalCompareOptions(**kwargs)
    qr = QueryRunner(options.debug, options.target, options.profile, options.dbt_path)

    relation_base, manifest_base = compare_options.get_relations_base(model, options.target, options.profile, qr)
    relation_compare, _ = compare_options.get_relations_compare(model, options.profile, qr)
    qr.manifest = manifest_base

    OutputFormatter.print_compared_relation(relation_base, relation_compare)

    qb = QueryBuilder(model, relation_compare.get_dbt_relation())
    query = qb.metrics_query(metric, dimensions)
    table = qr.run_query(query)
    OutputFormatter.print_agate_table(table, format=True)


@audit.command()
@click.argument("path", nargs=1)
@click.option("-R", "--recursive", is_flag=True, help="Recursively search for dbt files")
@global_test_options
def custom(path, recursive, **kwargs):
    """Run custom queries on a dbt project."""

    options = GlobalTestOptions(**kwargs)
    qr = QueryRunner(options.debug, options.target, options.profile, options.dbt_path)

    if recursive and os.path.isdir(path):
        files = get_files(path)
    elif os.path.isdir(path) and not recursive:
        raise click.ClickException(f"Directory {path} is not a file.")
    elif not os.path.exists(path) or not os.path.isfile(path):
        raise click.ClickException(f"File {path} does not exist")
    else:
        files = [File(content=open(path, "r").read(), name=path)]

    for f in files:
        table = qr.run_query(f.content)
        OutputFormatter.print_agate_table(table)
