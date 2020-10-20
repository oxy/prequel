"""Helpers to construct various combinations of values."""

from typing import Sequence

from . import types
from .expression import Expression, Operator


def group(values: Sequence[types.Value], op: Operator) -> types.Value:
    """Group a sequence of values with an operator.

    Args:
        values: sequence of values to combine
        op: operator to combine with

    Examples:
        >>> pq.group([pq.Column('name') == 'Oxy', pq.Column('id') == 101], pq.Operator.and_).flatten()
        ['(', '"name"', '=', pq.Variable('name', 'Oxy'), ')', 'AND', '(', '"id"', '=', Variable('id', 101), ')']
    """
    if not values:
        raise ValueError("No values given!")

    if len(values) < 2:
        return values[0]

    expr = Expression(values[0], op, values[1])
    for con in values[2:]:
        expr = Expression(expr, op, con)

    return expr
