from dataclasses import dataclass
from typing import List, Optional

from sqlglot import exp, parse_one


@dataclass
class Model:
    name: str
    schema: str
    database: str
    query: str

    def get_columns(self) -> List[str]:
        if not hasattr(self, "columns"):
            self.columns = self._compute_columns()

        return self.columns

    def _compute_columns(self) -> List[str]:
        parsed = parse_one(self.query)
        test = 1
        # print all column references (a and b)

        print("print col")
        for column in parse_one(self.query).find_all(exp.Column):
            print(column)

        # find all projections in select statements (a and c)
        print("print select")
        for select in parse_one(self.query).find_all(exp.Select):
            for projection in select.expressions:
                print(projection)

        col = []
        return col
