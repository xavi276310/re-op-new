from setuptools import setup, find_packages

setup(
    name="resume_matcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "openai<1.0.0",
        "PyPDF2",
        "Pillow",
        "pydantic",
        "termcolor",
        "reportlab",
        "markdown",
        "python-dotenv",
        "jinja2",
        "pdfkit",
    ],
    extras_require={
        'ocr': [
            "pytesseract",
            "pdf2image"
        ]
    }
) 