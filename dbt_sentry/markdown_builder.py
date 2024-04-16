import agate
import contextlib
import io
import tabulate


class MarkdownBuilder:
    def __init__(self):
        self.markdown = ""

    def add_line_break(self):
        self.markdown += "\n"

    def add_text(self, text):
        self.markdown += text
        self.markdown += "\n"

    def add_heading(self, text):
        self.markdown += f"# {text}\n"

    def add_subheading(self, text):
        self.markdown += f"## {text}\n"

    def add_subsubheading(self, text):
        self.markdown += f"### {text}\n"

    def add_code(self, code):
        self.markdown += f"```python\n{code}\n```\n"

    def add_image(self, url):
        # TODO: store image first
        self.markdown += f"![image]({url})\n"

    def add_table(self, table: agate.Table):
        buff = io.StringIO()
        table.print_table(output=buff, max_rows=None, max_columns=None)
        md_table = buff.getvalue()
        buff.close()
        self.markdown += md_table

    def write(self, path: str):
        with open(path, "w") as f:
            f.write(self.markdown)
