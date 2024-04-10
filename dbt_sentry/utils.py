from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest
import os
import json
from dataclasses import dataclass


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
