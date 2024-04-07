import click

from dataclasses import dataclass

_global_test_options = [
    click.option("-t", "--target", default=None, help="dbt target"),
    click.option("-p", "--profile", default=None, help="Path to dbt profile."),
    click.option("-d", "--debug", is_flag=True, help="Path to dbt profile."),
    click.option("--dbt-path", default=".", help="Path to dbt project.", show_default=True),
]


def global_test_options(func):
    for option in reversed(_global_test_options):
        func = option(func)
    return func


@dataclass
class GlobalTestOptions:
    target: str
    profile: str
    debug: bool
    dbt_path: str
