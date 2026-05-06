# LegaLens - Full-Stack AI Lease Analysis Application

A modern full-stack web application for AI-powered rental agreement compliance analysis. Built with FastAPI backend and Next.js frontend, featuring professional UI design with #2253b5 and black color scheme.

## 🚀 Features

- **AI-Powered Analysis**: GPT-4o powered lease agreement compliance checking
- **Jurisdiction Support**: 16+ jurisdictions including US states, UK, Canada, Scotland, and Ireland
- **Modern UI**: Professional design with responsive layout and smooth animations
- **Secure Authentication**: JWT-based authentication with access keys
- **PDF Reports**: Professional PDF generation with custom branding
- **Payment Integration**: Stripe webhook integration for access key management
- **Legal Pages**: Comprehensive terms, privacy, contact, and about pages

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Authentication**: JWT tokens with HTTP Bearer authentication
- **Database**: Supabase integration
- **AI**: OpenAI GPT-4o integration
- **File Processing**: PDF text extraction with PyPDF2
- **PDF Generation**: FPDF for professional reports

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom design system
- **State Management**: React hooks and localStorage
- **API Integration**: Axios with interceptors
- **Icons**: Lucide React icons

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- Supabase account
- OpenAI API key
- Stripe account

## 🔧 Installation & Setup

### 1. Clone and Setup Project Structure

```bash
# The project is already structured with backend/ and frontend/ directories
cd RealEstateAI
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

Edit `backend/.env` with your actual values:
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PAYMENT_LINK=https://buy.stripe.com/...
RESEND_API_KEY=re_...
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://...
SUPABASE_KEY=...
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local
```

Edit `frontend/.env.local` with your actual values:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PAYMENT_LINK=https://buy.stripe.com/...
```

### 4. Database Setup

Ensure your Supabase database has an `access_keys` table:

```sql
CREATE TABLE access_keys (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    email_owner VARCHAR(255),
    stripe_session_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Running the Application

### Development Mode

1. **Start Backend**:
```bash
cd backend
source venv/bin/activate
python main.py
```
Backend will run on `http://localhost:8000`

2. **Start Frontend**:
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:3000`

### Production Deployment

#### Backend Deployment
```bash
# Using Docker
cd backend
docker build -t leaseguard-backend .
docker run -p 8000:8000 leaseguard-backend

# Or using gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### Frontend Deployment
```bash
cd frontend
npm run build
npm start
# Or deploy to Vercel, Netlify, etc.
```

## 🔐 Environment Variables

### Backend (.env)
```env
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
RESEND_API_KEY=your_resend_api_key
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PAYMENT_LINK=https://buy.stripe.com/your-link
```

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - Login with access key
- `POST /webhook` - Stripe webhook handler

### Analysis
- `GET /jurisdictions` - Get available jurisdictions
- `POST /analyze` - Analyze PDF document
- `POST /generate-pdf` - Generate PDF report

### Pages
- `GET /pages/{page_name}` - Get page content (terms, contact, privacy, about)

## 🎨 Color Scheme

- **Primary**: #2253b5 (Professional blue)
- **Secondary**: Black (#000000)
- **Accent**: #94a3b8 (Light gray)
- **Background**: Gradient from #0a0a0a to #000000

## 🔒 Security Features

- JWT authentication with expiration
- CORS protection
- Input validation
- Secure file upload handling
- HTTPS enforcement in production

## 📱 Responsive Design

- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interactions
- Accessible navigation

## 🚀 Performance

- Lazy loading components
- Optimized images
- Efficient API calls
- Caching strategies

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

This project is proprietary software. All rights reserved.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For support, contact: contact@zartechai.com

## ⚠️ Legal Disclaimer

**LegaLens provides document review services only. This is NOT a substitute for professional legal advice. Users are solely responsible for reviewing AI findings with a qualified attorney.**
