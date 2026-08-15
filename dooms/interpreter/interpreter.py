import sys
from .environment import Environment
from .errors import DoomsRuntimeError
from dooms.tree.statements import ExpressionStatement, VariableDeclaration, BlockStatement, WhileStatement, IfStatement, FunctionDeclaration, ReturnStatement, ImportStatement, ClassDeclaration
from dooms.tree.expressions import Literal, Identifier, AssignmentExpression, BinaryExpression, CallExpression, ArrayLiteral, MemberExpression, DictionaryLiteral, IndexExpression, ThisExpression, SetExpression, SuperExpression
from dooms.lexer.token_type import TokenType
from .function import DoomsFunction
from .errors import ReturnException, DoomsRuntimeError
from .array import DoomsArray
from .dictionary import DoomsDictionary
from .module import DoomsModule
from .classes import DoomsClass, DoomsInstance
from .string_methods import get_string_method
import os

class DoomsSuper:
    def __init__(self, instance, superclass):
        self.instance = instance
        self.superclass = superclass

def builtin_print(args):
    # Print boolean as true/false to match JS output format
    def format_arg(a):
        if a is True: return "true"
        if a is False: return "false"
        return str(a)
    print(*(format_arg(a) for a in args))
    return None

class DoomsInputString(str):
    pass

def builtin_input(args):
    prompt = ""
    if len(args) > 0:
        prompt = str(args[0])
    try:
        val = input(prompt)
        return DoomsInputString(val)
    except EOFError:
        return DoomsInputString("")

