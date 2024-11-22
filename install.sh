#!/bin/bash

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    brew install tesseract
    brew install poppler
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr
    sudo apt-get install -y poppler-utils
else
    echo "Please install Tesseract OCR manually from: https://github.com/UB-Mannheim/tesseract/wiki"
fi

# 安装Python依赖
pip install -e . 