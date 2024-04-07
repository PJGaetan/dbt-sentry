import click
from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest
import os
import json
import agate
from dataclasses import dataclass
from itertools import zip_longest


@dataclass
class File:
    name: str
    content: str


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


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


def walk_dbt_project(dbt_path: str, debug: bool):
    os.chdir(dbt_path)
    is_dbt = is_dbt_project(debug)
    if not is_dbt:
        exit(1)


def run_queries(files: list[File], dbt_path: str, target: str, profile: str):
    os.chdir(dbt_path)
    is_dbt_project()

    cmd = [
        "parse",
        "--log-level",
        "none",
        *(["--profile", profile] if profile is not None else []),
        *(["--target", target] if target is not None else []),
    ]

    # use 'parse' command to load a Manifest
    res: dbtRunnerResult = dbtRunner().invoke(cmd)
    manifest: Manifest = res.result

    # initialize
    dbt = dbtRunner(manifest=manifest)

    for d in files:
        if d.name != "jaffle_shop/dbtci2/test_3.sql":
            continue
        # create CLI args as a list of strings
        # d.content.append("{{% do audit_results.to_csv('{}') %}}".format(d.stored_path))
        debug = False
        content = "".join(d.content)
        cli_args = [
            "show",
            "--inline",
            content,
            *(["--log-level", "none"] if not debug else []),
            "--limit",
            20,
        ]

        # run the command
        res: dbtRunnerResult = dbt.invoke(
            cli_args,
        )
        # res.result.results[0].agate_table.print_csv()
        # model_names = [m["name"] for m in res.result.results[0].node.refs]
        # type: ignore[nores.result.results[0].to_dict()
        print(json.dumps(res.result.results[0].to_dict(), indent=4))
