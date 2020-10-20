"""Data and logic for SQL function calls."""

import enum
from typing import List

from . import blocks, types
from .expression import ValueMixin


# TODO: Expand list of functions, possibly add other function information
class Function(enum.Enum):
    """Enum of SQL functions."""

    count = "COUNT"
    average = "AVG"
    min = "MIN"
    max = "MAX"


class FunctionCall(ValueMixin):
    """An SQL function call.

    Attributes:
        func: SQL function name.
        values: List of function arguments.
        boolean: If the function returns a boolean type.
    """

    def __init__(self, func: Function, vals: List[types.Value]):
        self.values = vals
        self.func = func
        self._boolean = False  # TODO: investigate if functions can return booleans

    def flatten(self) -> List[types.BuildingBlock]:
        return [self.func.value, "(", *blocks.CommaSeparated(self.values).flatten(), ")"]

    def as_value(self) -> List[types.BuildingBlock]:
        return ["(", *self.flatten(), ")"]

    @property
    def boolean(self):
        return self._boolean
