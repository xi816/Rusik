# Error messages colorer for Rusik programming language
from colorama import Fore
from normal_print import print, println

def i_error(msg: str) -> None:
  println(f"{Fore.RED}ERROR{Fore.RESET}: {msg}")
  exit(1)

def c_error(cond: bool, msg: str) -> None:
  if (cond): i_error(msg)

