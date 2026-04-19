import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client

load_dotenv()

# Clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(page_title="LegalLens", page_icon="⚖️")

# --- UI Header ---
st.title("⚖️ LegalLens: Real Estate AI")
st.markdown("""
Analyze rental agreements against **2026 local housing laws**. 
Protect yourself from illegal clauses and hidden costs instantly.
""")


# --- Helper Functions ---
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Basic cleaning for FPDF
    safe_text = report_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')


def check_db_for_key(user_key):
    try:
        res = supabase.table("access_keys").select("*").eq("key", user_key).execute()
        if res.data:
            if not res.data[0]["is_used"]:
                return True, "Success"
            return False, "This key has already been used."
        return False, "Invalid Key. Please check your email."
    except Exception as e:
        return False, f"Error: {str(e)}"


def mark_key_as_used(user_key):
    supabase.table("access_keys").update({"is_used": True}).eq("key", user_key).execute()


# --- Access Control ---
def gatekeeper():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.sidebar.title("🔐 Access Control")

        with st.sidebar.expander("Get an Access Key", expanded=True):
            st.write("One-time professional analysis for $9.99.")
            st.link_button("Buy Key 💳", os.getenv("STRIPE_PAYMENT_LINK"))
            st.caption("Key will be emailed immediately after payment.")

        st.sidebar.divider()
        input_key = st.sidebar.text_input("Enter Access Key", type="password")

        if st.sidebar.button("Unlock Analyzer"):
            valid, msg = check_db_for_key(input_key)
            if valid:
                st.session_state.authenticated = True
                st.session_state.current_key = input_key
                st.rerun()
            else:
                st.sidebar.error(msg)
        return False
    return True


# --- Main App Logic ---
if gatekeeper():
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    st.sidebar.success("Logged In")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    location = st.selectbox(
        "Property Jurisdiction",
        ["Australia (VIC/NSW/QLD)", "New Zealand (RTA 2026)", "USA (NYC/CA/TX)", "Other"]
    )

    uploaded_file = st.file_uploader("Upload Lease (PDF)", type="pdf")

    if uploaded_file:
        if st.session_state.analysis_done:
            st.info("Analysis complete! Download your report below.")
            st.download_button("📥 Download Report", create_pdf(st.session_state.last_report), "Lease_Report.pdf")
        else:
            if st.button("Start AI Legal Audit"):
                with st.spinner("Reviewing clauses against 2026 statutes..."):
                    # PDF Text Extraction
                    reader = PdfReader(uploaded_file)
                    text = " ".join([p.extract_text() for p in reader.pages])

                    # AI Legal Analysis
                    prompt = f"You are a Real Estate Lawyer specializing in {location}. Find red flags and negotiation points."
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}]
                    )

                    report = response.choices[0].message.content
                    st.session_state.last_report = report

                    # Burn key and show results
                    mark_key_as_used(st.session_state.current_key)
                    st.session_state.analysis_done = True
                    st.markdown(report)
                    st.download_button("📥 Download Report", create_pdf(report), "Lease_Report.pdf")