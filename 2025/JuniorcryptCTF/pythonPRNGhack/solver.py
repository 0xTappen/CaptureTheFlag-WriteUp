import socket
import time
import random
import math
import re

# Connection details for the server
HOST = "ctf.mf.grsu.by"
PORT = 9043

def solve():
    """
    Solves the challenge within a single, persistent connection.
    """
    try:
        # Establish a single connection for the entire process
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.settimeout(5) # Set a timeout for socket operations

            # 1. Receive the initial banner from the server
            # We increase the buffer and add a small delay to ensure we get all of it
            time.sleep(0.5)
            s.recv(4096)

            # 2. Request the first two numbers from the server
            print("[*] Requesting first two numbers from the server...")
            s.sendall(b'1\n')
            response1 = s.recv(1024).decode()
            num1 = int(re.search(r'\d+', response1).group(0))

            s.sendall(b'1\n')
            response2 = s.recv(1024).decode()
            num2 = int(re.search(r'\d+', response2).group(0))

            print(f"[*] Received numbers: {num1}, {num2}")

            # 3. Brute-force the seed that generates this exact sequence
            print("[*] Searching for the correct seed...")
            current_time_ms = math.ceil(time.time() * 1000000)
            found_seed = None
            
            # Widen the search window to 10 seconds to account for network latency
            for i in range(10000000):
                potential_seed = current_time_ms - i
                random.seed(potential_seed)
                # Check if this seed generates our exact sequence
                if random.getrandbits(32) == num1 and random.getrandbits(32) == num2:
                    found_seed = potential_seed
                    print(f"[*] Verified seed found: {found_seed}")
                    break
            
            if not found_seed:
                print("[!] Failed to find the seed. The server might be slow or the time window too small.")
                return

            # 4. The generator is now correctly seeded. Predict the NEXT number (the third one).
            prediction = random.getrandbits(32)
            print(f"[*] Predicting the next number is: {prediction}")

            # 5. Send the guess using the same connection
            s.sendall(b'2\n')
            time.sleep(0.5) # Wait for the prompt
            s.recv(1024)  # Receive "Ваше число: " prompt
            s.sendall(f"{prediction}\n".encode())
            
            final_response = s.recv(1024).decode()
            print("\n" + "="*20)
            print("Server Response:")
            print(final_response)
            print("="*20)

    except socket.timeout:
        print("[!] Socket timed out. The server is not responding as expected.")
    except Exception as e:
        print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
    solve()
