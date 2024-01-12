from functools import reduce

from RSError import i_error, c_error
from RSValues import NullVal, NumberVal, FloatVal, BooleanVal, StringVal, FileObjectVal, ArrayVal
from rout import base_num, to_base

def peek(fname: str, args: list, types: list) -> int:
  for i, j in enumerate(args):
    c_error(type(j) != types[i], f"В аргументах функции `{fname}` на позиции {i} ожидался тип {types[i]}, но дано {type(j)}")
  return 0

def toStrFn(args: list, scope):
  c_error(len(args) == 0, f"Функция `строка` ожидает больше 0 аргументов, но дано 0")
  res = StringVal("")
  for i in args:
    res.VALUE += str(i.VALUE)
  return res

def rangeFn(args: list, scope):
  c_error(len(args) not in [2, 3], f"Функция `отдо` ожидает 2 или 3 аргумента, но дано {len(args)}")
  if (len(args) == 2):
    res = ArrayVal(list(range(args[0].VALUE, args[1].VALUE)))
  elif (len(args) == 3):
    res = ArrayVal(list(range(args[0].VALUE, args[1].VALUE, args[2].VALUE)))
  return res

def sumFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `сумма` ожидает 1 аргумент, но дано {len(args)}")
  peek("сумма", args, [ArrayVal])
  return NumberVal(sum(map(lambda a: a.VALUE, args[0].VALUE)))

def lenFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `длина` ожидает 1 аргумент, но дано {len(args)}")
  return NumberVal(len(args[0].VALUE))

def toIntFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `число` ожидает 1 аргумент, но дано {len(args)}")
  c_error(not args[0].VALUE.isdigit(), f"Функция `число` не может перевести `{repr(args[0].VALUE)[1:-1]}` в число")
  return NumberVal(round(int(args[0].VALUE)))

def toFloatFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `дробное` ожидает 1 аргумент, но дано {len(args)}")
  return FloatVal(float(args[0].VALUE))

def toBoolFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `булево` ожидает 1 аргумент, но дано {len(args)}")
  return BooleanVal(int(args[0].VALUE))

def charFn(args: list, scope):
  c_error(len(args) == 0, f"Функция `символ` ожидает больше 0 аргументов, но дано {len(args)}")
  peek("символ", args, [NumberVal]*len(args))
  return StringVal("".join(map(lambda x: chr(int(x.VALUE)), args)))

def inputFn(args: list, scope):
  c_error(len(args) != 0, f"Функция `ввести` ожидает 0 аргументов, но дано {len(args)}")
  return StringVal(input())

def typeofFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `тип` ожидает 1 аргумент, но дано {len(args)}")
  if (type(args[0]) == NullVal):
    return StringVal("[тип ничего]")
  elif (type(args[0]) == NumberVal):
    return StringVal("[тип число]")
  elif (type(args[0]) == FloatVal):
    return StringVal("[тип дробное]")
  elif (type(args[0]) == StringVal):
    return StringVal("[тип строка]")
  else:
    i_error("IE-UN-TYPE: Тип не опознан. Эта ошибка может появится только, если создатель языка добавит новый тип, и забудет обновить функцию `тип`")

def exitFn(args: list, scope):
  c_error(len(args) not in [0, 1], f"Функция `выход` ожидает 0 или 1 аргумент, но дано {len(args)}")
  if (len(args) == 0):
    return ("CallExit", 0)
  else:
    return ("CallExit", args[0])

def printFn(args: list, scope):
  if (not args):
    return NullVal()
  for i in args:
    if (type(i) == StringVal):
      print(i.VALUE, end="")
    else:
      i_error("Функция `вывести` ожидает на вход строку")
  return NullVal()


def openFileFn(args: list, scope):
  c_error(len(args) != 2, f"Функция `открыть` ожидает 2 аргумента, но дано {len(args)}")
  peek("открыть", args, [StringVal, StringVal])
  args1tr = {"ч": "r", "п": "w", "д": "a"}.get(args[1].VALUE)
  openedFile = FileObjectVal(args[0], args1tr)
  openedFile.openFile()
  return openedFile

def readFileFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `прочитать` ожидает 1 аргумент, но дано {len(args)}")
  peek("прочитать", args, [FileObjectVal])
  return args[0].readFile()

def writeFileFn(args: list, scope):
  c_error(len(args) != 2, f"Функция `написать` ожидает 2 аргумента, но дано {len(args)}")
  peek("написать", args, [FileObjectVal, StringVal])
  args[0].writeFile(args[1].VALUE)
  return NullVal()

def closeFileFn(args: list, scope):
  c_error(len(args) != 1, f"Функция `закрыть` ожидает 1 аргумент, но дано {len(args)}")
  peek("закрыть", args, [FileObjectVal])
  args[0].closeFile()
  return NullVal()

def strFormatFn(args: list, scope):
  c_error(len(args) < 1, f"Функция `формат` ожидает как минимум 1 аргумент, но дано {len(args)}")
  peek("формат", [args[0]], [StringVal])
  main_str, *args = args
  main_str = main_str.VALUE
  global_str = ""
  pos = 0
  while (pos < len(main_str)):
    if (main_str[pos] == "%"):
      pos += 1
      if (main_str[pos] == "с"):
        sec_str, *args = args
        global_str += sec_str.VALUE
      elif (main_str[pos] == "ч"):
        sec_int, *args = args
        global_str += str(sec_int.VALUE)
      elif (main_str[pos] == "Ч"):
        pos += 1
        sec_buf = ""
        sec_int, *args = args
        while (main_str[pos] != ":"):
          sec_buf += main_str[pos]
          pos += 1
        global_str += str(to_base(sec_int.VALUE, int(sec_buf)))
      else:
        i_error(f"Неизвестный старт формата: {main_str[pos]}")
    else:
      global_str += main_str[pos]
    pos += 1
  return StringVal(global_str)

def numBaseFn(args: list, scope):
  c_error(len(args) != 2, f"Функция `база_числа` ожидает 2 аргумента, но дано {len(args)}")
  peek("база_числа", args, [NumberVal, NumberVal])
  return StringVal(to_base(args[0].VALUE, args[1].VALUE))

