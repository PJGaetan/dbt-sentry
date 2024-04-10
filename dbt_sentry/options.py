import click
from typing import Optional
from dbt.contracts.graph.manifest import Manifest
from .utils import Relation
from .query_runner import QueryRunner

from .compare_relation_resolver import resolve_relation_from_file, resolve_relation_from_object
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

    def __init__(self, **kwargs):
        self.target = kwargs.get("target")
        self.profile = kwargs.get("profile")
        self.debug = bool(kwargs.get("debug"))
        self.dbt_path = kwargs.get("dbt_path")


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

    def get_relations_compare(self, model, profile, qr: QueryRunner) -> tuple[Relation, Optional[Manifest]]:

        if self.target_compare is not None and self.manifest_compare_path is not None:
            raise click.UsageError("You can't use --target-compare and --manifest-compare-path at the same time.")

        if self.manifest_compare_path is not None:
            relation = resolve_relation_from_file(model, self.manifest_compare_path)
            return relation, None

        if self.target_compare is not None:
            manifest = qr.generate_manifest(self.target_compare, profile)
            relation = resolve_relation_from_object(model, manifest)
            return relation, manifest

        raise click.UsageError("You must use --target-compare or --manifest-compare-path.")

    def get_relations_base(self, model, target, profile, qr: QueryRunner) -> tuple[Relation, Manifest]:
        manifest = qr.generate_manifest(target, profile)

        relation = resolve_relation_from_object(model, manifest)
        return relation, manifest
