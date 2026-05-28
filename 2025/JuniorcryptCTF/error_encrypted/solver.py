def find_error_position(bits_str):
    """
    Menghitung posisi bit yang error dalam sebuah blok Hamming(7,4).
    Input adalah string 7-bit (misal: '0101111').
    Output adalah posisi error (sebuah integer dari 0-7).
    """
    # Mengubah string '0' dan '1' menjadi list of integer
    bits = [int(b) for b in bits_str]
    
    # Menambahkan padding agar bisa menggunakan 1-based indexing sesuai standar Hamming code
    # b[1] hingga b[7] akan berisi bit dari input
    b = [0] + bits

    # Menghitung bit-bit sindrom (c1, c2, c4)
    # Bit sindrom dihitung dengan operasi XOR
    c1 = b[1] ^ b[3] ^ b[5] ^ b[7]
    c2 = b[2] ^ b[3] ^ b[6] ^ b[7]
    c4 = b[4] ^ b[5] ^ b[6] ^ b[7]
    
    # Nilai biner dari sindrom (c4 c2 c1) menunjukkan posisi error
    error_pos = (c4 * 4) + (c2 * 2) + (c1 * 1)
    return error_pos

# --- Main Script ---
# List untuk menampung semua posisi error yang ditemukan
error_positions = []

try:
    # Membuka dan membaca file 'error.txt' baris per baris
    with open('error.txt', 'r') as file:
        for line in file:
            line = line.strip() # Menghapus spasi atau karakter newline
            if len(line) == 7:
                pos = find_error_position(line)
                error_positions.append(pos)

    # Setiap posisi error (0-7) adalah digit oktal yang setara dengan 3 bit biner.
    # Menggabungkan semua 3-bit biner menjadi satu string biner panjang.
    binary_string = "".join([format(p, '03b') for p in error_positions])

    # Memecah string biner panjang menjadi beberapa bagian 8-bit (byte)
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Mengubah setiap byte menjadi karakter ASCII untuk mendapatkan flag
    flag = ""
    for byte in byte_chunks:
        if len(byte) == 8:
            decimal_value = int(byte, 2)
            flag += chr(decimal_value)
    
    # Menampilkan flag yang berhasil didekripsi
    print("✅ Flag berhasil ditemukan:")
    print(flag)

except FileNotFoundError:
    print("❌ Error: File 'error.txt' tidak ditemukan.")
    print("Pastikan file tersebut berada di direktori yang sama dengan skrip Python ini.")
