import os
import json

from dbt.cli.main import dbtRunner
from typing import Optional
from dbt.contracts.graph.manifest import Manifest as DbtManifest
import click

from dbt_sentry.utils import run_invoke
import dbt_sentry.settings as s
from dbt_sentry.utils import Relation


class Manifest:
    def __init__(self, target: str, manifest_path: Optional[str], is_head: bool = False):
        self.target = target
        self.manifest_json = None
        self.manifest_object = None

        if manifest_path is not None:
            self.manifest_json = self._parse_json(manifest_path)
            return

        if target is not None or is_head:
            self.manifest_object = self._parse_object(s.PROFILE, target)
            return

        raise click.UsageError("Error: manifest_path is None and target is None too, at least one is required.")

    def _parse_json(self, manifest_path: str) -> dict:
        if manifest_path is None:
            raise ValueError("manifest_path is None")

        if not os.path.isfile(manifest_path):
            raise ValueError("manifest_path is not a file")

        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        return manifest

    def _parse_object(self, profile: str, target: str) -> DbtManifest:
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
        res = run_invoke(dbt, cmd)
        manifest: Manifest = res.result
        if not res.success:
            if s.DEBUG:
                raise Exception(res.exception)
            raise click.UsageError(res.exception)

        if s.DEBUG:
            click.echo("generated manifest.")

        return manifest

    def get_manifest_object(self) -> DbtManifest:
        """Get manifest object if exists else build it and return it."""
        if self.manifest_object is None:
            self.manifest_object = self._parse_object(s.PROFILE, self.target)
        return self.manifest_object

    def get_relation(self, model: str):
        if self.manifest_json is not None:
            for m in self.manifest_json["nodes"].values():
                if m["name"] == model and m["resource_type"] == "model":
                    return Relation(m.database, m.schema, m.name)

        if self.manifest_object is None:
            self.get_manifest_object()

        for m in self.manifest_object.nodes.values():
            if m.name == model and m.resource_type == "model":
                return Relation(m.database, m.schema, m.name)

        if s.DEBUG:
            raise Exception(f"{model} is not in target dbt project. You can't compare it.")
        raise click.UsageError(f"{model} is not in target dbt project. You can't compare it.")
