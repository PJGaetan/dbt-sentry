import click
from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest
import agate
import os


def is_dbt_project(debug) -> bool:
    """
    Check if the current directory is a dbt project.
    If not, exit with an error.
    """

    is_dbt_project = False
    if debug:
        print(f"Searching for dbt project in : {os.getcwd()}")
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


class QueryRunner:
    def __init__(self, debug: bool, target: str, profile: str, dbt_path: str):
        self.debug = debug
        self.target = target
        self.profile = profile
        self.dbt_path = dbt_path
        self.manifest = None

    def _run_invoke(self, dbt: dbtRunner, cli_args):
        current_path = os.getcwd()

        os.chdir(self.dbt_path)
        is_dbt = is_dbt_project(self.debug)
        if not is_dbt:
            exit(1)

        if self.debug:
            click.echo(f"dbt command : {cli_args}")

        res: dbtRunnerResult = dbt.invoke(cli_args)
        os.chdir(current_path)

        return res

    def generate_manifest(self, target: str, profile: str) -> Manifest:
        """
        Generate a Manifest from a dbt project.

        Assumes the current directory is a dbt project.
        """
        cmd = [
            "parse",
            "--log-level",
            "none",
            *(["--profile", profile] if profile is not None else []),
            *(["--target", target] if target is not None else []),
        ]

        # use 'parse' command to load a Manifest
        dbt = dbtRunner()
        res = self._run_invoke(dbt, cmd)
        manifest: Manifest = res.result

        if self.debug:
            print("generated manifest.")

        return manifest

    def run_query(self, query: str) -> agate.Table:
        """
        Run a query on a dbt project.

        Assumes the current directory is a dbt project.
        """

        if self.manifest is None:
            manifest = self.generate_manifest(self.target, self.profile)
            self.manifest = manifest

        # initialize
        dbt = dbtRunner(manifest=self.manifest)

        cli_args = [
            "show",
            "--inline",
            query,
            *(["--log-level", "none"] if not self.debug else ["--log-level", "debug"]),
            "--limit",
            20,
        ]

        # run the command
        res = self._run_invoke(dbt, cli_args)

        if not res.success:
            click.echo(res.exception)
            exit(1)
        # res.result.results[0].agate_table.print_csv()
        # model_names = [m["name"] for m in res.result.results[0].node.refs]
        # type: ignore[nores.result.results[0].to_dict()
        # print(json.dumps(res.result.results[0].to_dict(), indent=4))
        return res.result.results[0].agate_table
