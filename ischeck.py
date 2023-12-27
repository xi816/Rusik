# `Is` checking from a Rusik programming language code
def isalpha(c: str) -> bool:
  return (c.upper() != c.lower())

def isdigit(c: str) -> bool:
  return (c in "0123456789")

def iswhite(c: str) -> bool:
  return (c in " \n\0")

