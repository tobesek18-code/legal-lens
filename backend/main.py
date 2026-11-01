import os
import io
import uuid
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import stripe
from supabase import create_client, Client
import resend
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
from fpdf import FPDF
from knowledge_base import JURISDICTIONS
import jwt
from datetime import datetime, timedelta
import secrets
import tempfile

load_dotenv()

# Config
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
resend.api_key = os.getenv("RESEND_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Initialize Supabase with error handling
try:
    supabase: Client = create_client(url, key)
except Exception as e:
    print(f"⚠️  Warning: Could not initialize Supabase: {e}")
    print("Make sure SUPABASE_URL and SUPABASE_KEY are set correctly in .env")
    supabase = None

client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Security
# Load from env so tokens survive restarts and work across multiple workers.
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)
    print("⚠️  Warning: JWT_SECRET not set. Using a random key; "
          "tokens will be invalidated on every restart.")
ALGORITHM = "HS256"


def generate_key():
    return f"LL-{uuid.uuid4().hex[:8].upper()}"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        access_key: str = payload.get("sub")
        if access_key is None:
            return None
        return access_key
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_db_for_key(user_key: str):
    if not supabase:
        return False, "Database connection not available"
    try:
        res = supabase.table("access_keys").select("*").eq("key", user_key).execute()
        if res.data and not res.data[0]["is_used"]:
            return True, "Success"
        return False, "Invalid or used key."
    except Exception as e:
        return False, f"Connection issue: {e}"


def mark_key_as_used(user_key: str):
    if supabase:
        try:
            supabase.table("access_keys").update(
                {"is_used": True}
            ).eq("key", user_key).execute()
        except Exception as e:
            print(f"Error marking key as used: {e}")


def build_system_prompt(location: str, kb: dict):
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


def build_user_prompt(text: str):
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


