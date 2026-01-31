import easyocr

# 1. Initialize the reader
# We tell it to look for English ('en'). 
# gpu=False is safer for now if you don't have CUDA set up, 
# but set to True if you have an NVIDIA card.
print("Loading the AI model... (this happens once)")
reader = easyocr.Reader(['en'], gpu=False) 

# 2. Read the image
# 'detail=0' means "just give me the text lists", don't give me the confusing coordinates box.
print("Reading text from image...")
result = reader.readtext('menu.jpg', detail=0)

# 3. Print the raw output
print("\n--- RAW OUTPUT ---")
for line in result:
    print(line)

# 4. Save to a file (so we can inspect it later)
with open("raw_menu_text.txt", "w") as f:
    for line in result:
        f.write(line + "\n")
print("\nDone! Check raw_menu_text.txt")