import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from supabase import create_client, Client
from knowledge_base import JURISDICTIONS
from streamlit_javascript import st_javascript

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

    /* Footer Styles */
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1e293b;
        border-top: 1px solid #334155;
        padding: 10px 20px;
        z-index: 1000;
        
    }

    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }

    .footer-links {
        display: flex;
        gap: 20px;
    }

    .footer-links a {
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.2s ease;
    }

    .footer-links a:hover {
        color: #f8fafc;
    }

    .footer-copyright {
        color: #64748b;
        font-size: 0.8rem;
    }

    .footer-copyright a {
        color: #94a3b8;
        text-decoration: none;
    }

    .footer-copyright a:hover {
        color: #f8fafc;
    }

    /* Ensure content doesn't get hidden behind footer */
    .main .block-container {
        padding-bottom: 120px;
    }
    
    /* Footer fixed at bottom */
    .footer-link-style {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #0f172a;
        padding: 15px 20px;
        text-align: center;
        color: #64748b;
        font-size: 0.75rem;
        border-top: 1px solid #334155;
        z-index: 999;
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
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1588599316608347');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1588599316608347&ev=PageView&noscript=1"
/></noscript>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)
# Client Connections
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


# --- Helper Functions ---
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()

    # Set up fonts - try Verdana first, fallback to Arial
    try:
        # Add Verdana font (matching website font)
        pdf.add_font('Verdana', '', 'verdana.ttf', uni=True)
        font_name = 'Verdana'
    except:
        # Fallback to Arial if Verdana not available
        font_name = 'Arial'

    # Header with logo and company info
    pdf.set_fill_color(248, 250, 252)  # Light gray background like website
    pdf.rect(0, 0, 210, 30, 'F')  # Header background

    # Company logo
    try:
        pdf.image('logo.png', 10, 8, 20)
    except:
        pass  # Logo file not found, continue without it

    # Company name and title
    pdf.set_font(font_name, 'B', 14)
    pdf.set_text_color(51, 65, 85)  # Dark slate color
    pdf.set_xy(35, 10)
    pdf.cell(0, 10, 'LegalLens AI - Compliance Report', 0, 1, 'L')

    # Subtitle
    pdf.set_font(font_name, '', 9)
    pdf.set_text_color(100, 116, 139)  # Gray color
    pdf.set_xy(35, 18)
    pdf.cell(0, 6, 'AI-Powered Document Compliance Review', 0, 1, 'L')

    # ...existing code...

    # Main content
    pdf.set_xy(10, 40)
    pdf.set_font(font_name, '', 10)
    pdf.set_text_color(51, 65, 85)  # Dark text

    # Clean and format the text
    cleaned_text = report_text.encode('latin-1', 'ignore').decode('latin-1')

    # Split text into lines and add proper formatting
    lines = cleaned_text.split('\n')
    for line in lines:
        # Handle headers (lines starting with #)
        if line.strip().startswith('#'):
            pdf.set_font(font_name, 'B', 11)
            pdf.set_text_color(30, 41, 59)  # Darker for headers
            clean_line = line.strip('#').strip()
        elif line.strip().startswith('-') or line.strip().startswith('•'):
            pdf.set_font(font_name, '', 9)
            pdf.set_text_color(51, 65, 85)
            clean_line = '  ' + line.strip('-').strip('•').strip()
        elif line.strip() == '':
            clean_line = ''
        else:
            pdf.set_font(font_name, '', 10)
            pdf.set_text_color(51, 65, 85)
            clean_line = line

        if clean_line:
            # Check if we need a new page
            if pdf.get_y() > 270:
                pdf.add_page()
                pdf.set_xy(10, 20)

            pdf.multi_cell(0, 6, clean_line, 0, 'L')
            pdf.ln(2)

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


def render_footer():
    """Render clean footer without internal divider"""
    st.markdown("""
    <div class="footer-link-style">
        © 2026 LegalLens AI. All rights reserved. | 
        <a href="?page=terms" target="_self" style="color: #94a3b8; text-decoration: none;">Terms</a> | 
        <a href="?page=contact" target="_self" style="color: #94a3b8; text-decoration: none;">Contact</a> | 
        <a href="?page=privacy" target="_self" style="color: #94a3b8; text-decoration: none;">Privacy</a> | 
        <a href="?page=about" target="_self" style="color: #94a3b8; text-decoration: none;">About</a>
    </div>
    """, unsafe_allow_html=True)



if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Handle query parameters for footer links
try:
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.current_page = query_params["page"]
except:
    pass


