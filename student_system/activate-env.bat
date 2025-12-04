@echo off
echo 🎓 Activating Student Course Selection System Environment...
echo =========================================================

REM Activate virtual environment
call student_env\Scripts\activate

echo ✅ Virtual environment activated!
echo.
echo 📚 Installing project dependencies...
pip install -r requirements.txt

echo 🧪 Installing development dependencies...
pip install -r requirements-dev.txt

echo.
echo 🗄️ Running database migrations...
python manage.py migrate

echo ✅ Environment setup complete!
echo.
echo 🚀 To start the development server, run:
echo    python manage.py runserver
echo.
echo 💡 Your virtual environment is now active!
echo.

REM Keep the command prompt open with activated environment
cmd /k