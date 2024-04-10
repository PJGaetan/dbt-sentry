import click
import os
import json
from pathlib import Path
from dbt.contracts.graph.manifest import Manifest
from .utils import Relation


def resolve_relation_from_file(model: str, manifest_path: str):
    manifest_absolute_path = os.path.abspath(manifest_path)
    if not Path(manifest_absolute_path).is_file():
        raise click.UsageError(f"{manifest_path} is not a file.")

    with open(manifest_absolute_path, "r") as f:
        manifest = json.load(f)
    for n in manifest["nodes"].values():
        if n["name"] == model and n["resource_type"] == "model":
            return Relation(n.database, n.schema, n.name)
    raise click.UsageError(f"{model} is not in target dbt project. You can't compare it.")


def resolve_relation_from_object(model: str, manifest: Manifest):
    for m in manifest.nodes.values():
        if m.name == model and m.resource_type == "model":
            return Relation(m.database, m.schema, m.name)
    raise click.UsageError(f"{model} is not in target dbt project. You can't compare it.")
