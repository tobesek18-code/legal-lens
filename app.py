import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client

# MUST BE FIRST
st.set_page_config(page_title="LegalLens AI", page_icon="⚖️")

# --- EXECUTIVE UI OVERRIDE (Deep Slate & Silver) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent;} 

    /* Executive Font & Palette */
    html, body, [class*="css"] {
        font-family: "Verdana", sans-serif;
        color: #f1f5f9; /* Ice White text */
    }

    /* PROFESSIONAL SLATE BUTTONS (Including Upload/Download) */
    div.stButton > button, 
    div.stDownloadButton > button, 
    label[data-testid="stFileUploaderPreSignUrl"] {
        background-color: #334155 !important; /* Steel Slate */
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 4px !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        font-weight: 600 !important;
        height: 3.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover, 
    div.stDownloadButton > button:hover {
        background-color: #475569 !important;
        border-color: #94a3b8 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }

    /* Smaller Title Styling */
    h3 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #f8fafc;
    }
    </style>
    """, unsafe_allow_html=True)

# Client Connections
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


# --- Helper Functions ---
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
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


# --- Access Control Logic ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LANDING PAGE (Marketing & Retrieval) ---
if not st.session_state.authenticated:
    st.write("### ⚖️ LegalLens: Real Estate AI")
    st.caption("Protect your rights with **2026 AI-Powered Lease Auditing**.")

    st.markdown("""
    Don't sign a lease until you've scanned it. **LegalLens** identifies 'red flags' such as 
    hidden costs, unfair rules, or illegal termination penalties.
    """)

    st.divider()

    st.write("#### 🛠️ How it Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**1. Secure Upload**")
        st.caption("Drag and drop your PDF lease into our secure analyzer.")
    with col2:
        st.write("**2. AI Audit**")
        st.caption("Our system scans for predatory clauses based on 2026 laws.")
    with col3:
        st.write("**3. Negotiate**")
        st.caption("Download a professional PDF report to present to your landlord.")

    st.divider()

    st.write("#### 🔑 Obtaining Your Access Key")
    st.markdown("""
    1. **Purchase**: Click the 'Buy Access Key' button in the sidebar.
    2. **Instant Delivery**: Your unique key is **sent to your email address** immediately after payment.
    3. **Activation**: Enter that key in the sidebar to unlock the analyzer.
    """)

    # Sidebar for Payment & Entry
    st.sidebar.title("🔐 Premium Access")
    st.sidebar.link_button("Buy Access Key ($9.99) 💳", st.secrets["STRIPE_PAYMENT_LINK"])
    st.sidebar.divider()

    input_key = st.sidebar.text_input("Enter Access Key", type="password")
    if st.sidebar.button("Unlock Analysis"):
        valid, msg = check_db_for_key(input_key)
        if valid:
            st.session_state.authenticated = True
            st.session_state.current_key = input_key
            st.rerun()
        else:
            st.sidebar.error(msg)
    st.stop()

# --- ANALYSIS DASHBOARD (Only visible after unlock) ---
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

st.write("### 📑 Analysis Dashboard")
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
        if st.button("Run AI Legal Audit"):
            with st.spinner("Reviewing clauses against local statutes..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

                prompt = f"You are a Senior Real Estate Lawyer specializing in {location}. Review for illegal clauses."

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text}
                    ]
                )

                report = response.choices[0].message.content
                st.session_state.last_report = report
                mark_key_as_used(st.session_state.current_key)
                st.session_state.analysis_done = True

                st.markdown(report)
                st.download_button("📥 Download PDF Report", create_pdf(report), "Lease_Report.pdf")
                st.rerun()