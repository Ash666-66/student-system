@echo off
echo 🚀 GitHub Repository Setup Script
echo ==================================

:: Get GitHub username
set /p github_username=Enter your GitHub username:

if "%github_username%"=="" (
    echo ❌ Error: GitHub username is required
    pause
    exit /b 1
)

set repo_name=student-system

echo.
echo 📋 Repository Information:
echo   Username: %github_username%
echo   Repository: %repo_name%
echo   URL: https://github.com/%github_username%/%repo_name%
echo.

:: Confirm
set /p confirm=Continue with these settings? (y/N):
if /i not "%confirm%"=="y" (
    echo ❌ Setup cancelled
    pause
    exit /b 1
)

echo.
echo 🔧 Setting up Git remote...

:: Rename branch to main
git branch -M main

:: Add remote origin
git remote add origin https://github.com/%github_username%/%repo_name%.git

echo ✅ Remote configured successfully!
echo.
echo 📝 Next Steps:
echo 1. Make sure you've created the repository '%repo_name%' on GitHub
echo 2. Run: git push -u origin main
echo.
echo 💡 If you haven't created the repository yet, visit:
echo    https://github.com/new
echo.
echo 🎉 Ready to push to GitHub!
pause