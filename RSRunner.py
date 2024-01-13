# Interpreter for the Rusik programming language
import sys
from math import floor

from RSValues import ValueType, RuntimeVal, NumberVal, StringVal, NullVal, FloatVal, BooleanVal, ObjectVal, NativeFnValue, FnValue, ArrayVal
from RSAst import NodeType, Stmt, BinaryExpr, UnaryExpr, Program, VarDeclaration, AssignmentExpr, ObjectLiteral, CallExpr, NullLiteral, IfStatement, WhileStatement, GenStatement
from RSError import i_error, c_error
from RSEnv import REnvironment

from normal_print import print, println

from colorama import Fore

def eval_program(program: Program, env: REnvironment) -> RuntimeVal:
  lastEvaluated: list = []

  for current_stmt in program.body:
    lastEvaluated.append(evaluate(current_stmt, env))
  if (not lastEvaluated):
    lastEvaluated.append(NullVal())
  return lastEvaluated

def eval_numeric_unary_expr(hs: NumberVal, op: str):
  res = 0
  float_res = False
  if (op == "-"):
    res = -hs.VALUE
  elif (op == "+"):
    res = abs(hs.VALUE)
  elif (op == "/"):
    res = 1 / hs.VALUE
    float_res = True
  elif (op == "<"):
    res = int(hs.VALUE < 0)
  elif (op == ">"):
    res = int(hs.VALUE > 0)
  else:
    i_error(f"Неизвестная единичная операция `{op}`")
  if (float_res):
    return FloatVal(res)
  return NumberVal(res)

def eval_array_binary_expr(lhs: ArrayVal, rhs: ArrayVal, op: str):
  res = 0
  if (op == "+"):
    res = lhs.VALUE + rhs.VALUE
  else:
    i_error(f"Неизвестная единичная операция `{op}`")
  return ArrayVal(res)

def eval_arnum_binary_expr(lhs: ArrayVal, rhs: ArrayVal, op: str):
  res = 0
  if (op == "-"):
    res = lhs.VALUE[:-rhs.VALUE]
  else:
    i_error(f"Неизвестная единичная операция `{op}`")
  return ArrayVal(res)

def eval_float_unary_expr(hs: FloatVal, op: str):
  res = 0
  float_res = False
  if (op == "-"):
    res = -hs.VALUE
    float_res = True
  elif (op == "+"):
    res = abs(hs.VALUE)
    float_res = True
  elif (op == "/"):
    res = 1 / hs.VALUE
    float_res = True
  elif (op == "<"):
    res = int(hs.VALUE < 0)
  elif (op == ">"):
    res = int(hs.VALUE > 0)
  else:
    i_error(f"Неизвестная единичная операция `{op}`")
  if (float_res):
    return FloatVal(res)
  return NumberVal(res)

def eval_string_unary_expr(hs: NumberVal, op: str):
  res = 0
  if (op == "-"):
    res = hs.VALUE[::-1]
  else:
    i_error(f"Неизвестная единичная операция `{op}`")
  return StringVal(res)

def eval_numeric_binary_expr(lhs: NumberVal, rhs: NumberVal, op: str):
  res = 0
  float_res = False
  if (op == "+"):
    res = lhs.VALUE + rhs.VALUE
  elif (op == "-"):
    res = lhs.VALUE - rhs.VALUE
  elif (op == "*"):
    res = lhs.VALUE * rhs.VALUE
  elif (op == "/"):
    c_error(rhs.VALUE == 0, "Деление на ноль")
    res = lhs.VALUE / rhs.VALUE
    float_res = True
  elif (op == "%"):
    c_error(rhs.VALUE == 0, "Деление на ноль")
    res = lhs.VALUE % rhs.VALUE
  elif (op == "<<"):
    res = lhs.VALUE * (2 ** rhs.VALUE)
  elif (op == ">>"):
    res = floor(lhs.VALUE / (2 ** rhs.VALUE))
  elif (op == "=="):
    res = int(lhs.VALUE == rhs.VALUE)
  elif (op == "<"):
    res = int(lhs.VALUE < rhs.VALUE)
  elif (op == "<="):
    res = int(lhs.VALUE <= rhs.VALUE)
  elif (op == ">"):
    res = int(lhs.VALUE > rhs.VALUE)
  elif (op == ">="):
    res = int(lhs.VALUE >= rhs.VALUE)
  elif (op == "!="):
    res = int(lhs.VALUE != rhs.VALUE)
  elif (op == "~>"):
    c_error(rhs.VALUE == 0, "Нулевой корень")
    res = float(lhs.VALUE ** (1 / rhs.VALUE))
    float_res = True
  elif (op == "~~"):
    c_error(rhs.VALUE == 0, "Нулевая степень")
    res = float(lhs.VALUE ** rhs.VALUE)
    float_res = True
  else:
    i_error(f"Unexpected yet or unknown binary operator `{op}`")
  if (float_res):
    return FloatVal(res)
  return NumberVal(res)

