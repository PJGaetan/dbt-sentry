import click

from dbt_sentry.artefact.manifest import Manifest
from dbt_sentry.client import Client
from dbt_sentry.settings import SettingsOptions, settings_options
from .options import global_head_options, GlobalHeadOptions, global_compare_options, GlobalCompareOptions, primary_key
from .output_formatter import OutputFormatter
from .utils import get_files, File
import os


@click.group()
def audit():
    """Audit a specific piece of your dbt project."""
    pass


@audit.command()
@click.argument("model", nargs=1)
@settings_options
@global_head_options
def profile(model, **kwargs):
    """Generate the profile of a dbt model.

    Depends on dbt package data-mie/dbt-profiler.
    """
    client = Client.from_options(**kwargs)
    table = client.run_profile(model)
    OutputFormatter.print_agate_table(table)


@audit.command()
@click.argument("model", nargs=1)
@settings_options
@global_head_options
@global_compare_options
@primary_key
def compare_model(model, primary_key, **kwargs):
    """Compare columns and relations of a model."""
    client = Client.from_options(**kwargs)

    relation_head = client._get_relation_from_name(model, "head")
    relation_compare = client._get_relation_from_name(model, "compare")

    table = client.run_compare_columns(model)
    not_in_both_columns = []
    not_in_a = []
    not_in_b = []
    columns = []
    for row in table.rows:
        if row.get("in_a") == False:
            not_in_a.append(row.get("column_name"))
        if row.get("in_b") == False:
            not_in_b.append(row.get("column_name"))
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))
        else:
            columns.append(row.get("column_name").lower())
    if primary_key.lower() not in columns:
        raise click.ClickException(
            f"Primary key {primary_key} not a columns in both tables {relation_head} && {relation_compare}"
        )
    table = client.run_compare_model(model, primary_key, not_in_both_columns)

    # PRINTING

    # a: table_name_one && b: table_name_two
    OutputFormatter.print_compared_relation(relation_head, relation_compare)
    # Column(s) not in a: [list of columns]
    # Column(s) not in b: [list of columns]
    OutputFormatter.print_excluded_columns(not_in_a, not_in_b)

    OutputFormatter.print_agate_table(table, format=False)


@audit.command()
@click.argument("model", nargs=1)
@settings_options
@global_compare_options
@global_head_options
@primary_key
def compare_rows(model, primary_key, **kwargs):
    """Compare the rows difference a model."""
    client = Client.from_options(**kwargs)

    relation_head = client._get_relation_from_name(model, "head")
    relation_compare = client._get_relation_from_name(model, "compare")

    table = client.run_compare_columns(model)
    not_in_both_columns = []
    not_in_a = []
    not_in_b = []
    columns = []
    for row in table.rows:
        if row.get("in_a") == False:
            not_in_a.append(row.get("column_name"))
        if row.get("in_b") == False:
            not_in_b.append(row.get("column_name"))
        if row.get("in_both") == False:
            not_in_both_columns.append(row.get("column_name"))
        else:
            columns.append(row.get("column_name"))

    if primary_key.lower() not in columns:
        raise click.ClickException(
            f"Primary key {primary_key} not a columns in both tables {relation_head} && {relation_compare}"
        )

    table = client.run_compare_rows(model, primary_key, not_in_both_columns)

    # PRINTING

    OutputFormatter.print_compared_relation(relation_head, relation_compare)
    # Column(s) not in a: [list of columns]
    # Column(s) not in b: [list of columns]
    OutputFormatter.print_excluded_columns(not_in_a, not_in_b)

    # Filter missing columns
    OutputFormatter.print_agate_table(table, format=False)


@audit.command()
@click.argument("model", nargs=1)
@click.argument("metric", nargs=1)
@click.argument("dimensions", nargs=-1)
@settings_options
@global_compare_options
@global_head_options
def metric(model, metric, dimensions, **kwargs):
    """Audit the trend of a specific metrics in dbt."""

    client = Client.from_options(**kwargs)

    if len(dimensions) == 0:
        raise click.ClickException("Please specify at least one dimension")

    relation_head = client._get_relation_from_name(model, "head")
    relation_compare = client._get_relation_from_name(model, "compare")

    OutputFormatter.print_compared_relation(relation_head, relation_compare)

    table = client.run_metrics(model, dimensions, metric)
    OutputFormatter.print_agate_table(table, format=True)


@audit.command()
@click.argument("path", nargs=1)
@click.option("-R", "--recursive", is_flag=True, help="Recursively search for dbt files")
@settings_options
@global_head_options
def custom(path, recursive, **kwargs):
    """Run custom queries on a dbt project."""

    client = Client.from_options(**kwargs)

    if recursive and os.path.isdir(path):
        files = get_files(path)
    elif os.path.isdir(path) and not recursive:
        raise click.ClickException(f"Directory {path} is not a file.")
    elif not os.path.exists(path) or not os.path.isfile(path):
        raise click.ClickException(f"File {path} does not exist")
    else:
        files = [File(content=open(path, "r").read(), name=path)]

    for f in files:
        table = client._run_query(f.content)
        OutputFormatter.print_agate_table(table)
