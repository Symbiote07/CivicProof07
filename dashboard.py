import streamlit as st
import requests
import pandas as pd

# The URL of your running backend
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CivicProof Dashboard", layout="wide")

# --- HEADER ---
st.title("🏛️ CivicProof: Micro-Accountability Engine")
st.markdown("Real-time governance monitoring and AI verification system.")

# --- SIDEBAR (Controls) ---
st.sidebar.header("Control Panel")
refresh = st.sidebar.button("🔄 Refresh Data")

# --- FETCH DATA ---
try:
    # Get Tasks
    response = requests.get(f"{API_URL}/tasks")
    tasks = response.json()
    df_tasks = pd.DataFrame(tasks)
except:
    st.error("⚠️ Backend is offline. Is 'uvicorn main:app' running?")
    st.stop()

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)
total = len(df_tasks)
verified = len(df_tasks[df_tasks['status'].str.contains("Verified")])
pending = total - verified

col1.metric("Total Tasks", total)
col2.metric("Verified Works ✅", verified)
col3.metric("Pending Action ⏳", pending)

st.divider()

# --- MAIN VIEW: MAP & LIST ---
col_map, col_list = st.columns([2, 1])

with col_map:
    st.subheader("📍 Live Booth Activity Map")
    
    # We need to map the booth locations. 
    # Since our simple Tasks API sends 'booth_id', we'll simulate coordinates for the demo
    # In a real app, we would fetch Booth data specifically.
    
    # Hardcoding the seed coordinates for visualization (Lucknow)
    map_data = pd.DataFrame({
        'lat': [26.8467, 26.8500],
        'lon': [80.9462, 80.9400],
        'booth_name': ["Sector 14, Gali 3", "Hazratganj Main Market"]
    })
    
    st.map(map_data)

with col_list:
    st.subheader("📋 Task List")
    # Show a clean table of tasks
    st.dataframe(df_tasks[['title', 'status', 'id']], hide_index=True)

st.divider()

# --- LIVE VERIFICATION TEST ---
st.subheader("🔍 Manual Verification Override")
st.write("Upload a photo here to test the AI verification engine directly from the dashboard.")

uploaded_file = st.file_uploader("Upload Evidence Photo", type=['jpg', 'png', 'jpeg'])
task_id_input = st.number_input("Enter Task ID to Verify", min_value=1, step=1)

if uploaded_file is not None and st.button("Verify Now"):
    with st.spinner("AI is analyzing brightness and objects..."):
        # Send file to API
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{API_URL}/verify-task/{task_id_input}", files={"file": uploaded_file})
        
        # ... (Inside the button click logic) ...

        if res.status_code == 200:
            result = res.json()
            ai_data = result['ai_verdict']
            
            if ai_data['success']:
                st.success(f"✅ VERIFIED! Confidence: {ai_data['confidence']:.2f}")
                st.write(f"**Detected Tags:** {ai_data['tags']}")
                
                # --- NEW: DISPLAY SMS LOGS ---
                st.divider()
                st.subheader("📢 Citizen Notifications Triggered")
                
                if "notifications" in result and result["notifications"]:
                    for msg in result["notifications"]:
                        st.info(msg) # Creates a blue notification box
                else:
                    st.warning("No voters registered in this booth to notify.")
                # -----------------------------
                
            else:
                st.error(f"❌ REJECTED. Reason: {ai_data['status']}")