def eval_float_binary_expr(lhs: NumberVal, rhs: NumberVal, op: str):
  res = 0
  float_res = True
  if (op == "+"):
    res = lhs.VALUE + rhs.VALUE
  elif (op == "-"):
    res = lhs.VALUE - rhs.VALUE
  elif (op == "*"):
    res = lhs.VALUE * rhs.VALUE
  elif (op == "/"):
    c_error(rhs.VALUE == 0, "Деление на ноль")
    res = lhs.VALUE / rhs.VALUE
  elif (op == "%"):
    c_error(rhs.VALUE == 0, "Деление на ноль")
    res = lhs.VALUE % rhs.VALUE
  elif (op == "~~"):
    c_error(rhs.VALUE == 0, "Нулевая степень")
    res = float(lhs.VALUE ** rhs.VALUE)
  elif (op == "=="):
    res = int(lhs.VALUE == rhs.VALUE)
    float_res = False
  elif (op == "<"):
    res = int(lhs.VALUE < rhs.VALUE)
    float_res = False
  elif (op == "<="):
    res = int(lhs.VALUE <= rhs.VALUE)
    float_res = False
  elif (op == ">"):
    res = int(lhs.VALUE > rhs.VALUE)
    float_res = False
  elif (op == ">="):
    res = int(lhs.VALUE >= rhs.VALUE)
    float_res = False
  elif (op == "!="):
    res = int(lhs.VALUE != rhs.VALUE)
    float_res = False
  elif (op == "~>"):
    c_error(rhs.VALUE == 0, "Нулевой корень")
    res = float(lhs.VALUE ** (1 / rhs.VALUE))
  elif (op == "<<"):
    res = float(lhs.VALUE * (2 ** rhs.VALUE))
  elif (op == ">>"):
    res = float(lhs.VALUE / (2 ** rhs.VALUE))
  else:
    i_error(f"Unexpected yet or unknown binary operator `{op}`")
  if (float_res):
    return FloatVal(res)
  return NumberVal(res)

def eval_string_binary_expr(lhs: NumberVal, rhs: NumberVal, op: str):
  res = 0
  if (op == "=="):
    res = int(lhs.VALUE == rhs.VALUE)
  elif (op == "<"):
    res = int(lhs.VALUE < rhs.VALUE)
  elif (op == "<="):
    res = int(lhs.VALUE <= rhs.VALUE)
  elif (op == ">"):
    res = int(lhs.VALUE > rhs.VALUE)
  elif (op == ">="):
    res = int(lhs.VALUE >= rhs.VALUE)
  elif (op == "!="):
    res = int(lhs.VALUE != rhs.VALUE)
  else:
    i_error(f"Unexpected yet or unknown binary operator `{op}`")
  return NumberVal(res)

