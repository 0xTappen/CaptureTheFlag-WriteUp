import socket
import re
import time

# -- KONFIGURASI --
HOST = "ctf.mf.grsu.by"
PORT = 9044
NICKELS_START = 2000
NICKELS_TARGET = 20000
PROBE_LIMIT = 1000 # Batas atas untuk mencari nilai taruhan ajaib

# -- FUNGSI BANTUAN --

def recv_until_prompt(s, prompt="Your bet in game (0 - exit):"):
    """Membaca data dari socket sampai prompt tertentu terlihat."""
    data = ""
    # Set timeout sementara untuk pembacaan awal agar tidak menunggu selamanya
    s.settimeout(2.0)
    while True:
        try:
            chunk = s.recv(4096).decode('utf-8', errors='ignore')
            if not chunk:
                break
            data += chunk
            if prompt in data:
                break
        except socket.timeout:
            # Timeout kemungkinan berarti kita sudah menerima semua data yang tersedia
            break
    # Kembalikan ke timeout yang lebih lama untuk operasi normal
    s.settimeout(5.0)
    return data

def get_bank(data):
    """Mengekstrak jumlah uang dari output server."""
    match = re.search(r"Ваш банк / Your bank: (\d+)", data)
    if match:
        return int(match.group(1))
    return None

def get_reels(data):
    """Mengekstrak hasil putaran (reels) dari output server."""
    match = re.search(r"\[(\d+),\s*(\d+),\s*(\d+)\]", data)
    if match:
        return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
    return None

def calculate_win_nickels(reels, bet):
    """
    Menghitung total kemenangan dalam nikel berdasarkan hasil putaran dan taruhan.
    0: horseshoe, 1: star, 2: spade, 3: diamond, 4: hearts, 5: bell
    """
    payout_multiplier = 0
    # 3 Liberty Bells -> 50 sen (10 nikel)
    if reels.count(5) == 3: payout_multiplier = 10
    # 3 Hearts -> 40 sen (8 nikel)
    elif reels.count(4) == 3: payout_multiplier = 8
    # 3 Diamonds -> 30 sen (6 nikel)
    elif reels.count(3) == 3: payout_multiplier = 6
    # 3 Spades -> 20 sen (4 nikel)
    elif reels.count(2) == 3: payout_multiplier = 4
    # 2 Horseshoes + 1 Star -> 10 sen (2 nikel)
    elif reels.count(0) == 2 and reels.count(1) == 1: payout_multiplier = 2
    # 2 Horseshoes -> 5 sen (1 nikel - hanya mengembalikan taruhan)
    elif reels.count(0) == 2: payout_multiplier = 1
    
    return payout_multiplier * bet

# --- SOLVER UTAMA ---

magic_bet_value = -1
best_multiplier = 0

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        initial_response = recv_until_prompt(s)
        current_bank = get_bank(initial_response)
        print(f"[*] Terhubung ke server. Saldo awal: {current_bank} nikel.")

        # --- FASE 1: MENCARI NILAI TARUHAN AJAIB ---
        print(f"[*] Memulai Fase 1: Mencari taruhan ajaib hingga {PROBE_LIMIT} nikel...")
        
        # Simpan saldo awal sebelum probing
        bank_before_probing = current_bank

        for bet_probe in range(1, PROBE_LIMIT + 1):
            if current_bank < bet_probe:
                print(f"[!] Saldo tidak cukup untuk melanjutkan pencarian pada taruhan {bet_probe}. Berhenti mencari.")
                break

            # Kirim taruhan untuk diuji
            s.sendall(f"{bet_probe}\n".encode())
            response = recv_until_prompt(s)
            
            reels = get_reels(response)
            new_bank = get_bank(response)

            if not reels or new_bank is None:
                print("[!] Gagal mem-parsing respons server. Keluar.")
                print(response)
                exit()
            
            # Hitung pengganda kemenangan dari hasil putaran ini
            # (winnings / bet)
            winnings = new_bank - (current_bank - bet_probe)
            multiplier = winnings / bet_probe if bet_probe > 0 else 0

            print(f"    -> Mencoba bet={bet_probe: <4} | Reels: {str(reels): <14} | Pengganda: {multiplier:.1f}")

            # Jika kita menemukan pengganda yang lebih baik, simpan nilai taruhannya
            if multiplier > best_multiplier:
                best_multiplier = multiplier
                magic_bet_value = bet_probe
                print(f"    [+] Ditemukan kandidat taruhan baru! Bet={magic_bet_value}, Pengganda={best_multiplier:.1f}")

            # Jackpot ditemukan! (3 Lonceng = pengganda 10x)
            if multiplier >= 10:
                print(f"\n[!!!] JACKPOT DITEMUKAN! Nilai taruhan ajaib adalah: {magic_bet_value}")
                break
            
            current_bank = new_bank

        if magic_bet_value == -1 or best_multiplier <= 1:
            print("\n[-] Fase 1 gagal: Tidak ada taruhan yang menguntungkan ditemukan dalam batas pencarian.")
            exit()
            
        print(f"\n[*] Fase 1 Selesai. Taruhan terbaik ditemukan: {magic_bet_value} (Pengganda: {best_multiplier:.1f})")
        print(f"[*] Saldo saat ini: {current_bank} nikel.")

        # --- FASE 2: EKSPLOITASI ---
        print("\n[*] Memulai Fase 2: Eksploitasi.")
        
        while current_bank < NICKELS_TARGET:
            # Tentukan taruhan untuk putaran ini
            # Jika kita punya cukup uang, gunakan taruhan ajaib. Jika tidak, bertaruh 1.
            bet_amount = magic_bet_value if current_bank >= magic_bet_value else 1
            
            print(f"[*] Saldo: {current_bank: <5} | Bertaruh: {bet_amount}")
            s.sendall(f"{bet_amount}\n".encode())
            response = recv_until_prompt(s)

            new_bank = get_bank(response)
            if new_bank is None:
                print("[!] Gagal mendapatkan saldo baru. Menampilkan respons terakhir:")
                print(response)
                break
            
            # Jika saldo menjadi 0, kita kalah
            if new_bank == 0 and current_bank > 0:
                 print("[-] Kita kalah taruhan dan bangkrut!")
                 current_bank = 0
                 break

            current_bank = new_bank

        # --- HASIL AKHIR ---
        if current_bank >= NICKELS_TARGET:
            print(f"\n[+] BERHASIL! Target {NICKELS_TARGET} nikel tercapai!")
            print(f"[+] Saldo akhir: {current_bank} nikel.")
            print("\n[+] Mencari flag dalam respons terakhir dari server...")
            print("="*20)
            print(response)
            # Coba baca sekali lagi untuk memastikan tidak ada pesan tambahan
            try:
                final_message = s.recv(4096).decode('utf-8', errors='ignore')
                print(final_message)
            except socket.timeout:
                pass
            print("="*20)
        else:
            print(f"\n[-] GAGAL. Tidak mencapai target. Saldo akhir: {current_bank}")

except Exception as e:
    print(f"[!] Terjadi kesalahan: {e}")
