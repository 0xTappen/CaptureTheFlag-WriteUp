import re

def parse_data(filename="data.txt"):
    """
    Membaca dan mem-parsing file data.txt untuk mendapatkan n, e, dan tanda tangan yang bocor.
    
    Args:
        filename (str): Nama file yang akan di-parsing.

    Returns:
        tuple: Berisi (n, e, leaked_signs_dict).
    """
    leaked_signs = {}
    n, e = None, None
    
    # Pola regex untuk mengekstrak pesan (bilangan prima) dan tanda tangannya
    # Sign(<message>) = <signature>
    pattern = re.compile(r"Sign\((\d+)\)\s*=\s*(\d+)")

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('n ='):
                    n = int(line.split('=')[1].strip())
                elif line.startswith('e ='):
                    e = int(line.split('=')[1].strip())
                else:
                    match = pattern.match(line)
                    if match:
                        message = int(match.group(1))
                        signature = int(match.group(2))
                        leaked_signs[message] = signature
    except FileNotFoundError:
        print(f"Error: File '{filename}' tidak ditemukan. Pastikan file berada di direktori yang sama.")
        exit()
        
    if n is None or e is None or not leaked_signs:
        print(f"Error: Gagal mem-parsing data dari '{filename}'. Pastikan formatnya benar.")
        exit()

    return n, e, leaked_signs


def solve():
    """
    Menyelesaikan tantangan dengan memfaktorkan dream_sum dan mengalikan tanda tangan.
    """
    # 1. Ambil semua data yang diperlukan
    n, e, leaked_signs = parse_data("data.txt")
    
    dream_sum = 51999884711298256279139483764500625524555947558324683565293215223860861439365869245016556808946069376210234208051889905473428307099335266198556660549084421948376963868131939751733713217547145342061587754812000747394877170239958534615968079443224197703107182407137345808430083378360519257003496366898745432749

    print("Data berhasil dimuat. Memulai faktorisasi dream_sum...")

    # 2. Faktorkan dream_sum menggunakan bilangan prima yang diketahui
    factors = []
    temp_sum = dream_sum
    known_primes = sorted(leaked_signs.keys(), reverse=True)

    for prime in known_primes:
        # Gunakan loop while untuk menangani faktor berulang
        while temp_sum % prime == 0:
            factors.append(prime)
            temp_sum //= prime
            # Hentikan jika sudah selesai
            if temp_sum == 1:
                break
        if temp_sum == 1:
            break

    # Verifikasi faktorisasi berhasil
    if temp_sum != 1:
        print("\n[!] Gagal: Tidak dapat memfaktorkan dream_sum sepenuhnya dengan prima yang ada.")
        print(f"Sisa yang tidak terfaktorisasi: {temp_sum}")
        return

    print("Faktorisasi berhasil!")
    print(f"Faktor-faktor dari dream_sum: {factors}")

    # 3. Hitung tanda tangan baru dengan mengalikan tanda tangan faktor-faktornya
    dream_sign = 1
    for factor in factors:
        sign_of_factor = leaked_signs[factor]
        dream_sign = (dream_sign * sign_of_factor) % n

    print("\nMenghitung tanda tangan untuk dream_sum...")
    print(f"Tanda tangan yang dihitung: {dream_sign}")
    
    # 4. Tampilkan flag
    print("\n" + "="*40)
    print("✨ Flag ditemukan! ✨")
    print(f"grodno{{{dream_sign}}}")
    print("="*40)


if __name__ == "__main__":
    solve()
