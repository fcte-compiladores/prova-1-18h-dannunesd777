Nesse exercício, vamos extender a gramática de Lox para suportar listas. Para
manter a simplicidade, vamos assumir que uma lista é delimitada por colchetes e
cada elemento é separado por vírgulas, como abaixo:

```lox
[1, x, 40 + 2, "string"]
```

Lembre-se de suportar listas vazias

```lox
[]
```

e listas dentro de listas

```lox
[[1, 2, [3, [4]]]]
```

Também queremos aceitar a última vírgula opcional:

```lox
[   
    "primeiro", 
    "segundo",
]
```

Mas cuidado para não aceitar uma vírgula perdida `[,]`.

Você deve implementar suporte a listas na gramática e implementar o método eval
mais ou menos da seguinte forma:

```python


from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Any

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

class Expr:
    def eval(self, ctx: 'Ctx') -> Any:
        raise NotImplementedError()

@dataclass
class ListExpr(Expr):
    elements: List[Expr]

    def eval(self, ctx: 'Ctx'):
        return [elem.eval(ctx) for elem in self.elements]

@dataclass
class Literal(Expr):
    value: Any

    def eval(self, ctx: 'Ctx'):
        return self.value

@dataclass
class Variable(Expr):
    name: str

    def eval(self, ctx: 'Ctx'):
        return ctx.get(self.name)

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def eval(self, ctx: 'Ctx'):
        left_val = self.left.eval(ctx)
        right_val = self.right.eval(ctx)
        
        if self.operator.type == TokenType.PLUS:
            return left_val + right_val

class Ctx:
    def __init__(self):
        self.values = {}

    def get(self, name: str) -> Any:
        return self.values.get(name)

    def assign(self, name: str, value: Any):
        self.values[name] = value

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        return self.expression()

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        return self.list_()

    def list_(self) -> Expr:
        self.consume(TokenType.LEFT_BRACKET, "Expect '[' after list.")
        
        elements = []
        if not self.check(TokenType.RIGHT_BRACKET):
            while True:
                elements.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        
        self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after list elements.")
        return ListExpr(elements)

    def match(self, *types: TokenType) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def check(self, type_: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type_: TokenType, message: str) -> Token:
        if self.check(type_):
            return self.advance()
        raise RuntimeError(message)

class Interpreter:
    def __init__(self):
        self.ctx = Ctx()

    def interpret(self, expr: Expr):
        try:
            value = expr.eval(self.ctx)
            print(self.stringify(value))
        except RuntimeError as e:
            print(f"Error: {e}")

    def stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, list):
            return "[" + ", ".join(self.stringify(e) for e in obj) + "]"
        return str(obj)

def main():
    test_cases = [
        ("Lista vazia", [
            Token(TokenType.LEFT_BRACKET, "[", None, 1),
            Token(TokenType.RIGHT_BRACKET, "]", None, 1),
            Token(TokenType.EOF, "", None, 1)
        ]),
        ("Lista com elementos", [
            Token(TokenType.LEFT_BRACKET, "[", None, 1),
            Token(TokenType.NUMBER, "1", 1, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.NUMBER, "2", 2, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.NUMBER, "3", 3, 1),
            Token(TokenType.RIGHT_BRACKET, "]", None, 1),
            Token(TokenType.EOF, "", None, 1)
        ]),
        ("Lista com vírgula opcional no final", [
            Token(TokenType.LEFT_BRACKET, "[", None, 1),
            Token(TokenType.STRING, "'primeiro'", "primeiro", 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.STRING, "'segundo'", "segundo", 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.RIGHT_BRACKET, "]", None, 1),
            Token(TokenType.EOF, "", None, 1)
        ]),
        ("Lista aninhada", [
            Token(TokenType.LEFT_BRACKET, "[", None, 1),
            Token(TokenType.LEFT_BRACKET, "[", None, 1),
            Token(TokenType.NUMBER, "1", 1, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.NUMBER, "2", 2, 1),
            Token(TokenType.RIGHT_BRACKET, "]", None, 1),
            Token(TokenType.COMMA, ",", None, 1),
            Token(TokenType.NUMBER, "3", 3, 1),
            Token(TokenType.RIGHT_BRACKET, "]", None, 1),
            Token(TokenType.EOF, "", None, 1)
        ])
    ]

    interpreter = Interpreter()

    for name, tokens in test_cases:
        print(f"\nTeste: {name}")
        parser = Parser(tokens)
        expr = parser.parse()
        interpreter.interpret(expr)

if __name__ == "__main__":
    main()
```