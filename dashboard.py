import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(
    page_title="AI Gateway SOC Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# API endpoint
API_URL = "http://127.0.0.1:8000/v1/chat"

# Initialize session state for persistent audit logs
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []

st.title("🛡️ Enterprise AI Gateway — SOC Monitoring")
st.markdown("Real-time telemetry for Input Guardrails, Dual-Agent Sandboxing, and Egress Canary Detection.")

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
total_requests = len(st.session_state.audit_logs)
blocked_inputs = sum(1 for log in st.session_state.audit_logs if log["status"] == "BLOCKED_INPUT")
blocked_canaries = sum(1 for log in st.session_state.audit_logs if log["status"] == "CANARY_LEAK")
allowed_requests = sum(1 for log in st.session_state.audit_logs if log["status"] == "SUCCESS")

col1.metric("Total Scanned", total_requests)
col2.metric("Input Threats Blocked", blocked_inputs)
col3.metric("Canary Leaks Intercepted", blocked_canaries)
col4.metric("Clean Responses", allowed_requests)

st.divider()

# Layout: Test Console (Left) and Live Telemetry (Right)
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Simulate Incoming Request")
    prompt = st.text_area(
        "User Prompt / Ingestion Payload:",
        placeholder="Enter safe prompt or adversarial injection (e.g., 'ignore all previous instructions')...",
        height=120
    )
    fetch_ext = st.checkbox("Fetch External Untrusted Context (RAG with Canary Token)", value=True)
    
    if st.button("Transmit Through Gateway", type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt to test.")
        else:
            payload = {"user_prompt": prompt, "fetch_external_data": fetch_ext}
            timestamp = time.strftime("%H:%M:%S")
            
            try:
                res = requests.post(API_URL, json=payload, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Passed Gateway Perimeter")
                    st.json(data)
                    st.session_state.audit_logs.insert(0, {
                        "time": timestamp,
                        "prompt": prompt[:40] + "...",
                        "status": "SUCCESS",
                        "detail": "Passed all guardrails"
                    })
                elif res.status_code == 403:
                    err = res.json().get("detail", "Input blocked")
                    st.error(f"🚨 Layer 1 Violation: {err}")
                    st.session_state.audit_logs.insert(0, {
                        "time": timestamp,
                        "prompt": prompt[:40] + "...",
                        "status": "BLOCKED_INPUT",
                        "detail": err
                    })
                elif res.status_code == 451:
                    err = res.json().get("detail", "Egress blocked")
                    st.error(f"🛑 Layer 5 Violation: {err}")
                    st.session_state.audit_logs.insert(0, {
                        "time": timestamp,
                        "prompt": prompt[:40] + "...",
                        "status": "CANARY_LEAK",
                        "detail": err
                    })
                else:
                    st.warning(f"Unexpected response code: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach FastAPI at http://127.0.0.1:8000. Start your backend with `uvicorn main:app --reload`.")

with right_col:
    st.subheader("Gateway Audit Logs")
    if st.session_state.audit_logs:
        df = pd.DataFrame(st.session_state.audit_logs)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No events logged yet. Send a test prompt from the left panel.")
