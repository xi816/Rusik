# Value types for Rusik programming language
from enum import Enum, auto

class ValueType(Enum):
  Null = auto()
  Number = auto()
  Boolean = auto()

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

