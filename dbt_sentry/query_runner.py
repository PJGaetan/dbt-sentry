import click
from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest
import agate


class QueryRunner:
    def __init__(self, debug: bool, target: str, profile: str):
        self.debug = debug
        self.target = target
        self.profile = profile
        self.manifest = None

    def generate_manifest(self):
        """
        Generate a Manifest from a dbt project.

        Assumes the current directory is a dbt project.
        """
        cmd = [
            "parse",
            "--log-level",
            "none",
            *(["--profile", self.profile] if self.profile is not None else []),
            *(["--target", self.target] if self.target is not None else []),
        ]

        # use 'parse' command to load a Manifest
        res: dbtRunnerResult = dbtRunner().invoke(cmd)
        manifest: Manifest = res.result

        if self.debug:
            print("generated manifest.")

        self.manifest = manifest

    def run_query(self, query: str) -> agate.Table:
        """
        Run a query on a dbt project.

        Assumes the current directory is a dbt project.
        """

        if self.manifest is None:
            self.generate_manifest()

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
        res: dbtRunnerResult = dbt.invoke(cli_args)

        if not res.success:
            click.echo(res.exception)
            exit(1)
        # res.result.results[0].agate_table.print_csv()
        # model_names = [m["name"] for m in res.result.results[0].node.refs]
        # type: ignore[nores.result.results[0].to_dict()
        # print(json.dumps(res.result.results[0].to_dict(), indent=4))
        return res.result.results[0].agate_table
