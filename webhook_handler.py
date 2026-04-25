import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from stripe import Webhook
import stripe
from supabase import create_client, Client
import resend
from dotenv import load_dotenv

load_dotenv()

# Config
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
resend.api_key = os.getenv("RESEND_API_KEY")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

def generate_key():
    return f"LL-{uuid.uuid4().hex[:8].upper()}"

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        user_email = session["customer_details"]["email"]

        # 1. Check for duplicate processing (Idempotency)
        existing_record = supabase.table("access_keys") \
            .select("*") \
            .eq("stripe_session_id", session_id) \
            .execute()

        if existing_record.data:
            return {"status": "already_processed"}

        # 2. Generate and store the unique key
        new_key = generate_key()
        supabase.table("access_keys").insert({
            "key": new_key,
            "is_used": False,
            "email_owner": user_email,
            "stripe_session_id": session_id
        }).execute()

        # 3. Send dynamic email via Resend
        try:
            resend.Emails.send({
                "from": "LegalLens <contact@zartech.co.nz>",
                "to": user_email,
                "subject": "🔑 Your LegalLens Access Key",
                "html": f"""
                    <div style="font-family: sans-serif; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
                        <h1 style="color: #333;">Welcome to LegalLens!</h1>
                        <p>Your payment was successful. Use the access key below to begin your professional lease audit:</p>
                        <div style="background: #f4f4f4; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                            <h2 style="color: #2e7d32; font-size: 32px; letter-spacing: 2px; margin: 0;">{new_key}</h2>
                        </div>
                        <p style="color: #666; font-size: 14px;">
                            This key is valid for a <b>single analysis</b>. 
                            To use it, go to the LegalLens app and enter this key in the sidebar.
                        </p>
                    </div>
                """
            })
        except Exception as e:
            print(f"Resend error: {e}")

    return {"status": "success"}