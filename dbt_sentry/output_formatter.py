import agate
import click
from itertools import zip_longest
import io
from .utils import Relation


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class OutputFormatter:

    @staticmethod
    def print_agate_table(table: agate.Table, format: bool = True):
        if not format:
            buff = io.StringIO()
            table.print_table(max_rows=None, max_columns=None, output=buff)
            buff.close()
            click.echo(table_value)
            click.echo("\n")
            return

        buff = io.StringIO()
        columns = table.column_names
        col_grouped = grouper(columns[1:], 5)
        for col in col_grouped:
            t = table.select([columns[0], *[c for c in col if c is not None]])
            t.print_table(max_rows=None, max_columns=6, output=buff)
            buff.write("\n")
        table_value = buff.getvalue()
        buff.close()
        click.echo(table_value)

    @staticmethod
    def print_compared_relation(model: Relation, model_compare: Relation):
        click.echo(f"a: {model} && b: {model_compare}")

    @staticmethod
    def print_excluded_columns(not_in_a: list, not_in_b: list):
        """
        Prints the excluded columns in a and b

        Column(s) not in a: [list of columns]
        Column(s) not in b: [list of columns]

        """
        if len(not_in_a) > 0:
            click.echo("Column(s) not in a: " + ", ".join(not_in_a))
        else:
            click.echo("Column(s) not in a: None")
        if len(not_in_b) > 0:
            click.echo("Column(s) not in b: " + ", ".join(not_in_b))
        else:
            click.echo("Column(s) not in b: None")
