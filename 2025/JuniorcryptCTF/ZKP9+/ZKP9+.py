#!/usr/bin/env python3
import socket
import re
from random import randint
import time # <-- TAMBAHKAN INI

# --- Konfigurasi ---
HOST = 'ctf.mf.grsu.by'
PORT = 9049

def solve_dlog(g, y, p):
    """Mencari x dengan brute force."""
    for x in range(1, p):
        if pow(g, x, p) == y:
            return x
    return None

def main():
    """Menghubungkan ke server, memecahkan x, dan menyelesaikan ronde ZKP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[*] Terhubung ke {HOST}:{PORT}")

        def read_until(prompt):
            buffer = b""
            while prompt.encode() not in buffer:
                buffer += s.recv(1024)
            return buffer.decode('utf-8', errors='ignore')

        initial_output = read_until("Select r and send C = g^r mod p: ")
        print(initial_output)

        p_match = re.search(r'p=(\d+)', initial_output)
        g_match = re.search(r'g=(\d+)', initial_output)
        y_match = re.search(r'y=(\d+)', initial_output)

        p = int(p_match.group(1))
        g = int(g_match.group(1))
        y = int(y_match.group(1))
        print(f"[*] Parameter di-parsing: p={p}, g={g}, y={y}")

        x = solve_dlog(g, y, p)
        if x is None:
            print("[!] Tidak dapat menemukan rahasia x.")
            return
        print(f"[*] Rahasia ditemukan: x = {x}")

        num_rounds = 3
        for i in range(num_rounds):
            print(f"\n--- Round {i + 1} ---")
            
            r = randint(1, p - 2)
            C = pow(g, r, p)
            s.sendall(f"{C}\n".encode())
            print(f"[*] Prover -> Verifier: Mengirim C = {C}")

            challenge_output = read_until("Send s = r + e*x mod (p-1): ")
            print(challenge_output)
            e_match = re.search(r'Challenge e = (\d+)', challenge_output)
            if not e_match:
                break
            e = int(e_match.group(1))
            print(f"[*] Verifier -> Prover: Menerima e = {e}")
            
            s_val = (r + e * x) % (p - 1)
            s.sendall(f"{s_val}\n".encode())
            print(f"[*] Prover -> Verifier: Mengirim s = {s_val}")

        print("\n[*] Semua ronde berhasil. Menunggu flag...")
        
        # PERBAIKAN: Beri jeda 0.5 detik agar server sempat mengirim flag
        time.sleep(0.5) # <-- TAMBAHKAN INI

        final_output = s.recv(4096).decode('utf-8', errors='ignore')
        print("\n" + "#" * 50)
        print("###    RESPONS FINAL SERVER (FLAG)     ###")
        print("#" * 50)
        print(final_output)

    except Exception as e:
        print(f"\n[!] Terjadi error: {e}")
    finally:
        s.close()
        print("\n[*] Koneksi ditutup.")

if __name__ == "__main__":
    main()
