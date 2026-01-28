import sys
import os
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="Mega Giga What?",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar page selector with vertical radio buttons
st.sidebar.title("Mega Giga What?")
page = st.sidebar.radio(
  "",
  ("Home", "Storage Cost", "Transfer Time", "Your IP", "Blog / Docs")
)

if page == "Home":
    from pages.home import show as show_home
    show_home()
elif page == "Storage Cost":
    from pages.storage import show as show_storage
    show_storage()
elif page == "Transfer Time":
    from pages.transfer_time import show as show_transfer
    show_transfer()
elif page == "Your IP":
    from pages.your_ip import show_ip_trace as show_ip
    show_ip()
elif page == "Blog / Docs":
    st.markdown("""
<div class='glass-card'>
  <h1 id='docs'>MegaGigaWhat Docs</h1>
  <p>Welcome to the MegaGigaWhat suite! This page explains what each tool does and how we built it.</p>
  <nav>
    <ul>
      <li><a href='#home-base'>Home Base</a></li>
      <li><a href='#transfer-time'>Transfer Time</a></li>
      <li><a href='#storage-cost'>Storage Cost</a></li>
      <li><a href='#my-ip'>My IP</a></li>
      <li><a href='#how-built'>How It's Built</a></li>
    </ul>
  </nav>
</div>
<div class='glass-card' id='home-base'>
  <h2>Home Base</h2>
  <p><strong>Notes:</strong> Entry point for all tools.</p>
</div>
<div class='glass-card' id='transfer-time'>
  <h2>Transfer Time</h2>
  <p><strong>What:</strong> Calculates how long it takes to transfer large data sets.</p>
  <p><strong>Inputs:</strong> Data size (TB), Link speed (Mbit/s)</p>
  <p><strong>Output:</strong> Days, hours, minutes, seconds</p>
  <p><strong>Notes:</strong> Assumes continuous transfer, no throttling.</p>
</div>
<div class='glass-card' id='storage-cost'>
  <h2>Storage Cost</h2>
  <p><strong>What:</strong> Estimates cloud storage costs based on current pricing.</p>
  <p><strong>Inputs:</strong> Data size (TB), Duration (months)</p>
  <p><strong>Output:</strong> Total, monthly, and yearly cost</p>
  <p><strong>Notes:</strong> Pricing based on AWS S3 Standard, updated periodically.</p>
</div>
<div class='glass-card' id='my-ip'>
  <h2>My IP</h2>
  <p><strong>What:</strong> Shows your public IP address as seen by our server.</p>
  <p><strong>Inputs:</strong> None</p>
  <p><strong>Output:</strong> Your IP address and info</p>
  <p><strong>Notes:</strong> Uses a secure API endpoint.</p>
</div>
<div class='glass-card' id='how-built'>
  <h2>How It's Built</h2>
  <ul>
    <li><strong>Backend calculators:</strong> Python functions for transfer time and storage cost, with robust validation.</li>
    <li><strong>Validation:</strong> All inputs are clamped to valid ranges; zero is valid, not missing.</li>
    <li><strong>Region mapping:</strong> Pricing and latency are mapped by region for accuracy.</li>
    <li><strong>Pricing sources:</strong> AWS S3, public docs; subject to change, always check latest.</li>
    <li><strong>UI:</strong> Minimal, glassmorphism, always readable, responsive, and accessible.</li>
  </ul>
</div>
    """, unsafe_allow_html=True)
