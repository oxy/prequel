"""Expression and Operator types."""

from __future__ import annotations

import enum
from typing import Any, List, cast

from . import types

__all__ = ["Operator", "ValueMixin", "Expression", "Between"]


class Operator(enum.Enum):
    """Enum of SQL operators."""

    add = "+"
    sub = "-"
    mul = "*"
    truediv = "/"
    inv = "~"
    eq = "="
    ne = "<>"
    le = "<="
    lt = "<"
    ge = ">="
    gt = ">"
    and_ = "AND"
    or_ = "OR"
    like = "LIKE"


class ValueMixin(types.Value):
    """
    Provide mixins and helper utilities to be used by
    classes that implement `types.Value`.

    If the class implements `Value._convert_arg`,
    use it to convert arbitrary arguments to `pq.Value`
    """

    def __ne__(self, other: Any):
        other = self._convert_arg(other, "ne")
        return Expression(self, Operator.ne, other)

    def __eq__(self, other: Any):
        other = self._convert_arg(other, "eq")
        return Expression(self, Operator.eq, other)

    def __le__(self, other):
        other = self._convert_arg(other, "le")
        return Expression(self, Operator.le, other)

    def __lt__(self, other):
        other = self._convert_arg(other, "lt")
        return Expression(self, Operator.lt, other)

    def __ge__(self, other):
        other = self._convert_arg(other, "ge")
        return Expression(self, Operator.ge, other)

    def __gt__(self, other):
        other = self._convert_arg(other, "gt")
        return Expression(self, Operator.gt, other)

    def like(self, other: Any = None):
        """Helper function to generate LIKE constraints."""
        other = self._convert_arg(other, "like")
        return Expression(self, Operator.like, other)

    def between(self, cmin: Any = ..., cmax: Any = ...):
        """Helper function to generate BETWEEN constraints."""
        cmin = self._convert_arg(cmin, "min")
        cmax = self._convert_arg(cmax, "max")
        return Between(self, cmin, cmax)

    def __add__(self, other: types.Value):
        if self.boolean or other.boolean:
            return Expression(self, Operator.and_, other)
        return Expression(self, Operator.add, other)

    def __sub__(self, other: types.Value):
        return Expression(self, Operator.sub, other)

    def __mul__(self, other: types.Value):
        return Expression(self, Operator.mul, other)

    def __truediv__(self, other: types.Value):
        if self.boolean or other.boolean:
            return Expression(self, Operator.or_, other)
        return Expression(self, Operator.truediv, other)

    def _convert_arg(self, other: Any, opname: str) -> types.Value:
        return cast(types.Value, other)


class Expression(ValueMixin):
    """SQL expression.
    Implements an expression consisting of two values and an operator.
    Can be nested to form more complex expressions.

    Attributes:
        lhs: left hand value.
        op: operator.
        rhs: right hand value.

    Examples:
        >>> pq.Expression(pq.Column("name"), pq.Operator.eq, pq.Variable("name_var")).flatten()
        ["name", "=", pq.Variable("name_var")]
    """

    def __init__(self, lhs: types.Value, op: Operator, rhs: types.Value):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def flatten(self) -> List[types.BuildingBlock]:
        return [*self.lhs.as_value(), self.op.value, *self.rhs.as_value()]

    def as_value(self) -> List[types.BuildingBlock]:
        return ["(", *self.flatten(), ")"]

    @property
    def boolean(self):
        return self.op in {
            Operator.and_,
            Operator.or_,
            Operator.le,
            Operator.lt,
            Operator.ge,
            Operator.gt,
            Operator.ne,
            Operator.eq,
        }

    def __repr__(self):
        return f'pq.Expression(lhs={repr(self.lhs)}, op={repr(self.op)}, rhs={repr(self.rhs)})'


class Between(ValueMixin):
    """Between SQL comparison.

    Attributes:
        val: Value being compared.
        min: Minimum of range.
        max: Maximum of range.
    """
    boolean = True

    def __init__(self, val: types.Value, cmin: types.Value, cmax: types.Value):
        self.val = val
        self.min = cmin
        self.max = cmax

    def flatten(self) -> List[types.BuildingBlock]:
        return [*self.val.as_value(), "BETWEEN", *self.min.as_value(), "AND", *self.max.as_value()]
