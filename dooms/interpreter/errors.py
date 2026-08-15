class DoomsError(Exception):
    def __init__(self, message, line=None, column=None, hint=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.hint = hint

class DoomsLexerError(DoomsError):
    pass

class DoomsParserError(DoomsError):
    pass

class DoomsRuntimeError(DoomsError):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
