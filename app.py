import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client
from knowledge_base import JURISDICTIONS

# MUST BE FIRST - Set to expanded to help with mobile visibility
st.set_page_config(
    page_title="LegalLens AI",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- EXECUTIVE UI OVERRIDE ---
st.markdown("""
    <style>
    
    /* Hiding Streamlit Branding, GitHub, Share, and Status Badges */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Removes the "Hosted with Streamlit" badge in bottom right */
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}    
    
    [data-testid="stStatusWidget"] {
        visibility: hidden;
        display: none !important;
    }
    
    /* Removes the "Manage App" and other viewer-side elements */
    #viewer-badge {display: none !important;}    
    
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    #viewer-badge {display: none !important;}

    /* Executive Font & Palette */
    html, body, [class*="css"] {
        font-family: "Verdana", sans-serif;
    }

    /* THE CARD LOOK FOR SIDEBAR EXPANDER */
    div[data-testid="stExpander"] {
        border-radius: 8px;
    }

    /* PROFESSIONAL SLATE BUTTONS */
    div.stButton > button, 
    div.stDownloadButton > button, 
    label[data-testid="stFileUploaderPreSignUrl"] {
        background-color: #334155 !important;
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

    div.stButton > button:hover {
        background-color: #475569 !important;
        border-color: #94a3b8 !important;
    }

    h3 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #f8fafc;
    }
    [class^="_profilePreview_"] {
  display: none !important;
}
    </style>
    """, unsafe_allow_html=True)



hide_st_style = """
    <script>
    const streamlitDoc = window.parent.document;

    // Make the replacement
    document.addEventListener("DOMContentLoaded", function(event){
            streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "Provided by <a href='https://yourwebsite.com' target='_blank' class='css-z3au9t egzxvld2'>Your Link Display Text Here</a>";
        });
    </script>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)
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
        return False, f"Connection issue: {e}"


def mark_key_as_used(user_key):
    supabase.table("access_keys").update({"is_used": True}).eq("key", user_key).execute()


# --- Authentication Logic ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LANDING PAGE (Only visible if NOT authenticated) ---
if not st.session_state.authenticated:
    st.write("### ⚖️ LegalLens: Real Estate AI")
    st.caption("Analyze rental agreements against **2026 local housing laws**.")

    st.markdown("""
    Legal agreements often contain incompliant clauses that violate local statutes. **LegalLens** provides an instant professional audit agreements for tenants, landlords and property agents.
    """)

    st.divider()

    # Restored "How it Works" including Access Key process
    st.write("#### 🛠️ How it Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**1. Get Your Key**")
        st.caption("Purchase a key via Stripe. It is emailed to you instantly.")
    with col2:
        st.write("**2. Secure Audit**")
        st.caption("Upload your PDF. AI scans for incompliant clauses based on 2026 laws.")
    with col3:
        st.write("**3. Negotiate**")
        st.caption("Download a professional PDF report to present to your tenant/landlord/property agent.")

    st.divider()

    # Sidebar: Collapsable Access Control
    st.sidebar.title("🔐 Access Portal")

    with st.sidebar.expander("💳 Professional Access", expanded=True):
        st.markdown("""
            **One-time analysis for $49.99.**

            Key will be emailed immediately after payment.
        """)
        st.sidebar.link_button("Buy Access Key 💳", st.secrets["STRIPE_PAYMENT_LINK"])

    st.sidebar.divider()

    input_key = st.sidebar.text_input("Enter Access Key", type="password", placeholder="PASTE-KEY-HERE")
    if st.sidebar.button("Unlock Dashboard"):
        valid, msg = check_db_for_key(input_key)
        if valid:
            st.session_state.authenticated = True
            st.session_state.current_key = input_key
            st.rerun()
        else:
            st.sidebar.error(msg)

    st.stop()

# --- MAIN DASHBOARD (Visible ONLY after unlock) ---
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
            with st.spinner("Analyzing against 2026 statutes..."):
                reader = PdfReader(uploaded_file)
                text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

                # Build enhanced prompt
                system_content = f"You are a legal expert specializing in rental agreements for {location}. "
                if location in JURISDICTIONS:
                    kb = JURISDICTIONS[location]
                    system_content += f"Key statutes: {kb['statutes']}. Common red flags to check for: {', '.join(kb['red_flags'])}. Mandatory requirements to verify: {', '.join(kb['mandatory_checks'])}."
                else:
                    system_content += "Focus on compliance with local housing laws, fair housing practices, and tenant protections."

                user_content = f"Please analyze the following lease agreement text for compliance with relevant 2026 laws and regulations. Identify any clauses that may be illegal, unfair, or non-compliant. Highlight red flags, missing mandatory elements, and provide recommendations for amendments or negotiations. Structure your report clearly with sections for Summary, Violations Found, Missing Requirements, and Suggestions.\n\nLease Text:\n{text}"

                response = client.chat.completions.create(
                    model="gpt-4o",
                    temperature=0,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content}
                    ]
                )

                report = response.choices[0].message.content
                st.session_state.last_report = report
                mark_key_as_used(st.session_state.current_key)
                st.session_state.analysis_done = True
                st.markdown(report)
                st.download_button("📥 Download PDF Report", create_pdf(report), "Lease_Report.pdf")
                st.rerun()