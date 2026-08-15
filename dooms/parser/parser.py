from dooms.lexer.token_type import TokenType
from dooms.interpreter.errors import DoomsParserError
from dooms.tree.statements import Program, ExpressionStatement, VariableDeclaration, BlockStatement, WhileStatement, IfStatement, FunctionDeclaration, ReturnStatement, ImportStatement, ClassDeclaration, MethodDeclaration, FieldDeclaration
from dooms.tree.expressions import Identifier, Literal, CallExpression, BinaryExpression, AssignmentExpression, ArrayLiteral, MemberExpression, DictionaryLiteral, IndexExpression, ThisExpression, SetExpression, SuperExpression

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.current_token = self.lexer.next_token()
            return token
        else:
            raise DoomsParserError(
                f"Expected {token_type.name} but got {self.current_token.type.name}",
                self.current_token.line,
                self.current_token.column,
                f"Check syntax around line {self.current_token.line}."
            )

    def match(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
            return True
        return False

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.current_token.type == TokenType.LEFT_BRACE:
            return self.parse_block()
        if self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        if self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        if self.current_token.type == TokenType.FUNC:
            return self.parse_function_declaration()
        if self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        if self.current_token.type == TokenType.IMPORT:
            return self.parse_import_statement()
        if self.current_token.type in [TokenType.CLASS, TokenType.ABSTRACT]:
            return self.parse_class_declaration()
        if self.current_token.type in [TokenType.INT_TYPE, TokenType.STRING_TYPE, TokenType.BOOLEAN_TYPE, TokenType.ANY_TYPE, TokenType.LEFT_BRACKET]:
            return self.parse_variable_declaration()
        return self.parse_expression_statement()

    def parse_block(self):
        self.eat(TokenType.LEFT_BRACE)
        statements = []
        while self.current_token.type not in [TokenType.RIGHT_BRACE, TokenType.EOF]:
            statements.append(self.parse_statement())
        self.eat(TokenType.RIGHT_BRACE)
        return BlockStatement(statements)

    def parse_while_statement(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RIGHT_PAREN)
        body = self.parse_statement()
        return WhileStatement(condition, body)

    def parse_if_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RIGHT_PAREN)
        then_branch = self.parse_statement()
        
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.parse_statement()
            
        return IfStatement(condition, then_branch, else_branch)

    def parse_function_declaration(self):
        self.eat(TokenType.FUNC)
        name_token = self.eat(TokenType.IDENTIFIER)
        name = Identifier(name_token.value)
        
        self.eat(TokenType.LEFT_PAREN)
        params = []
        if self.current_token.type != TokenType.RIGHT_PAREN:
            var_type = self.eat(self.current_token.type).type
            param_name = self.eat(TokenType.IDENTIFIER)
            params.append({'name': Identifier(param_name.value), 'var_type': var_type})
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                var_type = self.eat(self.current_token.type).type
                param_name = self.eat(TokenType.IDENTIFIER)
                params.append({'name': Identifier(param_name.value), 'var_type': var_type})
                
        self.eat(TokenType.RIGHT_PAREN)
        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_class_declaration(self):
        is_abstract = False
        if self.match(TokenType.ABSTRACT):
            is_abstract = True
            
        self.eat(TokenType.CLASS)
        name_token = self.eat(TokenType.IDENTIFIER)
        name = Identifier(name_token.value)
        
        superclass = None
        if self.match(TokenType.EXTENDS):
            super_token = self.eat(TokenType.IDENTIFIER)
            superclass = Identifier(super_token.value)
            
        self.eat(TokenType.LEFT_BRACE)
        methods = []
        fields = []
        
        while self.current_token.type != TokenType.RIGHT_BRACE and self.current_token.type != TokenType.EOF:
            modifier = TokenType.PUBLIC
            if self.current_token.type in [TokenType.PUBLIC, TokenType.PRIVATE, TokenType.PROTECTED]:
                modifier = self.current_token.type
                self.eat(modifier)
            
            method_is_abstract = False
            if self.match(TokenType.ABSTRACT):
                method_is_abstract = True
                
            if self.current_token.type == TokenType.FUNC:
                methods.append(self.parse_method_declaration(modifier, method_is_abstract))
            else:
                fields.append(self.parse_field_declaration(modifier))
                
        self.eat(TokenType.RIGHT_BRACE)
        
        return ClassDeclaration(name, superclass, methods, fields, is_abstract)

    def parse_method_declaration(self, modifier, is_abstract):
        self.eat(TokenType.FUNC)
        name_token = self.eat(TokenType.IDENTIFIER)
        name = Identifier(name_token.value)
        
        self.eat(TokenType.LEFT_PAREN)
        params = []
        if self.current_token.type != TokenType.RIGHT_PAREN:
            var_type = self.eat(self.current_token.type).type
            param_name = self.eat(TokenType.IDENTIFIER)
            params.append({'name': Identifier(param_name.value), 'var_type': var_type})
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                var_type = self.eat(self.current_token.type).type
                param_name = self.eat(TokenType.IDENTIFIER)
                params.append({'name': Identifier(param_name.value), 'var_type': var_type})
                
        self.eat(TokenType.RIGHT_PAREN)
        
        body = None
        if is_abstract:
            self.eat(TokenType.SEMICOLON)
        else:
            body = self.parse_block()
            
        return MethodDeclaration(name, params, body, modifier, is_abstract)

    def parse_field_declaration(self, modifier):
        var_type = self.parse_type()
        name_token = self.eat(TokenType.IDENTIFIER)
        name = Identifier(name_token.value)
        self.eat(TokenType.SEMICOLON)
        return FieldDeclaration(name, var_type, modifier)

    def parse_return_statement(self):
        self.eat(TokenType.RETURN)
        value = None
        if self.current_token.type not in [TokenType.SEMICOLON, TokenType.RIGHT_BRACE, TokenType.EOF]:
            value = self.parse_expression()
        self.match(TokenType.SEMICOLON)
        return ReturnStatement(value)

    def parse_import_statement(self):
        self.eat(TokenType.IMPORT)
        filepath = self.parse_expression()
        
        namespace = None
        if self.match(TokenType.AS):
            namespace_token = self.eat(TokenType.IDENTIFIER)
            namespace = Identifier(namespace_token.value)
            
        self.match(TokenType.SEMICOLON)
        return ImportStatement(filepath, namespace)

    def parse_type(self):
        if self.current_token.type == TokenType.LEFT_BRACKET:
            self.eat(TokenType.LEFT_BRACKET)
            types = []
            types.append(self.eat(self.current_token.type).type)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                types.append(self.eat(self.current_token.type).type)
            self.eat(TokenType.RIGHT_BRACKET)
            return types
        return self.eat(self.current_token.type).type

    def parse_variable_declaration(self):
        var_type = self.parse_type()
        
        identifier_token = self.eat(TokenType.IDENTIFIER)
        name = Identifier(identifier_token.value)
        
        self.eat(TokenType.EQUAL)
        
        initializer = self.parse_expression()
        
        self.match(TokenType.SEMICOLON)
        
        return VariableDeclaration(name, initializer, var_type)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self.match(TokenType.SEMICOLON)
        return ExpressionStatement(expr)

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        expr = self.parse_comparison()

        if self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            value = self.parse_assignment()

            if isinstance(expr, Identifier):
                return AssignmentExpression(expr, value)
            elif isinstance(expr, MemberExpression):
                return SetExpression(expr.obj, expr.property, value)
            raise DoomsParserError(
                "Invalid assignment target.",
                self.current_token.line,
                self.current_token.column,
                "You can only assign values to variables or properties."
            )

        return expr

    def parse_comparison(self):
        expr = self.parse_additive()

        while self.current_token.type in [TokenType.LESS, TokenType.GREATER, TokenType.EQUAL_EQUAL]:
            operator = self.current_token
            self.eat(operator.type)
            right = self.parse_additive()
            expr = BinaryExpression(expr, operator.type, right)

        return expr

    def parse_additive(self):
        expr = self.parse_multiplicative()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token
            self.eat(operator.type)
            right = self.parse_multiplicative()
            expr = BinaryExpression(expr, operator.type, right)

        return expr

    def parse_multiplicative(self):
        expr = self.parse_call_member()

        while self.current_token.type in [TokenType.STAR, TokenType.SLASH]:
            operator = self.current_token
            self.eat(operator.type)
            right = self.parse_call_member()
            expr = BinaryExpression(expr, operator.type, right)

        return expr

    def parse_call_member(self):
        expr = self.parse_primary()
        
        while True:
            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                property_name = self.eat(TokenType.IDENTIFIER).value
                expr = MemberExpression(expr, Identifier(property_name))
            elif self.current_token.type == TokenType.LEFT_BRACKET:
                self.eat(TokenType.LEFT_BRACKET)
                index_expr = self.parse_expression()
                self.eat(TokenType.RIGHT_BRACKET)
                expr = IndexExpression(expr, index_expr)
            elif self.current_token.type == TokenType.LEFT_PAREN:
                self.eat(TokenType.LEFT_PAREN)
                args = []
                if self.current_token.type != TokenType.RIGHT_PAREN:
                    args.append(self.parse_expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.append(self.parse_expression())
                self.eat(TokenType.RIGHT_PAREN)
                expr = CallExpression(expr, args)
            else:
                break
        return expr

    def parse_primary(self):
        if self.current_token.type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RIGHT_PAREN)
            return expr
            
        if self.current_token.type == TokenType.THIS:
            self.eat(TokenType.THIS)
            return ThisExpression()
            
        if self.current_token.type == TokenType.SUPER:
            self.eat(TokenType.SUPER)
            return SuperExpression()
            
        if self.current_token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Literal(True)
        
        if self.current_token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Literal(False)

        if self.current_token.type == TokenType.LEFT_BRACE:
            self.eat(TokenType.LEFT_BRACE)
            keys = []
            values = []
            if self.current_token.type != TokenType.RIGHT_BRACE:
                keys.append(self.parse_expression())
                self.eat(TokenType.COLON)
                values.append(self.parse_expression())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    keys.append(self.parse_expression())
                    self.eat(TokenType.COLON)
                    values.append(self.parse_expression())
            self.eat(TokenType.RIGHT_BRACE)
            return DictionaryLiteral(keys, values)

        if self.current_token.type == TokenType.NUMBER:
            value = int(self.current_token.value)
            self.eat(TokenType.NUMBER)
            return Literal(value)

        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.eat(TokenType.STRING)
            return Literal(value)
        
        if self.current_token.type == TokenType.LEFT_BRACKET:
            self.eat(TokenType.LEFT_BRACKET)
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.eat(TokenType.LEFT_PAREN)
                size = int(self.current_token.value)
                self.eat(TokenType.NUMBER)
                self.eat(TokenType.RIGHT_PAREN)
                self.eat(TokenType.RIGHT_BRACKET)
                return ArrayLiteral([], fixed_size=size)
            
            elements = []
            if self.current_token.type != TokenType.RIGHT_BRACKET:
                elements.append(self.parse_expression())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    elements.append(self.parse_expression())
            self.eat(TokenType.RIGHT_BRACKET)
            return ArrayLiteral(elements)

        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            return Identifier(name)
        
        raise DoomsParserError(
            f"Unexpected token: '{self.current_token.value}'",
            self.current_token.line,
            self.current_token.column,
            "Did you forget a semicolon on the previous line, or use an invalid keyword?"
        )
