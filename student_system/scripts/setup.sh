#!/bin/bash

# Student Course Selection System - Development Setup Script

set -e  # Exit on any error

echo "🎓 Setting up Student Course Selection System..."
echo "============================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    pip install uv
fi

echo "🔧 Creating virtual environment..."
uv venv

echo "📚 Installing dependencies..."
uv pip sync --dev

echo "🗄️  Setting up database..."
uv run python manage.py migrate

echo "👤 Creating superuser..."
uv run python manage.py createsuperuser

echo "🔧 Setting up pre-commit hooks..."
uv run pre-commit install

echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Start development server: uv run python manage.py runserver"
echo ""
echo "Happy coding! 🚀"