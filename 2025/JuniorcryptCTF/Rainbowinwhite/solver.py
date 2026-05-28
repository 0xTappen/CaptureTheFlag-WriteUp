from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open("Grayscale_bit_0.png").convert("L")
arr = np.array(img)
flat = arr.flatten()

def try_shapes(total_pixels):
    candidates = []
    for i in range(100, int(np.sqrt(total_pixels)) + 1):
        if total_pixels % i == 0:
            h, w = i, total_pixels // i
            candidates.append((h, w))
    return candidates

shapes = try_shapes(flat.size)

for i, (h, w) in enumerate(shapes):
    reshaped = flat.reshape((h, w))
    plt.figure(figsize=(4, 3))
    plt.title(f"Shape: {h}x{w}")
    plt.imshow(reshaped, cmap='gray')
    plt.axis('off')
    plt.show()
    
    if i >= 5:
        break  # tampilkan hanya 6 kemungkinan pertama
