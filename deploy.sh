#!/bin/bash

# LegaLens - DigitalOcean Quick Deploy Script
# Usage: bash deploy.sh

set -e

echo "🚀 LegaLens - DigitalOcean Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${YELLOW}ℹ️  Running on macOS - building locally${NC}"
    IS_MAC=true
else
    echo -e "${YELLOW}ℹ️  Running on Linux - assuming Droplet environment${NC}"
    IS_MAC=false
fi

# Step 1: Build Frontend
echo ""
echo -e "${YELLOW}📦 Step 1: Building Frontend...${NC}"
cd frontend
npm install
npm run build
cd ..
echo -e "${GREEN}✓ Frontend built successfully${NC}"

# Step 2: Prepare Backend
echo ""
echo -e "${YELLOW}📦 Step 2: Preparing Backend...${NC}"
cd backend

if [ "$IS_MAC" = true ]; then
    # macOS - using python3.11
    python3.11 -m venv venv
    source venv/bin/activate
else
    # Linux Droplet
    python3.11 -m venv venv
    source venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Step 3: Check Environment Variables
echo ""
echo -e "${YELLOW}🔑 Step 3: Checking Environment Variables...${NC}"

if [ ! -f ".env.production" ]; then
    echo -e "${RED}✗ Missing .env.production file${NC}"
    echo -e "${YELLOW}Create .env.production with:${NC}"
    cat << 'EOF'
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_key
RESEND_API_KEY=re_your_key
OPENAI_API_KEY=sk_your_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_key
FLASK_ENV=production
EOF
    exit 1
fi
echo -e "${GREEN}✓ Environment variables configured${NC}"

# Step 4: Test Backend
echo ""
echo -e "${YELLOW}🧪 Step 4: Testing Backend...${NC}"
timeout 5 python main.py &
sleep 3
if curl -s http://localhost:8000/jurisdictions > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is working${NC}"
else
    echo -e "${RED}✗ Backend test failed${NC}"
    exit 1
fi
kill %1 2>/dev/null || true

cd ..

# Step 5: Create Deployment Archive
echo ""
echo -e "${YELLOW}📦 Step 5: Creating Deployment Archive...${NC}"
ZIP_FILE="leaseguard-pro-$(date +%Y%m%d-%H%M%S).zip"
zip -r "$ZIP_FILE" \
    frontend/.next \
    backend/venv \
    backend/main.py \
    backend/requirements.txt \
    backend/knowledge_base.py \
    backend/.env.production \
    frontend/.env.production \
    -x "*/node_modules/*" "*/.*"

echo -e "${GREEN}✓ Created $ZIP_FILE${NC}"

# Step 6: Display Next Steps
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Build Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Upload to DigitalOcean Droplet:"
echo "   scp $ZIP_FILE root@YOUR_DROPLET_IP:/var/www/"
echo ""
echo "2. SSH into Droplet:"
echo "   ssh root@YOUR_DROPLET_IP"
echo ""
echo "3. Extract and run:"
echo "   cd /var/www"
echo "   unzip $ZIP_FILE"
echo "   systemctl restart leaseguard-backend"
echo "   systemctl restart leaseguard-frontend"
echo ""
echo -e "${YELLOW}For complete guide, see: DIGITALOCEAN_DEPLOYMENT.md${NC}"
echo ""