def eval_numbool_binary_expr(lhs: BooleanVal, rhs: NumberVal, op: str):
  res = 0
  if (op == "+"):
    res = int(lhs.VALUE) + int(rhs.VALUE)
  elif (op == "-"):
    res = int(lhs.VALUE) - int(rhs.VALUE)
  elif (op == "*"):
    res = int(lhs.VALUE) * int(rhs.VALUE)
  elif (op == "/"):
    c_error(int(rhs.VALUE) == 0, "Деление на ноль")
    res = int(lhs.VALUE) / int(rhs.VALUE)
  elif (op == "%"):
    res = int(lhs.VALUE) % int(rhs.VALUE)
  elif (op == "<<"):
    res = int(lhs.VALUE) << int(rhs.VALUE)
  elif (op == ">>"):
    res = int(lhs.VALUE) >> int(rhs.VALUE)
  else:
    i_error(f"Unexpected yet or unknown binary operator `{op}`")
  return NumberVal(res)

def eval_unary_expr(unop: UnaryExpr, env: REnvironment) -> RuntimeVal:
  hs = evaluate(unop.node, env)
  if (hs.TYPE == ValueType.Number):
    return eval_numeric_unary_expr(hs, unop.op)
  elif (hs.TYPE == ValueType.Float):
    return eval_float_unary_expr(hs, unop.op)
  elif (hs.TYPE == ValueType.String):
    return eval_string_unary_expr(hs, unop.op)
  return NullVal()

def eval_binary_expr(binop: BinaryExpr, env: REnvironment) -> RuntimeVal:
  left_hs = evaluate(binop.left, env)
  right_hs = evaluate(binop.right, env)

  if (left_hs.TYPE == ValueType.Number and right_hs.TYPE == ValueType.Number):
    return eval_numeric_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Number and right_hs.TYPE == ValueType.Float):
    return eval_float_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Float and right_hs.TYPE == ValueType.Number):
    return eval_float_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Float and right_hs.TYPE == ValueType.Float):
    return eval_float_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Boolean and right_hs.TYPE == ValueType.Number):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Number and right_hs.TYPE == ValueType.Boolean):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Boolean and right_hs.TYPE == ValueType.Boolean):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.String and right_hs.TYPE == ValueType.String):
    return eval_string_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Array and right_hs.TYPE == ValueType.Array):
    return eval_array_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Array and right_hs.TYPE == ValueType.Number):
    return eval_arnum_binary_expr(left_hs, right_hs, binop.op)
  return NullVal()

def eval_identifier(ident, env: REnvironment) -> RuntimeVal:
  val = env.lookupVar(ident.symbol)
  return val

def eval_var_declaration(declaration: VarDeclaration, env: REnvironment) -> RuntimeVal:
  return env.declareVar(declaration.identifier, evaluate(declaration.value, env), declaration.constant)

def eval_assignment(node: AssignmentExpr, env: REnvironment) -> RuntimeVal:
  c_error(node.assigne.kind != NodeType.Identifier, f"Cannot assign value to `{node.assigne.kind}`")
  varname = node.assigne.symbol
  return env.assignVar(varname, evaluate(node.value, env))

def eval_object_expr(mobj: ObjectLiteral, env: REnvironment) -> RuntimeVal:
  map_obj = ObjectVal({})
  for i in range(len(mobj.properties)):
    map_key = mobj.properties[i].key
    map_value = mobj.properties[i].value
    runtmVal = (NullVal()) if (map_value is None) else (evaluate(map_value, env))
    map_obj.VALUE[map_key] = runtmVal
  return map_obj

def eval_call_expr(expr: CallExpr, env: REnvironment) -> RuntimeVal:
  args = list(map(lambda s: evaluate(s, env), expr.args))
  fn = evaluate(expr.caller, env)
  if (type(fn) == NativeFnValue):
    result = NativeFnValue(fn).fn_call.fn_call(args, env)
    if (isinstance(result, tuple)):
      if (result[0] == "CallExit"):
        sys.exit(result[1])
    else:
      return result
  elif (type(fn) == FnValue):
    scope = REnvironment(env)
    for i in range(len(args)):
      scope.declareVar(fn.args[i], args[i], False)
    result = NullVal()
    for stmt in fn.body:
      result = evaluate(stmt, scope)
    return result
  return NullVal()

