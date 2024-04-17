import click
from dbt_sentry.client import Client
from dataclasses import dataclass

from dbt_sentry.markdown_builder import MarkdownBuilder
from .options import global_head_options, global_compare_options
from dbt_sentry.settings import settings_options

from enum import Enum
import plotext as plt
from git import Repo
import re

THEME = "clear"
MARKER = "+"


@click.group()
def ci():
    """Publish the audit report."""
    pass


def get_file_changed(base_branch=None) -> list[str]:
    repo = Repo(search_parent_directories=True)
    if base_branch is not None and base_branch not in repo.heads:
        raise click.UsageError(f"Branch {base_branch} not found.")
    elif base_branch is not None:
        base = repo.heads[base_branch]
    elif "main" in repo.heads:
        base = repo.heads["main"]
    elif "master" in repo.heads:
        base = repo.heads["master"]
    else:
        raise click.UsageError("No main nor master branch found try providing a base-branch.")

    diff = base.commit.diff(repo.head.commit)

    files_changes = [f.b_path for f in diff]
    return files_changes


class ChangePriority(Enum):
    CHILDREN = 1
    PARENT = 2


@dataclass
class ModelImpacted:
    name: str
    priority: ChangePriority


def get_model_impacted(files, client: Client) -> list[ModelImpacted]:
    pattern = r"models\/.*.sql"
    filter = re.compile(pattern)

    models = [f.split("/")[-1].split(".")[0] for f in files if filter.search(f)]
    res = client.list_models(selected_models=models)
    if not res.success:
        raise click.UsageError(res.exception)
    impacted_models = [
        ModelImpacted(
            m.split(".")[-1],
            ChangePriority.PARENT if m.split(".")[-1] in models else ChangePriority.CHILDREN,
        )
        for m in res.result
    ]
    return impacted_models


OUTPUT_FOLDER = "dbts-artefact"


@ci.command()
@settings_options
@global_compare_options
@global_head_options
def generate(**kwargs):
    """Generates the audit report."""

    # 1. [x] detect git file changed
    # 2. [x] find all model that can be impacted (model+)
    # 3. [x] run audit xx for modelodi
    # 4. [x] generate report output

    client = Client.from_options(**kwargs)

    markdown = MarkdownBuilder()
    markdown.add_heading("Audit Report")

    files = get_file_changed()
    models = get_model_impacted(files, client)

    for m in models:
        if m.priority == ChangePriority.CHILDREN:
            continue
        relation_head = client._get_relation_from_name(m.name, "head")
        relation_compare = client._get_relation_from_name(m.name, "compare")

        markdown.add_subheading(f"Comparing {m.name}")
        markdown.add_text(f"Head: {relation_head}")
        markdown.add_line_break()
        markdown.add_text(f"Compare: {relation_compare}")

        # Generate profiles
        table = client.run_profile(m.name)
        table.to_csv(f"{OUTPUT_FOLDER}/{m.name}/profile.csv")
        markdown.add_subsubheading("Profile")
        markdown.add_table(table)
        markdown.add_line_break()

        # Get columns profile
        table = client.run_compare_columns(m.name)
        markdown.add_subsubheading("Columns profile comparison")
        markdown.add_table(table)
        markdown.add_line_break()
        table.to_csv(f"{OUTPUT_FOLDER}/{m.name}/columns.csv")
        not_in_both_columns = []
        for row in table.rows:
            if row.get("in_both") == False:
                not_in_both_columns.append(row.get("column_name"))

        # Get model compare
        table = client.run_compare_model(m.name, not_in_both_columns)
        table.to_csv(f"{OUTPUT_FOLDER}/{m.name}/compare.csv")
        markdown.add_subsubheading("Model comparison")
        markdown.add_table(table)
        markdown.add_line_break()

    markdown.write(f"{OUTPUT_FOLDER}/audit.md")


@ci.command()
def publish_gitlab():
    """Publishes the audit report to gitlab."""
    pass


@ci.command()
def publish_github():
    """Publishes the audit report to github."""
    pass
