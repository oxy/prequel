"""Provide value objects for Columns."""

from __future__ import annotations

from typing import Any, List, Optional, Union

from . import types
from .utils import quote_ident, clean_ident
from .expression import ValueMixin
from .variable import Variable

__all__ = ["Table", "Column"]


class Table:
    """SQL table.

    Attributes:
        table: name of table
    """

    def __init__(self, table: str):
        if not isinstance(table, str):
            raise TypeError(f"Cannot create table with name of type {type(table)}")
        self.table = table

    def __str__(self):
        return quote_ident(self.table)

    def col(self, column: str) -> Column:
        """Returns a column from the given table.

        Args:
            column: name of the column
        """
        return Column(table=self, column=column)

    @classmethod
    def as_table(cls, table: Union[Table, str]) -> Table:
        """Convert value to a table if it isn't already one.

        Args:
            table: value to convert
        """
        if isinstance(table, str):
            return cls(table)
        elif isinstance(table, Table):
            return table
        raise TypeError(f"Cannot convert {repr(table)} to Table.")


class Column(ValueMixin, types.Value):
    """SQL column.

    Attributes:
        column: name of column
        table: (optional) table which column belongs to
    """

    def __init__(self, column: str, *, table: Optional[Table] = None):
        self.table = Table.as_table(table) if table else None
        self.column = column

    def flatten(self) -> List[types.BuildingBlock]:
        """Flatten column to SQL representation."""
        return [str(self)]

    def as_value(self) -> List[types.BuildingBlock]:
        """Flatten column to SQL representation for use as a value."""
        return self.flatten()

    def as_arg(self) -> str:
        """Return a Python identifier to refer to the column by name."""
        name = clean_ident(self.column)
        if self.table:
            name = clean_ident(self.table.table) + "_" + name
        return name

    def __repr__(self):
        return f"{self.__class__.__name__}("\
            f"table={repr(self.table.table) if self.table else None}, "\
            f"column={repr(self.column)})"

    def __str__(self):
        prefix = (str(self.table) + ".") if self.table else ""
        return prefix + quote_ident(self.column)

    def _convert_arg(self, other: Any, opname: str) -> Variable:
        if isinstance(other, types.Value):
            return other
        else:
            name = self.as_arg()
            if opname != "eq":
                name += "_" + opname
            return Variable(name, other)
