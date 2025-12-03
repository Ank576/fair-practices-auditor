import streamlit as st
import json
from openai import OpenAI
import os
import re

client = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

st.set_page_config(page_title="RBI Fair Practices Auditor", layout="centered")
st.title("🏦 RBI Fair Practices Auditor")
st.markdown("Enter loan terms to check compliance with RBI fair practices code.")

# Input fields matching your image design
principal = st.number_input(
    "Loan Principal (₹)", 
    min_value=0.0, 
    value=100000.0, 
    step=1000.0,
    format="%.2f"
)

processing_fee_pct = st.number_input(
    "Processing Fee (%)", 
    min_value=0.0, 
    max_value=10.0, 
    value=0.50, 
    step=0.1,
    format="%.2f"
)

prepayment_penalty_pct = st.number_input(
    "Prepayment Penalty (%)", 
    min_value=0.0, 
    max_value=10.0, 
    value=1.00, 
    step=0.1,
    format="%.2f"
)

if st.button("Audit Loan Terms", type="primary", use_container_width=True):
    with st.spinner("Checking RBI compliance..."):
        prompt = f"""You are an RBI Fair Practices Code compliance auditor for loan terms.

Analyze these loan terms:
- Principal: ₹{principal:,.0f}
- Processing Fee: {processing_fee_pct}%
- Prepayment Penalty: {prepayment_penalty_pct}%

RBI Fair Practices Code Rules:
- Processing fee must be ≤1% of principal
- Prepayment penalty must be ≤2% per annum

Return ONLY valid JSON (no markdown, no code blocks):

{{
  "is_compliant": boolean,
  "recommendation": "APPROVE|REJECT|WARNING",
  "processing_fee_compliant": boolean,
  "prepayment_penalty_compliant": boolean,
  "processing_fee_absolute": number,
  "violations": ["string reasons if any"],
  "citations": ["RBI sources"],
  "reasoning": "string explanation"
}}"""

        try:
            response = client.chat.completions.create(
                model="sonar-pro",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            raw = response.choices[0].message.content.strip()
            
            # Clean markdown
            raw = re.sub(r'``````', '', raw)
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not json_match:
                st.error("No JSON found in LLM response")
                st.code(raw)
                st.stop()
            
            json_str = json_match.group(0)
            result = json.loads(json_str)
            
            # Display results
            st.subheader("Audit Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fee_status = "✅ Compliant" if result["processing_fee_compliant"] else "❌ Non-compliant (>1%)"
                st.metric(
                    "Processing Fee Check",
                    f"₹{result.get('processing_fee_absolute', 0):,.0f}",
                    f"{processing_fee_pct}%"
                )
                if result["processing_fee_compliant"]:
                    st.success(fee_status)
                else:
                    st.error(fee_status)
            
            with col2:
                penalty_status = "✅ Compliant" if result["prepayment_penalty_compliant"] else "❌ Non-compliant (>2%)"
                st.metric(
                    "Prepayment Penalty Check",
                    f"{prepayment_penalty_pct}%"
                )
                if result["prepayment_penalty_compliant"]:
                    st.success(penalty_status)
                else:
                    st.error(penalty_status)
            
            # Overall status
            if result["is_compliant"]:
                st.success("🎉 Loan terms approved!")
                st.balloons()
            else:
                st.error("🚫 Loan terms rejected due to non-compliance.")
            
            st.info(f"**RBI Reference**: {', '.join(result.get('citations', ['RBI Fair Practices Code']))}")
            
            # Expandable details
            with st.expander("📋 View Detailed Analysis"):
                st.json(result)
                st.write("**Reasoning:**", result.get('reasoning', 'N/A'))

        except json.JSONDecodeError as e:
            st.error(f"JSON Parse Error: {e}")
            st.code(json_str if 'json_str' in locals() else raw)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            st.info("Set PERPLEXITY_API_KEY in Streamlit secrets or environment variable")

st.markdown("---")
st.caption("**Disclaimer**: Demo only. Verify with RBI guidelines. Built with 🧡 by Ankit Saxena")