def eval_if_stmt(declaration, env: REnvironment) -> RuntimeVal:
  test = evaluate(declaration.test_cond, env)
  if (bool(test.VALUE)):
    return eval_body(declaration.body, env, False)
  else:
    if (declaration.alternate != None):
      if (type(declaration.alternate) == IfStatement):
        eval_if_stmt(declaration.alternate, env)
      else:
        return eval_body(declaration.alternate, env, False)
  return NullVal()

def eval_while_stmt(declaration, env: REnvironment) -> RuntimeVal:
  result = NullVal()
  if (evaluate(declaration.test_cond, env).VALUE):
    while (True):
      result = eval_body(declaration.body, env, False)
      test = evaluate(declaration.test_cond, env)
      if (not bool(test.VALUE)):
        break
  return result

def eval_element_stmt(declaration, env: REnvironment) -> RuntimeVal:
  result = env.lookupVar(declaration.ident.symbol)
  offset = list(map(lambda x: evaluate(x, env).VALUE, declaration.offset))
  for i in offset:
    c_error(i > len(result.VALUE), f"Значение индекса {i} превосходит длину массива ({len(result.VALUE)})")
    result = result.VALUE[i]
  return result

def eval_fn_stmt(declaration, env: REnvironment) -> RuntimeVal:
  result = FnValue(declaration.name, list(map(lambda a: a.symbol, declaration.args)), declaration.body)
  env.declareVar(declaration.name, result, True)
  return result

def eval_body(body: list, env: REnvironment, newEnv: bool = True) -> RuntimeVal:
  if (newEnv):
    scope = REnvironment(env)
  else:
    scope = env
  result: RuntimeVal = NullVal()
  for stmt in body:
    result = evaluate(stmt, scope)
  return result

def evaluate(astNode: Stmt, env: REnvironment) -> RuntimeVal:
  c_error(isinstance(astNode, tuple), "Найден конец файла в аргументе, недостаточно аргументов в операторе")
  if (astNode.kind == NodeType.NumericLiteral):
    return NumberVal(astNode.value)
  elif (astNode.kind == NodeType.FloatLiteral):
    return FloatVal(astNode.value)
  elif (astNode.kind == NodeType.StringLiteral):
    return StringVal(astNode.value)
  elif (astNode.kind == NodeType.ArrayLiteral):
    return ArrayVal(list(map(lambda x: evaluate(x, env), astNode.args)))
  elif (astNode.kind == NodeType.Identifier):
    return eval_identifier(astNode, env)
  elif (astNode.kind == NodeType.ObjectLiteral):
    return eval_object_expr(astNode, env)
  elif (astNode.kind == NodeType.CallExpr):
    return eval_call_expr(astNode, env)
  elif (astNode.kind == NodeType.ElementStmt):
    return eval_element_stmt(astNode, env)
  elif (astNode.kind == NodeType.SetStmt):
    return eval_set_stmt(astNode, env)
  elif (astNode.kind == NodeType.FunctionDef):
    return eval_fn_stmt(astNode, env)
  elif (astNode.kind == NodeType.AssignmentExpr):
    return eval_assignment(astNode, env)
  elif (astNode.kind == NodeType.NullLiteral):
    return NullVal()
  elif (astNode.kind == NodeType.BinaryExpr):
    return eval_binary_expr(astNode, env)
  elif (astNode.kind == NodeType.UnaryExpr):
    return eval_unary_expr(astNode, env)
  elif (astNode.kind == NodeType.VariableDeclaration):
    return eval_var_declaration(astNode, env)
  elif (astNode.kind == NodeType.IfStatement):
    return eval_if_stmt(astNode, env)
  elif (astNode.kind == NodeType.WhileStatement):
    return eval_while_stmt(astNode, env)
  elif (astNode.kind == NodeType.GenStatement):
    return eval_gen_stmt(astNode, env)
  elif (astNode.kind == NodeType.Program):
    return eval_program(astNode, env)
  else:
    i_error(f"Unexpected yet AST node {astNode}")

