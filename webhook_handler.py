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
        user_email = session["customer_details"]["email"]
        new_key = generate_key()

        # 1. Insert into Supabase
        supabase.table("access_keys").insert({
            "key": new_key,
            "is_used": False,
            "email_owner": user_email
        }).execute()

        # 2. Email the user via Resend
        resend.Emails.send({
            "from": "LegalLens <contact@zartech.co.nz>", # Replace with your verified domain
            "to": 'tobesek18@gmail.com',
            "subject": "🔑 Your LegalLens Access Key",
            "html": f"""
                <h1>Welcome to LegalLens!</h1>
                <p>Your payment was successful. Use the key below to analyze your lease:</p>
                <h2 style="color: #2e7d32;">{new_key}</h2>
                <p><i>Note: This key is valid for a single analysis.</i></p>
                {event["type"]}
                {event["data"]["object"]}
            """
        })

    return {"status": "success"}