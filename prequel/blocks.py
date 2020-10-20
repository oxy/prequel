"""Implement basic helpers that combine blocks."""

from typing import List, Sequence, Union

from . import types


class CommaSeparated(types.Block):
    """Implement a simple comma separated list of blocks, eg. for columns.

    Attributes:
        objs: A list of objects to be parsed.

    Examples:
        >>> pq.CommaSeparated("hi", "hello", "test").flatten()
        ["hi", ",", "hello", ",", "test"]
        >>> pq.CommaSeparated("hi", pq.Variable("hello")).flatten()
        ["hi", ",", pq.Variable("hello")]
    """

    def __init__(self, *objs: Sequence[Union[str, types.Block]]):
        self.objs = objs

    def flatten(self) -> List[types.BuildingBlock]:
        """Flatten the Blocks into a set of comma-separated building blocks."""
        res: List[types.BuildingBlock] = []
        for obj in self.objs:
            if isinstance(obj, str):
                res.append(obj)
            elif isinstance(obj, types.Value):
                res.extend(obj.flatten())
            res.append(",")
        res.pop()
        return res
