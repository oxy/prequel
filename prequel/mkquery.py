"""Function to convert building blocks into query functions"""

from __future__ import annotations

import itertools
import inspect
from typing import Any, List, Sequence, Tuple, Callable

from . import types

__all__ = ["mkquery"]


def mkquery(blocks: Sequence[types.BuildingBlock]) -> Callable:
    """Build a query from a sequence of building blocks.

    Args:
        blocks: List of blocks to combine into a query

    Returns:
        A callable that takes variable arguments
        and returns a tuple that can be passed to PostgreSQL drivers.
        (such as asyncpg)
    """
    query_context: types.QueryArgs = {}
    parts = []
    result: List[Any] = [str]
    params: List[inspect.Parameter] = []

    for block in blocks:
        if isinstance(block, str):
            parts.append(block)
        else:
            parts.append(block.compile(query_context))

    for arg, info in query_context.items():
        type_, default = info
        result.append(type_)
        if type_ is Any:
            inspect_type = inspect.Parameter.empty
        else:
            inspect_type = type_

        if default is Ellipsis:
            default = inspect.Parameter.empty

        params.append(
            inspect.Parameter(
                name=arg,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=default,
                annotation=inspect_type,
            )
        )

    query = ""
    for part in parts:
        if part in [")", ","]:
            query = query.rstrip()
        query += part
        if part != "(":
            query += " "

    query = query.rstrip()
    return_type = Tuple[Any]  # type: ignore
    return_type.__args__ = tuple(result)  # type: ignore

    def inner(*args, **kwargs):
        nonlocal query, query_context
        # ignore VSCode, the above is not an error
        # Python LS cannot bind values with type hinted declarations :/
        convert_kw = []

        if len(args) > len(query_context):
            raise TypeError(
                f"Query takes {len(query_context)} arguments but {len(args)} were given"
            )
        elif len(args) < len(query_context):
            iterator = query_context.items()

            # Consume n items from the query_context dict
            next(itertools.islice(iterator, len(args), len(args)), None)
            for arg, data in iterator:
                val = kwargs.pop(arg, data[1])
                if val is Ellipsis:
                    raise TypeError(
                        f"Query missing a required keyword-only argument: {repr(arg)}"
                    )

                convert_kw.append(val)

        if kwargs:
            raise TypeError(
                f"Query got unexpected keyword arguments {list(kwargs.keys())}"
            )

        return (query, *args, *convert_kw)

    inner.__signature__ = inspect.Signature(
        parameters=params, return_annotation=return_type
    )
    return inner
