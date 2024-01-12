base_num = "".join(map(chr, list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))))

def to_base(num: int, base: int):
  if (base == 1):
    return "1"*num
  res = ""
  while (num > 0):
    res += str(base_num[num % base])
    num //= base
  return res[::-1]

