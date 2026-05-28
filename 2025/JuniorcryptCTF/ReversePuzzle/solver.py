def unpuzzle_one_step(s: str) -> str:
    """Reverses one step of the puzzle function."""
    length = len(s)
    # Calculate the split point, equivalent to ceil(length / 2)
    split_point = (length + 1) // 2
    
    first_half = s[:split_point]  # Originally at even positions
    second_half = s[split_point:] # Originally at odd positions
    
    original_s = []
    # Interleave the two halves to reconstruct the original string
    for i in range(len(first_half)):
        original_s.append(first_half[i])
        if i < len(second_half):
            original_s.append(second_half[i])
            
    return "".join(original_s)

# The target string from the check_flag function
target_str = '789603251257384214725442633'

# We need to reverse the puzzle 5 times
steps_to_reverse = 5
current_str = target_str

for _ in range(steps_to_reverse):
    current_str = unpuzzle_one_step(current_str)

# The result is the content of the flag
flag_content = current_str

# Construct the final flag
flag = f"grodno{{{flag_content}}}"

print(f"The flag is: {flag}")
