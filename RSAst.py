from enum import Enum, auto

class NodeType(Enum):
  # Statements
  Program           = auto()
  VariableDeclaration = auto()
  IfStatement       = auto()
  WhileStatement    = auto()
  GenStatement    = auto()
  FunctionDef       = auto()

  # Expressions
  AssignmentExpr    = auto()
  MemberExpr        = auto()
  CallExpr          = auto()
  FunctionCallExpr  = auto()

  # Literals
  Property          = auto()
  ObjectLiteral     = auto()
  NumericLiteral    = auto()
  FloatLiteral      = auto()
  StringLiteral     = auto()
  NullLiteral       = auto()
  Identifier        = auto()
  UnaryExpr         = auto()
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

class UnaryExpr(Expr):
  def __init__(self, op, node):
    self.kind: str = NodeType.UnaryExpr
    self.op = op
    self.node = node

  def __repr__(self):
    return f"(UnaryExpr {self.op} {self.node})"

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

class FloatLiteral(Expr):
  def __init__(self, value):
    self.kind: str = NodeType.FloatLiteral
    self.value: float = value

  def __repr__(self):
    return f"(Float {self.value})"

class StringLiteral(Expr):
  def __init__(self, value):
    self.kind: str = NodeType.StringLiteral
    self.value: str = value

  def __repr__(self):
    return f"(String \"{repr(self.value)[1:-1]}\")"

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
    self.kind: str = NodeType.NullLiteral
    self.value: str = "null"

  def __repr__(self):
    return f"(Null)"

class AssignmentExpr(Expr):
  def __init__(self, assigne, value):
    self.kind = NodeType.AssignmentExpr
    self.assigne: Expr = assigne
    self.value: Expr = value

  def __repr__(self):
    return f"(Assign {self.assigne} {self.value})"

class Property(Expr):
  def __init__(self, key, value):
    self.kind = NodeType.Property
    self.key: str = key
    self.value = value

  def __repr__(self):
    return f"(Property {self.key} -> {self.value})"

class ObjectLiteral(Expr):
  def __init__(self, value):
    self.kind: str = NodeType.ObjectLiteral
    self.properties: list = value

  def __repr__(self):
    return f"(ObjectLiteral {self.properties})"

class CallExpr(Expr):
  def __init__(self, caller, args):
    self.kind = NodeType.CallExpr
    self.caller: Expr = caller
    self.args: list = args

  def __repr__(self):
    return f"(CallExpr {self.caller} {self.args})"

class MemberExpr(Expr):
  def __init__(self, map_obj, property_, computed):
    self.kind = NodeType.AssignmentExpr
    self.map_obj: Expr = map_obj
    self.property_: Expr = property_
    self.computed: bool = computed

  def __repr__(self):
    return f"(MemberExpr {self.map_obj} {self.property_}{' computed'*int(self.computed)})"

class FunctionCallExpr(Expr):
  def __init__(self, name, args):
    self.name: str = name
    self.args: list = args

  def __repr__(self):
    return f"(FunctionCall {self.name} {self.args})"

class IfStatement(Stmt):
  def __init__(self, body, test_cond, alternate = None):
    self.kind = NodeType.IfStatement
    self.body = body
    self.test_cond = test_cond
    self.alternate = alternate

  def __repr__(self):
    if (self.alternate != None):
      return f"(IfElse {self.test_cond} {self.body} {self.alternate})"
    return f"(If {self.test_cond} {self.body})"

class WhileStatement(Stmt):
  def __init__(self, body, test_cond):
    self.kind = NodeType.WhileStatement
    self.body = body
    self.test_cond = test_cond

  def __repr__(self):
    return f"(While {self.test_cond} {self.body})"

class GenStatement(Stmt):
  def __init__(self, body, test_cond):
    self.kind = NodeType.GenStatement
    self.body = body
    self.test_cond = test_cond

  def __repr__(self):
    return f"(Generator {self.test_cond} {self.body})"

class FunctionDef(Stmt):
  def __init__(self, name, args, body):
    self.kind = NodeType.FunctionDef
    self.name = name
    self.args = args
    self.body = body

  def __repr__(self):
    return f"(Fn {self.name} {self.args} {self.body})"

