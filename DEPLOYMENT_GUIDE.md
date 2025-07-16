# Deployment Guide for Temporary Email Service

## Quick Deployment to Vercel

### Prerequisites
- Node.js installed
- Vercel CLI installed globally (`npm install -g vercel`)
- Git repository (optional but recommended)

### Steps

1. **Navigate to the frontend directory**:
   ```bash
   cd /app/frontend
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

4. **Follow the prompts**:
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - What's your project's name? `temporary-email-service`
   - In which directory is your code located? `./`

### Environment Variables

The deployment will automatically use the backend URL configured in `vercel.json`:
```json
{
  "env": {
    "REACT_APP_BACKEND_URL": "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com"
  }
}
```

### Manual Deployment Steps

If you prefer manual deployment:

1. **Build the project**:
   ```bash
   yarn build
   ```

2. **Deploy the build folder**:
   ```bash
   vercel --prod
   ```

### Custom Domain Setup

To use a custom domain like `temp.udayscripts.in`:

1. **In Vercel Dashboard**:
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain
   - Configure DNS records as shown

2. **DNS Configuration**:
   - Add CNAME record: `temp.udayscripts.in` → `cname.vercel-dns.com`
   - Or A record: `temp.udayscripts.in` → `76.76.19.19`

## Backend Configuration

The backend remains hosted at:
`https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api`

**Backend features**:
- ✅ cPanel API integration
- ✅ IMAP email fetching
- ✅ MongoDB storage
- ✅ Auto-cleanup system
- ✅ Rate limiting

## Post-Deployment Checklist

After deployment, verify:
- [ ] Frontend loads correctly
- [ ] Email generation works
- [ ] Email fetching works
- [ ] Account deletion works
- [ ] Responsive design works on mobile
- [ ] API endpoints are accessible

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure backend has proper CORS configuration
2. **API not accessible**: Check if backend URL is correct in environment variables
3. **Build failures**: Ensure all dependencies are installed with `yarn install`

### Backend Health Check

Test the backend API:
```bash
curl https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/
```

Expected response:
```json
{"message": "Temporary Email API is running"}
```

## Production Recommendations

1. **Custom Domain**: Use temp.udayscripts.in for branding
2. **SSL Certificate**: Vercel provides automatic SSL
3. **CDN**: Vercel includes global CDN
4. **Analytics**: Add Vercel Analytics for usage tracking
5. **Monitoring**: Set up uptime monitoring for the backend

## Files Created for Deployment

- `vercel.json`: Vercel configuration
- `API_DOCUMENTATION.md`: Complete API documentation
- `DEPLOYMENT_GUIDE.md`: This deployment guide
- Updated `package.json`: Added vercel-build script

## Next Steps

1. Deploy to Vercel using the commands above
2. Test the deployed application
3. Configure custom domain if desired
4. Set up monitoring and analytics
5. Share the live URL with users

Your temporary email service is now ready for production deployment! 🚀