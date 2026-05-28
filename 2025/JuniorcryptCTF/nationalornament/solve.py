import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# ========== STEP 1: Load PDF and Convert to Image ==========
pdf_path = "OrnamentCipher.pdf"
doc = fitz.open(pdf_path)
pix = doc[0].get_pixmap(dpi=300)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
cipher_img = np.array(img)

# ========== STEP 2: Load and Slice Alphabet Image ==========
alphabet_img = cv2.imread("alphabet.jpg")
gray_ref = cv2.cvtColor(alphabet_img, cv2.COLOR_BGR2GRAY)
ref_thresh = cv2.threshold(gray_ref, 200, 255, cv2.THRESH_BINARY_INV)[1]

# Assume grid 5x6 = 30 slots, but only A-Z used
rows, cols = 5, 6
cell_h, cell_w = ref_thresh.shape[0] // rows, ref_thresh.shape[1] // cols

alphabet_templates = {}
for i in range(26):
    r, c = divmod(i, cols)
    char_img = ref_thresh[r*cell_h:(r+1)*cell_h, c*cell_w:(c+1)*cell_w]
    letter = chr(ord('A') + i)
    alphabet_templates[letter] = char_img

# ========== STEP 3: Threshold Cipher Image ==========
gray_cipher = cv2.cvtColor(cipher_img, cv2.COLOR_RGB2GRAY)
thresh_cipher = cv2.threshold(gray_cipher, 200, 255, cv2.THRESH_BINARY_INV)[1]

# ========== STEP 4: Find Symbols ==========
contours, _ = cv2.findContours(thresh_cipher, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by y (row), then x (left to right)
contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1]//50, cv2.boundingRect(c)[0]))

result_lines = []
current_line = []
last_y = -1

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w < 10 or h < 10:  # skip noise
        continue

    # Line separation logic
    if last_y != -1 and abs(y - last_y) > 50:
        result_lines.append(current_line)
        current_line = []

    symbol = thresh_cipher[y:y+h, x:x+w]
    resized = cv2.resize(symbol, (cell_w, cell_h))

    # Match with reference
    best_score = float('inf')
    matched_letter = '?'
    for letter, template in alphabet_templates.items():
        diff = cv2.absdiff(resized, template)
        score = np.sum(diff)
        if score < best_score:
            best_score = score
            matched_letter = letter

    current_line.append(matched_letter)
    last_y = y

# Append last line
if current_line:
    result_lines.append(current_line)

# ========== STEP 5: Build Final Output ==========
translated_words = [''.join(line) for line in result_lines]
print("Decoded Lines:")
for line in translated_words:
    print(line)

# Optional Flag Output
flag = '_'.join(translated_words)
print("\nFlag:", flag)
