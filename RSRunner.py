# Interpreter for the Rusik programming language
from RSValues import ValueType, RuntimeVal, NumberVal, NullVal, BooleanVal
from RSAst import NodeType, Stmt, BinaryExpr, Program, VarDeclaration
from RSError import i_error
from RSEnv import REnvironment

from colorama import Fore

def eval_program(program: Program, env: REnvironment) -> RuntimeVal:
  lastEvaluated: RuntimeVal = NullVal()

  for current_stmt in program.body:
    lastEvaluated = evaluate(current_stmt, env)

  return lastEvaluated

def eval_numeric_binary_expr(lhs: NumberVal, rhs: NumberVal, op: str):
  res = 0
  if (op == "+"):
    res = lhs.VALUE + rhs.VALUE
  elif (op == "-"):
    res = lhs.VALUE - rhs.VALUE
  elif (op == "*"):
    res = lhs.VALUE * rhs.VALUE
  elif (op == "/"):
    # TODO: Check for rhs == 0
    res = lhs.VALUE / rhs.VALUE
  elif (op == "%"):
    res = lhs.VALUE % rhs.VALUE
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
    res = int(lhs.VALUE) / int(rhs.VALUE)
  elif (op == "%"):
    res = int(lhs.VALUE) % int(rhs.VALUE)
  else:
    i_error(f"Unexpected yet or unknown binary operator `{op}`")
  return NumberVal(res)

def eval_binary_expr(binop: BinaryExpr, env: REnvironment) -> RuntimeVal:
  left_hs = evaluate(binop.left, env)
  right_hs = evaluate(binop.right, env)

  if (left_hs.TYPE == ValueType.Number and right_hs.TYPE == ValueType.Number):
    return eval_numeric_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Boolean and right_hs.TYPE == ValueType.Number):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Number and right_hs.TYPE == ValueType.Boolean):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  elif (left_hs.TYPE == ValueType.Boolean and right_hs.TYPE == ValueType.Boolean):
    return eval_numbool_binary_expr(left_hs, right_hs, binop.op)
  return NullVal()

def eval_identifier(ident, env: REnvironment) -> RuntimeVal:
  val = env.lookupVar(ident.symbol)
  return val

def eval_var_declaration(declaration: VarDeclaration, env: REnvironment) -> RuntimeVal:
  return env.declareVar(declaration.identifier, evaluate(declaration.value, env))

def evaluate(astNode: Stmt, env: REnvironment) -> RuntimeVal:
  if (astNode.kind == NodeType.NumericLiteral):
    return NumberVal(astNode.value)
  elif (astNode.kind == NodeType.Identifier):
    return eval_identifier(astNode, env)
  elif (astNode.kind == NodeType.NullLiteral):
    return NullLiteral()
  elif (astNode.kind == NodeType.BinaryExpr):
    return eval_binary_expr(astNode, env)
  elif (astNode.kind == NodeType.VariableDeclaration):
    return eval_var_declaration(astNode, env)
  elif (astNode.kind == NodeType.Program):
    return eval_program(astNode, env)
  else:
    i_error(f"Unexpected yet AST node {astNode}")

