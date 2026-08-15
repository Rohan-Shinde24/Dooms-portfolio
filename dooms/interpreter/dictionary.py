from .errors import DoomsRuntimeError
from .array import DoomsArray

class DoomsDictionary:
    def __init__(self, data=None):
        self.data = data or {}

    def get_value(self, key):
        if not isinstance(key, str):
            raise DoomsRuntimeError("Dictionary keys must be strings.")
        if key not in self.data:
            raise DoomsRuntimeError(f"KeyError: '{key}' not found in dictionary.")
        return self.data[key]

    def set_value(self, key, value):
        if not isinstance(key, str):
            raise DoomsRuntimeError("Dictionary keys must be strings.")
        self.data[key] = value

    def has_method(self, name):
        return name in ["set", "get", "keys", "values"]

    def get_method(self, name):
        if name == "set":
            return self.set_method
        elif name == "get":
            return self.get_method_func
        elif name == "keys":
            return self.keys_method
        elif name == "values":
            return self.values_method
        else:
            raise DoomsRuntimeError(f"Dictionary has no method '{name}'")

    def set_method(self, args):
        if len(args) != 2:
            raise DoomsRuntimeError(f"set() expects exactly 2 arguments, got {len(args)}")
        self.set_value(args[0], args[1])
        return None

    def get_method_func(self, args):
        if len(args) != 1:
            raise DoomsRuntimeError(f"get() expects exactly 1 argument, got {len(args)}")
        if args[0] in self.data:
            return self.data[args[0]]
        return None

    def keys_method(self, args):
        if len(args) != 0:
            raise DoomsRuntimeError(f"keys() expects 0 arguments")
        return DoomsArray(list(self.data.keys()))

    def values_method(self, args):
        if len(args) != 0:
            raise DoomsRuntimeError(f"values() expects 0 arguments")
        return DoomsArray(list(self.data.values()))

    def __str__(self):
        def format_el(e):
            if e is True: return "true"
            if e is False: return "false"
            if isinstance(e, str): return f'"{e}"'
            return str(e)
            
        items = [f'{format_el(k)}: {format_el(v)}' for k, v in self.data.items()]
        return "{" + ", ".join(items) + "}"
