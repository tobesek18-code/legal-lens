import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client

st.title("⚖️ LegalLens: Real Estate AI")
st.subheader("Don't sign a lease until you've scanned it.")

# A brief, catchy description
st.markdown("""
**LegalLens** is your personal AI-powered lease auditor. 
Whether you're in Sydney, Auckland, or New York, our AI analyzes your rental agreement 
against local 2026 housing laws to protect you from illegal clauses and hidden costs.
""")

# 1. SETUP & CONNECTIONS
load_dotenv()

# AI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Supabase Client
url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, supabase_key)

# st.set_page_config(page_title="LegalLens AI", page_icon="⚖️")

# "How it Works" Columns
st.write("### How it Works")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 1. Upload")
    st.write("Drag and drop your PDF lease agreement into our secure analyzer.")

with col2:
    st.markdown("### 2. Analyze")
    st.write("Our AI checks the text against specific 2026 laws for your city or country.")

with col3:
    st.markdown("### 3. Protect")
    st.write("Receive a professional PDF report highlighting red flags and negotiation tips.")



st.divider() # A visual line to separate the info from the login


# 2. HELPER FUNCTIONS
def create_pdf(report_text):
    """Sanitizes text and generates a downloadable PDF."""
    cleaned_text = (
        report_text.replace('’', "'").replace('‘', "'")
        .replace('—', "-").replace('“', '"').replace('”', '"')
        .replace('\u2013', "-").replace('\u2014', "-")
    )
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_text = cleaned_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')


def check_db_for_key(user_key):
    """Queries Supabase to see if the key exists and is not yet used."""
    try:
        response = supabase.table("access_keys").select("*").eq("key", user_key).execute()
        if len(response.data) > 0:
            key_data = response.data[0]
            if not key_data.get("is_used"):
                return True, "Success"
            else:
                return False, "This key has already been used for an analysis."
        return False, "Invalid Access Key. Please check your email or buy a new one. "
    except Exception as e:
        return False, f"Database Error: {str(e)}"


def mark_key_as_used(user_key):
    """Updates the database so this key can never be used again."""
    supabase.table("access_keys").update({"is_used": True}).eq("key", user_key).execute()


# 3. ACCESS CONTROL (GATEKEEPER)
def gatekeeper():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.sidebar.title("🔐 Premium Access")
        st.sidebar.info("Enter your unique key to unlock the analyzer.")

        input_key = st.sidebar.text_input("Access Key", type="password")

        if st.sidebar.button("Unlock App"):
            is_valid, msg = check_db_for_key(input_key)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.current_key = input_key  # Save for the final 'burn'
                st.sidebar.success("Key Validated!")
                st.rerun()
            else:
                st.sidebar.error(msg)
                st.sidebar.link_button("Buy a Key ($9.99)", "https://buy.stripe.com/your_link")
        return False
    return True


# 4. MAIN APP LOGIC
if gatekeeper():
    # Track the run in the current session
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    location = st.selectbox(
        "Property Jurisdiction",
        ["Australia (VIC/NSW/QLD)", "New Zealand (RTA 2026)", "USA (NYC/CA/TX)", "Other"]
    )

    local_laws = {
        "Australia (VIC/NSW/QLD)": "Focus: No-fault evictions, 12-month rent caps, and pet rights.",
        "New Zealand (RTA 2026)": "Focus: Healthy Homes standards and 2026 termination grounds.",
        "USA (NYC/CA/TX)": "Focus: Rent control, security deposit limits, and disclosure requirements.",
        "Other": "Focus: Standard hidden fees and termination penalties."
    }

    uploaded_file = st.file_uploader("Upload Lease (PDF)", type="pdf")

    if uploaded_file:
        if st.session_state.analysis_done:
            st.warning("⚠️ This key has been used. Please download your report below.")
            if "last_report" in st.session_state:
                st.download_button("📥 Download PDF Report", create_pdf(st.session_state.last_report), "Report.pdf")
        else:
            if st.button("Run Professional Analysis"):
                with st.spinner("Analyzing against local laws..."):
                    # Extract Text
                    reader = PdfReader(uploaded_file)
                    text = "".join([p.extract_text() for p in reader.pages])

                    # AI Call
                    prompt = f"You are a Real Estate Lawyer. Context: {local_laws[location]}. Analyze for Red Flags and Negotiation points."
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": text}
                        ]
                    )

                    report = response.choices[0].message.content
                    st.session_state.last_report = report

                    # 5. THE "BURN" - Mark key as used in DB
                    mark_key_as_used(st.session_state.current_key)
                    st.session_state.analysis_done = True

                    st.markdown(report)
                    st.download_button("📥 Download PDF Report", create_pdf(report), "Lease_Report.pdf")
                    st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()