"""SQL insert module."""
from typing import Optional, Sequence, Union, Callable

from . import types
from .blocks import CommaSeparated
from .column import Column, Table
from .mkquery import mkquery
from .select import Select
from .variable import Variable


class Insert:
    """SQL insert query.

    Attributes:
        table: Table to insert into
        columns: Columns of data
        values: List of data
    """
    def __init__(self, table: Union[str, Table], columns: Sequence[Union[str, Column]]):
        self.table = Table.as_table(table)
        self.columns = []
        for column in columns:
            if isinstance(column, Column):
                self.columns.append(column)
            else:
                self.columns.append(Column(column))
        self._values: Optional[Sequence[types.BuildingBlock]] = None

    def values_fromquery(self, select: Select):
        """Get values from a select query.

        Args:
            select: Select query to use.
        """
        if len(select.values) != len(self.columns):
            raise ValueError("SELECT does not unwrap to enough values.")

        self._values = select.flatten()
        return self

    def values(self, *values: Sequence[types.Block]):
        """Get values from Value objects."""
        if len(values) != len(self.columns):
            raise ValueError("SELECT does not unwrap to enough values.")

        self._values = CommaSeparated(values).flatten()
        return self

    def values_raw(self, *rawvalues: types.BuildingBlock):
        """Use a raw list of building blocks in VALUES.

        Args:
            *rawvalues: building blocks.
        """
        self._values = rawvalues
        return self

    def flatten(self) -> Sequence[types.BuildingBlock]:
        """Flatten into a list of blocks."""

        parts = []

        columns = ", ".join([str(column) for column in self.columns])
        table = str(self.table)

        values = self._values
        if not values:
            values = [Variable(col.as_arg(), ...) for col in self.columns]

        parts = [
            "INSERT INTO",
            table,
            "(",
            columns,
            ")",
            "VALUES",
            "(",
            *values,
            ")",
        ]

        return parts

    def to_query(self) -> Callable:
        """Build query into a callable."""
        return mkquery(self.flatten())
