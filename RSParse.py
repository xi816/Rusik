from normal_print import print, println
from RSError import i_error, c_error
from colorama import Fore

from RSValues import NullVal
from RSAst import Stmt, Program, Expr, BinaryExpr, NumericLiteral, NullLiteral, Identifier, VarDeclaration
from RSToken import TokenType, tokenize

EndOfFile = ("EOF", "Sys")

class RParser:
  def __init__(self):
    self.tokens = []
    self.pos = 0

  def clear(self):
    self.pos = 0

  def at(self):
    return self.tokens[self.pos]

  def eat(self):
    prev = self.tokens[self.pos]
    self.pos += 1
    return prev

  def expect(self, tp, errmsg):
    prev = self.tokens[self.pos]
    self.pos += 1
    if ((not prev) or (prev.TYPE != tp)):
      println(f"{Fore.RED}PARSE ERROR{Fore.RESET}: {errmsg}")
      exit(1)
    return prev

  def not_EOF(self):
    return (self.at() != TokenType.EOF)

  def parse_primary_expr(self) -> Expr:
    tk = self.at().TYPE
    if (tk == TokenType.Ident):
      return Identifier(self.eat().VALUE)
    elif (tk == TokenType.Null):
      self.eat()
      return NullLiteral("null")
    elif (tk == TokenType.Number):
      return NumericLiteral(float(self.eat().VALUE))
    elif (tk == TokenType.Paren_0):        # ( -- Paren_0, ) -- Paren_1
      self.eat()
      value = self.parse_expr()
      self.expect(TokenType.Paren_1, "Unterminated parenthesis expression") # Skip the Paren_0
      return value
    elif (tk == TokenType.EOF):
      return EndOfFile
    else:
      assert (False), f"Unexpected token {self.at()}"

  def parse_additive_expr(self) -> Expr:
    left = self.parse_multiplicative_expr()
    while (self.at().VALUE == "+" or self.at().VALUE == "-"):
      op = self.eat().VALUE
      right = self.parse_multiplicative_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_multiplicative_expr(self) -> Expr:
    left = self.parse_primary_expr()
    while (self.at().VALUE == "*" or self.at().VALUE == "/" or self.at().VALUE == "%"):
      op = self.eat().VALUE
      right = self.parse_primary_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_expr(self) -> Expr:
    addt_expr = self.parse_additive_expr()
    return addt_expr

  def parse_var_declaration(self):
    is_const = self.eat().TYPE == TokenType.Kw_Const
    identifier = self.expect(TokenType.Ident, "Expected identifier after будет | константа").VALUE
    self.expect(TokenType.Op_Eq, "Expected `=` token in var declaration")
    declaration = VarDeclaration(identifier, is_const, self.parse_expr())
    return declaration

  def parse_stmt(self) -> Stmt:
    if (self.at().TYPE == TokenType.Kw_Let):
      return self.parse_var_declaration()
    elif (self.at().TYPE == TokenType.Kw_Const):
      return self.parse_var_declaration()
    else:
      return (self.parse_expr())

  def produceAST(self, src: str) -> Program:
    self.tokens = tokenize(src)
    program = Program()

    while (True):
      parsed_stmt = self.parse_stmt()
      if (parsed_stmt == EndOfFile):
        break
      else:
        program.body.append(parsed_stmt)

    return program

