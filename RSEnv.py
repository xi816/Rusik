import RSValues
import RSFunction
from RSError import i_error, c_error

def MK_NFN(name):
  return RSValues.NativeFnValue(name)

def createGlobalEnv():
  env = REnvironment()

  # Булевы значения
  env.declareVar("истина", RSValues.BooleanVal(True), True)
  env.declareVar("ложь", RSValues.BooleanVal(False), True)

  # Функции
  ## Функции со строками
  env.declareVar("длина", MK_NFN(RSFunction.strLenFn), True)
  env.declareVar("строка", MK_NFN(RSFunction.toStrFn), True)
  env.declareVar("формат", MK_NFN(RSFunction.strFormatFn), True)
  env.declareVar("вывести", MK_NFN(RSFunction.printFn), True)
  env.declareVar("база_числа", MK_NFN(RSFunction.numBaseFn), True)
  env.declareVar("ввести", MK_NFN(RSFunction.inputFn), True)
  ## Функции с числами
  env.declareVar("число", MK_NFN(RSFunction.toIntFn), True)
  env.declareVar("символ", MK_NFN(RSFunction.charFn), True)
  env.declareVar("выход", MK_NFN(RSFunction.exitFn), True)
  ## Функции с дробными числами
  env.declareVar("дробное", MK_NFN(RSFunction.toFloatFn), True)
  ## Функции с булевой алгеброй
  env.declareVar("булево", MK_NFN(RSFunction.toBoolFn), True)
  ## Функции с файлами
  env.declareVar("открыть", MK_NFN(RSFunction.openFileFn), True)
  env.declareVar("прочитать", MK_NFN(RSFunction.readFileFn), True)
  env.declareVar("написать", MK_NFN(RSFunction.writeFileFn), True)
  env.declareVar("закрыть", MK_NFN(RSFunction.closeFileFn), True)
  ## Функции с любыми типами
  env.declareVar("тип", MK_NFN(RSFunction.typeofFn), True)

  return env

class REnvironment:
  def __init__(self, parentENV = None):
    self.is_global = (parentENV is None)
    self.parent: REnvironment = parentENV
    self.variables: dict = {}
    self.consts: set = set()

  __repr__ = lambda self: f"({self.variables})"

  def declareVar(self, varname: str, value, constant: bool):
    c_error(self.variables.get(varname) != None, f"Trying to declare a variable `{varname}`, but it is already defined")
    self.variables[varname] = value
    if (constant):
      self.consts.add(varname)
    return value

  def assignVar(self, varname: str, value):
    c_error(self.variables.get(varname) == None, f"Trying to assign value to a variable `{varname}`, but it's not defined yet")
    env = self.resolve(varname)
    c_error(varname in env.consts, f"Trying to assign new value to a constant")
    env.variables[varname] = value
    return value

  def lookupVar(self, varname: str):
    env = self.resolve(varname)
    return env.variables[varname]

  def resolve(self, varname: str):
    if (self.variables.get(varname) != None):
      return self
    c_error(self.parent == None, f"Trying to check the variable `{varname}`, but it was never declared")
    return self.parent.resolve(varname)

