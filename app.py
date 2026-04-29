import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client
from knowledge_base import JURISDICTIONS

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
    .stApp > footer {display: none !important;}
    footer[data-testid="stFooter"] {display: none !important;}
    .css-1lcbmhc {display: none !important;}  /* Common footer class */
    .css-1q1n0ol {display: none !important;}  /* Another footer variant */

    /* Removes the "Hosted with Streamlit" badge in bottom right */
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}    
    
    [data-testid="stStatusWidget"] {
        visibility: hidden;
        display: none !important;
    }
    
    /* Removes the "Manage App" and other viewer-side elements */
    #viewer-badge {display: none !important;}    
    .viewerBadge_container__1QSob {display: none !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    
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

.video-container {
        border: 2px solid #475569; /* Matches your button border color */
        border-radius: 12px;
        padding: 10px;
        background-color: #1e293b; /* Slightly darker slate background */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
        
        const streamlitDoc = window.parent.document;

    document.addEventListener("DOMContentLoaded", function(event){
            // Existing footer replacement logic
            streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "Provided by <a href='https://yourwebsite.com' target='_blank'>LegalLens</a>";
            
            // Disable right-click on all video elements
            const videos = streamlitDoc.getElementsByTagName("video");
            for (let i = 0; i < videos.length; i++) {
                videos[i].setAttribute("oncontextmenu", "return false;");
                videos[i].setAttribute("controlsList", "nodownload");
            }
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
    supabase.table("access_keys").update(
        {"is_used": True}
    ).eq("key", user_key).execute()


def build_system_prompt(location, kb):
    return f"""
You are a tenancy agreement compliance reviewer specializing in residential rental law for {location}.

Your task is to review tenancy agreements for legal compliance, missing mandatory clauses,
unfair terms, hidden risks, and negotiation opportunities.

IMPORTANT RULES:
- Do NOT invent laws, clauses, or facts not present in the agreement
- If something cannot be verified, clearly state: "Unable to verify from provided agreement"
- Focus strictly on compliance review, not legal representation
- This is NOT formal legal advice
- Provide a confidence level for each finding: High / Medium / Low
- Provide a severity level for each finding: Critical / High / Medium / Low
- Quote the exact problematic clause when possible
- Identify both problematic clauses and missing mandatory requirements
- Suggest negotiation amendments where appropriate
- Keep findings jurisdiction-specific to {location}

Jurisdiction Knowledge:
Statutes: {kb.get("statutes", "")}

Mandatory Checks:
{", ".join(kb.get("mandatory_checks", []))}

Common Red Flags:
{", ".join(kb.get("red_flags", []))}
"""


def build_user_prompt(text):
    return f"""
Review the following tenancy agreement for compliance with 2026 residential tenancy laws.

Generate a structured report with:

1. Executive Summary

2. Critical Violations Found
- issue
- severity
- confidence
- clause quote
- legal concern
- recommendation

3. Missing Mandatory Requirements

4. Unfair or Risky Clauses

5. Negotiation Suggestions

6. Overall Risk Score (Low / Medium / High)
Include a short reason for the score.

7. Final Disclaimer
State clearly this is a compliance review and not formal legal advice.

Lease Agreement Text:

{text}
"""


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.write("### ⚖️ LegalLens: Real Estate AI")
    st.caption("AI-powered document compliance review for rental agreements.")

    st.markdown("""
    Legal agreements often contain incompliant clauses that violate local statutes. **LegalLens** performs automated compliance checks on rental agreements against 2026 housing regulations. 

    **⚠️ Important:** This is a document review tool only. Results are not legal advice and should not replace professional legal consultation.
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
        st.caption("Upload your PDF. AI scans for potential compliance issues based on 2026 regulations.")

    with col3:
        st.write("**3. Review Results**")
        st.caption("Download a detailed compliance report to review with your legal professional.")
    st.write("")  # Extra spacing for breathing room
    st.write("")  # Extra spacing for breathing room

    v_col1, v_col2, v_col3 = st.columns([0.5, 3, 0.5])

    with v_col2:
        # Wrapping the video in a div with our new CSS class
        st.markdown('<div class="video-container">', unsafe_allow_html=True)

        video_file = open('1.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # Sidebar: Collapsable Access Control
    st.sidebar.title("🔐 Access Portal")

    with st.sidebar.expander("💳 Professional Access", expanded=True):
        st.markdown("""
            **One-time analysis for $39.99.**

            Key will be emailed immediately after payment.
        """)
        st.sidebar.link_button("Don't have a key? Get one here 💳", st.secrets["STRIPE_PAYMENT_LINK"])

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
location = st.selectbox(
    "Property Jurisdiction",
    list(JURISDICTIONS.keys()) + ["Other"]
)

uploaded_file = st.file_uploader("Upload Lease (PDF)", type="pdf")

if uploaded_file and st.button("Run AI Legal Audit"):
    with st.spinner("Reviewing tenancy agreement..."):
        reader = PdfReader(uploaded_file)
        text = " ".join(
            [p.extract_text() for p in reader.pages if p.extract_text()]
        )

        kb = JURISDICTIONS.get(location, {
            "statutes": "General local housing law compliance",
            "mandatory_checks": [],
            "red_flags": []
        })

        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": build_system_prompt(location, kb)
                },
                {
                    "role": "user",
                    "content": build_user_prompt(text)
                }
            ]
        )

        report = response.choices[0].message.content
        st.session_state.last_report = report
        st.session_state.analysis_done = True
        mark_key_as_used(st.session_state.current_key)

if st.session_state.analysis_done:
    st.success("Analysis Complete")
    st.markdown(st.session_state.last_report)
    st.download_button(
        "📥 Download PDF Report",
        create_pdf(st.session_state.last_report),
        "Lease_Report.pdf"
    )
