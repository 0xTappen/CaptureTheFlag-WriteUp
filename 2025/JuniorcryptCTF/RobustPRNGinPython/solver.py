import socket
import time
import random
import math
import re

# --- Configuration ---
HOST = "ctf.mf.grsu.by"
PORT = 9045
# A 4-second window should be enough to cover latency and clock skew.
SEARCH_WINDOW_SECONDS = 4

def get_number_from_response(response: str) -> int:
    """Extracts the integer from the server's response line."""
    match = re.search(r'(\d+)', response)
    if match:
        return int(match.group(1))
    raise ValueError("Could not parse number from server response.")

def solve():
    """Connects to the server and executes the attack."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Record local time just before connecting to estimate the server's time
        connect_time_utc = time.time()
        s.connect((HOST, PORT))

        # Receive the initial banner and prompts
        s.recv(4096)

        # 1. Request the first random number
        s.sendall(b'1\n')
        response1 = s.recv(1024).decode('utf-8')
        server_r1 = get_number_from_response(response1)
        print(f"[*] Received first number: {server_r1}")

        # 2. Request the second random number
        s.sendall(b'1\n')
        response2 = s.recv(1024).decode('utf-8')
        server_r2 = get_number_from_response(response2)
        print(f"[*] Received second number: {server_r2}")

        # 3. Brute-force the seed in a time window around our connection time
        print(f"[*] Starting seed search around UTC time: {connect_time_utc:.2f}")
        
        # The seed 'm' is math.ceil(time.time() * 1_000_000).
        # We can iterate through potential integer values of 'm'.
        start_seed = math.ceil((connect_time_utc - SEARCH_WINDOW_SECONDS / 2) * 1_000_000)
        end_seed = math.ceil((connect_time_utc + SEARCH_WINDOW_SECONDS / 2) * 1_000_000)
        
        prediction = None
        for seed_guess in range(start_seed, end_seed):
            random.seed(seed_guess)
            local_r1 = random.getrandbits(31)

            # Check if the first number matches
            if local_r1 == server_r1:
                local_r2 = random.getrandbits(31)
                # If first matches, check the second to confirm
                if local_r2 == server_r2:
                    print(f"\n[+] Found correct seed: {seed_guess}")
                    # The next number is our prediction
                    prediction = random.getrandbits(31)
                    break
        
        if prediction is None:
            print("\n[-] Failed to find the seed. Try increasing SEARCH_WINDOW_SECONDS.")
            return

        # 4. Submit the prediction and get the flag
        print(f"[+] Predicting next number: {prediction}")
        s.sendall(b'2\n')
        s.recv(1024) # Wait for 'Ваше число: ' prompt
        s.sendall(f'{prediction}\n'.encode())

        # 5. Print the final response from the server
        flag_response = s.recv(1024).decode('utf-8')
        print("\n--- Server Response ---")
        print(flag_response)

if __name__ == "__main__":
    solve()
