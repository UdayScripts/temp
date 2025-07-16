# Temporary Email Service API Documentation

## Overview

The Temporary Email Service provides a RESTful API for creating and managing temporary email addresses. This service allows users to generate disposable email addresses that automatically expire after a specified time period.

**Base URL**: `https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api`

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Rate Limiting

The API implements rate limiting to prevent abuse:
- **Email Creation**: 5 requests per minute per IP
- **Other endpoints**: No specific rate limits (subject to server capacity)

## API Endpoints

### 1. Health Check

Check if the API is running and accessible.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Temporary Email API is running"
}
```

**Status Codes**:
- `200 OK`: API is healthy

---

### 2. Create Temporary Email

Create a new temporary email address with specified expiration time.

**Endpoint**: `POST /email/create`

**Request Body**:
```json
{
  "expiration_minutes": 60
}
```

**Parameters**:
- `expiration_minutes` (integer, optional): Email expiration time in minutes. Default: 60 minutes

**Response**:
```json
{
  "email": "abc123def4@udayscripts.in",
  "password": "Xy9#kL2m4N8p",
  "expires_at": "2025-07-16T13:15:30.123456",
  "remaining_time": 3600
}
```

**Response Fields**:
- `email` (string): The generated temporary email address
- `password` (string): Password for the email account
- `expires_at` (string): ISO timestamp when the email expires
- `remaining_time` (integer): Remaining time in seconds

**Status Codes**:
- `200 OK`: Email created successfully
- `500 Internal Server Error`: Failed to create email account

**Example**:
```bash
curl -X POST "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/create" \
  -H "Content-Type: application/json" \
  -d '{"expiration_minutes": 60}'
```

---

### 3. Get Email Account Information

Retrieve information about a specific email account.

**Endpoint**: `GET /email/{email_address}/info`

**Parameters**:
- `email_address` (string): The email address to get information for

**Response**:
```json
{
  "email": "abc123def4@udayscripts.in",
  "created_at": "2025-07-16T12:15:30.123456",
  "expires_at": "2025-07-16T13:15:30.123456",
  "remaining_time": 3600,
  "active": true,
  "last_checked": "2025-07-16T12:20:30.123456"
}
```

**Response Fields**:
- `email` (string): The email address
- `created_at` (string): ISO timestamp when the email was created
- `expires_at` (string): ISO timestamp when the email expires
- `remaining_time` (integer): Remaining time in seconds
- `active` (boolean): Whether the email account is active
- `last_checked` (string, nullable): ISO timestamp when emails were last checked

**Status Codes**:
- `200 OK`: Email information retrieved successfully
- `404 Not Found`: Email account not found
- `410 Gone`: Email account has expired

**Example**:
```bash
curl "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in/info"
```

---

### 4. Get Email Messages

Retrieve all messages for a specific email account.

**Endpoint**: `GET /email/{email_address}/messages`

**Parameters**:
- `email_address` (string): The email address to get messages for

**Response**:
```json
[
  {
    "id": "uuid-string",
    "account_email": "abc123def4@udayscripts.in",
    "uid": 1,
    "sender": "sender@example.com",
    "subject": "Welcome to our service",
    "date": "2025-07-16T12:30:00.000000",
    "body_text": "Welcome! This is the plain text version of the email...",
    "body_html": "<html><body><h1>Welcome!</h1><p>This is the HTML version...</p></body></html>",
    "attachments": [],
    "received_at": "2025-07-16T12:30:15.123456",
    "read": false
  }
]
```

**Response Fields**:
- `id` (string): Unique identifier for the email message
- `account_email` (string): The recipient email address
- `uid` (integer): Unique identifier from the mail server
- `sender` (string): Email address of the sender
- `subject` (string): Email subject line
- `date` (string): ISO timestamp when the email was sent
- `body_text` (string): Plain text version of the email body
- `body_html` (string): HTML version of the email body
- `attachments` (array): List of email attachments (currently empty)
- `received_at` (string): ISO timestamp when the email was received
- `read` (boolean): Whether the email has been read

**Status Codes**:
- `200 OK`: Messages retrieved successfully (empty array if no messages)
- `404 Not Found`: Email account not found
- `410 Gone`: Email account has expired

**Example**:
```bash
curl "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in/messages"
```

---

### 5. Delete Email Account

Delete an email account and all associated messages.

**Endpoint**: `DELETE /email/{email_address}`

**Parameters**:
- `email_address` (string): The email address to delete

**Response**:
```json
{
  "message": "Email account abc123def4@udayscripts.in deleted successfully"
}
```

**Status Codes**:
- `200 OK`: Email account deleted successfully
- `404 Not Found`: Email account not found

**Example**:
```bash
curl -X DELETE "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in"
```

---

## Error Handling

All endpoints return JSON error responses with the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Error Codes**:
- `400 Bad Request`: Invalid request format or parameters
- `404 Not Found`: Resource not found
- `410 Gone`: Resource has expired
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Data Models

### EmailAccount
```json
{
  "id": "uuid-string",
  "email": "string",
  "password": "string",
  "created_at": "datetime",
  "expires_at": "datetime",
  "active": "boolean",
  "last_checked": "datetime | null"
}
```

### EmailMessage
```json
{
  "id": "uuid-string",
  "account_email": "string",
  "uid": "integer",
  "sender": "string",
  "subject": "string",
  "date": "datetime",
  "body_text": "string",
  "body_html": "string",
  "attachments": "array",
  "received_at": "datetime",
  "read": "boolean"
}
```

## Usage Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_BASE = 'https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api';

// Create temporary email
async function createTempEmail() {
  try {
    const response = await axios.post(`${API_BASE}/email/create`, {
      expiration_minutes: 60
    });
    return response.data;
  } catch (error) {
    console.error('Error creating email:', error.response.data);
  }
}

// Get emails
async function getEmails(emailAddress) {
  try {
    const response = await axios.get(`${API_BASE}/email/${emailAddress}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error getting emails:', error.response.data);
  }
}

