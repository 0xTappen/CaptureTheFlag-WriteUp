import re
from PIL import Image

data = """1(15)0(1)1(3)0(1)1(2)0(1)1(14)0(1)1(2)0(6)1(6)0(1)1(4)0(2)1(4)0(1)1(6)0(1)1(4)0(1)1(2)0(1)1(3)0(1)1(4)0(1)1(2)0(1)1(3)0(1)1(2)0(1)1(1)0(2)1(1)0(5)1(14)0(1)1(24)0(1)1(1)0(1)1(1)0(2)1(13)0(2)1(15)0(6)1(6)0(2)1(10)0(1)1(18)0(1)1(11)0(1)1(3)0(1)1(2)0(1)1(4)0(1)1(9)0(1)1(1)0(1)1(23)0(1)1(4)0(1)1(3)0(1)1(24)0(2)1(6)0(1)1(1)0(6)1(6)0(1)1(4)0(1)1(6)0(1)1(4)0(1)1(3)0(1)1(2)0(6)1(8)0(2)1(32)0(2)1(5)0(2)1(1)0(6)1(1)0(1)1(4)0(1)1(4)0(1)1(6)0(1)1(4)0(1)1(4)0(8)1(1)0(1)1(19)0(1)1(6)0(1)1(18)0(3)1(4)0(1)1(9)0(1)1(3)0(1)1(15)0(1)1(13)0(1)1(2)0(6)1(6)0(1)1(11)0(1)1(11)0(6)1(2)0(1)1(22)0(1)1(8)0(1)1(8)0(1)1(16)0(1)1(29)0(2)1(6)0(1)1(1)0(6)1(6)0(1)1(4)0(1)1(2)0(1)1(3)0(1)1(4)0(1)1(3)0(1)1(2)0(6)1(8)0(2)1(19)0(1)1(13)0(1)1(3)0(1)1(2)0(1)1(34)0(2)1(4)0(1)1(4)0(3)1(1)0(1)1(2)0(2)1(1)0(2)1(2)0(1)1(4)0(4)1(3)0(1)1(11)0(1)1(16)0(1)1(4)0(3)1(4)0(1)1(2)0(7)1(4)0(1)1(6)0(1)1(4)0(1)1(6)0(1)1(4)0(7)1(7)0(3)1(17)0(1)1(2)0(2)1(16)0(1)1(16)0(1)1(2)0(1)1(26)0(2)1(4)0(1)1(4)0(3)1(4)0(2)1(1)0(2)1(2)0(1)1(4)0(4)1(3)0(1)1(11)0(1)1(2)0(1)1(14)0(1)1(5)0(1)1(4)0(2)1(5)0(1)1(4)0(8)1(11)0(1)1(3)0(1)1(33)"""  # potong demi singkat, kamu ganti dengan full data
# atau bisa copy seluruh string panjang itu langsung di sini

# Ekstrak pattern 1(x) dan 0(y)
pattern = re.findall(r'(1|0)\((\d+)\)', data)

# Bentuk stream biner
bitstream = ''.join([bit * int(count) for bit, count in pattern])

# Konversi ke list boolean (True = putih, False = hitam)
pixels = [255 if b == '1' else 0 for b in bitstream]

# Ukuran gambar: coba-coba, atau bisa kamu tentuin dari panjang data
# Misal kita coba lebar 64 dulu, atau 128
width = 128
height = len(pixels) // width

# Bikin gambar
img = Image.new('L', (width, height))  # 'L' = grayscale 8-bit
img.putdata(pixels)
img = img.convert('1')  # ubah ke 1-bit (b/w)

# Simpan atau tampilkan
img.save('broken_pixels_output.png')
img.show()
