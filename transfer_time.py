import streamlit as st
from static.css.streamlit_style import CUSTOM_CSS
from static.html.footer import get_footer_html



st.set_page_config(
    page_title="Transfer Time Calculator - Mega Giga What?",
    page_icon="⏱",
    layout="wide"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def show():
    st.title("Transfer Time Calculator")
    st.markdown('<p style="font-size:1.1rem; color:#388e3c;">Calculate how long your data transfer will take</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        unit = st.selectbox("Unit", ["TB", "GB"], index=0)
        data_amount = st.number_input(
            f"Data Amount ({unit})",
            min_value=0.0,
            value=1.0,
            step=0.1,
            format="%.2f",
            key="amount_transfer_time",
            help=f"Enter the total amount of data you want to transfer in {unit}"
        )

    with col2:
        link_mbit = st.number_input(
            "Link Speed (Mbit/s)",
            min_value=1.0,
            value=100.0,
            step=1.0,
            format="%.0f",
            key="mbit_transfer_time",
            help="Enter your network connection speed in Megabits per second"
        )

    st.info("""
    **How It Works**

    **Calculation Formula**

    We use the following formula to calculate transfer time:

    ```
    Convert TB/GB to bits: bits = Amount × 8 × 1024³ (GB) or 1024⁴ (TB)
    Convert Mbit/s to bits/s: bandwidth = Mbit/s × 1,000,000
    Calculate time: seconds = bits ÷ bandwidth
    Convert to days, hours, minutes, and seconds
    ```
    """)
    if st.button("Calculate Transfer Time", key="calc_transfer_time", use_container_width=True):
        if data_amount <= 0 or link_mbit <= 0:
            st.error("Please enter valid positive numbers")
        else:
            from backends_2 import calculate_transfer_time
            result = calculate_transfer_time(data_amount, unit, link_mbit)
            st.success(f"Transferring **{data_amount:.2f} {unit}** at **{link_mbit:.0f} Mbit/s** will take:\n\n**{result['days']} days, {result['hours']} hours, {result['minutes']} minutes, {result['seconds']} seconds**")
    st.markdown("""
    ---
    ### Tips & Real-World Factors
    - Network overhead typically reduces effective speed by 5-10%
    - Protocol overhead (TCP/IP) adds additional time
    - Distance and routing can affect transfer speeds

    ---
    ### Common Speeds
    - Fast Ethernet: 100 Mbit/s
    - Gigabit Ethernet: 1000 Mbit/s
    - 10G Ethernet: 10000 Mbit/s

    ---
    <p style='text-align:center; color:#888;'>© 2026 Mega Giga What? All rights reserved.</p>
    """, unsafe_allow_html=True)


show()
