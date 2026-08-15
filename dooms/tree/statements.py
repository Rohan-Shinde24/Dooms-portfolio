from dataclasses import dataclass
from typing import List, Any
from .expressions import Expression, Identifier
from dooms.lexer.token_type import TokenType

@dataclass
class Statement:
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class VariableDeclaration(Statement):
    name: Identifier
    initializer: Expression
    var_type: Any

@dataclass
class BlockStatement(Statement):
    statements: List[Statement]

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Statement

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None

@dataclass
class FunctionDeclaration(Statement):
    name: Identifier
    params: List[dict] # dict with 'name': Identifier, 'var_type': TokenType
    body: BlockStatement

@dataclass
class ReturnStatement(Statement):
    value: Expression | None

@dataclass
class ImportStatement(Statement):
    filepath: Expression
    namespace: Identifier | None

@dataclass
class ClassDeclaration(Statement):
    name: Identifier
    superclass: Identifier | None
    methods: List['MethodDeclaration']
    fields: List['FieldDeclaration']
    is_abstract: bool

@dataclass
class MethodDeclaration(Statement):
    name: Identifier
    params: List[dict]
    body: BlockStatement | None
    modifier: TokenType
    is_abstract: bool

@dataclass
class FieldDeclaration(Statement):
    name: Identifier
    var_type: Any
    modifier: TokenType

@dataclass
class Program:
    body: List[Statement]
