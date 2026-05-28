import base64

def lfsr(state, mask):
    """
    Generates a new bit and updates the LFSR state.
    """
    bit = (state & 1)
    state = state >> 1
    if bit:
        state ^= mask
    return state, bit

# Known parameters
initial_state = 0b1100101011110001
mask          = 0b1011010000000001

# The intercepted message, Base64 encoded
b64_ciphertext = """vOALn6jMkGzJb28s6aPrn1AAU1hkczys29kgWML9F7Lch3XpmfyHAV0K+4s4kHH1
cQNfwqalv3eLWvHTXFPl7JxCVz1VtFWeaRcHvaWV1jVvHzORQULYpeAvL7P9Cms18+49
kc7gRwxuOoTjqlu0xj2Wgo40Loybw1LkksbsPNyffSOcoWOUWx8sb/j4czUdF78XFWRu
WrUIC+0RZ1CQSzq/Sz+9zISrAK5+kJurxZoJ43dGc26Maz8D0GABBidUAAMIwQrnNZMb
AZOLvZUpeCXMp68YqhH3R2XBx+mE5exdYceEJuxynGfsg3DvBXYnxF6zq+9upqM/LG6f
VxNLPrhcn55B6fULln13cHE9RM+DxYCbZncYTJWDT5/9HK170eMBS8UWtP227RKNH+w1
B4g4EiZLcnhmw88y6LXKawODpekHlTzkgwKutyVe+bg9dqsv9qflhhIjVHZzGcgNAwZk
ALaBb+iBYg+jRX21M8lOtN3JeVeWxezgWJinH1LcxQM8k1R7c+HIXGUwSzwlnJEghoxb
JK40m4YBo3mBnbUKFo0ZAZXGTao8I5OcZvyAiF0Q4RgO31Atrvh1gadot4Tg/6LIGUe3
rt7wyyUZuMldqlNn+Ef2DdNaVyaHMzSptXDn9p9yf61v46Q6TM3BI7PQf6ZXV4EsWFYD
lLydhAwhwty+A251+r4BeMUrUdjd"""

# Decode the Base64 ciphertext
ciphertext = base64.b64decode(b64_ciphertext)

current_state = initial_state
decrypted_message = bytearray()

# Decrypt the message byte by byte
for i in range(len(ciphertext)):
    keystream_byte = 0
    # Generate 8 bits to form one byte of the keystream
    for _ in range(8):
        current_state, bit = lfsr(current_state, mask)
        # Shift the byte left and add the new bit to the LSB position.
        # This makes the first generated bit the MSB of the final byte.
        keystream_byte = (keystream_byte << 1) | bit # <--- THIS LINE IS CHANGED

    # XOR the ciphertext byte with the keystream byte
    decrypted_byte = ciphertext[i] ^ keystream_byte
    decrypted_message.append(decrypted_byte)

# Decode the result to reveal the flag
try:
    flag = decrypted_message.decode('utf-8')
    print("Decryption successful! ✅")
    print(f"Flag: {flag}")
except UnicodeDecodeError:
    print("Decryption failed again. The result is still not valid UTF-8. 🤔")
