import click


from .ci import ci
from .audit import audit


@click.group()
def cli():
    """dbt_sentry: A tool to audit your dbt project."""
    pass


cli.add_command(ci)
cli.add_command(audit)


# @cli.command()
# @click.option("--path", default="dbtci", help="Path to look for files in.")
# @click.option("--dbt-path", default=".", help="Path to dbt project.")
# @click.option("-t", "--target", default=None, help="dbt target")
# @click.option("-p", "--profile", default=None, help="Path to dbt profile.")
# def run_files(path, dbt_path, target, profile):
#     """Run a dbt file(s)."""
#     files = get_files(path)
#     run_queries(files, dbt_path, target=target, profile=profile)


if __name__ == "__main__":
    cli()
