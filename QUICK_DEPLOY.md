# 🚀 LegaLens - Quick Deployment to DigitalOcean

## 5-Minute Setup on DigitalOcean

### **Step 1: Create DigitalOcean Droplet (2 minutes)**

1. Go to https://cloud.digitalocean.com
2. Click **Create** → **Droplet**
3. Select:
   - **Image**: Ubuntu 22.04 x64
   - **Size**: $12/month (2GB RAM)
   - **Authentication**: Add SSH key
   - Click **Create**

### **Step 2: Connect to Droplet (30 seconds)**

```bash
ssh root@YOUR_DROPLET_IP
```

### **Step 3: Install Everything (2 minutes)**

```bash
# Copy and paste this entire block:

apt update && apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Install Python 3.11
apt install -y python3.11 python3.11-venv python3.11-dev

# Install other tools
apt install -y git nginx certbot python3-certbot-nginx npm

# Clone your repo
cd /var/www
git clone https://github.com/YOUR_USERNAME/RealEstateAI.git
cd RealEstateAI
```

### **Step 4: Setup Backend (1 minute)**

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create production .env file
cat > .env.production << 'EOF'
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_key
RESEND_API_KEY=re_your_key
OPENAI_API_KEY=sk_your_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_key
FLASK_ENV=production
EOF

# Edit with your real keys
nano .env.production
```

### **Step 5: Setup Frontend (1 minute)**

```bash
cd ../frontend

# Create production .env file
cat > .env.production << 'EOF'
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_STRIPE_PAYMENT_LINK=https://buy.stripe.com/your-link
EOF

# Build
npm install
npm run build
```

### **Step 6: Configure Nginx**

```bash
# Create Nginx config
cat > /etc/nginx/sites-available/leaseguard << 'EOF'
upstream frontend {
    server localhost:3000;
}

upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/leaseguard /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### **Step 7: Enable SSL**

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **Step 8: Create Services**

**Backend Service:**
```bash
cat > /etc/systemd/system/leaseguard-backend.service << 'EOF'
[Unit]
Description=LegaLens Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/RealEstateAI/backend
Environment="PATH=/var/www/RealEstateAI/backend/venv/bin"
EnvironmentFile=/var/www/RealEstateAI/backend/.env.production
ExecStart=/var/www/RealEstateAI/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

**Frontend Service:**
```bash
cat > /etc/systemd/system/leaseguard-frontend.service << 'EOF'
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
EOF
```

**Start Services:**
```bash
systemctl daemon-reload
systemctl enable leaseguard-backend leaseguard-frontend
systemctl start leaseguard-backend leaseguard-frontend

# Check status
systemctl status leaseguard-backend
systemctl status leaseguard-frontend
```

### **Step 9: Verify Deployment**

```bash
# Check if services are running
curl http://localhost:3000        # Frontend
curl http://localhost:8000/jurisdictions  # Backend

# Check logs
journalctl -u leaseguard-backend -f
journalctl -u leaseguard-frontend -f
```

---

## ✅ You're Live!

Your application is now running at:
- **Frontend**: https://yourdomain.com
- **API**: https://yourdomain.com/api

---

## 🔧 Useful Commands

```bash
# View logs
journalctl -u leaseguard-backend -f
journalctl -u leaseguard-frontend -f

# Restart services
systemctl restart leaseguard-backend
systemctl restart leaseguard-frontend

# Update code
cd /var/www/RealEstateAI
git pull origin main
systemctl restart leaseguard-backend leaseguard-frontend

# Monitor system
htop          # CPU/Memory usage
df -h         # Disk usage
nethogs       # Network usage
```

---

## 💰 Cost

| Item | Cost |
|------|------|
| Droplet (2GB, $12/mo) | $12 |
| Domain (optional) | $10-15 |
| SSL (free) | $0 |
| **Total** | **$12-27/month** |

---

## 📞 Troubleshooting

**Can't reach domain?**
- Check Nginx: `nginx -t && systemctl restart nginx`
- Check firewall: Allow ports 80, 443
- Check DNS: Make sure domain points to Droplet IP

**Backend not responding?**
```bash
systemctl restart leaseguard-backend
journalctl -u leaseguard-backend -n 50
```

**No SSL certificate?**
```bash
certbot renew --dry-run
certbot renew
```

---

##✨ Next: Read Full Guide

For advanced setup, monitoring, backups, and troubleshooting:
👉 See `DIGITALOCEAN_DEPLOYMENT.md`


