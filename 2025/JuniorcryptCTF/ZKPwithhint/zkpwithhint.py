import math
from pwn import *
import traceback

def solve_bsgs(p, g_base, h_target, search_space_bits):
    N = 1 << search_space_bits
    n = math.ceil(math.sqrt(N))
    log.info(f"BSGS: Solving for {search_space_bits}-bit secret, step size n={n}")

    log.info("BSGS: Calculating baby steps...")
    baby_steps = {}
    val = 1
    for j in range(n):
        baby_steps[val] = j
        val = (val * g_base) % p
    
    log.info("BSGS: Calculating giant steps...")
    g_inv_n = pow(g_base, -n, p)
    val = h_target
    for i in range(n):
        if val in baby_steps:
            j = baby_steps[val]
            x = i * n + j
            log.success(f"BSGS: Found secret k = {x}")
            return x
        val = (val * g_inv_n) % p
    
    # JANGAN HENTIKAN SCRIPT, KEMBALIKAN SAJA None
    log.warn("BSGS: Secret k not found in this run.")
    return None

def find_full_r(p, g, C, r_leak):
    N_LEAK_BITS = 464
    N_SECRET_BITS = 512 - N_LEAK_BITS
    g_leak_inv = pow(pow(g, r_leak, p), -1, p)
    h_target = (C * g_leak_inv) % p
    g_base = pow(g, 1 << N_LEAK_BITS, p)
    k = solve_bsgs(p, g_base, h_target, N_SECRET_BITS)
    if k is not None:
        return (k << N_LEAK_BITS) + r_leak
    return None

def solve_challenge():
    conn = None
    context.log_level = 'info'
    try:
        conn = remote('ctf.mf.grsu.by', 9052)
        
        conn.recvuntil(b"p=")
        p = int(conn.recvline().strip())
        conn.recvuntil(b"g=")
        g = int(conn.recvline().strip())
        conn.recvuntil(b"y=")
        y = int(conn.recvline().strip())
        
        log.info("Parameters received.")
        secret_x = None

        for i in range(1, 3): # Loop untuk 2 Ronde
            log.info(f"--- Attempting Round {i} ---")
            conn.recvuntil(b"C = g^r mod p: ")
            C = int(conn.recvline().strip())
            conn.recvuntil(b"leak(r): ")
            r_leak = int(conn.recvline().strip())
            conn.recvuntil(b"e = ")
            e = int(conn.recvline().strip())

            if secret_x is None:
                r_full = find_full_r(p, g, C, r_leak)
                
                # Kirim s=1 untuk memajukan server ke response selanjutnya
                conn.sendline(b"1")
                
                if r_full:
                    log.success(f"Round {i}: Recovered full r = {r_full}")
                    conn.recvuntil(b"Correct s is: ")
                    s_correct = int(conn.recvline().strip())
                    
                    try:
                        phi = p - 1
                        e_inv = pow(e, -1, phi)
                        secret_x = ((s_correct - r_full) * e_inv) % phi
                        log.success(f"Round {i}: Recovered secret x = {secret_x}")
                    except ValueError:
                        log.warn(f"Round {i}: e={e} is not invertible, cannot find x yet.")
                        conn.recvline() # Konsumsi sisa output
                else:
                    log.error(f"Round {i}: Failed to recover r. Skipping to next round.")
                    conn.recvall(timeout=1) # Konsumsi sisa output error
            else:
                # Jika x sudah ditemukan, selesaikan ronde ini dengan benar
                r_full = find_full_r(p, g, C, r_leak)
                if r_full:
                    s_to_send = (r_full + e * secret_x) % (p - 1)
                    log.info(f"Round {i}: Sending correct s = {s_to_send}")
                    conn.sendline(str(s_to_send).encode())
                else:
                    log.error(f"Round {i}: Failed to find r even with x known. Sending dummy value.")
                    conn.sendline(b"1") # Kirim asal-asalan jika r gagal ditemukan

        # Setelah loop selesai, coba terima flag
        log.info("All rounds attempted. Waiting for final response...")
        flag_data = conn.recvall(timeout=5).decode()
        if "CTF" in flag_data:
            log.success(f"FLAG DATA:\n{flag_data.strip()}")
        else:
            log.warn(f"Could not find flag. Final server output was:\n{flag_data.strip()}")

    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        # print(traceback.format_exc())
    finally:
        if conn and conn.connected():
            conn.close()

if __name__ == "__main__":
    solve_challenge()
