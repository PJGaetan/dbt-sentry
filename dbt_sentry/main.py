import click

from dbt_sentry.audit import audit
from dbt_sentry.ci import ci


@click.group()
def cli():
    """dbt_sentry: A tool to audit your dbt project."""
    pass


cli.add_command(ci)
cli.add_command(audit)


if __name__ == "__main__":
    cli()
