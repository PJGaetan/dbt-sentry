from dbt.cli.main import dbtRunner, dbtRunnerResult
import os
import io
import click
from dataclasses import dataclass
import dbt_sentry.settings as s
import contextlib


@dataclass
class Relation:
    database: str
    schema: str
    name: str

    def get_dbt_relation(self):
        return f"api.Relation.create(database='{self.database}', schema='{self.schema}', identifier='{self.name}')"

    def __str__(self):
        return f"{self.database}.{self.schema}.{self.name}"


@dataclass
class File:
    name: str
    content: str


def is_dbt_project() -> bool:
    """
    Check if the current directory is a dbt project.
    If not, exit with an error.
    """

    is_dbt_project = False
    if s.DEBUG:
        click.echo(f"Searching for dbt project in : {os.getcwd()}")
    for _, _, filenames in os.walk("."):
        for f in filenames:
            if f.endswith("dbt_project.yml"):
                is_dbt_project = True
                break

        if not is_dbt_project:
            print(f"dbt project not found in {os.getcwd()}")
            return False
        break
    return True


def run_invoke(dbt: dbtRunner, cli_args):
    current_path = os.getcwd()

    os.chdir(s.DBT_PATH)
    is_dbt = is_dbt_project()
    if not is_dbt:
        exit(1)

    if s.DEBUG:
        click.echo(f"dbt command : {cli_args}")

    res: dbtRunnerResult = dbt.invoke(cli_args)
    os.chdir(current_path)

    return res


def run_invoke_capture_io(dbt: dbtRunner, cli_args):
    current_path = os.getcwd()

    os.chdir(s.DBT_PATH)
    is_dbt = is_dbt_project()
    if not is_dbt:
        exit(1)

    if s.DEBUG:
        click.echo(f"dbt command : {cli_args}")
    with contextlib.redirect_stdout(io.StringIO()):
        res: dbtRunnerResult = dbt.invoke(cli_args)

    os.chdir(current_path)

    return res


def get_files(path: str) -> list[File]:
    files = []
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(dirpath, f))
    data = [
        File(
            content=open(f, "r").read(),
            name=f,
        )
        for f in files
        if f.endswith(".sql")
    ]
    return data
