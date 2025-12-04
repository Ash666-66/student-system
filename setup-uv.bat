@echo off
echo 🎓 Setting up Student Course Selection System with uv...
echo ============================================

REM Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing uv...
    curl -LsSf https://astral.sh/uv/install.bat | powershell -c -
    echo.
    echo Please restart your command prompt and run this script again.
    pause
    exit /b 1
)

echo 🐍 Found uv
uv --version

echo 📋 Creating virtual environment...
uv venv

echo 📚 Installing dependencies...
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

echo 🗄️  Running database migrations...
.venv\Scripts\python.exe manage.py migrate

echo 🗄️  Collecting static files...
.venv\Scripts\python.exe manage.py collectstatic --noinput

echo ✅ Setup complete!
echo.
echo To activate the virtual environment:
echo   .venv\Scripts\activate
echo.
echo To start the development server:
echo   .venv\Scripts\activate
echo   python manage.py runserver
echo.
echo To create a superuser:
echo   .venv\Scripts\activate
echo   python manage.py createsuperuser
echo.
echo Happy coding! 🚀
pause