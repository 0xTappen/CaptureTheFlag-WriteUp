import numpy as np

def decrypt_hill_cipher():
    """
    Fungsi untuk mendekripsi pesan yang dienkripsi menggunakan Hill Cipher
    berdasarkan matriks kunci A dan data terenkripsi yang diberikan.
    """
    # Matriks kunci A dan data terenkripsi dari soal
    A_list = [[193, 243, 218], [240, 186, 172], [62, 118, 70]]
    encrypted_list = [
        [76, 252, 109], [67, 73, 222], [227, 49, 104], [199, 230, 167], 
        [118, 74, 4], [253, 70, 40], [78, 123, 230], [16, 240, 85], 
        [62, 184, 34], [87, 50, 233], [224, 188, 40]
    ]
    modulus = 257

    # Konversi list ke numpy array untuk operasi matriks
    A = np.array(A_list)
    encrypted_matrix = np.array(encrypted_list)

    # Langkah 1: Hitung invers modular dari matriks kunci A
    # Ini adalah kunci untuk dekripsi
    
    # Hitung determinan
    det = int(round(np.linalg.det(A)))
    
    # Hitung invers modular dari determinan
    # pow(x, -1, m) adalah cara Python untuk menghitung invers modular
    det_inv = pow(det, -1, modulus)
    
    # Hitung matriks adjoin
    adjugate = np.round(det * np.linalg.inv(A)).astype(int)
    
    # Hitung matriks invers modular (kunci dekripsi)
    A_inv = (det_inv * adjugate) % modulus

    # Langkah 2: Dekripsi pesan
    # Rumus dekripsi: P = C * (A_inv)^T mod m
    decrypted_matrix = (encrypted_matrix @ A_inv.T) % modulus

    # Langkah 3: Ubah matriks hasil dekripsi kembali ke bytes
    decrypted_bytes = decrypted_matrix.flatten().tobytes()

    # Langkah 4: Hapus padding (byte null '\x00' di akhir)
    flag = decrypted_bytes.rstrip(b'\x00')

    # Tampilkan flag yang berhasil didekripsi
    print(f"✅ Flag yang berhasil didekripsi: {flag.decode()}")

if __name__ == "__main__":
    decrypt_hill_cipher()
