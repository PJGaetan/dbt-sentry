import click
import agate
import dbt_sentry.settings as s
from typing import Optional
from dbt_sentry.artefact.manifest import Manifest
from dbt.cli.main import dbtRunner
from dbt_sentry.utils import run_invoke, run_invoke_capture_io, Relation

from dbt_sentry.options import GlobalHeadOptions, GlobalCompareOptions
from dbt_sentry.template_query import (
    PROFILE_QUERY,
    COMPARE_MODEL_QUERY,
    COLUMNS_PROFILE_QUERY,
    COMPARE_ROWS_QUERY,
    TEMPLATED_METRICS_JINJA_QUERY,
)


class Client:
    def __init__(self, manifest_head: Manifest, manifest_compare: Optional[Manifest]):
        self.manifest_head = manifest_head
        self.manifest_compare = manifest_compare

    @classmethod
    def from_options(cls, **kwargs):
        assert "profile" in kwargs
        assert "debug" in kwargs
        assert "dbt_path" in kwargs
        s.SettingsOptions(**kwargs)

        assert "target" in kwargs and "manifest_path" in kwargs
        options_head = GlobalHeadOptions(**kwargs)

        if "target_compare" in kwargs and "manifest_compare_path" in kwargs:
            options_compare = GlobalCompareOptions(**kwargs)
        else:
            options_compare = None

        manifest_head = Manifest(options_head.target, options_head.manifest_path, is_head=True)
        if options_compare is not None:
            manifest_compare = Manifest(options_compare.target_compare, options_compare.manifest_compare_path)
        else:
            manifest_compare = None
        client = cls(manifest_head, manifest_compare)
        return client

    def list_models(self, index="head", selected_models: list = []):
        """
        List models in a project.

        Args:
            index: 'head' or 'compare'
            selected_models: list of models to select
        """
        model_selection = (
            "+ ".join(selected_models) if selected_models is not None and len(selected_models) > 0 else None
        )
        cmd = [
            "list",
            "--log-level",
            "none",
            "--resource-type",
            "model",
            *(["--select", model_selection] if model_selection is not None else []),
        ]

        if index == "head":
            manifest = self.manifest_head.get_manifest_object()
        elif index == "compare":
            manifest = self.manifest_compare.get_manifest_object()
        else:
            raise ValueError("index should be 'head' or 'compare'")

        dbt = dbtRunner(manifest)
        res = run_invoke_capture_io(dbt, cmd)
        return res

    def _run_query(self, query: str, index="head") -> agate.Table:
        """
        Run a query on a dbt project.

        Args:
            query: query to run
            index: 'head' or 'compare'
        """
        if index == "head":
            manifest = self.manifest_head.get_manifest_object()
        elif index == "compare":
            manifest = self.manifest_compare.get_manifest_object()
        else:
            raise ValueError("index should be 'head' or 'compare'")

        # initialize
        dbt = dbtRunner(manifest)

        cli_args = [
            "show",
            "--inline",
            query,
            *(["--log-level", "none"] if not s.DEBUG else ["--log-level", "debug"]),
            "--limit",
            20,
        ]

        # run the command
        res = run_invoke(dbt, cli_args)

        if not res.success:
            if s.DEBUG:
                raise Exception(res.exception)
            click.echo(res.exception)
            exit(1)
        return res.result.results[0].agate_table

    def run_profile(self, model: str, index="head") -> agate.Table:
        """
        Run a profile query on a dbt project.

        Args:
            index: 'head' or 'compare'
        """
        m = self._get_relation_from_name(model, index="head")
        query = PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", m.name)
        return self._run_query(query, index=index)

    def _get_relation_from_name(self, name: str, index="head") -> Relation:
        if index == "head":
            return self.manifest_head.get_relation(name)
        elif index == "compare":
            return self.manifest_compare.get_relation(name)
        else:
            raise ValueError("index should be 'head' or 'compare'")

    def run_compare_columns(self, model: str) -> agate.Table:
        """
        Run a profile query on dbt columns.

        Args:
            model: DBT model
            index: 'head' or 'compare'
        """
        model_head = self._get_relation_from_name(model, index="head")
        model_compare = self._get_relation_from_name(model, index="compare")

        query = COLUMNS_PROFILE_QUERY.replace("PLACEHOLDER_MODEL_NAME", model_head.name).replace(
            "RELATION_TO_REPLACE", model_compare.get_dbt_relation()
        )
        return self._run_query(query)

    def run_compare_model(self, model: str, primary_key: str, excluded_columns: list[str]) -> agate.Table:
        """
        Run a compare query on dbt tables.

        Args:
            model: DBT model
            excluded_columns: list of columns to exclude
        """
        model_head = self._get_relation_from_name(model, index="head")
        model_compare = self._get_relation_from_name(model, index="compare")
        excluded_columns_str = "" if len(excluded_columns) == 0 else f"""'{"','".join(excluded_columns)}'"""
        query = (
            COMPARE_MODEL_QUERY.replace("PLACEHOLDER_MODEL_NAME", model_head.name)
            .replace("RELATION_TO_REPLACE", model_compare.get_dbt_relation())
            .replace("EXCLUDED_COLUMNS", excluded_columns_str)
            .replace("PRIMARY_KEY", primary_key)
        )
        return self._run_query(query)

    def run_compare_rows(self, model: str, primary_key: str, excluded_columns: list[str]) -> agate.Table:
        """
        Run a compare rows query on dbt tables.

        Args:
            model: DBT model
            excluded_columns: list of columns to exclude
        """
        model_head = self._get_relation_from_name(model, index="head")
        model_compare = self._get_relation_from_name(model, index="compare")
        excluded_columns_str = "" if len(excluded_columns) == 0 else f"""'{"','".join(excluded_columns)}'"""
        query = (
            COMPARE_ROWS_QUERY.replace("PLACEHOLDER_MODEL_NAME", model_head.name)
            .replace("RELATION_TO_REPLACE", model_compare.get_dbt_relation())
            .replace("EXCLUDED_COLUMNS", excluded_columns_str)
            .replace("PRIMARY_KEY", primary_key)
        )
        return self._run_query(query)

    def run_metrics(
        self,
        model: str,
        dimensions: list[str],
        metric: str,
        index="head",
    ) -> agate.Table:
        """
        Run a metrics query on a dbt project.

        Args:
            model: DBT model
            dimensions: list of dimensions
            metric: metric
            index: 'head' or 'compare'
        """
        model_head = self._get_relation_from_name(model, index="head")
        model_compare = self._get_relation_from_name(model, index="compare")
        columns_to_replace = f"""'{"','".join(dimensions)}'"""
        metric_to_replace = f"'{metric}'"
        query = (
            TEMPLATED_METRICS_JINJA_QUERY.replace("PLACEHOLDER_MODEL_NAME", model_head.name)
            .replace("COLUMNS_TO_REPLACE", columns_to_replace)
            .replace("METRICS_TO_REPLACE", metric_to_replace)
            .replace("RELATION_TO_REPLACE", model_compare.get_dbt_relation())
        )
        return self._run_query(query, index=index)
