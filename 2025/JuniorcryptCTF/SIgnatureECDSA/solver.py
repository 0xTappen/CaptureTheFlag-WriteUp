# Solver untuk tantangan ECDSA dengan kerentanan k-reuse

# 1. Definisikan parameter kurva dan nilai-nilai publik dari output
# ===================================================================

# Order dari kurva SECP256k1
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Nilai publik dari dua tanda tangan yang dihasilkan
r = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
s1 = 0xdf88df0b8b3cc27eedddc4f3a1ecfb55e63c94739e003c1a56397ba261ba381d
h1 = 0x315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3
s2 = 0x2291d4ab9e8b0c412d74fb4918f57580b5165f8732fd278e65c802ff8be86f61
h2 = 0xa6ab91893bbd50903679eb6f0d5364dba7ec12cd3ccc6b06dfb04c044e43d300

# 2. Terapkan rumus untuk menemukan kunci privat (d)
# ===================================================================
# Rumus: d = (s2*h1 - s1*h2) * modInverse(r*(s1-s2)) mod n

# Hitung bagian pembilang (numerator)
numerator = (s2 * h1 - s1 * h2) % n

# Hitung bagian penyebut (denominator)
denominator = (r * (s1 - s2)) % n

# Lakukan invers modular pada penyebut untuk menyelesaikan "pembagian"
# pow(x, -1, n) adalah cara Python untuk menghitung invers modular
inv_denominator = pow(denominator, -1, n)

# Kalikan pembilang dengan invers penyebut untuk mendapatkan d
d = (numerator * inv_denominator) % n

# 3. Tampilkan kunci privat yang berhasil ditemukan
# ===================================================================
print(f"🔑 Kunci Privat (d) berhasil ditemukan!")
print(f"   - Heksadesimal: {hex(d)}")

# (Opsional) Banyak tantangan CTF menyembunyikan flag dalam kunci privat.
# Coba konversi kunci dari heksadesimal ke teks ASCII.
try:
    d_hex_string = hex(d)[2:] # Hapus prefix '0x'
    ascii_key = bytes.fromhex(d_hex_string).decode('utf-8')
    print(f"   - Teks ASCII  : {ascii_key}")
except:
    print("   - Tidak dapat dikonversi ke ASCII.")
