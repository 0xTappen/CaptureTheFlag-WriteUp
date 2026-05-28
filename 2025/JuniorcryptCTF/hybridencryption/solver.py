import base64

def decrypt_flag():
    """
    Reverses the encryption process to find the original flag.
    """
    encrypted_b64 = "np2Z3p2c3s6YmZ3ezs2ZmM/Tnc7NmJmdz5yYm96cz8+Ym53Z3w=="

    # Step 1: Decode the Base64 string
    decoded_bytes = base64.b64decode(encrypted_b64)

    # Step 2: Reverse the XOR operation
    # The XOR operation is its own inverse, so we XOR with 0xAA again
    original_bytes = bytes([b ^ 0xAA for b in decoded_bytes])

    # Step 3: Decode bytes to get the middle part of the flag
    middle_part = original_bytes.decode()

    # Step 4: Reconstruct the full flag
    flag = "grodno{" + middle_part + "}"
    
    return flag

# Find and print the correct flag
correct_flag = decrypt_flag()
print(f"The correct flag is: {correct_flag}")
