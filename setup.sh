#!/bin/bash

# Stock Sentiment Analyzer - Setup Script
# This script sets up the environment and installs dependencies

echo "=================================="
echo "Stock Sentiment Analyzer Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (recommended) [y/N]: " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    echo "✓ Virtual environment created and activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All dependencies installed successfully!"
    echo ""
else
    echo ""
    echo "✗ Error installing dependencies. Please check the error messages above."
    exit 1
fi

# Run tests
read -p "Run component tests? [Y/n]: " run_tests

if [[ ! $run_tests =~ ^[Nn]$ ]]; then
    echo ""
    echo "Running tests..."
    echo ""
    python3 test_app.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================="
        echo "Setup Complete!"
        echo "=================================="
        echo ""
        echo "To start the app, run:"
        echo "  streamlit run stock_sentiment_app.py"
        echo ""
        echo "Or simply:"
        echo "  ./run.sh"
        echo ""
    else
        echo ""
        echo "Tests failed. Please review the errors above."
        exit 1
    fi
else
    echo ""
    echo "=================================="
    echo "Setup Complete!"
    echo "=================================="
    echo ""
    echo "To start the app, run:"
    echo "  streamlit run stock_sentiment_app.py"
    echo ""
fi

# Create run script
cat > run.sh << 'EOF'
#!/bin/bash
# Quick run script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
fi

# Run the app
streamlit run stock_sentiment_app.py
EOF

chmod +x run.sh

echo "✓ Created run.sh for easy startup"
echo ""
