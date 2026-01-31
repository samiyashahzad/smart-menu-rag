import streamlit as st
import json
import difflib


@st.cache_data
def load_data():
    with open("sample_data.json", "r") as f:
        return json.load(f)

menu = load_data()


def find_dish(query, max_price=None):
    query = query.lower().strip()
    matches = []


    if query in ["menu", "show menu", "list", "all", "show me the menu"]:
        return [item for item in menu if float(item['price']) <= (max_price or 99999)]

  
    try:
        budget_query = float(query)
        # Return items cheaper than this number
        return [item for item in menu if float(item['price']) <= budget_query]
    except ValueError:
        pass # Not a number? Continue to text search...


    for item in menu:
        # Get all data fields safely
        dish_name = item.get('dish', '').lower()
        category = item.get('category', '').lower() # We check this now!
        price = float(item.get('price', 0))

        # Check Sidebar Slider (if used)
        if max_price is not None:
            if price > max_price:
                continue 
        
    
        if query in dish_name:
            matches.append(item)
            

        elif query in category:
            matches.append(item)
            
    
        elif difflib.SequenceMatcher(None, query, dish_name).ratio() > 0.6:
            matches.append(item)
            
    return matches

st.title("🍔 Digital  Menu AI")
st.caption("Ask me about food or filter by price!")


with st.sidebar:
    st.header("💰 Wallet Filter")
    # A slider from 0 to 2000 rupees
    budget = st.slider("Max Budget (Rs.)", 0, 2000, 2000) 
    st.write(f"Showing items under: **{budget}**")

st.markdown("### 🤖 Quick Options")
col1, col2, col3 = st.columns(3)


def handle_click(query_text):
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": query_text})
    
  

    results = find_dish(query_text, max_price=budget)
    
    if results:
       
        if len(results) > 10: 
             response = f"I found the whole menu ({len(results)} items) for you!\n\n"
        else:
             response = f"I found **{len(results)}** items under {budget}:\n\n"
             
        for item in results:
            response += f"- **{item['dish']}**: {item['price']}\n"
    else:
        response = "Sorry, nothing found!"
        

    st.session_state.messages.append({"role": "assistant", "content": response})
    
  
    st.rerun()


if col1.button("📜 Show Full Menu"):
    handle_click("Show me the menu")

if col2.button("🍳 Breakfast"):
    handle_click("breakfast")

if col3.button("💵 Cheap Eats (< 500)"):
    handle_click("500")

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
