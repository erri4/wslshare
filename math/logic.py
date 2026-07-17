import re
import sys
import itertools

TOKEN_SPEC = [
    ("IFF_SYM",     r"<=>"),
    ("IMPLIES_SYM1", r"=>"),
    ("IMPLIES_SYM2", r"->"),
    ("EQ1", r"=="),
    ("EQ2", r"="),
    ("AND_SYM",     r"&&|&"),
    ("OR_SYM",      r"\|\||\|"),
    ("XOR_SYM",     r"\^"),
    ("NOT_SYM",     r"-"),
    ("TRUE_SYM",    r"1"),
    ("FALSE_SYM",   r"0"),
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("WORD",        r"[A-Za-z_][A-Za-z0-9_]*"),
    ("SKIP",        r"[ \t]+"),
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))
SYMBOL_TOKEN_MAP = {
    "IFF_SYM": ("IFF", None),
    "IMPLIES_SYM1": ("IMPLIES", None),
    "IMPLIES_SYM2": ("IMPLIES", None),
    "EQ1": ("IFF", None),
    "EQ2": ("IFF", None),
    "AND_SYM": ("AND", None),
    "OR_SYM": ("OR", None),
    "XOR_SYM": ("XOR", None),
    "NOT_SYM": ("NOT", None),
    "TRUE_SYM": ("CONST", True),
    "FALSE_SYM": ("CONST", False),
}

WORD_KEYWORDS = {
    "not": ("NOT", None),
    "and": ("AND", None),
    "or": ("OR", None),
    "xor": ("XOR", None),
    "implies": ("IMPLIES", None),
    "iff": ("IFF", None),
    "true": ("CONST", True),
    "false": ("CONST", False),
    "v": ("OR", None),
    "f": ("CONST", False),
    "t": ("CONST", True),
}

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


def tokenize(text):
    tokens = []
    pos = 0
    while pos < len(text):
        match = TOKEN_RE.match(text, pos)
        if not match:
            raise SyntaxError(f"Unexpected character {text[pos]!r} at position {pos}")
        kind = match.lastgroup
        value = match.group()
        pos = match.end()
        if kind == "SKIP":
            continue
        if kind in SYMBOL_TOKEN_MAP:
            tok_kind, tok_value = SYMBOL_TOKEN_MAP[kind]
            tokens.append(Token(tok_kind, value if tok_value is None else tok_value))
        elif kind == "WORD":
            lowered = value.lower()
            if lowered in WORD_KEYWORDS:
                tok_kind, tok_value = WORD_KEYWORDS[lowered]
                tokens.append(Token(tok_kind, value if tok_value is None else tok_value))
            else:
                tokens.append(Token("VAR", value))
        else:
            tokens.append(Token(kind, value))
    tokens.append(Token("EOF", None))
    return tokens

class Var:
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return bool(env[self.name])

    def __repr__(self):
        return self.name


class Const:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

    def __repr__(self):
        return str(self.value)


class Not:
    def __init__(self, operand: BinOp):
        self.operand = operand

    def eval(self, env):
        return not self.operand.eval(env)

    def __repr__(self):
        return f"(not {self.operand})"


class BinOp:
    def __init__(self, op: str, left: "BinOp", right: "BinOp"):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if self.op == "and":
            return a and b
        if self.op == "or":
            return a or b
        if self.op == "xor":
            return a != b
        if self.op == "implies":
            return (not a) or b
        if self.op == "iff":
            return a == b
        raise ValueError(f"Unknown operator {self.op}")

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, kind):
        tok = self.peek()
        if tok.kind != kind:
            raise SyntaxError(f"Expected {kind} but found {tok.kind} ({tok.value!r})")
        return self.advance()

    def parse(self):
        node = self.parse_iff()
        self.expect("EOF")
        return node

    def parse_iff(self):
        node = self.parse_implies()
        while self.peek().kind == "IFF":
            self.advance()
            right = self.parse_implies()
            node = BinOp("iff", node, right)
        return node

    def parse_implies(self):
        node = self.parse_or()
        while self.peek().kind == "IMPLIES":
            self.advance()
            right = self.parse_or()
            node = BinOp("implies", node, right)
        return node

    def parse_or(self):
        node = self.parse_xor()
        while self.peek().kind == "OR":
            self.advance()
            right = self.parse_xor()
            node = BinOp("or", node, right)
        return node

    def parse_xor(self):
        node = self.parse_and()
        while self.peek().kind == "XOR":
            self.advance()
            right = self.parse_and()
            node = BinOp("xor", node, right)
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.peek().kind == "AND":
            self.advance()
            right = self.parse_not()
            node = BinOp("and", node, right)
        return node

    def parse_not(self):
        if self.peek().kind == "NOT":
            self.advance()
            return Not(self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        if tok.kind == "VAR":
            self.advance()
            return Var(tok.value)
        if tok.kind == "CONST":
            self.advance()
            return Const(tok.value)
        if tok.kind == "LPAREN":
            self.advance()
            node = self.parse_iff()
            self.expect("RPAREN")
            return node
        raise SyntaxError(f"Unexpected token {tok.kind} ({tok.value!r})")


def parse_expression(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    return parser.parse()


def collect_variables(node, found=None):
    if found is None:
        found = []
    if isinstance(node, Var):
        if node.name not in found:
            found.append(node.name)
    elif isinstance(node, Not):
        collect_variables(node.operand, found)
    elif isinstance(node, BinOp):
        collect_variables(node.left, found)
        collect_variables(node.right, found)
    return found

def print_truth_table(texts: list[str], asts: list[BinOp], variables: list[str]):
    print(f"\nExpressions: {', '.join(texts)}")
    print(f"Parsed as : {', '.join([repr(ast) for ast in asts])}\n")

    header = ['x'] + variables + texts
    col_width = 1
    print(" | ".join(h.center(col_width) for h in header))
    print("-+-".join("-" * len(h) for h in header))

    for combo in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, combo))
        row = [str(int(''.join([str(int(bit)) for bit in combo]), 2))] + [str(int(v)).center(col_width) for v in combo]
        for text, ast in zip(texts, asts):
            result = ast.eval(env)
            row += [str(int(result)).center(max(col_width, len(text)))]
        print(" | ".join(row))


def main():
    texts = input("Enter a logic expression: ").strip().split(',')
    texts = [text.strip() for text in texts]
    try:
        asts = [parse_expression(text.strip()) for text in texts]
    except SyntaxError as e:
        print(f"\nInvalid expression: {e}")
        sys.exit(1)

    variables = []
    for ast in asts:
        variables = list(dict.fromkeys(collect_variables(ast) + variables))
    variables.sort()

    if not variables:
        for text, ast in zip(texts, asts):
            print(f"\nExpressions: {text}")
            print(f"Parsed as : {ast}")
            print(f"Result    : {ast.eval({})}")
        return

    print(f"\nFound variables: {', '.join(variables)}")
    choice = 'y'#input("Show full truth table? (y/n): ").strip().lower()

    if choice.startswith("y"):
        print_truth_table(texts, asts, variables)
    else:
        env = {}
        for v in variables:
            val = input(f"Value of {v} (True/False): ").strip().lower()
            env[v] = val in ("true", "1", "t", "yes")
        result = ast.eval(env)
        print(f"\nExpression: {text}")
        print(f"Parsed as : {ast}")
        print(f"Result    : {result}")


if __name__ == "__main__":
    main()
