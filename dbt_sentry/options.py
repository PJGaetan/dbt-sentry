import click
from dataclasses import dataclass

_global_head_options = [
    click.option("-t", "--target", default=None, help="dbt target"),
    click.option("--manifest-path", default=None, help="Load manifest head from this path."),
]


def global_head_options(func):
    for option in reversed(_global_head_options):
        func = option(func)
    return func


@dataclass
class GlobalHeadOptions:
    target: str
    manifest_path: str

    def __init__(self, **kwargs):
        self.target = kwargs.get("target")
        self.manifest_path = kwargs.get("manifest_path")


_global_compare_options = [
    click.option("--target-compare", default=None, help="Compare to this dbt target"),
    click.option("--manifest-compare-path", default=None, help="Compare thanks to this manifest."),
]


def global_compare_options(func):
    for option in reversed(_global_compare_options):
        func = option(func)
    return func


@dataclass
class GlobalCompareOptions:
    target_compare: str
    manifest_compare_path: str

    def __init__(self, **kwargs):
        self.target_compare = kwargs.get("target_compare")
        self.manifest_compare_path = kwargs.get("manifest_compare_path")


primary_key = click.option("-k", "--primary-key", help="Primary key used to compare the tables.")
