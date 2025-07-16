# Backend Deployment Guide 🚀

## Quick Overview

Your FastAPI backend needs to be deployed to a platform that supports:
- **Python applications**
- **Background tasks** (for email cleanup)
- **Persistent connections** (for MongoDB and IMAP)
- **Environment variables** (for cPanel credentials)

## 🏆 **Recommended Platforms**

### 1. **Railway** (Easiest & Best)
- ✅ **One-click deploy** from GitHub
- ✅ **Free tier** available
- ✅ **Automatic scaling**
- ✅ **Built-in PostgreSQL/MongoDB**
- ✅ **Perfect for FastAPI**

### 2. **Render** (Great Alternative)
- ✅ **Free tier** with some limitations
- ✅ **Auto-deploy** from Git
- ✅ **Good for Python apps**

### 3. **Digital Ocean App Platform**
- ✅ **Reliable** and fast
- ✅ **$5/month** starting price
- ✅ **Great performance**

---

## 🚀 **Option 1: Railway (Recommended)**

### Step 1: Prepare Your Code

```bash
# 1. Create a new directory for backend deployment
mkdir temp-email-backend
cd temp-email-backend

# 2. Copy backend files
cp -r /app/backend/* .

# 3. Create Railway-specific files
```

### Step 2: Create Railway Configuration

**Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn server:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**Create `Procfile`:**
```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Step 3: Deploy to Railway

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/temp-email-backend.git
   git push -u origin main
   ```

2. **Deploy via Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub"
   - Select your repository
   - Railway will auto-detect Python and deploy

3. **Set Environment Variables:**
   ```env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=temp_emails
   CPANEL_HOST=https://cpanel.udayscripts.in
   CPANEL_USER=udayscr1
   CPANEL_TOKEN=D0UHIIP2P42BGZWY8HSDW93U0CSR2Y3W
   DOMAIN=udayscripts.in
   SMTP_HOST=mail.udayscripts.in
   SMTP_PORT=465
   SMTP_USER=support@udayscripts.in
   SMTP_PASSWORD=###@UDAY381
   IMAP_HOST=mail.udayscripts.in
   IMAP_PORT=993
   ```

---

## 🚀 **Option 2: Render**

### Step 1: Create `render.yaml`

```yaml
services:
  - type: web
    name: temp-email-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn server:app --host 0.0.0.0 --port $PORT"
    healthCheckPath: "/api/"
    envVars:
      - key: MONGO_URL
        value: mongodb://localhost:27017
      - key: DB_NAME
        value: temp_emails
      - key: CPANEL_HOST
        value: https://cpanel.udayscripts.in
      - key: CPANEL_USER
        value: udayscr1
      - key: CPANEL_TOKEN
        value: D0UHIIP2P42BGZWY8HSDW93U0CSR2Y3W
      - key: DOMAIN
        value: udayscripts.in
      - key: IMAP_HOST
        value: mail.udayscripts.in
      - key: IMAP_PORT
        value: 993
```

### Step 2: Deploy to Render

1. **Push to GitHub** (same as Railway)
2. **Go to render.com**
3. **Connect GitHub** and select repository
4. **Deploy** - Render will auto-detect Python

---

## 🚀 **Option 3: Digital Ocean App Platform**

### Step 1: Create `.do/app.yaml`

```yaml
name: temp-email-api
services:
- name: api
  source_dir: /
  github:
    repo: yourusername/temp-email-backend
    branch: main
  run_command: uvicorn server:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  health_check:
    http_path: /api/
  envs:
  - key: MONGO_URL
    value: mongodb://localhost:27017
  - key: DB_NAME
    value: temp_emails
  - key: CPANEL_HOST
    value: https://cpanel.udayscripts.in
  - key: CPANEL_USER
    value: udayscr1
  - key: CPANEL_TOKEN
    value: D0UHIIP2P42BGZWY8HSDW93U0CSR2Y3W
  - key: DOMAIN
    value: udayscripts.in
  - key: IMAP_HOST
    value: mail.udayscripts.in
  - key: IMAP_PORT
    value: 993
```

---

