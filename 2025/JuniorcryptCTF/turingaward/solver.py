import string
from itertools import product

# Data XOR dari chall
enc = [0x6e, 0x49, 0x60, 0x09, 0x78, 0x75, 0x01, 0x3f, 0x58, 0x68, 0x4f]
key = b"MYSECRETKEY"
targets = [enc[i] ^ key[i] for i in range(11)]

# Fungsi verifikasi
def check_flag(flag):
    if not flag.startswith("grodno{") or not flag.endswith("}") or len(flag) != 30:
        return False
    middle = flag[7:-1]
    for i in range(11):
        if (ord(middle[i*2]) ^ ord(middle[i*2+1])) != (enc[i] ^ key[i]):
            return False
    return True

# Hanya huruf besar/kecil dan '-'
valid_chars = string.ascii_letters + '-'

# Semua pasangan (c1, c2) yang valid untuk tiap target
possible_pairs = []
for t in targets:
    valid = []
    for a in valid_chars:
        for b in valid_chars:
            if ord(a) ^ ord(b) == t:
                valid.append(a + b)
    possible_pairs.append(valid)

# Gabungkan semua kemungkinan
for combo in product(*possible_pairs):
    middle = ''.join(combo)
    if middle.count('--') == 1 and middle.count('-') == 3:
        flag = f"grodno{{{middle}}}"
        if check_flag(flag):
            print(f"[✓] Flag valid: {flag}")
            break
