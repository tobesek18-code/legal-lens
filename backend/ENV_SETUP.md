# 🔑 LegaLens - Environment Setup Guide

## Step 1: Create `.env` File
Copy the `.env.example` file and create `.env`:
```bash
cd /Users/zartech/PycharmProjects/RealEstateAI/backend
cp .env.example .env
```

## Step 2: Get Your API Keys

### 📌 Stripe Configuration
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to **Developers > API Keys**
3. Copy your **Secret Key** (starts with `sk_test_` or `sk_live_`)
4. For webhook secret:
   - Go to **Developers > Webhooks**
   - Create a new endpoint or find existing one
   - Copy the **Signing secret** (starts with `whsec_`)

**Add to `.env`:**
```env
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_key_here
```

### 📌 OpenAI Configuration
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Click **API keys** in the left sidebar
3. Click **Create new secret key**
4. Copy the key (starts with `sk-`)

**Add to `.env`:**
```env
OPENAI_API_KEY=sk_your_key_here
```

### 📌 Supabase Configuration
1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Select your project
3. Go to **Settings > API**
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Anon public key** → `SUPABASE_KEY`

**Add to `.env`:**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ****your_key_here
```

### 📌 Resend Email Service
1. Go to [Resend Dashboard](https://resend.com/dashboard)
2. Click **API Keys** in the left menu
3. Copy your API key (starts with `re_`)

**Add to `.env`:**
```env
RESEND_API_KEY=re_your_key_here
```

## Step 3: Update `.env` File
Edit `/Users/zartech/PycharmProjects/RealEstateAI/backend/.env` with your actual keys:
```env
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
RESEND_API_KEY=re_xxxxx
OPENAI_API_KEY=sk_xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ_xxxxx
```

## Step 4: Run the Application

### Backend (Terminal 1):
```bash
cd /Users/zartech/PycharmProjects/RealEstateAI/backend
python main.py
```
✅ Backend running on `http://localhost:8000`

### Frontend (Terminal 2):
```bash
cd /Users/zartech/PycharmProjects/RealEstateAI/frontend
npm run dev
```
✅ Frontend running on `http://localhost:3000`

## ✅ Complete!
Your LegaLens application is now fully functional! 🎉

### Features:
- ✅ AI-Powered Lease Analysis
- ✅ Jurisdiction-Specific Compliance Checks
- ✅ PDF Report Generation
- ✅ Stripe Payment Integration
- ✅ Professional Dashboard
- ✅ Access Key Management

---

## 🆘 Troubleshooting

**Error: "Invalid API key" for Supabase**
- Make sure you're using the **Anon public key**, not the Service Role key
- Check that `SUPABASE_URL` includes `https://` prefix

**Error: "Invalid Stripe Secret Key"**
- Use the **Secret Key**, not the Publishable Key
- Make sure it starts with `sk_test_` or `sk_live_`

**Error: Backend won't start**
- Ensure all 6 environment variables are set
- Check that Python 3.14 is being used

**Frontend won't connect to backend**
- Make sure backend is running on port 8000
- Check that `NEXT_PUBLIC_API_URL=http://localhost:8000` in frontend `.env.local`