## 🗄️ **Database Options**

### Option A: MongoDB Atlas (Recommended)
```bash
# 1. Sign up at mongodb.com/atlas
# 2. Create free cluster
# 3. Get connection string
# 4. Update MONGO_URL in environment variables

MONGO_URL=mongodb+srv://username:password@cluster0.mongodb.net/temp_emails?retryWrites=true&w=majority
```

### Option B: Railway PostgreSQL
```bash
# Railway provides free PostgreSQL
# You'll need to modify the code to use PostgreSQL instead of MongoDB
```

---

## 🔧 **Pre-Deployment Checklist**

### Update Backend Code for Production

**Update `server.py`:**
```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Temporary Email API", version="1.0.0")

# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-frontend.vercel.app"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use environment port
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Update `requirements.txt`:**
```txt
fastapi==0.110.1
uvicorn==0.25.0
boto3>=1.34.129
requests-oauthlib>=2.0.0
cryptography>=42.0.8
python-dotenv>=1.0.1
pymongo==4.5.0
pydantic>=2.6.4
email-validator>=2.2.0
pyjwt>=2.10.1
passlib>=1.7.4
tzdata>=2024.2
motor==3.3.1
pytest>=8.0.0
black>=24.1.1
isort>=5.13.2
flake8>=7.0.0
mypy>=1.8.0
python-jose>=3.3.0
requests>=2.31.0
pandas>=2.2.0
numpy>=1.26.0
python-multipart>=0.0.9
jq>=1.6.0
typer>=0.9.0
imapclient>=3.0.1
python-dateutil>=2.8.2
bcrypt>=4.1.0
html2text>=2025.4.15
```

---

## 📝 **Complete Deployment Script**

```bash
#!/bin/bash

echo "🚀 Deploying Backend to Railway..."

# 1. Create deployment directory
mkdir -p temp-email-backend
cd temp-email-backend

# 2. Copy backend files
cp -r /app/backend/* .

# 3. Create Railway configuration
cat > railway.json << 'EOF'
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn server:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF

# 4. Create Procfile
echo "web: uvicorn server:app --host 0.0.0.0 --port \$PORT" > Procfile

# 5. Initialize git
git init
git add .
git commit -m "Initial backend deployment"

echo "✅ Backend prepared for deployment!"
echo "📋 Next steps:"
echo "1. Push to GitHub: git remote add origin <your-repo-url> && git push -u origin main"
echo "2. Deploy to Railway: Connect GitHub repo at railway.app"
echo "3. Set environment variables in Railway dashboard"
echo "4. Update frontend REACT_APP_BACKEND_URL with new Railway URL"
```

---

## 🔄 **Update Frontend After Backend Deployment**

After deploying backend, update your frontend:

**Update `/app/frontend/.env`:**
```env
REACT_APP_BACKEND_URL=https://your-railway-app.railway.app
```

**Update `/app/frontend/vercel.json`:**
```json
{
  "env": {
    "REACT_APP_BACKEND_URL": "https://your-railway-app.railway.app"
  }
}
```

---

## 🎯 **Quick Start (Railway)**

1. **Create GitHub repo** with backend code
2. **Go to [railway.app](https://railway.app)**
3. **Click "Deploy from GitHub"**
4. **Select repository**
5. **Set environment variables**
6. **Deploy!**

Your backend will be live at: `https://your-app.railway.app`

---

## 🔍 **Testing Deployed Backend**

```bash
# Test health check
curl https://your-deployed-backend.railway.app/api/

# Test email creation
curl -X POST "https://your-deployed-backend.railway.app/api/email/create" \
  -H "Content-Type: application/json" \
  -d '{"expiration_minutes": 60}'
```

---

## 💡 **Pro Tips**

1. **Use Railway** for easiest deployment
2. **MongoDB Atlas** for database (free tier)
3. **Set up monitoring** with Railway dashboard
4. **Use environment variables** for all secrets
5. **Enable auto-deploy** from GitHub
6. **Test thoroughly** before switching frontend URL

Your backend will be production-ready with proper scaling, monitoring, and security! 🚀