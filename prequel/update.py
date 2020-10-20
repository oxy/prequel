from typing import Any, Mapping, Optional, Sequence, Union

from . import types
from .blocks import CommaSeparated
from .column import Column, Table
from .expression import Expression, Operator
from .helpers import group
from .mkquery import mkquery
from .variable import Variable


class Update:
    """SQL Update query.

    Examples:

    >>> pq.Update("user").set(name=str).where(id=int).to_query()("oxy", 123)
    ('UPDATE "user" SET "name" = $1 WHERE "id" = $2', 'oxy', 123)
    """

    def __init__(self, table: Union[str, Table]):
        self.table = Table.as_table(table)
        self.updates: Sequence[types.Block] = []
        self.constraints = None

    def set(self, 
            *columns: Sequence[Union[str, Column]],
            **updates: Mapping[Union[str, Column], types.Value]):
        """Columns to update, and values to use.

        Examples:

        >>> pq.Update("user").set("name").where(id=int).to_query()(id=101, name="Oxy")
        ('UPDATE "user" SET "name" = $1 WHERE id = $2', 'Oxy', 101)
        """

        var_updates = [Column(col) == Variable(col) for col in columns]
        fixed_updates = [Column(col) == val for col, val in updates.items()]

        self.updates.extend([*var_updates, *fixed_updates])
        return self

    def where(self, *constraints: types.Value, **constraints_and: Mapping[str, Any]):
        """Specify constraints to be used. TODO complete
        """
        self.constraints = group(
            list(constraints) + [Column(col) == val for col, val in constraints_and.items()],
            Operator.and_,
        )
        return self

    def __repr__(self):
        return str(self.to_query())

    def flatten(self) -> Sequence[types.BuildingBlock]:
        """Flatten into a list of blocks."""
        columns = CommaSeparated(*self.updates).flatten()  # type: ignore

        parts = ["UPDATE", str(self.table), "SET", *columns]

        if self.constraints is not None:
            parts.append("WHERE")
            parts.extend(self.constraints.flatten())

        return parts

    def to_query(self):
        """Compile into a query function."""
        return mkquery(self.flatten())
