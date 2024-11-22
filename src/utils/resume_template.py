from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

class ResumeTemplate:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.page_width, self.page_height = A4
        
        # 创建自定义样式
        self.styles.add(ParagraphStyle(
            name='Section',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=16,
            textColor=colors.HexColor('#2E75B6')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#2F5496')
        ))
        
        self.styles.add(ParagraphStyle(
            name='Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='Skills',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            bulletIndent=20,
            leftIndent=35
        ))

    def create_header(self, name, contact_info):
        """创建简历头部"""
        elements = []
        
        # 添加姓名
        elements.append(Paragraph(name, self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # 添加联系信息
        for info in contact_info:
            elements.append(Paragraph(info, self.styles['Normal']))
        
        elements.append(Spacer(1, 20))
        return elements

    def create_section(self, title, content):
        """创建简历章节"""
        elements = []
        elements.append(Paragraph(title, self.styles['Section']))
        
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    # 处理工作经历或教育经历
                    elements.append(Paragraph(
                        f"<b>{item.get('title', '')}</b> | {item.get('organization', '')}",
                        self.styles['SubSection']
                    ))
                    elements.append(Paragraph(
                        f"{item.get('date', '')} | {item.get('location', '')}",
                        self.styles['Normal']
                    ))
                    for detail in item.get('details', []):
                        elements.append(Paragraph(f"• {detail}", self.styles['Skills']))
                else:
                    # 处理普通列表项
                    elements.append(Paragraph(f"• {item}", self.styles['Skills']))
        else:
            elements.append(Paragraph(content, self.styles['Normal']))
        
        elements.append(Spacer(1, 12))
        return elements

    def generate_resume(self, resume_data):
        """生成简历PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        elements = []
        
        # 添加头部
        elements.extend(self.create_header(
            resume_data['name'],
            resume_data['contact_info']
        ))
        
        # 添加各个章节
        for section in resume_data['sections']:
            elements.extend(self.create_section(
                section['title'],
                section['content']
            ))
        
        # 生成PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer 