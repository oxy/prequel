"""Type checking information for various Protocols implemented by prequel objects."""

from typing import Any, Dict, List, Protocol, Tuple, Union, runtime_checkable

__all__ = ["QueryArgs", "BaseBlock", "BuildingBlock", "Block", "Value"]


QueryArgs = Dict[str, Tuple[Any, Any]]


class BaseBlock(Protocol):  # pylint: disable=too-few-public-methods
    """
    Abstract class for objects that can be understood by mkquery().
    """

    def compile(self, query_args: QueryArgs) -> str:
        """Compile an object into a finalized string."""
        ...


BuildingBlock = Union[str, BaseBlock]


class Block(Protocol):  # pylint: disable=too-few-public-methods
    """Abstract class that implements a basic query block object."""

    def flatten(self) -> List[BuildingBlock]:
        """Flattens a block to a list of building blocks."""
        ...


@runtime_checkable
class Value(Block, Protocol):
    """Abstract base class for values.

    A Value must implement three methods:
    - `Value.__init__()`
        creates an instance of a value
    - `Value.as_value()`
        returns a list of objects that can be passed to mkquery()
    - `Value._convert_arg()` (optional)
        which converts any object to a Value when used to form a Constraint.
    """

    def as_value(self) -> List[BuildingBlock]:
        ...

    @property
    def boolean(self) -> bool:
        ...
