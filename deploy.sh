#!/bin/bash

echo "🚀 Medical LSTM Chatbot Deployment Script"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy medical chatbot - $(date)"

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No remote repository configured."
    echo "Please run the following commands:"
    echo ""
    echo "1. Create a new repository on GitHub"
    echo "2. Then run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. Deploy to Railway/Render using the web interface"
else
    echo "🌐 Pushing to remote repository..."
    git push origin main
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "🎉 Next steps:"
    echo "1. Go to Railway.app or Render.com"
    echo "2. Create new project"
    echo "3. Connect your GitHub repository"
    echo "4. Deploy!"
fi

echo ""
echo "📋 Files prepared for deployment:"
echo "✅ Procfile"
echo "✅ runtime.txt" 
echo "✅ requirements.txt"
echo "✅ .gitignore"
echo "✅ lstm_web_interface.py (production ready)"
echo ""
echo "🔗 Your chatbot will be available at the URL provided by the platform" 