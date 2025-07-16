#!/bin/bash

# Deployment script for Temporary Email Service to Vercel

echo "🚀 Starting deployment to Vercel..."

# Check if we're in the correct directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
yarn install

# Build the project
echo "🔨 Building project..."
yarn build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

# Deploy to Vercel
echo "🌍 Deploying to Vercel..."
vercel --prod

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo "🎉 Deployment successful!"
    echo ""
    echo "📋 Deployment Summary:"
    echo "   Frontend: Deployed to Vercel"
    echo "   Backend: Running at https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api"
    echo "   API Docs: Available at /docs.html"
    echo ""
    echo "🔗 Links:"
    echo "   Live App: Check Vercel output above"
    echo "   API Health: https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api/"
    echo ""
    echo "✅ Your temporary email service is now live!"
else
    echo "❌ Deployment failed!"
    exit 1
fi