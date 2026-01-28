import streamlit as st

# Pure function (NO API)
from backends_2 import calculate_storage_cost


def show():
    st.title("💾 Storage Cost Calculator")
    st.caption("Estimate your cloud storage costs with a simple, modern interface.")
    st.divider()

    col1, col2 = st.columns([2, 2])

    with col1:
        amount = st.number_input(
            "📦 Data Amount",
            min_value=0.0,
            value=1.0,
            step=0.1,
            format="%.2f",
            help="Enter the amount of data you want to store.",
        )
        unit = st.selectbox("Unit", ["TB", "GB"], index=0)
        storage_class = st.selectbox("Storage Class", ["standard", "archive"], index=0)
        region = st.selectbox("Region", ["us-east-1", "eu-west-1", "ap-southeast-1"], index=0)

    with col2:
        months = st.number_input(
            "🗓️ Duration (Months)",
            min_value=1,
            value=12,
            step=1,
            format="%d",
            help="Enter the number of months you'll store the data.",
        )

        # Retrieval is only meaningful for archive
        retrieval_gb = st.number_input(
            "Retrieval (GB, archive only)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            disabled=(storage_class != "archive"),
        )

        egress_gb = st.number_input(
            "Egress (GB)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.2f",
        )

        num_requests = st.number_input(
            "Requests (count)",
            min_value=0,
            value=0,
            step=1000,
            help="Total monthly request count (GET/PUT/etc combined, simplified).",
        )

    st.info(
        """
**Cloud Storage Pricing (Example)**  
Standard: $0.023/GB-month  
Archive: $0.004/GB-month  
Retrieval (Archive): $0.02/GB  
Egress: $0.09/GB  
Requests: $0.005/1000
"""
    )

    if st.button("Calculate Storage Cost", key="calc_storage", use_container_width=True):
        if amount <= 0:
            st.error("Please enter a positive data amount.")
            return

        # If standard, force retrieval to 0
        if storage_class != "archive":
            retrieval_gb = 0.0

        # Pure function call (no backend HTTP)
        result = calculate_storage_cost(
            amount=amount,
            unit=unit,
            months=int(months),
            storage_class=storage_class,
            retrieval_gb=float(retrieval_gb),
            egress_gb=float(egress_gb),
            requests_count=int(num_requests),
        )

        st.markdown(
            f"""
<div style='background:rgba(56,142,60,0.07);border-radius:12px;padding:1.2em 1em;margin-top:1em;'>
  <h4 style="margin:0 0 .6em 0;">Summary</h4>
  <ul style="margin:0; padding-left:1.2em;">
    <li><b>Region:</b> {region}</li>
    <li><b>Data:</b> {amount:.2f} {unit}</li>
    <li><b>Duration:</b> {int(months)} months</li>
    <li><b>Storage:</b> ${result['storage']:.2f} USD</li>
    <li><b>Retrieval:</b> ${result['retrieval']:.2f} USD</li>
    <li><b>Egress:</b> ${result['egress']:.2f} USD</li>
    <li><b>Requests:</b> ${result['requests']:.2f} USD</li>
    <li><b>Total Cost:</b> <span style='color:#388e3c; font-weight:700;'>${result['total']:.2f} USD</span></li>
    <li><b>Monthly (avg):</b> ${result.get('monthly', result['total'] / int(months)):.2f} USD</li>
    <li><b>Annualised:</b> ${result.get('yearly', (result['total'] / int(months)) * 12):.2f} USD</li>
  </ul>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
---
#### Calculation Notes
- This is a simplified estimator. Real cloud bills include tiering, minimums, request class differences, and regional variance.
- **TB → GB conversion** here uses 1024. Some providers bill in decimal (1000). Adjust in `backend/logic.py` if needed.

---
#### Common Network Speeds
- Fast Ethernet: 100 Mbit/s
- Gigabit Ethernet: 1000 Mbit/s
- 10G Ethernet: 10000 Mbit/s
"""
    )


show()
