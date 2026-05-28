import socket
import re
import time

# Server details
HOST = 'ctf.mf.grsu.by'
PORT = 9057

def solve_hamming_robust():
    """
    Connects to the server, decodes the Hamming codes, and solves the challenge
    with robust network I/O and parsing.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.settimeout(5)  # Set a timeout to avoid hanging
        print(">>> Connected to the server.")

        # A buffer to hold received data
        buffer = ""

        try:
            # The server specifies 20 rounds
            for round_num in range(20):
                # Read from the server until we get the prompt
                while ">>" not in buffer:
                    data = s.recv(1024).decode()
                    if not data:
                        print("!!! Server closed connection unexpectedly.")
                        return
                    buffer += data
                
                print(f"\n--- Round {round_num + 1} ---")
                
                # Use a more specific regex to find the code right before the prompt
                match = re.search(r"([01]{7}),\s*позиция:данные >>", buffer)
                if not match:
                    print("!!! Error: Could not find 7-bit code prompt.")
                    print(f"--- Buffer content ---\n{buffer}\n----------------------")
                    break
                
                received_code_str = match.group(1)
                
                # Clean the buffer for the next round, keeping any partial data
                buffer = buffer[match.end():]

                print(f"Received code: {received_code_str}")

                # --- The Hamming decoding logic (remains the same) ---
                c = [int(bit) for bit in received_code_str]

                s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
                s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
                s3 = c[3] ^ c[4] ^ c[5] ^ c[6]

                error_pos_1_indexed = (s3 * 4) + (s2 * 2) + s1
                
                reported_pos = 0
                if error_pos_1_indexed > 0:
                    reported_pos = error_pos_1_indexed - 1
                
                print(f"Syndrome (s3s2s1): {s3}{s2}{s1} -> 1-indexed pos: {error_pos_1_indexed}")

                corrected_code = list(c)
                if error_pos_1_indexed > 0:
                    error_index_0_indexed = error_pos_1_indexed - 1
                    corrected_code[error_index_0_indexed] = 1 - corrected_code[error_index_0_indexed]
                
                d1 = corrected_code[2]
                d2 = corrected_code[4]
                d3 = corrected_code[5]
                d4 = corrected_code[6]
                original_data = f"{d1}{d2}{d3}{d4}"
                
                print(f"Extracted data: {original_data}")

                answer = f"{reported_pos}:{original_data}\n"
                
                print(f">>> Sending answer: {answer.strip()}")
                s.sendall(answer.encode())
                time.sleep(0.2) # Small delay to be nice to the server

            # After the loop, read the final flag
            while True:
                data = s.recv(1024).decode()
                if not data:
                    break
                buffer += data

            print("\n<<< Final Response:\n" + buffer)

        except socket.timeout:
            print("\n!!! Socket timed out. Did not receive data in time.")
            print(f"--- Final buffer content ---\n{buffer}\n--------------------------")
        except Exception as e:
            print(f"!!! An error occurred: {e}")

if __name__ == '__main__':
    solve_hamming_robust()
