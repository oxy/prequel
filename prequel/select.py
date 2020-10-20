"""SQL select query."""

from typing import Any, List, Mapping, Optional, Sequence, Union

from . import types
from .blocks import CommaSeparated
from .column import Column, Table
from .expression import Operator
from .helpers import group
from .mkquery import mkquery


class Select:
    """Simple Select query. 
    
    Does not support complex joins or relationships in current state.

    Examples:
        >>> pq.Select("id", "name", "pwhash").from_("user").to_query()()
        ('SELECT "id", "name", "pwhash" FROM "user"', )
    """

    def __init__(self, *values: Union[types.Value, str]):
        self.values: List[types.Value] = []
        for val in values:
            if isinstance(val, str):
                self.values.append(Column(val))
            else:
                self.values.append(val)

        self.constraints: Optional[types.Value] = None
        self.table: Optional[Table] = None

    def where(self, *constraints: types.Value, **constraints_and: Mapping[str, Any]):
        """Specify constraints to be used.

        Takes constraints either as values, eg. expressions,
        or keyword arguments, eg. id=int

        Examples:
            >>> pq.Select("id").from_("user").wheree(i)
        """
        self.constraints = group(
            list(constraints) + [Column(col) == val for col, val in constraints_and.items()],
            Operator.and_,
        )
        return self

    def from_(self, table: str):
        """Choose table to query from.

        Args:
            table: name of table.
        """
        self.table = Table.as_table(table)
        return self

    def __repr__(self):
        return str(self.to_query())

    def flatten(self) -> Sequence[types.BuildingBlock]:
        """Flatten into a list of blocks."""
        columns = CommaSeparated(*self.values).flatten()  # type: ignore

        parts = ["SELECT", *columns]
        if self.table:
            parts.extend(["FROM", str(self.table)])

        if self.constraints is not None:
            parts.append("WHERE")
            parts.extend(self.constraints.flatten())

        return parts

    def to_query(self):
        """Compile into a query function."""
        return mkquery(self.flatten())
