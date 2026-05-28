from pwn import *
import gmpy2 # Used for fast modular inverse of large numbers

# Connect to the server
r = remote('ctf.mf.grsu.by', 9054)

# --- Receive and parse server data ---
# Read the public key line
pub_key_line = r.recvline().decode()
# Extract the tuple string, then use eval to parse it into a Python tuple
n, g = eval(pub_key_line.split('=')[1].strip())

# Read the encrypted balance line
enc_balance_line = r.recvline().decode()
# Extract the number
c_current = int(enc_balance_line.split('=')[1].strip())

print(f"[*] Received n: {n}")
print(f"[*] Received g: {g}")
print(f"[*] Received Encrypted Balance: {c_current}")

# --- Perform the homomorphic calculation ---
n_sq = n * n
target_amount = 1000000

# 1. Calculate Enc(1000000)
# According to Paillier, a simplified encryption (with r=1) is g^m mod n^2
c_target = pow(g, target_amount, n_sq)

# 2. Calculate the modular inverse of the current encrypted balance
# This is equivalent to Enc(-current_balance)
inv_c_current = gmpy2.invert(c_current, n_sq)

# 3. Calculate the required transaction amount: Enc(1,000,000 - current_balance)
# This is Enc(1,000,000) * Enc(-current_balance)
c_amount_to_send = (c_target * inv_c_current) % n_sq

print(f"\n[*] Calculated payload to send: {c_amount_to_send}")

# --- Send the payload and get the flag ---
r.sendlineafter(b'>> Enc(amount) = ', str(c_amount_to_send).encode())

# Print the server's response to get the flag
r.interactive()
