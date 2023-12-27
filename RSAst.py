from enum import Enum, auto

# Types of AST Nodes:
#  "Program",
#  "NumericLiteral",
#  "NullLiteral",
#  "Identifier",
#  "BinaryExpr"

class NodeType(Enum):
  # Statements
  Program           = auto()
  VariableDeclaration = auto()

  # Expressions
  NumericLiteral    = auto()
  NullLiteral       = auto()
  Identifier        = auto()
  BinaryExpr        = auto()


class Stmt:
  def __init__(self, kind):
    self.kind: NodeType

class Program(Stmt):
  def __init__(self):
    self.kind: str = NodeType.Program
    self.body: list = []

  def __repr__(self):
    return f"(Program {self.body})"

class Expr(Stmt):
  pass

class BinaryExpr(Expr):
  def __init__(self, left, right, op):
    self.kind: str = NodeType.BinaryExpr
    self.left = left
    self.right = right
    self.op = op

  def __repr__(self):
    return f"(BinaryExpr {self.op} {self.left} {self.right})"

class Identifier(Expr):
  def __init__(self, symbol):
    self.kind: str = NodeType.Identifier
    self.symbol: str = symbol

  def __repr__(self):
    return f"(Identifier {self.symbol})"

class NumericLiteral(Expr):
  def __init__(self, value):
    self.kind: str = NodeType.NumericLiteral
    self.value: int = value

  def __repr__(self):
    return f"(Number {self.value})"

class VarDeclaration(Stmt):
  def __init__(self, identifier, is_constant, def_value):
    self.kind: str = NodeType.VariableDeclaration
    self.constant: bool = is_constant
    self.identifier: str = identifier
    self.value: Expr = def_value

  def __repr__(self):
    return f"(VariableDeclaration {'!'*int(not self.constant)}const {self.identifier} {self.value})"

class NullLiteral(Expr):
  def __init__(self, value):
    self.kind: str = "NullLiteral"
    self.value: str = "null"

  def __repr__(self):
    return f"(Null)"

