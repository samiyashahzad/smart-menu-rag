import json
import google.generativeai as genai
import time

# 1. Setup the AI
# Replace with your actual key!
API_KEY = "YOUR_API_KEY_HERE" 
genai.configure(api_key=API_KEY)

# Use 'gemini-1.5-flash' because it's fast and cheap (free tier)
model = genai.GenerativeModel('gemini-3-flash-preview')

# 2. Load the Dirty Data
print("Loading dirty menu...")
with open("menu.json", "r") as f:
    dirty_data = f.read() # Read as raw string

# 3. The Prompt (The "Instructions")
# We give the AI the data and strict rules on how to fix it.
prompt = f"""
You are a Data Cleaning Assistant for a restaurant.
Here is a raw JSON list of menu items containing OCR errors and typos:

{dirty_data}

TASKS:
1. Fix all spelling errors (e.g., "Bonedicl" -> "Benedict").
2. Standardize prices to numbers (remove currency symbols).
3. Identify the likely category (Breakfast, Main, Salad) based on the item name.
4. Return ONLY the clean JSON. Do not add markdown like ```json.

Output format:
[
  {{ "dish": "Correct Name", "price": 50.0, "category": "Breakfast" }}
]
"""

# 4. Call the AI
print("Asking AI to clean the data... (this takes 5-10 seconds)")
try:
    response = model.generate_content(prompt)
    cleaned_text = response.text
    
    # 5. Clean up response (sometimes AI adds backticks)
    cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()

    # 6. Save the Result
    # Verify it parses as JSON before saving
    json_data = json.loads(cleaned_text)
    
    with open("menu_clean.json", "w") as f:
        json.dump(json_data, f, indent=2)
        
    print("Success! Created 'menu_clean.json'")
    print(f"cleaned {len(json_data)} items.")

except Exception as e:
    print(f"Error: {e}")
# import google.generativeai as genai

# # Put your key here
# genai.configure(api_key="YOUR_API_KEY_HERE")

# print("Listing available models...")
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)