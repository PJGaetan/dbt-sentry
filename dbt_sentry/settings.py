import click
from dataclasses import dataclass
from typing import Optional


DEBUG = False
DBT_PATH = "."
PROFILE = None

_settions_options = [
    click.option("-p", "--profile", default=None, help="Path to dbt profile."),
    click.option("-d", "--debug", is_flag=True, help="Path to dbt profile."),
    click.option("--dbt-path", default=".", help="Path to dbt project.", show_default=True),
]


def settings_options(func):
    for option in reversed(_settions_options):
        func = option(func)
    return func


@dataclass
class SettingsOptions:
    profile: Optional[str]
    debug: bool
    dbt_path: str

    def __init__(self, **kwargs):
        self.profile = kwargs.get("profile")
        self.debug = bool(kwargs.get("debug"))
        self.dbt_path = kwargs.get("dbt_path")
        set_global_options(self)


def set_global_options(options):
    global DEBUG
    global DBT_PATH
    global PROFILE
    DEBUG = options.debug
    DBT_PATH = options.dbt_path
    PROFILE = options.profile
