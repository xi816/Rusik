from RSValues import RuntimeVal
from RSError import i_error, c_error

class REnvironment:
  def __init__(self, parentENV = None):
    self.parent: REnvironment = parentENV
    self.variables: dict = {}

  __repr__ = lambda self: f"({self.variables})"

  def declareVar(self, varname: str, value: RuntimeVal) -> RuntimeVal:
    c_error(self.variables.get(varname) != None, f"Trying to declare a variable `{varname}`, but it is already defined")
    self.variables[varname] = value
    return value

  def assignVar(self, varname: str, value: RuntimeVal) -> RuntimeVal:
    c_error(self.variables.get(varname) == None, f"Trying to assign value to a variable `{varname}`, but it's not defined yet")
    env = self.resolve(varname)
    env.variables[varname] = value

  def lookupVar(self, varname: str) -> RuntimeVal:
    env = self.resolve(varname)
    return env.variables[varname]

  def resolve(self, varname: str):
    if (self.variables.get(varname) != None):
      return self
    c_error(self.parent == None, f"Trying to check the variable `{varname}`, but it was never declared")
    return self.parent.resolve(varname)

