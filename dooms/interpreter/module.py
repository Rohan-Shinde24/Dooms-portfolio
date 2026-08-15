from .errors import DoomsRuntimeError

class DoomsModule:
    def __init__(self, environment):
        self.environment = environment

    def get_value(self, name):
        try:
            return self.environment.get(name)
        except DoomsRuntimeError:
            raise DoomsRuntimeError(f"Module has no export named '{name}'.")

    def __str__(self):
        return "<module>"
