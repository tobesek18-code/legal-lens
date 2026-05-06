# 📚 LegaLens - DigitalOcean Deployment Guide

## Overview

This guide will help you deploy LegaLens on DigitalOcean using:
- **Backend**: Flask API on Python 3.11
- **Frontend**: Next.js on Node.js
- **Database**: Supabase (managed)
- **Email**: Resend
- **Payments**: Stripe

---

## 📋 Prerequisites

1. **DigitalOcean Account** - Create at [digitalocean.com](https://www.digitalocean.com)
2. **GitHub Account** - Push your code to GitHub for easy deployment
3. **Domain Name** - (Optional) For custom domain
4. **All API Keys Ready**:
   - Stripe (live keys for production)
   - Resend API key
   - OpenAI API key
   - Supabase credentials

---

## 🚀 Step 1: Prepare Your Application

### 1.1 Create Production Builds

**Frontend Build:**
```bash
cd /Users/zartech/PycharmProjects/RealEstateAI/frontend
npm run build
```

**Backend Verification:**
```bash
cd /Users/zartech/PycharmProjects/RealEstateAI/backend
pip install -r requirements.txt
python main.py  # Test it works
```

### 1.2 Push to GitHub

```bash
cd /Users/zartech/PycharmProjects/RealEstateAI
git init
git add .
git commit -m "Initial commit: LegaLens"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/RealEstateAI.git
git push -u origin main
```

### 1.3 Create `.env.production` Files

**Backend** (`backend/.env.production`):
```env
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
RESEND_API_KEY=re_your_key
OPENAI_API_KEY=sk_your_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_key
FLASK_ENV=production
DEBUG=False
```

**Frontend** (`frontend/.env.production`):
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_STRIPE_PAYMENT_LINK=https://buy.stripe.com/your-link
```

---

## 🌐 Step 2: Create DigitalOcean App Platform

### 2.1 Create App on App Platform (Easiest Method)

1. Log in to DigitalOcean Dashboard
2. Click **Create** → **App**
3. Connect your GitHub repository
4. DigitalOcean will auto-detect your project structure

### 2.2 Configure App Spec

Create `app.yaml` in project root:

```yaml
name: leaseguard-pro
services:
- name: backend
  github:
    repo: YOUR_USERNAME/RealEstateAI
    branch: main
  source_dir: backend
  build_command: pip install -r requirements.txt
  run_command: gunicorn -w 4 -b 0.0.0.0:8080 main:app
  envs:
  - key: STRIPE_SECRET_KEY
    value: ${STRIPE_SECRET_KEY}
  - key: STRIPE_WEBHOOK_SECRET
    value: ${STRIPE_WEBHOOK_SECRET}
  - key: RESEND_API_KEY
    value: ${RESEND_API_KEY}
  - key: OPENAI_API_KEY
    value: ${OPENAI_API_KEY}
  - key: SUPABASE_URL
    value: ${SUPABASE_URL}
  - key: SUPABASE_KEY
    value: ${SUPABASE_KEY}
  - key: FLASK_ENV
    value: production
  http_port: 8080
  
- name: frontend
  github:
    repo: YOUR_USERNAME/RealEstateAI
    branch: main
  source_dir: frontend
  build_command: npm install && npm run build
  run_command: npm start
  envs:
  - key: NEXT_PUBLIC_API_URL
    value: https://${backend.ondigitalocean.app}
  http_port: 3000

static_sites:
- name: docs
  source_dir: frontend/.next/static

```

---

## 🖥️ Step 3: Deploy on Droplet (Alternative Method)

### 3.1 Create Ubuntu Droplet

1. **Click Create** → **Droplet**
2. **Choose Image**: Ubuntu 22.04 x64
3. **Choose Size**: $12/month (2GB RAM, 2 vCPU) minimum
4. **Authentication**: Add SSH key
5. **Enable Backups**: Yes
6. **Click Create**

### 3.2 SSH Into Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

### 3.3 Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Install Python 3.11
apt install -y python3.11 python3.11-venv python3.11-dev

# Install Git
apt install -y git

# Install Nginx
apt install -y nginx

# Install Certbot for SSL
apt install -y certbot python3-certbot-nginx
```

### 3.4 Clone Repository

```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/RealEstateAI.git
cd RealEstateAI
```

### 3.5 Setup Backend

```bash
cd /var/www/RealEstateAI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env production file
nano .env.production
# Add all your production environment variables

# Test
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 3.6 Setup Frontend

```bash
cd /var/www/RealEstateAI/frontend

# Install dependencies
npm install

# Build
npm run build

# Install serving library
npm install -g pm2
```

### 3.7 Configure Nginx

Create `/etc/nginx/sites-available/leaseguard`:

```nginx
# Frontend
upstream frontend {
    server localhost:3000;
}

# Backend API
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/leaseguard /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 3.8 Setup SSL Certificate

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3.9 Create Systemd Services

**Backend Service** (`/etc/systemd/system/leaseguard-backend.service`):
```ini
[Unit]
Description=LegaLens Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/RealEstateAI/backend
Environment="PATH=/var/www/RealEstateAI/backend/venv/bin"
EnvironmentFile=/var/www/RealEstateAI/backend/.env.production
ExecStart=/var/www/RealEstateAI/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Frontend Service** (`/etc/systemd/system/leaseguard-frontend.service`):
```ini
[Unit]
Description=LegaLens Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/RealEstateAI/frontend
ExecStart=/usr/bin/npm start
Restart=always
Environment="NODE_ENV=production"

[Install]
WantedBy=multi-user.target
```

Enable services:
```bash
systemctl daemon-reload
systemctl enable leaseguard-backend
systemctl enable leaseguard-frontend
systemctl start leaseguard-backend
systemctl start leaseguard-frontend
```

---

## 🔒 Step 4: Setup Database

### Using Supabase (Recommended)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get your Supabase credentials
4. Add to environment variables

Your database is already managed in the cloud!

---

## 📊 Step 5: Monitor & Maintain

### Check Logs

```bash
# Backend logs
journalctl -u leaseguard-backend -f

# Frontend logs
journalctl -u leaseguard-frontend -f

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Enable Monitoring

```bash
# DigitalOcean provides built-in monitoring
# Check Droplet Dashboard → Graphs
```

### Backup

```bash
# Enable DigitalOcean backups in dashboard
# Or manually backup database:
# https://supabase.com/docs/guides/platform/backups
```

---

## 💰 Cost Estimation

| Service | Cost/Month |
|---------|-----------|
| DigitalOcean Droplet (2GB) | $12 |
| Managed Database (if used) | $15+ |
| Backups | Free with Droplet |
| **Total** | **~$12-27/month** |

*Supabase managed database is free tier available*

---

## 🆘 Troubleshooting

### Application won't start
```bash
# Check logs
journalctl -u leaseguard-backend -n 50
# Check environment variables
cat /var/www/RealEstateAI/backend/.env.production
```

### Port 8000 already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
```

### Nginx not working
```bash
# Test config
nginx -t
# Restart
systemctl restart nginx
```

### CORS errors
Add to `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 Support

- **DigitalOcean Docs**: https://docs.digitalocean.com
- **Supabase Support**: https://supabase.com/docs
- **Stripe Docs**: https://stripe.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Flask Docs**: https://flask.palletsprojects.com

---

## ✅ Deployment Checklist

- [ ] All API keys are valid (live keys for production)
- [ ] Environment variables configured
- [ ] SSL certificate installed
- [ ] Database backups enabled
- [ ] Monitoring enabled
- [ ] Custom domain configured
- [ ] Payment webhooks working
- [ ] Email service working
- [ ] Error logging setup
- [ ] Performance tested under load

---

**Your LegaLens is now live on DigitalOcean!** 🎉

