from pwn import *
import traceback

# Configure pwntools for the challenge
context.log_level = 'info'
context.timeout = 15

def solve():
    """
    Connects to the server and solves the challenge.
    """
    conn = None
    try:
        conn = remote('ctf.mf.grsu.by', 9050)
        
        # --- 1. Parse Initial Parameters ---
        conn.recvuntil(b"p = ")
        p = int(conn.recvline().strip())
        conn.recvuntil(b"r = ")
        r = int(conn.recvline().strip())
        phi = p - 1
        log.info(f"Received p and r. Calculated phi = p-1.")

        secret_x = None

        # --- 2. Loop through rounds to find x ---
        for i in range(1, 6):
            conn.recvuntil(f"=== Round {i} ===".encode())
            conn.recvuntil(b"Challenge e = ")
            e_current = int(conn.recvline().strip())
            log.info(f"Round {i}: Received challenge e = {e_current}")

            if secret_x is None:
                # If we haven't found the secret, trigger the leak
                log.info(f"Round {i}: Secret not found. Sending s=1 to trigger leak.")
                conn.sendline(b'1')
                conn.recvuntil(b"Verification failed!")
                conn.recvuntil(b"s = ")
                s_correct = int(conn.recvline().strip())

                try:
                    # Attempt to find x.
                    e_inv = pow(e_current, -1, phi)
                    s_minus_r = (s_correct - r) % phi
                    secret_x = (s_minus_r * e_inv) % phi
                    log.success(f"Success! Found secret x in Round {i}.")
                    log.success(f"x = {secret_x}")
                except ValueError:
                    # THE FIX IS HERE: Use log.warn() instead of log.error()
                    log.warn(f"Round {i}: e={e_current} is not invertible mod phi. Trying again in the next round.")
            
            else:
                # If we have the secret, send the correct response
                s_to_send = (r + e_current * secret_x) % phi
                log.info(f"Round {i}: Secret is known. Sending correct s = {s_to_send}")
                conn.sendline(str(s_to_send).encode())

            # Every round prints this message, so we consume it to clear the buffer
            conn.recvuntil(b"Round passed!")

        # --- 3. Final step: Submit the secret ---
        if secret_x is not None:
            log.success("All rounds passed. Submitting final secret.")
            conn.recvuntil(b"x:")
            conn.sendline(str(secret_x).encode())
            
            # Print the flag
            flag_output = conn.recvall(timeout=5).decode()
            log.success(f"FLAG: {flag_output.strip()}")
        else:
            log.error("Could not find the secret after all rounds.")

    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        # Uncomment line below for full debug trace if needed
        # print(traceback.format_exc()) 

    finally:
        if conn and conn.connected():
            conn.close()

if __name__ == "__main__":
    solve()
