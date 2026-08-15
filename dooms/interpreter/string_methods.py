from .errors import DoomsRuntimeError
from .array import DoomsArray

def get_string_method(obj_str: str, name: str):
    def length_method(args):
        if len(args) != 0: raise DoomsRuntimeError("length() expects 0 args")
        return len(obj_str)
        
    def upper_method(args):
        if len(args) != 0: raise DoomsRuntimeError("upper() expects 0 args")
        return obj_str.upper()
        
    def lower_method(args):
        if len(args) != 0: raise DoomsRuntimeError("lower() expects 0 args")
        return obj_str.lower()
        
    def split_method(args):
        if len(args) != 1 or not isinstance(args[0], str):
            raise DoomsRuntimeError("split() expects 1 string argument")
        parts = obj_str.split(args[0])
        return DoomsArray(parts)

    methods = {
        "length": length_method,
        "upper": upper_method,
        "lower": lower_method,
        "split": split_method
    }
    
    if name in methods:
        return methods[name]
    raise DoomsRuntimeError(f"String has no method '{name}'")
