import streamlit as st
import json
import difflib

# 1. Load Data (Cached so it doesn't reload on every click)
@st.cache_data
def load_data():
    with open("sample_data.json", "r") as f:
        return json.load(f)

menu = load_data()

# 2. The Logic Function (Reusing your "Brain")
def find_dish(query, max_price=None):
    query = query.lower()
    matches = []
    
    for item in menu:
        dish_name = item['dish']
        # Clean price for math
        try:
            price_val = float(item['price'])
        except:
            price_val = 0.0
            
        # Logic A: Price Filter (If sidebar is used)
        if max_price is not None:
            if price_val > max_price:
                continue # Skip if too expensive
        
        # Logic B: Text Search
        # If query is empty, show everything (that fits budget)
        if not query: 
            matches.append(item)
            continue
            
        # If query exists, check name match
        if query in dish_name.lower():
            matches.append(item)
        elif difflib.SequenceMatcher(None, query, dish_name.lower()).ratio() > 0.6:
            matches.append(item)
            
    return matches

# --- UI LAYOUT ---
st.title("🍔 Saqafat Menu AI")
st.caption("Ask me about food or filter by price!")

# Sidebar for Budget
with st.sidebar:
    st.header("💰 Wallet Filter")
    # A slider from 0 to 2000 rupees
    budget = st.slider("Max Budget (Rs.)", 0, 2000, 2000) 
    st.write(f"Showing items under: **{budget}**")

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! What are you craving today?"}]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Type 'burger' or 'eggs'..."):
    # 1. Show User Message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Get Bot Response
    # We pass the slider value (budget) into the logic
    results = find_dish(prompt, max_price=budget)
    
    # 3. Format the Output
    if results:
        response = f"I found **{len(results)}** items for you under {budget}:\n\n"
        for item in results:
            response += f"- **{item['dish']}**: {item['price']}\n"
    else:
        response = f"Sorry, I couldn't find anything matching '{prompt}' under {budget}."

    # 4. Show Bot Message
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})