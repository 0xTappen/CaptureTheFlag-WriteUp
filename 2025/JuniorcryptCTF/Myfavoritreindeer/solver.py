import base64
import reedsolo
import sys
import os

# Menonaktifkan output error dari reedsolo untuk menjaga kebersihan output
# os.environ['REEDSOLO_VERBOSE'] = '0'

# Data terenkode Base64 yang diberikan
b64_data = "TXkgZmF2b3JpdGUgcmVpbmQE/v9NMC7EPgT+fVKtYX1uAP1zYW1iaQT+ZXNpjl6WWlMZ+F06cKpDoSF7cIQ2Ug9OxlQ2VQ58otSA6jm+xjhwUFcr02pIxVfyY85y84/QFG8T94M="

# Dekode data dari Base64
full_data = base64.b64decode(b64_data)

# Kita akan menguji dua kemungkinan: payload penuh, dan payload setelah header dipisah
payloads_to_test = {
    "101-byte (payload penuh)": full_data,
    "85-byte (setelah header dipisah)": full_data[16:]
}

solution_found = False
for payload_desc, payload in payloads_to_test.items():
    if solution_found:
        break
    print(f"\n{'='*50}\n[*] Menguji skenario: {payload_desc}\n{'='*50}")
    payload_len = len(payload)
    
    # Loop untuk n1. nsym tidak bisa lebih besar dari panjang data.
    for n1 in range(1, payload_len):
        if solution_found:
            break
        # Tampilkan progres tanpa membuat output berantakan
        sys.stdout.write(f"\r    -> Mencoba n1 = {n1}...")
        sys.stdout.flush()
        
        try:
            rs1 = reedsolo.RSCodec(n1)
            decoded1, _, _ = rs1.decode(payload)

            # Jika dekode tahap 1 berhasil, coba tahap 2
            decoded1_len = len(decoded1)
            # Loop untuk n0
            for n0 in range(1, decoded1_len):
                try:
                    rs0 = reedsolo.RSCodec(n0)
                    decoded0, _, _ = rs0.decode(decoded1)

                    # Jika dekode tahap 2 berhasil, bersihkan dan periksa hasilnya
                    cleaned = decoded0.rstrip(b'\x00')
                    if not cleaned: continue

                    text = cleaned.decode('utf-8')

                    # Solusi yang paling mungkin mengandung huruf dan mungkin pemisah
                    if len(text) > 5 and all(31 < ord(c) < 127 for c in text):
                        print(f"\n\n[!!!] KEMUNGKINAN SOLUSI DITEMUKAN [!!!]")
                        print(f"    Skenario     : {payload_desc}")
                        print(f"    Parameter    : n1={n1}, n0={n0}")
                        print(f"    Teks         : '{text}'")
                        final_text = text.replace(' ', ';').replace(':', ';')
                        print(f"    Jawaban Akhir: grodno{{{final_text}}}")
                        print(f"{'='*50}\n")
                        solution_found = True
                        break # Hentikan loop n0

                except (reedsolo.ReedSolomonError, UnicodeDecodeError, ValueError):
                    continue # Gagal, lanjut ke n0 berikutnya
        
        except reedsolo.ReedSolomonError:
            continue # Gagal, lanjut ke n1 berikutnya

if not solution_found:
    print("\n\nPencarian selesai. Tidak ada solusi yang ditemukan.")
