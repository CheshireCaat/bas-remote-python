from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class Response:
    success: bool = False
    message: str = None
    result: Any = None


__all__ = ['Response']
