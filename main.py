import sys
import io

# Set UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("🧸 CryptoBear structure loaded.")

