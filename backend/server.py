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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Temporary Email API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic Models
class EmailAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    active: bool = True
    last_checked: Optional[datetime] = None

class EmailMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_email: str
    uid: int
    sender: str
    subject: str
    date: datetime
    body_text: str
    body_html: str
    attachments: List[Dict[str, Any]] = []
    received_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False

class EmailAccountCreate(BaseModel):
    expiration_minutes: int = 60

class EmailAccountResponse(BaseModel):
    email: str
    password: str
    expires_at: datetime
    remaining_time: int

# Helper Functions
def generate_random_string(length: int = 10) -> str:
    """Generate random string for email username"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_password(length: int = 12) -> str:
    """Generate secure password for email account"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for i in range(length))

async def create_cpanel_email(username: str, password: str, domain: str) -> bool:
    """Create email account using cPanel API"""
    try:
        url = f"{os.environ['CPANEL_HOST']}/execute/Email/add_pop"
        headers = {
            "Authorization": f"cpanel {os.environ['CPANEL_USER']}:{os.environ['CPANEL_TOKEN']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "email": username,
            "password": password,
            "domain": domain,
            "quota": 100,  # 100MB quota
            "skip_update_db": 0
        }
        
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=30)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == 1:
            logger.info(f"Successfully created email account: {username}@{domain}")
            return True
        else:
            logger.error(f"Failed to create email account: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error creating cPanel email: {str(e)}")
        return False

async def delete_cpanel_email(email_address: str) -> bool:
    """Delete email account using cPanel API"""
    try:
        url = f"{os.environ['CPANEL_HOST']}/execute/Email/delete_pop"
        headers = {
            "Authorization": f"cpanel {os.environ['CPANEL_USER']}:{os.environ['CPANEL_TOKEN']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "email": email_address
        }
        
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=30)
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == 1:
            logger.info(f"Successfully deleted email account: {email_address}")
            return True
        else:
            logger.error(f"Failed to delete email account: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error deleting cPanel email: {str(e)}")
        return False

def parse_email_content(email_message) -> tuple:
    """Parse email content and extract text and HTML"""
    body_text = ""
    body_html = ""
    
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body_text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                elif content_type == "text/html":
                    body_html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content_type = email_message.get_content_type()
            payload = email_message.get_payload(decode=True)
            if payload:
                content = payload.decode('utf-8', errors='ignore')
                if content_type == "text/html":
                    body_html = content
                    body_text = html2text.html2text(content)
                else:
                    body_text = content
    except Exception as e:
        logger.error(f"Error parsing email content: {str(e)}")
        body_text = "Error parsing email content"
        
    return body_text, body_html

async def fetch_emails_from_imap(account: EmailAccount) -> List[EmailMessage]:
    """Fetch emails from IMAP server"""
    emails = []
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with IMAPClient(host=os.environ['IMAP_HOST'], port=int(os.environ['IMAP_PORT']), ssl=True, ssl_context=context) as imap_client:
            try:
                imap_client.login(account.email, account.password)
                imap_client.select_folder('INBOX')
                
                # Search for all messages
                messages = imap_client.search(['NOT', 'DELETED'])
                
                if messages:
                    # Fetch message data
                    response = imap_client.fetch(messages, ['RFC822', 'ENVELOPE'])
                    
                    for uid, message_data in response.items():
                        try:
                            email_message = email.message_from_bytes(message_data[b'RFC822'])
                            envelope = message_data[b'ENVELOPE']
                            
                            # Parse email content
                            body_text, body_html = parse_email_content(email_message)
                            
                            # Extract date
                            date_str = email_message.get('Date', '')
                            try:
                                email_date = email.utils.parsedate_to_datetime(date_str)
                            except:
                                email_date = datetime.utcnow()
                            
                            email_obj = EmailMessage(
                                account_email=account.email,
                                uid=uid,
                                sender=email_message.get('From', ''),
                                subject=email_message.get('Subject', ''),
                                date=email_date,
                                body_text=body_text,
                                body_html=body_html,
                                attachments=[]
                            )
                            emails.append(email_obj)
                            
                        except Exception as e:
                            logger.error(f"Error processing email UID {uid}: {str(e)}")
                            continue
                            
            except Exception as e:
                logger.error(f"IMAP connection error for {account.email}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error fetching emails for {account.email}: {str(e)}")
        
    return emails

