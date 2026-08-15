from dataclasses import dataclass
from typing import Any
from .token_type import TokenType

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
