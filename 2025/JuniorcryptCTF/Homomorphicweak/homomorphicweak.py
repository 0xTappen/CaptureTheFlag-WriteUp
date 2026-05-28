# Solver for the provided n and c values.

import gmpy2
from Crypto.Util.number import long_to_bytes

# --- Values for this stage ---
n = 12103820557099104485760656016245953173352844327620589726138415747840748086830381582934158393855426143281451493380430561322543240649251048720976561585245773
c = 99588365183163436912207488485172071463487987058498970692865450363111028841076957631154134170434567442308457033997185585980762906689933919648140338958934890935891019732195821285252944133459505026707469125647417487543001578691309680245580895614444509990533644366242035562806292081265413061807837686189329681687


def solve():
    """Factors n, decrypts c, and prints the flag."""
    print("[-] Starting Fermat's factorization...")
    a = gmpy2.isqrt(n) + 1
    while True:
        b_squared = a * a - n
        if gmpy2.is_square(b_squared):
            b = gmpy2.isqrt(b_squared)
            p = a - b
            q = a + b
            if p * q == n:
                print(f"[+] Found factors p and q!")
                break
        a += 1

    print("[-] Decrypting ciphertext...")
    # Using the simplified Paillier decryption for g = n+1
    lamb = gmpy2.lcm(p - 1, q - 1)
    mu = gmpy2.invert(lamb, n)
    power_val = pow(c, lamb, n * n)
    L_val = (power_val - 1) // n
    m = (L_val * mu) % n

    # Convert the final number to the flag string
    flag = long_to_bytes(m)
    print(f"\n[+] Success! The flag is: {flag.decode()}")

if __name__ == "__main__":
    solve()
