from .errors import DoomsRuntimeError

class DoomsArray:
    def __init__(self, elements, fixed_size=None):
        self.elements = elements
        self.fixed_size = fixed_size

    def push(self, args):
        if len(args) != 1:
            raise DoomsRuntimeError(f"push() expects exactly 1 argument, got {len(args)}")
        if self.fixed_size is not None and len(self.elements) >= self.fixed_size:
            raise DoomsRuntimeError(f"Cannot push: array is fixed to size {self.fixed_size}")
        self.elements.append(args[0])
        return None

    def append(self, args):
        return self.push(args)

    def insert(self, args):
        if len(args) != 2:
            raise DoomsRuntimeError(f"insert() expects exactly 2 arguments (index, value), got {len(args)}")
        
        index, value = args[0], args[1]
        if not isinstance(index, int):
            raise DoomsRuntimeError("insert() index must be an integer")
            
        if self.fixed_size is not None and len(self.elements) >= self.fixed_size:
            raise DoomsRuntimeError(f"Cannot insert: array is fixed to size {self.fixed_size}")
            
        self.elements.insert(index, value)
        return None

    def pop(self, args):
        if len(args) != 0:
            raise DoomsRuntimeError(f"pop() expects exactly 0 arguments, got {len(args)}")
        if len(self.elements) == 0:
            raise DoomsRuntimeError("Cannot pop from an empty array")
        return self.elements.pop()

    def get_method(self, name):
        if name == "push":
            return self.push
        elif name == "append":
            return self.append
        elif name == "insert":
            return self.insert
        elif name == "pop":
            return self.pop
        else:
            raise DoomsRuntimeError(f"Array has no method '{name}'")

    def __str__(self):
        def format_el(e):
            if e is True: return "true"
            if e is False: return "false"
            return str(e)
        return "[" + ", ".join(format_el(e) for e in self.elements) + "]"
