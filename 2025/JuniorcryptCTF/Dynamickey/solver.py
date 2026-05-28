expected = b'\x74\xab\x9a\x62\x95\x6b\x9f\x81\x6b\x87\xbd\x99\x81\xb9\x93\x98\xb5\x80\x8d\xa9\x5b\x4a\xb1\x8e\xac\xa7\x9c\xb9\xa9\xa4\xa8\xb1\x39\xdc\xd7\x26\xd5\xea\xee\xdb\xc8\xc7\xca\xf5\x39\xc8\xc0\xcb'

for key in range(128):
    try:
        decrypted = ''.join(
            chr((b ^ (i * 2)) - key)
            for i, b in enumerate(expected)
        )
        if all(32 <= ord(c) <= 126 for c in decrypted):  # Check printable ASCII
            print(f"[+] Key: {key} | Flag: grodno{{{decrypted}}}")
    except:
        continue
