import socket
import sys
import time

# --- Konfigurasi ---
HOST = 'ctf.mf.grsu.by'
PORT = 9042
ENCODING = 'utf-8' # Encoding yang benar adalah UTF-8

# --- Konstanta dari script server ---
B = 2**51 - 1

def read_until_prompt(s, prompt='> '):
    """Membaca data dari socket sampai menemukan prompt."""
    buffer = b""
    while not buffer.decode(ENCODING, errors='ignore').endswith(prompt):
        try:
            buffer += s.recv(1)
        except socket.timeout:
            break
    return buffer.decode(ENCODING, errors='ignore')

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0) # Set timeout untuk mencegah skrip hang
        s.connect((HOST, PORT))
        print(f"[*] Berhasil terhubung ke {HOST}:{PORT}")

        # 1. Baca semua pesan selamat datang sampai prompt pertama '>'
        print("[*] Membersihkan buffer, membaca pesan selamat datang...")
        read_until_prompt(s)

        # 2. Kirim perintah '1' untuk mendapatkan angka
        print("[*] Meminta angka pertama (M)...")
        s.sendall(b'1\n')

        # 3. Baca respons yang berisi angka
        response_data = read_until_prompt(s)
        
        # 4. Parsing respons untuk mendapatkan nilai M
        try:
            # Cari baris yang mengandung "Следующее число:"
            line_with_number = ""
            for line in response_data.splitlines():
                if "Следующее число:" in line:
                    line_with_number = line
                    break
            
            if not line_with_number:
                raise ValueError("Baris dengan angka tidak ditemukan.")
            
            m_str = line_with_number.split(':')[1].strip()
            M = int(m_str)
            print(f"[*] Angka pertama (M) diterima: {M}")

        except (IndexError, ValueError) as e:
            print(f"[!] Gagal mem-parsing M dari respons. Error: {e}")
            print(f"--- RAW RESPONSE ---\n{response_data}\n--------------------")
            sys.exit(1)
        
        # 5. Hitung angka berikutnya
        x1_predicted = B % M
        print(f"[*] Angka selanjutnya (X1) dihitung: {x1_predicted}")

        # 6. Kirim tebakan
        print("[*] Mengirim tebakan...")
        s.sendall(b'2\n')

        # Baca prompt tebakan "Ваше число: "
        read_until_prompt(s, prompt=': ')
        
        # Kirim angka yang sudah dihitung
        s.sendall(f"{x1_predicted}\n".encode())

        # 7. Terima dan tampilkan flag
        print("\n[+] Berhasil! Menunggu flag dari server...")
        # Beri sedikit waktu untuk server merespons
        time.sleep(0.5)
        final_response = s.recv(2048).decode(ENCODING, errors='ignore')
        print("="*40)
        print(f"RESPONS FINAL DARI SERVER:\n\n{final_response}")
        print("="*40)

except Exception as e:
    print(f"[!] Terjadi error: {e}")
