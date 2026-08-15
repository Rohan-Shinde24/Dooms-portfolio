from .token import Token
from .token_type import TokenType
from dooms.interpreter.errors import DoomsLexerError

KEYWORDS = {
    'int': TokenType.INT_TYPE,
    'str': TokenType.STRING_TYPE,
    'boo': TokenType.BOOLEAN_TYPE,
    'any': TokenType.ANY_TYPE,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'while': TokenType.WHILE,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'func': TokenType.FUNC,
    'return': TokenType.RETURN,
    'import': TokenType.IMPORT,
    'as': TokenType.AS,
    'class': TokenType.CLASS,
    'this': TokenType.THIS,
    'extends': TokenType.EXTENDS,
    'super': TokenType.SUPER,
    'public': TokenType.PUBLIC,
    'private': TokenType.PRIVATE,
    'protected': TokenType.PROTECTED,
    'abstract': TokenType.ABSTRACT,
}

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def peek(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]

    def advance(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        char = self.source[self.position]
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def is_at_end(self) -> bool:
        return self.position >= len(self.source)

    def is_alpha(self, char: str) -> bool:
        return char.isalpha() or char == '_'

    def is_digit(self, char: str) -> bool:
        return char.isdigit()

    def is_alpha_numeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)

    def next_token(self) -> Token:
        self.skip_whitespace()

        if self.is_at_end():
            return Token(TokenType.EOF, None, self.line, self.column)

        char = self.peek()
        start_column = self.column
        start_line = self.line

        if char == '(':
            self.advance()
            return Token(TokenType.LEFT_PAREN, '(', start_line, start_column)
        if char == ')':
            self.advance()
            return Token(TokenType.RIGHT_PAREN, ')', start_line, start_column)
        if char == '{':
            self.advance()
            return Token(TokenType.LEFT_BRACE, '{', start_line, start_column)
        if char == '}':
            self.advance()
            return Token(TokenType.RIGHT_BRACE, '}', start_line, start_column)
        if char == '[':
            self.advance()
            return Token(TokenType.LEFT_BRACKET, '[', start_line, start_column)
        if char == ']':
            self.advance()
            return Token(TokenType.RIGHT_BRACKET, ']', start_line, start_column)
        if char == '.':
            self.advance()
            return Token(TokenType.DOT, '.', start_line, start_column)
        if char == '=':
            self.advance()
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.EQUAL_EQUAL, '==', start_line, start_column)
            return Token(TokenType.EQUAL, '=', start_line, start_column)
        if char == '<':
            self.advance()
            return Token(TokenType.LESS, '<', start_line, start_column)
        if char == '>':
            self.advance()
            return Token(TokenType.GREATER, '>', start_line, start_column)
        if char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+', start_line, start_column)
        if char == '-':
            self.advance()
            return Token(TokenType.MINUS, '-', start_line, start_column)
        if char == '*':
            self.advance()
            return Token(TokenType.STAR, '*', start_line, start_column)
        if char == '/':
            self.advance() # consume first '/'
            if self.peek() == '/':
                self.advance() # consume second '/'
                if self.peek() == '/':
                    self.advance() # consume third '/'
                    # Multi-line comment
                    while not self.is_at_end():
                        if self.peek() == '/' and self.position + 2 < len(self.source) and self.source[self.position+1] == '/' and self.source[self.position+2] == '/':
                            self.advance()
                            self.advance()
                            self.advance()
                            break
                        self.advance()
                    return self.next_token()
                else:
                    # Single-line comment
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                    return self.next_token()

            return Token(TokenType.SLASH, '/', start_line, start_column)
        if char == ',':
            self.advance()
            return Token(TokenType.COMMA, ',', start_line, start_column)
        if char == ';':
            self.advance()
            return Token(TokenType.SEMICOLON, ';', start_line, start_column)
        if char == ':':
            self.advance()
            return Token(TokenType.COLON, ':', start_line, start_column)
        if char == '"':
            return self.read_string()
        if self.is_digit(char):
            return self.read_number()
        if self.is_alpha(char):
            return self.read_identifier()

        raise DoomsLexerError(f"Unexpected character: '{char}'", self.line, self.column, "Ensure you aren't using invalid characters or missing spaces.")

    def skip_whitespace(self):
        while True:
            char = self.peek()
            if char in [' ', '\r', '\t', '\n']:
                self.advance()
            else:
                break

    def read_string(self) -> Token:
        start_column = self.column
        start_line = self.line
        start = self.position
        self.advance() # consume opening quote

        while self.peek() != '"' and not self.is_at_end():
            self.advance()

        if self.is_at_end():
            raise DoomsLexerError("Unterminated string.", start_line, start_column, "Make sure you have a closing quote (\") for your string.")

        self.advance() # consume closing quote
        value = self.source[start + 1 : self.position - 1]
        return Token(TokenType.STRING, value, start_line, start_column)

    def read_number(self) -> Token:
        start_column = self.column
        start_line = self.line
        value = ""

        while self.is_digit(self.peek()) and not self.is_at_end():
            value += self.advance()

        return Token(TokenType.NUMBER, int(value), start_line, start_column)

    def read_identifier(self) -> Token:
        start_column = self.column
        start_line = self.line
        value = ""

        while self.is_alpha_numeric(self.peek()) and not self.is_at_end():
            value += self.advance()

        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
        return Token(token_type, value, start_line, start_column)