def create_pdf(report_text: str):
    pdf = FPDF()
    pdf.add_page()

    # Set up fonts - try Verdana first, fallback to Arial
    try:
        pdf.add_font('Verdana', '', 'verdana.ttf', uni=True)
        font_name = 'Verdana'
    except:
        font_name = 'Arial'

    # Header with logo and company info
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(0, 0, 210, 30, 'F')

    # Company logo
    try:
        pdf.image('../logo.png', 10, 8, 20)
    except:
        pass

        # Company name and title
    pdf.set_font(font_name, 'B', 14)
    pdf.set_text_color(51, 65, 85)
    pdf.set_xy(35, 10)
    pdf.cell(0, 10, 'LegalLens - Compliance Report', 0, 1, 'L')

    # Subtitle
    pdf.set_font(font_name, '', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(35, 18)
    pdf.cell(0, 6, 'AI-Powered Document Compliance Review', 0, 1, 'L')

    # Main content
    pdf.set_xy(10, 40)
    pdf.set_font(font_name, '', 10)
    pdf.set_text_color(51, 65, 85)

    cleaned_text = report_text.encode('latin-1', 'ignore').decode('latin-1')

    lines = cleaned_text.split('\n')
    for line in lines:
        if line.strip().startswith('#'):
            pdf.set_font(font_name, 'B', 11)
            pdf.set_text_color(30, 41, 59)
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
            if pdf.get_y() > 270:
                pdf.add_page()
                pdf.set_xy(10, 20)

            pdf.multi_cell(0, 6, clean_line, 0, 'L')
            pdf.ln(2)

    return pdf.output(dest='S').encode('latin-1')


# API Routes
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or 'access_key' not in data:
        return jsonify({"error": "Access key required"}), 400

    valid, msg = check_db_for_key(data['access_key'])
    if not valid:
        return jsonify({"error": msg}), 401

    access_token = create_access_token({"sub": data['access_key']})
    return jsonify({"access_token": access_token, "token_type": "bearer"})


@app.route("/jurisdictions", methods=["GET"])
def get_jurisdictions():
    return jsonify({"jurisdictions": list(JURISDICTIONS.keys()) + ["Other"]})


@app.route("/analyze", methods=["POST"])
def analyze_document():
    access_key = verify_token()
    if not access_key:
        return jsonify({"error": "Invalid or expired token"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    jurisdiction = request.form.get('jurisdiction')

    if not file or not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    if not jurisdiction:
        return jsonify({"error": "Jurisdiction is required"}), 400

    try:
        # Read PDF content safely into an in-memory byte stream buffer
        content = file.read()
        file_stream = io.BytesIO(content)

        # Pass the memory stream instead of the raw immutable bytes object
        reader = PdfReader(file_stream)
        text = " ".join(
            [p.extract_text() for p in reader.pages if p.extract_text()]
        )

        if not text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400

        kb = JURISDICTIONS.get(jurisdiction, {
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
                    "content": build_system_prompt(jurisdiction, kb)
                },
                {
                    "role": "user",
                    "content": build_user_prompt(text)
                }
            ]
        )

        report = response.choices[0].message.content
        mark_key_as_used(access_key)

        return jsonify({"report": report})

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf_endpoint():
    access_key = verify_token()
    if not access_key:
        return jsonify({"error": "Invalid or expired token"}), 401

    data = request.get_json()
    if not data or 'report' not in data:
        return jsonify({"error": "Report text is required"}), 400

    try:
        report_text = data['report']
        pdf_content = create_pdf(report_text)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_content)
            temp_filename = temp_file.name

        return send_file(
            temp_filename,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Lease_Report.pdf"
        )

    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500


@app.route("/pages/<page_name>", methods=["GET"])
def get_page_content(page_name):
    pages = {
        "terms": {
            "title": "Terms & Conditions",
            "content": """
#### 1. Service Description
LegalLens provides **document review services only**. This is NOT a substitute for professional legal advice.
Our AI analyzes rental agreements for potential compliance issues with local housing regulations.

#### 2. User Responsibilities
- Users are solely responsible for reviewing AI findings with a qualified attorney
- Users must not rely on our analysis as legal advice
- Users acknowledge all compliance reviews are for informational purposes only

#### 3. Liability Limitation
LegalLens shall not be liable for any damages, losses, or consequences arising from the use of our service.
Professional legal consultation is required for legal decisions.

#### 4. Intellectual Property
All content, analysis methods, and reports are proprietary to LegalLens.

#### 5. Modifications
We reserve the right to modify terms at any time. Continued use implies acceptance.
            """
        },
        "contact": {
            "title": "Contact Us",
            "content": """
Have questions about LegalLens? We'd love to hear from you.

**Email:** contact@zartechai.com

**Hours:** Monday - Friday, 9AM - 5PM NZST

**Response Time:** We typically respond within 24 hours.

**For urgent legal matters:** Please contact a licensed attorney in your jurisdiction.
            """
        },
        "privacy": {
            "title": "Privacy Policy",
            "content": """
#### Data Collection
LegalLens collects:
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
            """
        },
        "about": {
            "title": "About LegalLens",
            "content": """
#### Our Mission
LegalLens empowers renters and landlords with **AI-powered document analysis** to identify potential
compliance issues in rental agreements before signing.

#### What We Do
We review rental agreements for:
- Compliance with local housing regulations
- Missing mandatory clauses
- Unfair or risky terms
- Red flags and negotiation opportunities

#### Important Disclaimer
⚠️ **LegalLens is NOT a substitute for professional legal advice.**

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
            """
        }
    }

    if page_name not in pages:
        return jsonify({"error": "Page not found"}), 404

    return jsonify(pages[page_name])


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    if not supabase:
        return jsonify({"error": "Database not available"}), 503

    payload = request.get_data()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        user_email = session["customer_details"]["email"]

        try:
            existing_record = supabase.table("access_keys") \
                .select("*") \
                .eq("stripe_session_id", session_id) \
                .execute()

            if existing_record.data:
                return jsonify({"status": "already_processed"})

            new_key = generate_key()
            supabase.table("access_keys").insert({
                "key": new_key,
                "is_used": False,
                "email_owner": user_email,
                "stripe_session_id": session_id
            }).execute()
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({"error": str(e)}), 500

        try:
            resend.Emails.send({
                "from": "LegalLens <contact@zartechai.com>",
                "cc": ["contact@zartechai.com"],
                "to": user_email,
                "subject": "🔑 Your LegalLens Access Key",
                "html": f"""
                    <div style="font-family: sans-serif; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
                        <h1 style="color: #2253b5;">Welcome to LegalLens!</h1>
                        <p>Your payment was successful. Use the access key below to begin your professional lease audit:</p>
                        <div style="background: linear-gradient(135deg, #2253b5 0%, #1a3d8b 100%); padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                            <h2 style="color: #ffffff; font-size: 32px; letter-spacing: 2px; margin: 0;">{new_key}</h2>
                        </div>
                        <p style="color: #666; font-size: 14px;">
                            This key is valid for a <b>single analysis</b>.
                            To use it, go to the LegalLens app and enter this key in the dashboard interface.
                        </p>
                    </div>
                """
            })
        except Exception as e:
            print(f"Resend error: {e}")

    return jsonify({"status": "success"})


if __name__ == "__main__":
    # Debug mode exposes an interactive debugger; keep it off unless explicitly enabled.
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    host = "127.0.0.1" if debug_mode else "0.0.0.0"
    app.run(host=host, port=8000, debug=debug_mode)