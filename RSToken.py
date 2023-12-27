# Token definition for Rusik programming language
from normal_print import print, println

from enum import Enum, auto
from dataclasses import dataclass

from ischeck import isalpha, isdigit, iswhite

class TokenType(Enum):
  Null          = auto()
  Number        = auto()
  Ident         = auto()
  Op_Plus       = auto()
  Op_Minus      = auto()
  Op_Star       = auto()
  Op_Fslash     = auto()
  Op_Eq         = auto()
  Semicolon     = auto()
  Paren_0       = auto()
  Paren_1       = auto()
  Op_Binary     = auto()
  Kw_Let        = auto()
  Kw_Const      = auto()
  EOF           = auto()

@dataclass
class Token:
  TYPE: TokenType
  VALUE: str

KEYWORDS: dict = {
  "будет": TokenType.Kw_Let,
  "константа": TokenType.Kw_Const,
  "ничего": TokenType.Null
}

def to_token(TYPE: TokenType, VALUE: str = "") -> Token:
  return Token(TYPE, VALUE)

def tokenize(src: str) -> list:
  src += "\0"
  pos = 0

  tokens = []
  buf = ""

  while (src[pos] != "\0"):
    if (src[pos] == "("):
      tokens.append(to_token(TokenType.Paren_0))
      pos += 1
    elif (src[pos] == ")"):
      tokens.append(to_token(TokenType.Paren_1))
      pos += 1
    elif (src[pos] == "+"):
      tokens.append(to_token(TokenType.Op_Binary, "+"))
      pos += 1
    elif (src[pos] == "-"):
      tokens.append(to_token(TokenType.Op_Binary, "-"))
      pos += 1
    elif (src[pos] == "*"):
      tokens.append(to_token(TokenType.Op_Binary, "*"))
      pos += 1
    elif (src[pos] == "/"):
      tokens.append(to_token(TokenType.Op_Binary, "/"))
      pos += 1
    elif (src[pos] == "%"):
      tokens.append(to_token(TokenType.Op_Binary, "%"))
      pos += 1
    elif (src[pos] == "="):
      tokens.append(to_token(TokenType.Op_Eq))
      pos += 1
    elif (src[pos] == ";"):
      tokens.append(to_token(TokenType.Semicolon))
      pos += 1
    else:
      if (isdigit(src[pos])):
        while (src[pos] != "\0\n" and isdigit(src[pos])):
          buf += src[pos]
          pos += 1
        tokens.append(to_token(TokenType.Number, buf))
        buf = ""
      elif (isalpha(src[pos])):
        while (src[pos] != "\0\n" and isalpha(src[pos])):
          buf += src[pos]
          pos += 1
        if (KEYWORDS.get(buf) == None):
          tokens.append(to_token(TokenType.Ident, buf))
        else:
          tokens.append(to_token(KEYWORDS[buf], buf))
        buf = ""
      elif (iswhite(src[pos])):
        pos += 1
      else:
        println(f"Unknown `{src[pos]}`")
        exit(1)

  tokens.append(to_token(TokenType.EOF, "EndOfFile"))
  return tokens

