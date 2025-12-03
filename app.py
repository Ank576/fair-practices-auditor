import streamlit as st

st.title("🏦 RBI Fair Practices Auditor")
st.markdown("Enter loan terms to check compliance with RBI fair practices code.")

# Input fields
principal = st.number_input("Loan Principal (₹)", min_value=0.0, value=100000.0, step=1000.0)
processing_fee_pct = st.number_input("Processing Fee (%)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
prepayment_penalty_pct = st.number_input("Prepayment Penalty (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

if st.button("Audit Loan Terms"):
    processing_fee_abs = (processing_fee_pct / 100) * principal
    compliant_fee = processing_fee_pct <= 1.0
    compliant_penalty = prepayment_penalty_pct <= 2.0
    
    st.subheader("Audit Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Processing Fee Check", f"₹{processing_fee_abs:,.0f}", delta=f"{processing_fee_pct}%")
        st.success("✅ Compliant" if compliant_fee else "❌ Non-compliant (>1%)")
    
    with col2:
        st.metric("Prepayment Penalty Check", f"{prepayment_penalty_pct}%")
        st.success("✅ Compliant" if compliant_penalty else "❌ Non-compliant (>2%)")
    
    overall = compliant_fee and compliant_penalty
    st.balloons() if overall else st.error("Loan terms rejected due to non-compliance.")
    st.info("**RBI Reference**: Processing fee ≤1% of principal; prepayment penalty ≤2% per annum.")
