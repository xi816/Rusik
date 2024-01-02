from RSValues import RuntimeVal, BooleanVal, NullVal
from RSError import i_error, c_error

def createGlobalEnv():
  env = REnvironment()
  env.declareVar("истина", BooleanVal(True), True)
  env.declareVar("ложь", BooleanVal(False), True)
  return env

class REnvironment:
  def __init__(self, parentENV = None):
    self.is_global = (parentENV is None)
    self.parent: REnvironment = parentENV
    self.variables: dict = {}
    self.consts: set = set()

  __repr__ = lambda self: f"({self.variables})"

  def declareVar(self, varname: str, value: RuntimeVal, constant: bool) -> RuntimeVal:
    c_error(self.variables.get(varname) != None, f"Trying to declare a variable `{varname}`, but it is already defined")
    self.variables[varname] = value
    if (constant):
      self.consts.add(varname)
    return value

  def assignVar(self, varname: str, value: RuntimeVal) -> RuntimeVal:
    c_error(self.variables.get(varname) == None, f"Trying to assign value to a variable `{varname}`, but it's not defined yet")
    env = self.resolve(varname)
    c_error(varname in env.consts, f"Trying to assign new value to a constant")
    env.variables[varname] = value
    return value

  def lookupVar(self, varname: str) -> RuntimeVal:
    env = self.resolve(varname)
    return env.variables[varname]

  def resolve(self, varname: str):
    if (self.variables.get(varname) != None):
      return self
    c_error(self.parent == None, f"Trying to check the variable `{varname}`, but it was never declared")
    return self.parent.resolve(varname)

