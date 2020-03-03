from dataclasses import dataclass, field
from random import randint
from typing import Any

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Message:
    async_: bool = field(
        metadata=config(
            field_name="async",
        )
    )
    type_: str = field(
        metadata=config(
            field_name="type")
    )
    id_: int = field(
        metadata=config(
            field_name="id"
        ),
        default=randint(100000, 999999)
    )
    data: Any = None


__all__ = ['Message']
