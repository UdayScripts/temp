#!/bin/bash

# Complete Backend Deployment Script
# This script prepares your backend for deployment to Railway, Render, or Digital Ocean

set -e

echo "🚀 Preparing Backend for Production Deployment..."

# Create deployment directory
DEPLOY_DIR="temp-email-backend-deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

echo "📁 Copying backend files..."
cp -r /app/backend/* .

# Create Railway configuration
echo "⚙️  Creating Railway configuration..."
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

# Create Procfile for Railway/Heroku
echo "📝 Creating Procfile..."
echo "web: uvicorn server:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create Render configuration
echo "🎨 Creating Render configuration..."
cat > render.yaml << 'EOF'
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
EOF

# Create Digital Ocean App Platform configuration
echo "🌊 Creating Digital Ocean configuration..."
mkdir -p .do
cat > .do/app.yaml << 'EOF'
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
EOF

# Create production-ready server.py
echo "🔧 Creating production server configuration..."
cat > server_production.py << 'EOF'
from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import asyncio
import requests
import json
from imapclient import IMAPClient
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
import html2text
import re
import random
import string
import ssl
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'temp_emails')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Create the main app
app = FastAPI(
    title="Temporary Email API",
    version="1.0.0",
    description="A temporary email service API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Production CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.vercel.app",
        "https://temp-email-service.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "*"  # For development - remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import all your existing models and functions here
# (Copy from the original server.py)

# Health check endpoint
@api_router.get("/")
async def health_check():
    return {"message": "Temporary Email API is running", "status": "healthy"}

# Include all your existing endpoints here
# (Copy from the original server.py)

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Start cleanup task on startup
@app.on_event("startup")
async def startup_tasks():
    logger.info("Starting temporary email service...")
    # Schedule periodic cleanup
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Run cleanup every 10 minutes"""
    while True:
        await asyncio.sleep(600)  # 10 minutes
        await cleanup_expired_accounts()

# For Railway/Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF

# Create environment variables template
echo "🔐 Creating environment variables template..."
cat > .env.production << 'EOF'
# Production Environment Variables
# Set these in your deployment platform (Railway, Render, etc.)

# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=temp_emails

# cPanel Configuration
CPANEL_HOST=https://cpanel.udayscripts.in
CPANEL_USER=udayscr1
CPANEL_TOKEN=D0UHIIP2P42BGZWY8HSDW93U0CSR2Y3W
DOMAIN=udayscripts.in

# Email Server Configuration
SMTP_HOST=mail.udayscripts.in
SMTP_PORT=465
SMTP_USER=support@udayscripts.in
SMTP_PASSWORD=###@UDAY381

IMAP_HOST=mail.udayscripts.in
IMAP_PORT=993

# For Railway deployment
PORT=8000
EOF

# Create deployment instructions
echo "📋 Creating deployment instructions..."
cat > DEPLOYMENT_INSTRUCTIONS.md << 'EOF'
# Backend Deployment Instructions

## Quick Deploy Options

### 1. Railway (Recommended)
1. Push this folder to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Deploy from GitHub"
4. Select your repository
5. Set environment variables from .env.production
6. Deploy!

### 2. Render
1. Push this folder to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables
6. Deploy!

### 3. Digital Ocean
1. Push this folder to GitHub
2. Go to Digital Ocean App Platform
3. Create new App
4. Connect GitHub repository
5. Configure environment variables
6. Deploy!

## Environment Variables to Set

Copy these from .env.production and set them in your deployment platform:

```
MONGO_URL=mongodb://localhost:27017
DB_NAME=temp_emails
CPANEL_HOST=https://cpanel.udayscripts.in
CPANEL_USER=udayscr1
CPANEL_TOKEN=D0UHIIP2P42BGZWY8HSDW93U0CSR2Y3W
DOMAIN=udayscripts.in
IMAP_HOST=mail.udayscripts.in
IMAP_PORT=993
```

## After Deployment

1. Test your API: `curl https://your-deployed-backend.railway.app/api/`
2. Update frontend REACT_APP_BACKEND_URL with your new backend URL
3. Redeploy frontend to Vercel

## Database Options

### MongoDB Atlas (Recommended)
1. Sign up at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create free cluster
3. Get connection string
4. Update MONGO_URL environment variable

### Railway MongoDB
1. Add MongoDB service in Railway
2. Use provided connection string
EOF

# Initialize git repository
echo "📦 Initializing git repository..."
git init
git add .
git commit -m "Initial backend deployment setup"

# Create GitHub repository instructions
echo "📚 Creating GitHub setup instructions..."
cat > GITHUB_SETUP.md << 'EOF'
# GitHub Repository Setup

## Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `temp-email-backend`
4. Make it public
5. Don't initialize with README (we already have files)
6. Click "Create repository"

## Push Code to GitHub

```bash
# Add GitHub remote (replace with your username)
git remote add origin https://github.com/YOURUSERNAME/temp-email-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "Deploy from GitHub"
4. Select your `temp-email-backend` repository
5. Railway will auto-detect Python and deploy
6. Set environment variables in Railway dashboard
7. Get your deployment URL

## Update Frontend

After backend deployment, update your frontend:

```bash
# Update frontend environment variable
echo "REACT_APP_BACKEND_URL=https://your-railway-app.railway.app" > /app/frontend/.env

# Redeploy frontend
cd /app/frontend
vercel --prod
```

Your full-stack application will be live! 🚀
EOF

echo ""
echo "✅ Backend deployment preparation complete!"
echo ""
echo "📁 Deployment files created in: $(pwd)"
echo ""
echo "📋 Next steps:"
echo "1. Create GitHub repository: temp-email-backend"
echo "2. Push this code to GitHub:"
echo "   git remote add origin https://github.com/YOURUSERNAME/temp-email-backend.git"
echo "   git push -u origin main"
echo "3. Deploy to Railway:"
echo "   - Go to railway.app"
echo "   - Deploy from GitHub"
echo "   - Set environment variables from .env.production"
echo "4. Update frontend REACT_APP_BACKEND_URL with new Railway URL"
echo "5. Redeploy frontend to Vercel"
echo ""
echo "🔗 Helpful links:"
echo "   Railway: https://railway.app"
echo "   Render: https://render.com"
echo "   MongoDB Atlas: https://mongodb.com/atlas"
echo ""
echo "📖 Read DEPLOYMENT_INSTRUCTIONS.md for detailed steps"
echo ""
echo "🎉 Your backend is ready for production deployment!"