class Interpreter:
    def __init__(self, environment=None):
        self.environment = environment or Environment()
        self.environment.define("print", builtin_print, TokenType.ANY_TYPE)
        self.environment.define("input", builtin_input, TokenType.ANY_TYPE)

    def interpret(self, program):
        for statement in program.body:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, ImportStatement):
            filepath_val = self.evaluate(statement.filepath)
            if not isinstance(filepath_val, str):
                raise DoomsRuntimeError("Import filepath must be a string.")
            
            # Read and parse the imported file
            if not os.path.exists(filepath_val):
                raise DoomsRuntimeError(f"Module not found: '{filepath_val}'")
            
            with open(filepath_val, 'r') as f:
                source = f.read()
            
            from dooms.lexer.lexer import Lexer
            from dooms.parser.parser import Parser
            lexer = Lexer(source)
            parser = Parser(lexer)
            module_program = parser.parse()
            
            if statement.namespace:
                # Option B: Namespaced Import
                module_env = Environment()
                module_interpreter = Interpreter(module_env)
                module_interpreter.interpret(module_program)
                
                module_obj = DoomsModule(module_env)
                self.environment.define(statement.namespace.name, module_obj, TokenType.ANY_TYPE)
            else:
                # Option A: Global Inclusion
                # We execute the imported file's AST within the current environment
                for stmt in module_program.body:
                    self.execute(stmt)
            return

        if isinstance(statement, ExpressionStatement):
            self.evaluate(statement.expression)
        elif isinstance(statement, VariableDeclaration):
            value = self.evaluate(statement.initializer)
            self.environment.define(statement.name.name, value, statement.var_type)
        elif isinstance(statement, BlockStatement):
            self.execute_block(statement.statements, Environment(self.environment))
        elif isinstance(statement, WhileStatement):
            while self.is_truthy(self.evaluate(statement.condition)):
                self.execute(statement.body)
        elif isinstance(statement, IfStatement):
            if self.is_truthy(self.evaluate(statement.condition)):
                self.execute(statement.then_branch)
            elif statement.else_branch is not None:
                self.execute(statement.else_branch)
        elif isinstance(statement, ClassDeclaration):
            superclass = None
            if statement.superclass:
                superclass = self.evaluate(statement.superclass)
                if not isinstance(superclass, DoomsClass):
                    raise DoomsRuntimeError("Superclass must be a class.")

            fields = {}
            for field in statement.fields:
                fields[field.name.name] = field
                
            methods = {}
            dooms_class = DoomsClass(statement.name.name, methods, superclass, fields, statement.is_abstract)
            
            for method in statement.methods:
                function = DoomsFunction(method, self.environment, dooms_class)
                methods[method.name.name] = function
            
            self.environment.define(statement.name.name, dooms_class, TokenType.ANY_TYPE)
        elif isinstance(statement, FunctionDeclaration):
            function = DoomsFunction(statement, self.environment)
            self.environment.define(statement.name.name, function)
        elif isinstance(statement, ReturnStatement):
            value = None
            if statement.value is not None:
                value = self.evaluate(statement.value)
            raise ReturnException(value)
        else:
            raise DoomsRuntimeError(f"Unknown statement type: {type(statement).__name__}")

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def evaluate(self, expr):
        if isinstance(expr, ArrayLiteral):
            if expr.fixed_size is not None:
                return DoomsArray([], fixed_size=expr.fixed_size)
            elements = [self.evaluate(el) for el in expr.elements]
            return DoomsArray(elements)
            
        if isinstance(expr, DictionaryLiteral):
            data = {}
            for k, v in zip(expr.keys, expr.values):
                key_val = self.evaluate(k)
                if not isinstance(key_val, str):
                    raise DoomsRuntimeError("Dictionary keys must be strings.")
                data[key_val] = self.evaluate(v)
            return DoomsDictionary(data)
            
        if isinstance(expr, IndexExpression):
            obj = self.evaluate(expr.obj)
            index = self.evaluate(expr.index)
            if isinstance(obj, DoomsDictionary):
                return obj.get_value(index)
            elif isinstance(obj, DoomsArray):
                if not isinstance(index, int):
                    raise DoomsRuntimeError("Array index must be integer.")
                if index < 0 or index >= len(obj.elements):
                    raise DoomsRuntimeError("Array index out of bounds.")
                return obj.elements[index]
            raise DoomsRuntimeError("Only arrays and dictionaries support index access.")

        if isinstance(expr, MemberExpression):
            obj = self.evaluate(expr.obj)
            
            current_class = None
            try:
                current_class = self.environment.get("__current_class__")
            except DoomsRuntimeError:
                pass
                
            if isinstance(obj, DoomsSuper):
                method = obj.superclass.find_method(expr.property.name)
                if not method:
                    raise DoomsRuntimeError(f"Undefined property '{expr.property.name}' on superclass.")
                return method.bind(obj.instance)
            elif isinstance(obj, DoomsInstance):
                return obj.get_value(expr.property.name, current_class)
            elif isinstance(obj, DoomsArray):
                return obj.get_method(expr.property.name)
            elif isinstance(obj, DoomsDictionary):
                if obj.has_method(expr.property.name):
                    return obj.get_method(expr.property.name)
                return obj.get_value(expr.property.name)
            elif isinstance(obj, DoomsModule):
                return obj.get_value(expr.property.name)
            elif isinstance(obj, str):
                return get_string_method(obj, expr.property.name)
            raise DoomsRuntimeError("Only instances, arrays, strings, dictionaries, and modules have methods/properties.")

        if isinstance(expr, Literal):
            if expr.value is True:
                return True
            if expr.value is False:
                return False
            return expr.value

        if isinstance(expr, ThisExpression):
            return self.environment.get("this")

        if isinstance(expr, SuperExpression):
            try:
                current_class = self.environment.get("__current_class__")
            except DoomsRuntimeError:
                raise DoomsRuntimeError("Cannot use 'super' outside of a class.")
            if not current_class.superclass:
                raise DoomsRuntimeError(f"Class '{current_class.name}' has no superclass.")
            this_instance = self.environment.get("this")
            return DoomsSuper(this_instance, current_class.superclass)

        if isinstance(expr, Identifier):
            return self.environment.get(expr.name)

        if isinstance(expr, AssignmentExpression):
            value = self.evaluate(expr.value)
            self.environment.assign(expr.name.name, value)
            return value

        if isinstance(expr, SetExpression):
            obj = self.evaluate(expr.obj)
            
            current_class = None
            try:
                current_class = self.environment.get("__current_class__")
            except DoomsRuntimeError:
                pass
                
            if isinstance(obj, DoomsInstance):
                val = self.evaluate(expr.value)
                obj.set_value(expr.property.name, val, current_class)
                return val
            elif isinstance(obj, DoomsDictionary):
                val = self.evaluate(expr.value)
                obj.set_value(expr.property.name, val)
                return val
            raise DoomsRuntimeError("Only instances and dictionaries have settable properties.")

        if isinstance(expr, BinaryExpression):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator == TokenType.PLUS:
                return left + right
            elif expr.operator == TokenType.MINUS:
                return left - right
            elif expr.operator == TokenType.STAR:
                return left * right
            elif expr.operator == TokenType.SLASH:
                return left // right
            elif expr.operator == TokenType.LESS:
                return left < right
            elif expr.operator == TokenType.GREATER:
                return left > right
            elif expr.operator == TokenType.EQUAL_EQUAL:
                return left == right

        if isinstance(expr, CallExpression):
            callee = self.evaluate(expr.callee)
            
            evaluated_args = []
            for arg in expr.args:
                evaluated_args.append(self.evaluate(arg))
                
            if isinstance(callee, DoomsFunction):
                return callee(self, evaluated_args)
            elif isinstance(callee, DoomsClass):
                return callee(self, evaluated_args)
            elif callable(callee):
                return callee(evaluated_args)
            else:
                raise DoomsRuntimeError("Can only call functions and classes.")

        raise DoomsRuntimeError(f"Unknown expression type: {type(expr).__name__}")