# Background Tasks
async def cleanup_expired_accounts():
    """Background task to cleanup expired email accounts"""
    try:
        current_time = datetime.utcnow()
        expired_accounts = await db.email_accounts.find({
            "expires_at": {"$lt": current_time},
            "active": True
        }).to_list(100)
        
        for account_doc in expired_accounts:
            account = EmailAccount(**account_doc)
            
            # Delete from cPanel
            await delete_cpanel_email(account.email)
            
            # Mark as inactive in database
            await db.email_accounts.update_one(
                {"id": account.id},
                {"$set": {"active": False}}
            )
            
            # Delete associated emails
            await db.emails.delete_many({"account_email": account.email})
            
            logger.info(f"Cleaned up expired account: {account.email}")
            
    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")

# API Endpoints
@api_router.post("/email/create", response_model=EmailAccountResponse)
async def create_temporary_email(request: EmailAccountCreate, background_tasks: BackgroundTasks):
    """Create a new temporary email account"""
    try:
        # Generate random username and password
        username = generate_random_string(10)
        password = generate_password()
        domain = os.environ['DOMAIN']
        email_address = f"{username}@{domain}"
        
        # Calculate expiration time
        expiration_time = datetime.utcnow() + timedelta(minutes=request.expiration_minutes)
        
        # Create email account via cPanel
        success = await create_cpanel_email(username, password, domain)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create email account")
        
        # Save to database
        account = EmailAccount(
            email=email_address,
            password=password,
            expires_at=expiration_time
        )
        
        await db.email_accounts.insert_one(account.dict())
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_expired_accounts)
        
        # Calculate remaining time in seconds
        remaining_seconds = int((expiration_time - datetime.utcnow()).total_seconds())
        
        return EmailAccountResponse(
            email=email_address,
            password=password,
            expires_at=expiration_time,
            remaining_time=remaining_seconds
        )
        
    except Exception as e:
        logger.error(f"Error creating temporary email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create temporary email: {str(e)}")

@api_router.get("/email/{email_address}/messages", response_model=List[EmailMessage])
async def get_emails(email_address: str):
    """Get all emails for a specific email address"""
    try:
        # Check if account exists and is active
        account_doc = await db.email_accounts.find_one({
            "email": email_address,
            "active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not account_doc:
            raise HTTPException(status_code=404, detail="Email account not found or expired")
        
        account = EmailAccount(**account_doc)
        
        # Fetch emails from IMAP
        emails = await fetch_emails_from_imap(account)
        
        # Store/update emails in database
        for email_obj in emails:
            await db.emails.update_one(
                {"account_email": email_address, "uid": email_obj.uid},
                {"$set": email_obj.dict()},
                upsert=True
            )
        
        # Update last checked time
        await db.email_accounts.update_one(
            {"email": email_address},
            {"$set": {"last_checked": datetime.utcnow()}}
        )
        
        return emails
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get emails: {str(e)}")

@api_router.get("/email/{email_address}/info")
async def get_email_info(email_address: str):
    """Get information about email account"""
    try:
        account_doc = await db.email_accounts.find_one({
            "email": email_address,
            "active": True
        })
        
        if not account_doc:
            raise HTTPException(status_code=404, detail="Email account not found")
        
        account = EmailAccount(**account_doc)
        current_time = datetime.utcnow()
        
        if account.expires_at < current_time:
            raise HTTPException(status_code=410, detail="Email account has expired")
        
        remaining_seconds = int((account.expires_at - current_time).total_seconds())
        
        return {
            "email": account.email,
            "created_at": account.created_at,
            "expires_at": account.expires_at,
            "remaining_time": remaining_seconds,
            "active": account.active,
            "last_checked": account.last_checked
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting email info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get email info: {str(e)}")

@api_router.delete("/email/{email_address}")
async def delete_email_account(email_address: str):
    """Delete an email account"""
    try:
        # Check if account exists
        account_doc = await db.email_accounts.find_one({"email": email_address})
        if not account_doc:
            raise HTTPException(status_code=404, detail="Email account not found")
        
        # Delete from cPanel
        await delete_cpanel_email(email_address)
        
        # Mark as inactive in database
        await db.email_accounts.update_one(
            {"email": email_address},
            {"$set": {"active": False}}
        )
        
        # Delete associated emails
        await db.emails.delete_many({"account_email": email_address})
        
        return {"message": f"Email account {email_address} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting email account: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete email account: {str(e)}")

@api_router.get("/")
async def root():
    return {"message": "Temporary Email API is running"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Start cleanup task on startup
@app.on_event("startup")
async def startup_tasks():
    # Schedule periodic cleanup
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Run cleanup every 10 minutes"""
    while True:
        await asyncio.sleep(600)  # 10 minutes
        await cleanup_expired_accounts()