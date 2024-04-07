import click
from .options import global_test_options


@click.command()
@global_test_options
def generate(target, profile, dbt_path):
    """Generates the audit report."""
    pass
