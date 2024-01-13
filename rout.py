base_num = "".join(map(chr, list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))))

def forreplace(s: str, fr: str, to: str):
  for a,b in zip(fr, to):
    s = s.replace(a, b)
  return s

def to_base(num: int, base: int):
  if (base == 1):
    return "1"*num
  res = ""
  while (num > 0):
    res += str(base_num[num % base])
    num //= base
  return res[::-1]

