from pathlib import Path
import json
from datetime import datetime
import io
import re
from jinja2 import Template, Environment, FileSystemLoader
import pdfkit
from PyPDF2 import PdfReader

class ResumeGenerator:
    @staticmethod
    def extract_resume_info(text):
        """从文本中提取简历信息"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # 提取姓名
        name = next((line for line in lines if "FITRIYANI" in line.upper()), '')

        # 提取联系信息
        contact_info = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['@', 'phone', 'tel', '+60']):
                contact_info.append(line.strip())
            elif 'Jln.' in line:
                contact_info.append(line.strip())

        # 初始化各个部分
        sections = []
        current_section = None
        current_education = None
        education_items = []

        # 定义部分标识符
        section_identifiers = {
            'EDUCATION': 'education',
            'SKILL': 'skills',
            'EXPERIENCE': 'experience',
            'PROFILE': 'profile',
            'CONTACT': 'contact',
            'CURRICULUM VITAE': None  # 忽略这个标题
        }

        # 处理每一行
        for line in lines:
            # 检查是否是新的部分
            section_type = None
            for identifier, type_name in section_identifiers.items():
                if identifier in line.upper():
                    # 如果有未完成的教育条目，添加它
                    if current_education:
                        education_items.append(current_education)
                        current_education = None

                    if current_section and current_section['content']:
                        if current_section['type'] == 'education':
                            current_section['content'] = education_items
                        sections.append(current_section)

                    if type_name:  # 不为None的部分才创建新section
                        current_section = {
                            'title': line.strip(':'),
                            'type': type_name,
                            'content': []
                        }
                    section_type = type_name
                    break

            if not section_type and current_section:
                # 处理教育经历
                if current_section['type'] == 'education':
                    if any(str(year) in line for year in range(2000, 2025)):
                        # 如果有未完成的教育条目，添加它
                        if current_education:
                            education_items.append(current_education)
                        # 开始新的教育条目
                        current_education = {
                            'date': line.strip(),
                            'school': '',
                            'degree': '',
                            'location': ''
                        }
                    elif current_education and 'school' in current_education:
                        if not current_education['degree']:
                            current_education['degree'] = line.strip()
                    elif current_education:
                        current_education['school'] = line.strip()

                # 处理技能部分
                elif current_section['type'] == 'skills':
                    # 处理带有 • 的技能项
                    if '•' in line:
                        skill = line.replace('•', '').strip()
                        if skill not in current_section['content']:  # 避免重复
                            current_section['content'].append(skill)
                    # 处理其他格式的技能项
                    elif line.strip() and not any(identifier in line.upper() for identifier in section_identifiers):
                        if line.strip() not in current_section['content']:  # 避免重复
                            current_section['content'].append(line.strip())

                # 处理其他部分
                else:
                    current_section['content'].append(line)

        # 处理最后一个教育条目
        if current_education:
            education_items.append(current_education)

        # 处理最后一个部分
        if current_section:
            if current_section['type'] == 'education':
                current_section['content'] = education_items
            sections.append(current_section)

        return {
            'name': name,
            'contact_info': contact_info,
            'sections': sections
        }

    @staticmethod
    def apply_modifications(resume_data, modifications):
        """应用修改到简历数据"""
        modified_data = {
            'name': resume_data['name'],
            'contact_info': list(dict.fromkeys(resume_data['contact_info'])),  # 去重
            'sections': []
        }
        
        # 处理各个部分
        has_skills_section = False
        
        for section in resume_data['sections']:
            new_section = {
                'title': section['title'],
                'type': section['type'],
                'content': []
            }
            
            # 根据不同类型处理内容
            if section['type'] == 'skills':
                has_skills_section = True
                # 处理技能部分
                existing_skills = set()
                
                # 保留原有内容（除非需要删除）
                for skill in section['content']:
                    if isinstance(skill, str) and skill not in modifications['content_to_remove']:
                        new_section['content'].append(skill)
                        existing_skills.add(skill)
                
                # 添加修改后的内容（不替换原内容）
                for original, suggested in modifications['content_to_modify'].items():
                    if suggested not in existing_skills:
                        new_section['content'].append(suggested)
                        existing_skills.add(suggested)
                
                # 添加新技能
                for skill, experience in modifications['skills_to_add'].items():
                    if skill not in existing_skills:
                        new_section['content'].append(f"{skill}: {experience}")
                        existing_skills.add(skill)
                    
            elif section['type'] == 'contact':
                # 只保留联系信息，不添加修改的内容
                for item in section['content']:
                    if str(item) not in modifications['content_to_remove']:
                        new_section['content'].append(item)
            
            else:
                # 处理其他部分
                processed_items = set()
                
                # 保留原有内容（除非需要删除）
                for item in section['content']:
                    if str(item) not in modifications['content_to_remove']:
                        new_section['content'].append(item)
                        processed_items.add(str(item))
            
            # 只添加非空的部分
            if new_section['content']:
                modified_data['sections'].append(new_section)
        
        # 如果没有技能部分，但有新增技能，创建新的技能部分
        if not has_skills_section and modifications['skills_to_add']:
            skills_section = {
                'title': 'Skills',
                'type': 'skills',
                'content': [f"{skill}: {experience}" for skill, experience in modifications['skills_to_add'].items()]
            }
            modified_data['sections'].append(skills_section)
        
        return modified_data

    @staticmethod
    def generate_modified_resume(original_pdf, modifications, output_dir="output"):
        """生成修改后的简历文档"""
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # 提取文本
        reader = PdfReader(io.BytesIO(original_pdf))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # 提取简历信息
        resume_data = ResumeGenerator.extract_resume_info(text)

        # 应用修改
        modified_data = ResumeGenerator.apply_modifications(resume_data, modifications)

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_path = output_path / f"modified_resume_{timestamp}.txt"
        json_path = output_path / f"modifications_{timestamp}.json"

        # 生成文档内容
        doc_content = []

        # 添加个人信息
        doc_content.append(f"Name: {modified_data['name']}\n")
        doc_content.append("Contact Information:")
        for contact in modified_data['contact_info']:
            doc_content.append(f"  {contact}")
        doc_content.append("")

        # 添加各个部分
        for section in modified_data['sections']:
            doc_content.append(f"\n{section['title']}")
            doc_content.append("=" * len(section['title']))

            if section['type'] == 'skills':
                for skill in section['content']:
                    doc_content.append(f"• {skill}")

            elif section['type'] == 'education':
                for edu in section['content']:
                    doc_content.append(f"• {edu['school']}")
                    if edu['degree']:
                        doc_content.append(f"  Major: {edu['degree']}")
                    doc_content.append(f"  Date: {edu['date']}")
                    if edu['location']:
                        doc_content.append(f"  Location: {edu['location']}")
                    doc_content.append("")

            else:
                for item in section['content']:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if value:
                                doc_content.append(f"• {key}: {value}")
                    else:
                        doc_content.append(f"• {item}")

            doc_content.append("")

        # 写入文件
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(doc_content))

        # 保存修改记录
        json_modifications = {
            'skills_to_add': modifications['skills_to_add'],
            'content_to_remove': list(modifications['content_to_remove']),
            'content_to_modify': modifications['content_to_modify']
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_modifications, f, indent=2, ensure_ascii=False)

        return str(doc_path), str(json_path)

