@echo off
echo 🎓 Setting up Student Course Selection System...
echo ============================================

REM Check if uv is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing uv...
    pip install uv
)

echo 🔧 Creating virtual environment...
uv venv

echo 📚 Installing dependencies...
uv pip sync --dev

echo 🗄️ Setting up database...
uv run python manage.py migrate

echo 👤 Creating superuser...
uv run python manage.py createsuperuser

echo ✅ Setup complete!
echo.
echo To start development:
echo   1. Activate virtual environment: .venv\Scripts\activate
echo   2. Start development server: uv run python manage.py runserver
echo.
echo Happy coding! 🚀

pause