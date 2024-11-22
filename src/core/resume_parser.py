from PyPDF2 import PdfReader
from PIL import Image
import io
import tempfile
import os
import logging
from pathlib import Path

class ResumeParser:
    @staticmethod
    def extract_text_and_image(file):
        """
        从PDF文件中提取文本和图片
        """
        try:
            # 尝试导入 pytesseract 和 pdf2image
            try:
                import pytesseract
                from pdf2image import convert_from_path
                USE_OCR = True
            except ImportError:
                logging.warning("pytesseract or pdf2image not installed. OCR functionality will be disabled.")
                USE_OCR = False

            # 如果是上传的文件，先保存到临时文件
            if hasattr(file, 'read'):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(file.read())
                    file_path = tmp_file.name
            else:
                file_path = file

            text = ""
            resume_images = []

            # 使用PyPDF2提取文本
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            # 如果安装了OCR相关包，则使用OCR功能
            if USE_OCR:
                try:
                    images = convert_from_path(file_path)
                    for i, img in enumerate(images):
                        # 转换为灰度图像并压缩
                        img_gray = img.convert('L')
                        img_buffer = io.BytesIO()
                        img_gray.save(img_buffer, format='JPEG', quality=51)
                        img_buffer.seek(0)
                        resume_images.append(img_buffer.getvalue())

                        # 如果文本提取不足，使用OCR
                        if not text or len(text.strip()) < 500:
                            try:
                                ocr_text = pytesseract.image_to_string(img_gray)
                                text += ocr_text + "\n"
                            except Exception as e:
                                logging.error(f"OCR error: {str(e)}")

                except Exception as e:
                    logging.error(f"PDF to image conversion error: {str(e)}")

            # 清理临时文件
            if hasattr(file, 'read'):
                os.unlink(file_path)

            return text.strip(), resume_images

        except Exception as e:
            logging.error(f"Error extracting text and image from PDF: {str(e)}")
            return "", [] 