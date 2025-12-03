# 🏦 RBI Fair Practices Auditor (LLM + Compliance Checker)

This repo is a Streamlit web app that validates loan terms against RBI Fair Practices Code using a Perplexity Sonar model. It takes loan parameters (principal, processing fee, prepayment penalty) and returns a compliance decision with real-time regulatory citations and reasoning.

Live demo: [DEMO-CLICK](https://fair-practices-auditor-dzvt2uid5mjeq9v8qizr8h.streamlit.app/)

> Note: This is a prototype for product exploration and learning. It does NOT provide legal advice, regulatory consultation, or official RBI compliance certification.

---

## 🎯 What this app does

- Collects loan term inputs:
  - Loan Principal (₹)
  - Processing Fee (%)
  - Prepayment Penalty (%)
- Sends a structured prompt to Perplexity's Sonar model via the OpenAI-compatible Chat Completions API.
- Asks the model to:
  - Validate against RBI Fair Practices Code rules:
    - Processing fee ≤ 1% of principal
    - Prepayment penalty ≤ 2% per annum
  - Return compliance status (APPROVE/REJECT/WARNING)
  - Provide detailed reasoning and RBI regulatory citations
- Parses the JSON response and visualizes:
  - Overall compliance status (✅ APPROVED / ❌ REJECTED)
  - Individual checks for processing fee and prepayment penalty
  - Absolute fee amounts and violation details
  - Full JSON payload for auditing or downstream integration

This is ideal as:
- A PM/fintech compliance prototype
- A reference implementation for LLM-powered regulatory checks
- A starting point for advanced lending compliance sandbox tools
- A portfolio piece demonstrating RBI guidelines understanding

---

## 🧱 Tech stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **LLM backend**: [Perplexity Sonar models](https://docs.perplexity.ai/getting-started/models) via OpenAI-compatible client
- **Language**: Python 3.11
- **Hosting**: Streamlit Community Cloud
- **Config**: API key injected via Streamlit Secrets as TOML environment variable

---

## 📁 Repo structure

```
fair-practices-auditor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .python-version        # Python version specification (3.11)
└── README.md             # This file
```

---

## 🚀 Quick start

### 1. Clone the repo
```bash
git clone https://github.com/Ank576/fair-practices-auditor.git
cd fair-practices-auditor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API key

Create `.streamlit/secrets.toml`:
```toml
PERPLEXITY_API_KEY = "pplx-your-api-key-here"
```

Get your free API key from: [Perplexity API Settings](https://www.perplexity.ai/settings/api)

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔧 How it works

### Step 1: User Input
User enters loan terms via Streamlit number inputs:
- Principal amount (with +/- controls)
- Processing fee percentage
- Prepayment penalty percentage

### Step 2: LLM Prompt Engineering
The app constructs a structured prompt:
```python
prompt = f"""
You are an RBI Fair Practices Code compliance auditor.

Analyze these loan terms:
- Principal: ₹{principal:,.0f}
- Processing Fee: {processing_fee_pct}%
- Prepayment Penalty: {prepayment_penalty_pct}%

Return ONLY valid JSON with compliance status, violations, and RBI citations.
"""
```

### Step 3: API Call to Perplexity
```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1
)
```

### Step 4: JSON Parsing & Display
The app extracts JSON from the response using regex, parses it, and displays:
- Metric cards for each compliance check
- Success/error messages with emojis
- Expandable detailed analysis section
- RBI regulatory citations

---

## 📊 Sample JSON response

```json
{
  "is_compliant": false,
  "recommendation": "REJECT",
  "processing_fee_compliant": false,
  "prepayment_penalty_compliant": true,
  "processing_fee_absolute": 1500,
  "violations": ["Processing fee > 1%"],
  "citations": [
    "RBI Fair Practices Code 2003",
    "RBI/2019-20/88 - Master Direction on Loan System for Banks"
  ],
  "reasoning": "Processing fee of 1.5% exceeds the RBI limit of 1% of principal amount."
}
```

---

## 🎨 Features

- ✅ **Real-time RBI compliance checking**
- 🤖 **LLM-powered regulatory analysis**
- 📊 **Visual metric cards with status indicators**
- 🎯 **Structured JSON output for API integration**
- 📚 **Automatic RBI guideline citations**
- 🎨 **Clean, professional UI matching fintech standards**
- 🔒 **Secure API key management via Streamlit Secrets**

---

## 🛠️ Deployment on Streamlit Cloud

1. Push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repo
4. Add `PERPLEXITY_API_KEY` to Secrets (Settings → Secrets)
5. Deploy!

---

## 📋 RBI Fair Practices Code reference

This app validates against:
- **Processing Fee**: Must not exceed 1% of loan principal
- **Prepayment Penalty**: Must not exceed 2% per annum

Official sources:
- [RBI Fair Practices Code for NBFCs](https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11567&Mode=0)
- [RBI Master Direction - Loan System for Banks](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11556)

---

## 🔮 Future enhancements

- [ ] Support for additional RBI compliance checks (interest rate caps, disclosure requirements)
- [ ] PDF report generation for audit trails
- [ ] Batch processing for multiple loan applications
- [ ] Historical compliance tracking dashboard
- [ ] Integration with loan origination systems (LOS)
- [ ] Multi-lender comparison mode
- [ ] Export API for programmatic access

---

## 🤝 Contributing

This is a learning/portfolio project. Feel free to fork and adapt for your use cases!

For suggestions or issues:
1. Open a GitHub issue
2. Submit a pull request
3. Connect via [LinkedIn](https://linkedin.com/in/ankit-product)

---

## 📄 License & Disclaimer

**License**: MIT (or your preferred open source license)

**Disclaimer**: 
- This tool is for educational and prototyping purposes only
- NOT a substitute for professional legal/compliance advice
- RBI guidelines are subject to change - always verify with official sources
- No liability for decisions made based on this tool's output
- Consult qualified legal/regulatory professionals for actual compliance

---

## 👨‍💻 About

Built with love 💙 by [Ankit Saxena](https://github.com/Ank576)

**Product Manager | Fintech Enthusiast | LLM Explorer**

Part of my fintech portfolio demonstrating:
- RBI regulatory domain knowledge
- LLM integration for compliance automation
- Product thinking for lending/BNPL use cases
- Streamlit rapid prototyping skills

---

## 🔗 Related projects

- [BNPL Eligibility Checker](https://github.com/Ank576/bnpl-eligibility-checker) - LLM-powered BNPL approval simulator
- More fintech prototypes coming soon!

---

**⭐ If you find this useful, consider starring the repo!**
