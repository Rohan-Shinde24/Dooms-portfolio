from .errors import DoomsRuntimeError
from dooms.lexer.token_type import TokenType

class DoomsClass:
    def __init__(self, name, methods, superclass=None, fields=None, is_abstract=False):
        self.name = name
        self.methods = methods
        self.superclass = superclass
        self.fields = fields or {}
        self.is_abstract = is_abstract
        
    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.find_method(name)
        return None
        
    def __call__(self, interpreter, args):
        if self.is_abstract:
            raise DoomsRuntimeError(f"Cannot instantiate abstract class '{self.name}'.")
            
        self.check_abstract_methods_implemented(self)
        
        instance = DoomsInstance(self)
        self._init_fields(instance, interpreter)
        
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance)(interpreter, args)
        return instance

    def check_abstract_methods_implemented(self, concrete_class):
        for name, method in self.methods.items():
            if getattr(method.declaration, 'is_abstract', False):
                concrete_method = concrete_class.find_method(name)
                if not concrete_method or getattr(concrete_method.declaration, 'is_abstract', False):
                    raise DoomsRuntimeError(f"Class '{concrete_class.name}' must implement abstract method '{name}'.")
        if self.superclass:
            self.superclass.check_abstract_methods_implemented(concrete_class)
            
    def _init_fields(self, instance, interpreter):
        if self.superclass:
            self.superclass._init_fields(instance, interpreter)
        for name, field_decl in self.fields.items():
            instance.fields[name] = None

    def __str__(self):
        return f"<class {self.name}>"

class DoomsInstance:
    def __init__(self, dooms_class):
        self.dooms_class = dooms_class
        self.fields = {}
        
    def check_access(self, modifier, defining_class, access_context_class):
        if modifier == TokenType.PUBLIC:
            return True
        if modifier == TokenType.PRIVATE:
            return defining_class == access_context_class
        if modifier == TokenType.PROTECTED:
            cls = access_context_class
            while cls:
                if cls == defining_class:
                    return True
                cls = cls.superclass
            return False
        return True

    def get_field_info(self, cls, name):
        if name in cls.fields:
            return (cls.fields[name].modifier, cls)
        if cls.superclass:
            return self.get_field_info(cls.superclass, name)
        return None

    def get_value(self, name, access_context_class=None):
        if name in self.fields:
            field_info = self.get_field_info(self.dooms_class, name)
            if field_info:
                mod, def_class = field_info
                if not self.check_access(mod, def_class, access_context_class):
                    raise DoomsRuntimeError(f"Cannot access property '{name}' due to access modifiers.")
            return self.fields[name]
            
        method = self.dooms_class.find_method(name)
        if method:
            mod = getattr(method.declaration, 'modifier', TokenType.PUBLIC)
            if not self.check_access(mod, method.defining_class, access_context_class):
                raise DoomsRuntimeError(f"Cannot access method '{name}' due to access modifiers.")
            return method.bind(self)
            
        raise DoomsRuntimeError(f"Undefined property '{name}'.")
        
    def set_value(self, name, value, access_context_class=None):
        if name not in self.fields:
            raise DoomsRuntimeError(f"Cannot set undefined property '{name}'. All fields must be explicitly declared.")
            
        field_info = self.get_field_info(self.dooms_class, name)
        if field_info:
            mod, def_class = field_info
            if not self.check_access(mod, def_class, access_context_class):
                raise DoomsRuntimeError(f"Cannot set property '{name}' due to access modifiers.")
                
        self.fields[name] = value

    def __str__(self):
        return f"<{self.dooms_class.name} instance>"
