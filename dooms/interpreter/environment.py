from typing import Any
from .errors import DoomsRuntimeError
from dooms.lexer.token_type import TokenType

def validate_type(name: str, value: Any, expected_type: Any):
    from dooms.interpreter.array import DoomsArray
    from dooms.interpreter.interpreter import DoomsInputString

    def validate_type_single(val, exp):
        if isinstance(val, DoomsInputString):
            if exp == TokenType.INT_TYPE:
                try:
                    return int(val)
                except ValueError:
                    raise DoomsRuntimeError(f"Cannot convert input '{val}' to int.")
            if exp == TokenType.BOOLEAN_TYPE:
                if val.lower() == 'true': return True
                if val.lower() == 'false': return False
                raise DoomsRuntimeError(f"Cannot convert input '{val}' to boo.")

        if exp == TokenType.ANY_TYPE:
            return val
        if exp == TokenType.INT_TYPE:
            if not isinstance(val, int) or isinstance(val, bool):
                raise DoomsRuntimeError(f"Type mismatch: cannot assign {type(val).__name__} to int variable '{name}'")
        elif exp == TokenType.STRING_TYPE:
            if not isinstance(val, str):
                raise DoomsRuntimeError(f"Type mismatch: cannot assign {type(val).__name__} to str variable '{name}'")
        elif exp == TokenType.BOOLEAN_TYPE:
            if not isinstance(val, bool):
                raise DoomsRuntimeError(f"Type mismatch: cannot assign {type(val).__name__} to boo variable '{name}'")
        return val

    if isinstance(expected_type, list):
        if not isinstance(value, DoomsArray):
            raise DoomsRuntimeError(f"Type mismatch: expected tuple, got {type(value).__name__}")
        if len(value.elements) != len(expected_type):
            raise DoomsRuntimeError(f"Tuple length mismatch: expected {len(expected_type)}, got {len(value.elements)}")
        
        new_elements = []
        for i in range(len(expected_type)):
            new_elements.append(validate_type_single(value.elements[i], expected_type[i]))
        value.elements = new_elements
        return value

    if isinstance(value, DoomsArray):
        new_elements = []
        for element in value.elements:
            new_elements.append(validate_type_single(element, expected_type))
        value.elements = new_elements
        return value

    return validate_type_single(value, expected_type)

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value, expected_type=TokenType.ANY_TYPE):
        if name in self.values:
            raise DoomsRuntimeError(f"Variable '{name}' is already defined.")
        value = validate_type(name, value, expected_type)
        self.values[name] = {'value': value, 'type': expected_type}

    def assign(self, name, value):
        if name in self.values:
            expected_type = self.values[name]['type']
            value = validate_type(name, value, expected_type)
            self.values[name]['value'] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise DoomsRuntimeError(f"Undefined variable: {name}")

    def get(self, name: str):
        if name in self.values:
            return self.values[name]["value"]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise DoomsRuntimeError(f"Undefined variable: {name}")
