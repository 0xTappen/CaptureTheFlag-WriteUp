import subprocess

# Password yang sudah diketahui dari hash SHA256
password = "p8a8s8s8w8o8r8d8"

# Jalankan main0.exe dan kirim password sebagai argumen
try:
    result = subprocess.run(
        ["./main0.exe", password],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    print(result.stdout.strip())

except subprocess.CalledProcessError as e:
    print("Terjadi error saat menjalankan main0.exe:")
    print(e.stderr)
