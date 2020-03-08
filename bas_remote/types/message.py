from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Message:
    """Class that represents default BAS message."""

    async_: bool = field(
        metadata=config(
            field_name="async",
        )
    )
    """Is message async."""

    type_: str = field(
        metadata=config(
            field_name="type"
        )
    )
    """Message type string."""

    id_: int = field(
        metadata=config(
            field_name="id"
        )
    )
    """Message id number."""

    data: Any = None
    """Message data object."""


__all__ = ['Message']
