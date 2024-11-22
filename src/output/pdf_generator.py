from weasyprint import HTML
import markdown

class PDFGenerator:
    def __init__(self, font_styles):
        self.font_styles = font_styles
    
    def generate_pdf(self, unified_resume, output_path):
        # PDF生成逻辑...
        pass 