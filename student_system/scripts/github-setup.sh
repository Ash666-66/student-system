#!/bin/bash

# GitHub Repository Setup Script for Student Course Selection System

echo "🚀 GitHub Repository Setup Script"
echo "=================================="

# Get GitHub username
echo -n "Enter your GitHub username: "
read github_username

if [ -z "$github_username" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

# Repository name
repo_name="student-system"

echo "📋 Repository Information:"
echo "  Username: $github_username"
echo "  Repository: $repo_name"
echo "  URL: https://github.com/$github_username/$repo_name"
echo ""

# Confirm
echo -n "Continue with these settings? (y/N): "
read confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "🔧 Setting up Git remote..."

# Rename branch to main
git branch -M main

# Add remote origin
git remote add origin https://github.com/$github_username/$repo_name.git

echo "✅ Remote configured successfully!"
echo ""
echo "📝 Next Steps:"
echo "1. Make sure you've created the repository '$repo_name' on GitHub"
echo "2. Run: git push -u origin main"
echo ""
echo "💡 If you haven't created the repository yet, visit:"
echo "   https://github.com/new"
echo ""
echo "🎉 Ready to push to GitHub!"