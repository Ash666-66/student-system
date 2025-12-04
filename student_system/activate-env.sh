#!/bin/bash

echo "🎓 Activating Student Course Selection System Environment..."
echo "========================================================="

# Check if virtual environment exists
if [ ! -d "student_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv student_env
fi

echo "🔄 Activating virtual environment..."
source student_env/bin/activate

echo "📚 Installing project dependencies..."
pip install -r requirements.txt

echo "🧪 Installing development dependencies..."
pip install -r requirements-dev.txt

echo ""
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Environment setup complete!"
echo ""
echo "🚀 To start the development server, run:"
echo "    python manage.py runserver"
echo ""
echo "💡 Your virtual environment is now active!"