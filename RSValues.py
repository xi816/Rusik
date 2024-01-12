# Value types for Rusik programming language
from enum import Enum, auto

class ValueType(Enum):
  Null = auto()
  Number = auto()
  Float = auto()
  String = auto()
  Boolean = auto()
  Array = auto()
  Obj = auto()
  NativeFunction = auto()
  Function = auto()

class RuntimeVal():
  def __init__(self, TYPE):
    self.TYPE: ValueType = TYPE

class NullVal(RuntimeVal):
  def __init__(self):
    self.TYPE: ValueType = ValueType.Null
    self.VALUE: ValueType = ValueType.Null

  def __repr__(self):
    return "ничего"

class BooleanVal(RuntimeVal):
  def __init__(self, VALUE):
    self.TYPE: ValueType = ValueType.Boolean
    self.VALUE: bool = VALUE

  def __repr__(self):
    return ["ложь", "истина"][int(self.VALUE)]

class NumberVal(RuntimeVal):
  def __init__(self, VALUE):
    self.TYPE: ValueType = ValueType.Number
    self.VALUE: int = VALUE

  def __repr__(self):
    return f"{self.VALUE}"

class FloatVal(RuntimeVal):
  def __init__(self, VALUE):
    self.TYPE: ValueType = ValueType.Float
    self.VALUE: float = VALUE

  def __repr__(self):
    return f"{self.VALUE}"

class StringVal(RuntimeVal):
  def __init__(self, VALUE):
    self.TYPE: ValueType = ValueType.String
    self.VALUE: str = VALUE

  def __repr__(self):
    return f"\"{self.VALUE}\""

class ObjectVal(RuntimeVal):
  def __init__(self, VALUE):
    self.TYPE: ValueType = ValueType.Obj
    self.VALUE: dict = VALUE

  def __repr__(self):
    res_p = list(zip(list(self.VALUE.keys()), self.VALUE.values()))
    res = "{"
    for i, j in enumerate(res_p):
      res += f"{j[0]}: {j[1]}"
      if (i == len(self.VALUE)-1):
        res += "}"
      else:
        res += ", "
    return f"{res}"

class FunctionCall():
  def __init__(self, args, env):
    self.args = args
    self.env = env

  def __repr__(self):
    return f"(FnCall {self.args} {self.env})"

class NativeFnValue(RuntimeVal):
  def __init__(self, fn_call):
    self.TYPE = ValueType.NativeFunction
    self.fn_call: FunctionCall = fn_call

  def __repr__(self):
    return f"<Function {self.fn_call}>"

class ArrayVal(RuntimeVal):
  def __init__(self, elements):
    self.TYPE = ValueType.Array
    self.VALUE = elements

  def __repr__(self):
    return f"{self.VALUE}"

class FnValue(RuntimeVal):
  def __init__(self, name, args, body):
    self.TYPE = ValueType.Function
    self.name = name
    self.args = args
    self.body = body

  def __repr__(self):
    return f"<Fn {self.name} {self.args} {self.body}>"

class FileObjectVal(RuntimeVal):
  def __init__(self, filename, openmode):
    self.filename = filename
    self.openmode = openmode
    self.buf = None

  def __repr__(self):
    return f"<Файл {self.filename}>"

  def openFile(self):
    self.buf = open(self.filename.VALUE, self.openmode)

  def closeFile(self):
    self.buf.close()

  def readFile(self):
    return StringVal(self.buf.read())

  def writeFile(self, text):
    self.buf.write(text)

