"""SQL variables."""

import keyword
import warnings
from typing import Any, List

from . import types
from .expression import ValueMixin

__all__ = ["Variable"]


class Variable(ValueMixin, types.BaseBlock):
    """Provide a building block for SQL variables.

    Attributes:
        name: Name of the variable to use in Python code.
            SQL variables themselves are not named in queries.
        default: Default value for the variable,
            None indicates a default of NULL,
            Ellipsis indicates no default.
    """

    def __init__(self, name: str, default: Any = ...):
        if not name.isidentifier() or keyword.iskeyword(name):
            raise ValueError("Cannot use {repr(name)} as a variable name.")
        self.name = name
        self.default = default
        self._boolean = isinstance(default, bool)

    def flatten(self) -> List[types.BuildingBlock]:
        return [self]

    def as_value(self) -> List[types.BuildingBlock]:
        return [self]

    def compile(self, query_args: types.QueryArgs) -> str:
        if self.default is Ellipsis or self.default is None:
            type_ = Any  # type: ignore
            default = self.default
        elif isinstance(self.default, type):
            type_ = self.default
            default = Ellipsis
        else:
            type_ = type(self.default)
            default = self.default

        res = (type_, default)

        if self.name in query_args:
            if res != query_args[self.name]:
                warnings.warn(
                    f"Variable with name {repr(self.name)} has multiple types/values: \
{res} and {query_args[self.name]}"
                )
        else:
            query_args[self.name] = res

        index = list(query_args.keys()).index(self.name) + 1
        return f"${index}"

    def __repr__(self):
        default_part = ""
        if self.default is not Ellipsis:
            default_part = ", " + repr(self.default)
        return f"{self.__class__.__name__}({repr(self.name)}{default_part})"

    @property
    def boolean(self):
        return self._boolean
