#!/bin/bash
# Gemini MCP Server Installation Script

echo "🚀 Gemini MCP Server Installation"
echo "=================================="

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1-2)
required_version="3.8"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📝 Next steps:"
echo "1. Set your Gemini API key:"
echo "   export GEMINI_API_KEY='your-api-key-here'"
echo ""
echo "2. Test the installation:"
echo "   source .venv/bin/activate"
echo "   python demo.py"
echo ""
echo "3. Start the MCP server:"
echo "   python run_server.py"
echo ""
echo "🔗 For more information, see QUICKSTART.md"