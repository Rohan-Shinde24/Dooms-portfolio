from dataclasses import dataclass
from typing import Any, List
from dooms.lexer.token_type import TokenType

@dataclass
class Expression:
    pass

@dataclass
class Literal(Expression):
    value: Any

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class CallExpression(Expression):
    callee: Expression
    args: List[Expression]

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression

@dataclass
class MemberExpression(Expression):
    obj: Expression
    property: Identifier

@dataclass
class IndexExpression(Expression):
    obj: Expression
    index: Expression

@dataclass
class ArrayLiteral(Expression):
    elements: List[Expression]
    fixed_size: int | None = None

@dataclass
class DictionaryLiteral(Expression):
    keys: List[Expression]
    values: List[Expression]

@dataclass
class ThisExpression(Expression):
    pass

@dataclass
class SetExpression(Expression):
    obj: Expression
    property: Identifier
    value: Expression

@dataclass
class AssignmentExpression(Expression):
    name: Identifier
    value: Expression

@dataclass
class SuperExpression(Expression):
    pass
