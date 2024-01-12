from normal_print import print, println
from RSError import i_error, c_error
from colorama import Fore

from RSValues import NullVal
from RSAst import NodeType, Stmt, Program, Expr, BinaryExpr, UnaryExpr, NumericLiteral, FloatLiteral, StringLiteral, NullLiteral, Identifier, VarDeclaration, AssignmentExpr, Property, ObjectLiteral, FunctionCallExpr, IfStatement, WhileStatement, MemberExpr, CallExpr, FunctionDef, GenStatement, ArrayLiteral
from RSToken import TokenType, tokenize

EndOfFile = ("EOF", "Sys")

class RParser:
  def __init__(self, lexer_flags):
    self.tokens = []
    self.lexer_flags = lexer_flags
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
      println(f"{Fore.RED}ОШИБКА ПАРСИНГА{Fore.RESET}\nФайл {Fore.RED}{prev.FILENAME}{Fore.RESET}:{Fore.YELLOW}{prev.POS[0]}{Fore.RESET}:{Fore.GREEN}{prev.POS[1]}{Fore.RESET}: {errmsg}")
      exit(1)
    return prev

  def not_EOF(self):
    return (self.at() != TokenType.EOF)

  def parse_primary_expr(self) -> Expr:
    tk = self.at().TYPE
    if (tk == TokenType.Op_Binary):
      val = self.at().VALUE
      if (val == "+" or val == "-" or val == "/"):
        return UnaryExpr(self.eat().VALUE, self.parse_stmt())
    elif (tk == TokenType.Ident):
      return Identifier(self.eat().VALUE)
    elif (tk == TokenType.Number):
      return NumericLiteral(int(self.eat().VALUE))
    elif (tk == TokenType.Float):
      return FloatLiteral(float(self.eat().VALUE))
    elif (tk == TokenType.String):
      return StringLiteral(self.eat().VALUE)
    elif (tk == TokenType.Bracket_0):
      return self.parse_array()
    elif (tk == TokenType.Paren_0):
      self.eat()
      value = self.parse_expr()
      self.expect(TokenType.Paren_1, "Нет закрывающей скобки в выражении")
      return value
    elif (tk == TokenType.EOF):
      return EndOfFile
    else:
      self.expect(None, f"Не ожидался токен `{self.at().TYPE} {self.at().VALUE}`")

  def parse_array(self) -> Expr:
    self.expect(TokenType.Bracket_0, "Нет окрывающей квадратной скобки (`[`) в начале массива")
    args = self.parse_arguments_list(TokenType.Bracket_1)
    self.expect(TokenType.Bracket_1, "Нет закрывающей квадратной скобки (`]`) в конце массива")
    return ArrayLiteral(args)

  def parse_comparison_expr(self) -> Expr:
    left = self.parse_additive_expr()
    while (self.at().VALUE == "==" or self.at().VALUE == "<" or self.at().VALUE == ">" or self.at().VALUE == "<=" or self.at().VALUE == ">=" or self.at().VALUE == "!="):
      op = self.eat().VALUE
      right = self.parse_additive_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_additive_expr(self) -> Expr:
    left = self.parse_multiplicative_expr()
    while (self.at().VALUE == "+" or self.at().VALUE == "-"):
      op = self.eat().VALUE
      right = self.parse_multiplicative_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_multiplicative_expr(self) -> Expr:
    left = self.parse_shift_expr()
    while (self.at().VALUE == "*" or self.at().VALUE == "/" or self.at().VALUE == "%"):
      op = self.eat().VALUE
      right = self.parse_call_member_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_shift_expr(self) -> Expr:
    left = self.parse_call_member_expr()
    while (self.at().VALUE == "<<" or self.at().VALUE == ">>" or self.at().VALUE == "~>" or self.at().VALUE == "~~"):
      op = self.eat().VALUE
      right = self.parse_call_member_expr()
      left: BinaryExpr = BinaryExpr(left, right, op)
    return left

  def parse_call_expr(self, caller: Expr) -> Expr:
    call_expr = CallExpr(caller, self.parse_args())
    if (self.at().TYPE == TokenType.Paren_0):
      self.parse_call_expr(call_expr)
    return call_expr

  def parse_args(self) -> list:
    self.expect(TokenType.Paren_0, "Ожидалась открывающая скобка (`(`) в начале списка аргументов")
    args = [] if (self.at().TYPE == TokenType.Paren_1) else self.parse_arguments_list()
    self.expect(TokenType.Paren_1, "Ожидалась закрывающая скобка (`)`) в конце списка аргументов")
    return args

  def parse_arguments_list(self, end = None) -> list:
    if (self.at().TYPE == end):
      return []
    args = [self.parse_assignment_expr()]
    while (self.at().TYPE == TokenType.Comma) and (self.eat()):
      if (self.at().TYPE == end):
        break
      args.append(self.parse_assignment_expr())
    return args

  def parse_member_expr(self) -> Expr:
    map_obj = self.parse_primary_expr()
    while (self.at().TYPE == TokenType.Dot) or (self.at().TYPE == TokenType.Bracket_0):
      operator = self.eat()
      if (operator.TYPE == TokenType.Dot):
        computed = False
        m_property = Identifier(self.eat().VALUE)
        c_error(m_property.kind != NodeType.Identifier, "Cannot use DMU expression when type is not an identifier")
      else:
        computed = True
        m_property = self.parse_expr()
        self.expect(TokenType.Bracket_1, "No closing bracket (`]`) in DMC expression")
      map_obj = MemberExpr(map_obj, m_property, computed)
    return map_obj

  def parse_call_member_expr(self) -> Expr:
    member = self.parse_member_expr()
    if (self.at().TYPE == TokenType.Paren_0):
      return self.parse_call_expr(member)
    return member

  def parse_assignment_expr(self) -> Expr:
    left = self.parse_object_expr()
    if (self.at().TYPE == TokenType.Op_Eq):
      self.eat()
      value = self.parse_stmt()
      return AssignmentExpr(left, value)
    elif (self.at().TYPE == TokenType.Op_Binary):
      if (self.at().VALUE == "++" or self.at().VALUE == "--" or self.at().VALUE == "**"):
        oper = self.at().VALUE
        self.eat()
        value = self.parse_stmt()
        return AssignmentExpr(left, BinaryExpr(left, value, oper[0]))
    return left

  def parse_if_stmt(self):
    self.eat()
    self.expect(TokenType.Paren_0, "No opening parenthesis (`(`) at the start of an if-block condition")
    test_cond = self.parse_expr()
    self.expect(TokenType.Paren_1, "No closing parenthesis (`)`) at the end of an if-block condition")
    if_body = self.parse_block()
    alter = None
    if (self.at().TYPE == TokenType.Kw_Else):
      self.eat()
      if (self.at().TYPE == TokenType.Kw_If):
        alter = self.parse_if_stmt()
      else:
        alter = self.parse_block()

    return IfStatement(if_body, test_cond, alter)

  def parse_fn_stmt(self):
    self.eat()
    name = self.eat().VALUE
    args = self.parse_args()
    body = self.parse_block()
    return FunctionDef(name, args, body)

  def parse_while_stmt(self):
    self.eat()
    self.expect(TokenType.Paren_0, "No opening parenthesis (`(`) at the start of an while-block loop")
    test_cond = self.parse_expr()
    self.expect(TokenType.Paren_1, "No closing parenthesis (`)`) at the end of an while-block loop")
    while_body = self.parse_block()

    return WhileStatement(while_body, test_cond)

  def parse_gen_stmt(self):
    self.eat()
    self.expect(TokenType.Paren_0, "No opening parenthesis (`(`) at the start of an gen-block loop")
    test_cond = self.parse_expr()
    self.expect(TokenType.Paren_1, "No closing parenthesis (`)`) at the end of an gen-block loop")
    gen_body = self.parse_block()

    return GenStatement(gen_body, test_cond)

  def parse_block(self) -> list:
    self.expect(TokenType.Brace_0, "No opening curly brace (`{`) at the start of a block")
    body = []
    while (self.at().TYPE != TokenType.Brace_1):
      stmt = self.parse_stmt()
      body.append(stmt)
    self.expect(TokenType.Brace_1, "No closing curly brace (`}`) at the end of a block")
    return body

  def parse_expr(self) -> Expr:
   return self.parse_assignment_expr()

  def parse_object_expr(self) -> Expr:
    if (self.at().TYPE != TokenType.Brace_0):
      return self.parse_comparison_expr()
    self.eat()
    properties = []
    while (self.at().TYPE != TokenType.Brace_1):
      map_key = self.expect(TokenType.Ident, "Expected key name for key-value pairs in map definition").VALUE
      if (self.at().TYPE == TokenType.Comma): # {key,}
        self.eat()
        properties.append(Property(map_key, NullVal()))
        continue
      elif (self.at().TYPE == TokenType.Brace_1): # {key}
        properties.append(Property(map_key, NullVal()))
        continue
      self.expect(TokenType.Colon, "No colon in map definition") # {key: val}
      map_value = self.parse_expr()
      properties.append(Property(map_key, map_value))
      if (self.at().TYPE != TokenType.Brace_1): # {key1: val1, ...}
        self.expect(TokenType.Comma, "Missing comma or closing brace in map definition")
    self.expect(TokenType.Brace_1, "Unterminated map literal")
    return ObjectLiteral(properties)

  def parse_var_declaration(self):
    is_const = self.eat().TYPE == TokenType.Kw_Const
    identifier = self.expect(TokenType.Ident, f"Ожидалось название переменной после `{['будет', 'константа'][int(is_const)]}`").VALUE
    if (self.at().TYPE == TokenType.Op_Eq):
      self.eat()
      declaration = VarDeclaration(identifier, is_const, self.parse_stmt())
    else:
      declaration = VarDeclaration(identifier, is_const, NullLiteral("null"))
    # self.expect(TokenType.Op_Eq, "Expected `=` token in var declaration")
    return declaration

  def parse_stmt(self) -> Stmt:
    if (self.at().TYPE == TokenType.Kw_Let):
      result = self.parse_var_declaration()
    elif (self.at().TYPE == TokenType.Kw_Const):
      result = self.parse_var_declaration()
    elif (self.at().TYPE == TokenType.Kw_If):
      result = self.parse_if_stmt()
    elif (self.at().TYPE == TokenType.Kw_While):
      result = self.parse_while_stmt()
    elif (self.at().TYPE == TokenType.Kw_Gen):
      result = self.parse_gen_stmt()
    elif (self.at().TYPE == TokenType.Kw_Fn):
      result = self.parse_fn_stmt()
    else:
      result = (self.parse_expr())
    return result

  def pretty_puts_program(self, program, spaces = 0) -> str:
    res = "(Program\n"
    spaces = 2
    for i in program.body:
      res += f"{' '*spaces}{i}\n"
    res += ')'
    return res

  def produceAST(self, src: str, debug_ast = False) -> Program:
    self.tokens = tokenize(src, self.lexer_flags)
    program = Program()

    while (True):
      parsed_stmt = self.parse_stmt()
      if (parsed_stmt == EndOfFile):
        break
      else:
        program.body.append(parsed_stmt)

    if (debug_ast):
      println(self.pretty_puts_program(program))
    return program

