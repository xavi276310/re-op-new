#!/bin/bash

echo "Installing system dependencies..."

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "Installing Tesseract, Poppler and wkhtmltopdf..."
    brew install tesseract
    brew install poppler
    brew install wkhtmltopdf
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Installing Tesseract, Poppler and wkhtmltopdf..."
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr
    sudo apt-get install -y poppler-utils
    sudo apt-get install -y wkhtmltopdf
else
    echo "Please install dependencies manually:"
    echo "1. Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "2. wkhtmltopdf: https://wkhtmltopdf.org/downloads.html"
fi

echo "Installing Python dependencies..."
pip install -e ".[ocr]"

echo "Testing installations..."
python -c "import pytesseract; print('Pytesseract installation successful!')"
python -c "from pdf2image import convert_from_path; print('pdf2image installation successful!')"
python -c "import pdfkit; print('pdfkit installation successful!')"

echo "Installation complete!" 