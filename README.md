# Temporary Email Service 📧

A full-featured temporary email service built with React, FastAPI, and MongoDB. Generate disposable email addresses that automatically expire, perfect for testing, avoiding spam, or temporary registrations.

## 🌟 Features

- ✅ **Generate temporary email addresses** (@udayscripts.in)
- ✅ **Real-time email fetching** via IMAP
- ✅ **Auto-expiration** (customizable, default 1 hour)
- ✅ **Mobile-responsive design** with Tailwind CSS
- ✅ **HTML email rendering** with text fallback
- ✅ **RESTful API** for integration
- ✅ **Automatic cleanup** of expired accounts
- ✅ **cPanel integration** for real email accounts
- ✅ **Copy-to-clipboard** functionality
- ✅ **Real-time countdown** timer

## 🚀 Live Demo

- **Frontend**: [Deploy to Vercel](#deployment)
- **Backend**: https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api
- **API Docs**: `/docs.html` (available after deployment)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  cPanel + IMAP  │
│                 │    │                 │    │                 │
│ • Email UI      │◄──►│ • Email API     │◄──►│ • Email Creation│
│ • Responsive    │    │ • IMAP Client   │    │ • Mail Storage  │
│ • Real-time     │    │ • Auto-cleanup  │    │ • SSL/TLS       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        ▼                        │
         │              ┌─────────────────┐                │
         │              │    MongoDB      │                │
         │              │                 │                │
         └──────────────►│ • Email Accounts│◄───────────────┘
                        │ • Messages      │
                        │ • Metadata      │
                        └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **React** - UI framework
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Vercel** - Deployment

### Backend
- **FastAPI** - Python web framework
- **MongoDB** - Database
- **IMAPClient** - Email fetching
- **Requests** - cPanel API integration
- **Pydantic** - Data validation

### Infrastructure
- **cPanel** - Email account management
- **IMAP/SMTP** - Email protocols
- **SSL/TLS** - Security

## 📚 API Documentation

### Base URL
```
https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api
```

### Endpoints

#### Create Temporary Email
```bash
POST /email/create
Content-Type: application/json

{
  "expiration_minutes": 60
}
```

#### Get Email Info
```bash
GET /email/{email_address}/info
```

#### Get Messages
```bash
GET /email/{email_address}/messages
```

#### Delete Email
```bash
DELETE /email/{email_address}
```

[📖 Full API Documentation](./API_DOCUMENTATION.md)

## 🚀 Deployment

### Quick Deploy to Vercel

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Run deployment script**:
   ```bash
   ./deploy.sh
   ```

4. **Follow prompts** and get your live URL!

### Manual Deployment

1. **Build the project**:
   ```bash
   yarn build
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

[📖 Detailed Deployment Guide](./DEPLOYMENT_GUIDE.md)

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
REACT_APP_BACKEND_URL=https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com
```

#### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CPANEL_HOST=https://cpanel.udayscripts.in
CPANEL_USER=udayscr1
CPANEL_TOKEN=your_token_here
DOMAIN=udayscripts.in
IMAP_HOST=mail.udayscripts.in
IMAP_PORT=993
```

### cPanel Configuration

1. **API Token**: Generate in cPanel Security settings
2. **MX Records**: Configure for mail.udayscripts.in
3. **SSL**: Enable for secure connections

## 📱 Usage Examples

### JavaScript
```javascript
const API_BASE = 'https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api';

// Create temporary email
const response = await fetch(`${API_BASE}/email/create`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ expiration_minutes: 60 })
});

const emailData = await response.json();
console.log('Created email:', emailData.email);
```

### Python
```python
import requests

API_BASE = 'https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api'

# Create temporary email
response = requests.post(f'{API_BASE}/email/create', 
                        json={'expiration_minutes': 60})
email_data = response.json()
print(f"Created email: {email_data['email']}")
```

### cURL
```bash
curl -X POST "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/email/create" \
  -H "Content-Type: application/json" \
  -d '{"expiration_minutes": 60}'
```

## 🔒 Security Features

- **SSL/TLS encryption** for all connections
- **Rate limiting** to prevent abuse
- **Auto-cleanup** of expired accounts
- **Secure password generation** for email accounts
- **CORS protection** for API endpoints

## 🎯 Use Cases

- **Testing** - Register for services without using real email
- **Privacy** - Avoid giving out personal email addresses
- **Development** - Test email functionality in applications
- **Temporary access** - One-time registrations
- **Spam prevention** - Protect your inbox from unwanted emails

## 📥 Cloning a Specific Branch

To clone a specific branch of this repository (for example, `copilot/update-fastapi-to-latest-version`), use the `-b` flag with `git clone`:

```bash
git clone -b copilot/update-fastapi-to-latest-version https://github.com/UdayScripts/temp.git
```

This clones only the specified branch. To also fetch all other branches, run:

```bash
git fetch --all
```

Alternatively, clone the full repository and then switch to the desired branch:

```bash
git clone https://github.com/UdayScripts/temp.git
cd temp
git checkout copilot/update-fastapi-to-latest-version
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For technical support or questions:
- Check the [API Documentation](./API_DOCUMENTATION.md)
- Review the [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- Open an issue on GitHub

## 🚀 Roadmap

- [ ] **Email forwarding** - Forward emails to real addresses
- [ ] **Attachment support** - Handle email attachments
- [ ] **Custom domains** - Support multiple domains
- [ ] **Analytics dashboard** - Usage statistics
- [ ] **Mobile app** - Native iOS/Android apps
- [ ] **Email templates** - Pre-built email formats
- [ ] **Webhooks** - Real-time notifications
- [ ] **Email aliases** - Multiple addresses per account

## 📊 Performance

- **Email generation**: ~2-3 seconds (includes cPanel account creation)
- **Email fetching**: ~1-2 seconds via IMAP
- **Auto-cleanup**: Every 10 minutes
- **Concurrent users**: Scales with server capacity
- **Storage**: MongoDB with TTL indexing

## 🏆 Achievements

- ✅ **Full cPanel integration** - Real email accounts
- ✅ **Production-ready** - Comprehensive error handling
- ✅ **Mobile-first design** - Works on all devices
- ✅ **RESTful API** - Clean, documented endpoints
- ✅ **Real-time updates** - Live email fetching
- ✅ **Auto-cleanup** - No manual maintenance needed

---

**Built with ❤️ by the development team**

*Making temporary email services accessible and secure for everyone.*