import base64
from tqdm import tqdm

def lfsr(state, mask):
    feedback = state & 1
    state >>= 1
    if feedback:
        state ^= mask
    return state, feedback

def generate_keystream(state, mask, length):
    keystream = []
    for _ in range(length * 8):  # 8 bits per byte
        state, bit = lfsr(state, mask)
        keystream.append(bit)
    # Convert bits to bytes
    keystream_bytes = bytearray()
    for i in range(0, len(keystream), 8):
        byte = 0
        for j in range(8):
            byte |= (keystream[i + j] << j)
        keystream_bytes.append(byte)
    return keystream_bytes

# Decode ciphertext
b64_Enc_XOR_text = "rKcUtOpHHO6ZXNzB3IwyLXPzQX9pkAYLNfrolB191POUEJoz3xQANLSTm1inSV3jh88w15d5jcaQttzpNyewT7mPufbvtVf+xMTS7Zeeai4u6/TyeFHGLPH9cHnCNg=="
ciphertext = base64.b64decode(b64_Enc_XOR_text)

# Brute-force LFSR params
for init_state in tqdm(range(1, 0x10000)):
    for mask in range(1, 0x10000):
        ks = generate_keystream(init_state, mask, len(ciphertext))
        decrypted = bytes([c ^ k for c, k in zip(ciphertext, ks)])
        if b"Tenesys{" in decrypted or b"CTF{" in decrypted or b"flag{" in decrypted:
            print(f"[*] Found! initial_state=0x{init_state:04X}, mask=0x{mask:04X}")
            print("Plaintext:", decrypted.decode(errors='ignore'))
            exit()