// Usage
createTempEmail().then(emailData => {
  console.log('Created email:', emailData.email);
  
  // Check for emails every 10 seconds
  setInterval(() => {
    getEmails(emailData.email).then(emails => {
      console.log(`Found ${emails.length} emails`);
    });
  }, 10000);
});
```

### Python

```python
import requests
import time

API_BASE = 'https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api'

def create_temp_email(expiration_minutes=60):
    """Create a temporary email"""
    response = requests.post(f'{API_BASE}/email/create', 
                           json={'expiration_minutes': expiration_minutes})
    return response.json()

def get_emails(email_address):
    """Get emails for an address"""
    response = requests.get(f'{API_BASE}/email/{email_address}/messages')
    return response.json()

def delete_email(email_address):
    """Delete an email account"""
    response = requests.delete(f'{API_BASE}/email/{email_address}')
    return response.json()

# Usage
email_data = create_temp_email()
print(f"Created email: {email_data['email']}")

# Check for emails
while True:
    emails = get_emails(email_data['email'])
    print(f"Found {len(emails)} emails")
    time.sleep(10)
```

### cURL Examples

```bash
# Create temporary email
curl -X POST "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/create" \
  -H "Content-Type: application/json" \
  -d '{"expiration_minutes": 60}'

# Get email info
curl "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in/info"

# Get messages
curl "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in/messages"

# Delete email
curl -X DELETE "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/abc123def4@udayscripts.in"
```

## System Features

### Automatic Cleanup
- Email accounts are automatically deleted after expiration
- Background cleanup runs every 10 minutes
- Expired accounts are removed from both the mail server and database

### Email Fetching
- Emails are fetched from the IMAP server in real-time
- Supports both plain text and HTML email content
- Emails are stored in the database for quick retrieval

### Security Features
- Email accounts are created with strong random passwords
- SSL/TLS encryption for all IMAP connections
- Rate limiting to prevent abuse

## Limitations

1. **Email Sending**: The service only supports receiving emails, not sending
2. **Attachments**: Currently, email attachments are not fully supported
3. **Storage**: Emails are stored temporarily and deleted with the account
4. **Domain**: Only supports @udayscripts.in domain
5. **Concurrent Access**: Multiple clients accessing the same email may cause conflicts

## Support

For technical support or questions about the API, please contact the system administrator.

---

*Last updated: July 16, 2025*