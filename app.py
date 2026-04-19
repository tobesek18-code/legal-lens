import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client

# MUST BE FIRST
# st.set_page_config(page_title="LegalLens AI", page_icon="⚖️")
st.write("### ⚖️ LegalLens: Real Estate AI")
st.caption("Analyze rental agreements against **2026 local housing laws**.")
# --- EXECUTIVE UI OVERRIDE ---
st.markdown("""
    <style>
    /* Hides the GitHub icon and Share menu but KEEPS the toggle visible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent;} 

    /* Executive Font & Palette */
    html, body, [class*="css"] {
        font-family: "Verdana", sans-serif;
    }
        h1 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #f8fafc; /* Ice color to match your palette */
        }
   
    </style>
    """, unsafe_allow_html=True)

# Use st.secrets for Streamlit Cloud Deployment
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- Helper Functions ---
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Sanitize Unicode for basic FPDF (standard Latin-1)
    cleaned_text = report_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=cleaned_text)
    return pdf.output(dest='S').encode('latin-1')


def check_db_for_key(user_key):
    try:
        res = supabase.table("access_keys").select("*").eq("key", user_key).execute()
        if res.data and not res.data[0]["is_used"]:
            return True, "Success"
        return False, "Invalid or used key."
    except Exception as e:
        return False, f"Database connection issue: {e}"


def mark_key_as_used(user_key):
    supabase.table("access_keys").update({"is_used": True}).eq("key", user_key).execute()


# --- Access Control ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("🔐 Premium Access")
    st.sidebar.info("Analyze your lease with our 2026 AI Legal Auditor.")
    st.sidebar.link_button("Buy Access Key ($9.99) 💳", st.secrets["STRIPE_PAYMENT_LINK"])

    st.sidebar.divider()

    input_key = st.sidebar.text_input("Enter Access Key", type="password")
    if st.sidebar.button("Unlock App"):
        valid, msg = check_db_for_key(input_key)
        if valid:
            st.session_state.authenticated = True
            st.session_state.current_key = input_key
            st.rerun()
        else:
            st.sidebar.error(msg)
    st.stop()

# --- Main App Logic ---
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# Sidebar Tools once unlocked
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

location = st.selectbox("Property Jurisdiction",
                        ["Australia (VIC/NSW/QLD)", "New Zealand (RTA 2026)", "USA (NYC/CA/TX)", "Other"])
uploaded_file = st.file_uploader("Upload Lease (PDF)", type="pdf")

if uploaded_file:
    if st.session_state.analysis_done:
        st.success("Analysis Complete")
        st.download_button("📥 Download Report", create_pdf(st.session_state.last_report), "Lease_Report.pdf")
        st.markdown(st.session_state.last_report)
    else:
        if st.button("Start AI Legal Audit"):
            with st.spinner("Analyzing against local 2026 statutes..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

                # Context-aware Prompting
                prompt = f"You are a Senior Real Estate Lawyer specializing in {location}. Review this lease for illegal clauses, hidden fees, and points of negotiation."

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text}
                    ]
                )

                report = response.choices[0].message.content
                st.session_state.last_report = report

                # Commit to DB
                mark_key_as_used(st.session_state.current_key)
                st.session_state.analysis_done = True

                st.markdown(report)
                st.download_button("📥 Download PDF Report", create_pdf(report), "Lease_Report.pdf")
                st.rerun()