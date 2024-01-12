# Token definition for Rusik programming language
from normal_print import print, println

from enum import Enum, auto
from dataclasses import dataclass

from ischeck import isalpha, isdigit, iswhite
from RSError import i_error, c_error

class TokenType(Enum):
  Number        = auto()
  Float         = auto()
  String        = auto()
  Ident         = auto()
  Op_Plus       = auto()
  Op_Minus      = auto()
  Op_Star       = auto()
  Op_Fslash     = auto()
  Op_Eq         = auto()
  Colon         = auto()
  Comma         = auto()
  Dot           = auto()
  Semicolon     = auto()
  Paren_0       = auto()
  Paren_1       = auto()
  Bracket_0     = auto()
  Bracket_1     = auto()
  Brace_0       = auto()
  Brace_1       = auto()
  Op_Binary     = auto()
  Kw_Let        = auto()
  Kw_Const      = auto()
  Kw_If         = auto()
  Kw_Else       = auto()
  Kw_While      = auto()
  Kw_Gen        = auto()
  Kw_Fn         = auto()
  EOF           = auto()

@dataclass
class Token:
  TYPE: TokenType
  VALUE: str
  POS: tuple
  FILENAME: str = "[ввод]"

KEYWORDS: dict = {
  "будет": TokenType.Kw_Let,
  "константа": TokenType.Kw_Const,
  "если": TokenType.Kw_If,
  "иначе": TokenType.Kw_Else,
  "пока": TokenType.Kw_While,
  "генератор": TokenType.Kw_Gen,
  "функция": TokenType.Kw_Fn,
}
RUS_CAPITAL = "".join(map(chr, list(range(1040, 1046))+[1025]+list(range(1046, 1072))))

def to_token(TYPE: TokenType, VALUE: str, ROW: int, COL: int) -> Token:
  return Token(TYPE, VALUE, (ROW, COL))

def tokenize(src: str, lexer_flags: list) -> list:
  src += "\0"
  pos = 0
  c_row = 1
  c_col = 1

  tokens = []
  buf = ""

  while (src[pos] != "\0"):
    if (src[pos] == "\n"):
      c_row += 1
      c_col = 1
      pos += 1
    elif (src[pos] == "("):
      tokens.append(to_token(TokenType.Paren_0, "(", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == ")"):
      tokens.append(to_token(TokenType.Paren_1, ")", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "["):
      tokens.append(to_token(TokenType.Bracket_0, "[", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "]"):
      tokens.append(to_token(TokenType.Bracket_1, "]", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "{"):
      tokens.append(to_token(TokenType.Brace_0, "{", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "}"):
      tokens.append(to_token(TokenType.Brace_1, "}", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "+"):
      temp_token = TokenType.Op_Binary, "+", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "++", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == "-"):
      temp_token = TokenType.Op_Binary, "-", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "--", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == "*"):
      temp_token = TokenType.Op_Binary, "*", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "**", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == "/"):
      if (src[pos+1] != "/"):
        tokens.append(to_token(TokenType.Op_Binary, "/", c_row, c_col))
        pos += 1
        c_col += 1
      else:
        pos += 2
        c_col += 2
        while (src[pos] not in "\0\r\n"):
          pos += 1
          c_col += 1
    elif (src[pos] == "%"):
      tokens.append(to_token(TokenType.Op_Binary, "%", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "<"):
      temp_token = TokenType.Op_Binary, "<", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "<=", c_row, c_col
      elif (src[pos+1] == "<"):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "<<", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == ">"):
      temp_token = TokenType.Op_Binary, ">", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, ">=", c_row, c_col
      elif (src[pos+1] == ">"):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, ">>", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == "!"):
      temp_token = TokenType.Op_Binary, "!", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "!=", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == "="):
      temp_token = TokenType.Op_Eq, "=", c_row, c_col
      if (src[pos+1] == "="):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "==", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    elif (src[pos] == ";"):
      tokens.append(to_token(TokenType.Semicolon, ";", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == ":"):
      tokens.append(to_token(TokenType.Colon, ":", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == ","):
      tokens.append(to_token(TokenType.Comma, ",", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "."):
      tokens.append(to_token(TokenType.Dot, ".", c_row, c_col))
      pos += 1
      c_col += 1
    elif (src[pos] == "~"):
      temp_token = TokenType.Op_Binary, "~", c_row, c_col
      if (src[pos+1] == "~"):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "~~", c_row, c_col
      elif (src[pos+1] == ">"):
        pos += 1
        c_col += 1
        temp_token = TokenType.Op_Binary, "~>", c_row, c_col
      tokens.append(to_token(*temp_token))
      pos += 1
      c_col += 1
    else:
      if (isdigit(src[pos])):
        while (src[pos] not in "\0\n" and (isdigit(src[pos]) or src[pos] in ".")):
          buf += src[pos]
          pos += 1
          c_col += 1
        if (buf.count(".") == 0):
          tokens.append(to_token(TokenType.Number, buf, c_row, c_col))
        elif (buf.count(".") == 1):
          tokens.append(to_token(TokenType.Float, buf, c_row, c_col))
        buf = ""
      elif (src[pos] == "\""):
        pos += 1
        c_col += 1
        while (src[pos] != "\""):
          if (src[pos] == "^"):
            pos += 1
            c_col += 1
            if (src[pos] == "^"):
              buf += "^"
            elif (src[pos] == "0"):
              buf += "\0"
            elif (src[pos] in RUS_CAPITAL):
              buf += chr(RUS_CAPITAL.index(src[pos])+1)
            elif (src[pos] in "["):
              buf += chr(27)
          else:
            buf += src[pos]
          pos += 1
          c_col += 1
        tokens.append(to_token(TokenType.String, buf, c_row, c_col))
        pos += 1
        c_col += 1
        buf = ""
      elif (isalpha(src[pos])):
        print()
        while (src[pos] not in "\0\n" and ((isalpha(src[pos])) or (src[pos] in "_0123456789") or (src[pos] == "-") * int("var-decl-dash" in lexer_flags))):
          buf += src[pos]
          pos += 1
          c_col += 1
        if (KEYWORDS.get(buf) == None):
          tokens.append(to_token(TokenType.Ident, buf, c_row, c_col))
        else:
          tokens.append(to_token(KEYWORDS[buf], buf, c_row, c_col))
        buf = ""
      elif (iswhite(src[pos])):
        pos += 1
        c_col += 1
      elif (src[pos] == "\t"):
        i_error(f"{c_row}:{c_col}: Запрещено использовать табы (символ 9) вместо пробелов (символ 32). Если вы ходите сделать хорошую читабельность кода, используйте пробелы")
      else:
        i_error(f"{c_row}:{c_col}: Неизвестный символ {ord(src[pos])} -> `{src[pos]}`")
        exit(1)

  tokens.append(to_token(TokenType.EOF, "EndOfFile", c_row, c_col))
  return tokens