# --- PAGE ROUTING ---
if st.session_state.current_page == "terms":
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back Home"):
            st.query_params.clear()  # This removes the ?page=... from the browser address bar
            st.session_state.current_page = "home"
            st.rerun()

    st.write("### 📋 Terms & Conditions")
    st.markdown("""
    #### 1. Service Description
    LegalLens AI provides **document review services only**. This is NOT a substitute for professional legal advice. 
    Our AI analyzes rental agreements for potential compliance issues with local housing regulations.
    
    #### 2. User Responsibilities
    - Users are solely responsible for reviewing AI findings with a qualified attorney
    - Users must not rely on our analysis as legal advice
    - Users acknowledge all compliance reviews are for informational purposes only
    
    #### 3. Liability Limitation
    LegalLens AI shall not be liable for any damages, losses, or consequences arising from the use of our service.
    Professional legal consultation is required for legal decisions.
    
    #### 4. Intellectual Property
    All content, analysis methods, and reports are proprietary to LegalLens AI.
    
    #### 5. Modifications
    We reserve the right to modify terms at any time. Continued use implies acceptance.
    """)
    render_footer()

elif st.session_state.current_page == "contact":
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back Home"):
            st.query_params.clear()  # This removes the ?page=... from the browser address bar
            st.session_state.current_page = "home"
            st.rerun()

    st.write("### 📧 Contact Us")
    st.markdown("""
    Have questions about LegalLens AI? We'd love to hear from you.
    
    **Email:** contact@zartechai.com
    
    **Hours:** Monday - Friday, 9AM - 5PM NZST
    
    **Response Time:** We typically respond within 24 hours.
        
    **For urgent legal matters:** Please contact a licensed attorney in your jurisdiction.
    """)
    render_footer()

elif st.session_state.current_page == "privacy":
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back Home"):
            st.query_params.clear()  # This removes the ?page=... from the browser address bar
            st.session_state.current_page = "home"
            st.rerun()

    st.write("### 🔒 Privacy Policy")
    st.markdown("""
    #### Data Collection
    LegalLens AI collects:
    - PDF documents you upload for analysis
    - User email and access key information
    - Usage analytics (non-personally identifiable)
    
    #### Data Usage
    - Documents are used solely for AI analysis
    - Data is NOT stored permanently after analysis
    - We do NOT share your data with third parties
    - All data transmission is encrypted (HTTPS)
    
    #### Data Retention
    - Analysis results are deleted within 30 days
    - Metadata may be retained for service improvement
    - You can request data deletion at any time
    
    #### Security
    We implement industry-standard security measures to protect your information.
    
    #### Your Rights
    You have the right to:
    - Access what data we hold about you
    - Request deletion of your data
    - Opt-out of analytics
    """)
    render_footer()

elif st.session_state.current_page == "about":
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back Home"):
            st.query_params.clear()  # This removes the ?page=... from the browser address bar
            st.session_state.current_page = "home"
            st.rerun()

    st.write("### ℹ️ About LegalLens AI")
    st.markdown("""
    #### Our Mission
    LegalLens AI empowers renters and landlords with **AI-powered document analysis** to identify potential 
    compliance issues in rental agreements before signing.
    
    #### What We Do
    We review rental agreements for:
    - Compliance with local housing regulations
    - Missing mandatory clauses
    - Unfair or risky terms
    - Red flags and negotiation opportunities
    
    #### Important Disclaimer
    ⚠️ **LegalLens AI is NOT a substitute for professional legal advice.**
    
    Our service provides **document review only**. Always consult with a licensed attorney in your 
    jurisdiction before signing any legal document or making legal decisions.
    
    #### How We Analyze Documents
    - AI scans for jurisdiction-specific compliance issues
    - Generates detailed reports with severity ratings
    - Provides negotiation suggestions
    - Includes confidence levels for all findings
    
    #### Our Commitment
    We believe renters deserve clarity and protection. Rental agreements can be complex, 
    and our goal is to help you understand potential risks before it's too late.
    
    **Always seek professional legal advice for legal decisions.**
    """)
    render_footer()

elif not st.session_state.authenticated:
    # Display logo at top left


    st.write("### ⚖️ LegalLens: Lease Review AI")
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

    v_col1, v_col2, v_col3 = st.columns([0.5, 3, 0.5])

    with v_col2:
        # Wrapping the video in a div with our new CSS class
        st.markdown('<div class="video-container">', unsafe_allow_html=True)

        video_file = open('2.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar.expander("💳 Professional Access", expanded=True):
        st.markdown("""
            **One-time analysis for $49.99.**

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

    # Show footer on home page
    render_footer()
    st.stop()

# --- MAIN DASHBOARD (Visible ONLY after unlock) ---
if not st.session_state.authenticated:
    st.stop()

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

if uploaded_file and not st.session_state.analysis_done and st.button("Run AI Legal Audit"):
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




