import re
import json

# 1. Load the raw text we just saved
with open("raw_menu_text.txt", "r") as f:
    lines = f.readlines()

menu_data = []
current_item = None

# 2. Iterate through each line to find pairs
for line in lines:
    text = line.strip() # Remove invisible spaces
    
    if not text: continue # Skip empty lines
    if text.upper() in ["MENU", "RESTAURANT", "BREAKFAST", "MAIN", "SALADS"]: continue # Skip headers

    # CHECK: Is this line a Price?
    # Regex Explanation: Look for digits (0-9) that might have a comma or dot
    if re.search(r'\d', text): 
        # It has numbers, so it's likely a price
        if current_item:
            # Clean the price (replace comma with dot, remove spaces)
            clean_price = text.replace(',', '.').replace(' ', '')
            
            # Save the pair
            menu_data.append({
                "dish": current_item,
                "price": clean_price
            })
            current_item = None # Reset for next dish
    else:
        # It has no numbers, so it's likely a Dish Name
        current_item = text

# 3. Print the Result as JSON
print(json.dumps(menu_data, indent=2))

# 4. Save it (This is your database!)
with open("menu.json", "w") as f:
    json.dump(menu_data, f, indent=2)