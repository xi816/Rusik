# Value types for Rusik programming language
from enum import Enum, auto

class ValueType(Enum):
  Null = auto()
  Number = auto()
  Boolean = auto()
  Obj = auto()

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

