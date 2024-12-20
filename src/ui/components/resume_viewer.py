import sys
import os
import streamlit as st
from PIL import Image
import io

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def show_resume_preview(resume_text, resume_images):
    """显示简历预览"""
    st.header("简历预览")
    
    # 显示文本内容
    st.subheader("文本内容")
    st.text(resume_text)
    
    # 显示结构化的简历分类
    st.subheader("简历分类")
    
    # 从session state获取结构化数据
    if 'structured_resume' in st.session_state:
        structured_resume = st.session_state.structured_resume
        
        # 显示技能
        st.write("**Skills:**")
        if structured_resume.get("skills"):
            for skill in structured_resume["skills"]:
                st.write(f"• {skill}")
        else:
            st.write("No skills listed")
        st.write("")
        
        # 显示工作经验
        st.write("**Experiences:**")
        if structured_resume.get("experiences"):
            for exp in structured_resume["experiences"]:
                # 处理字典或字符串格式的经验
                if isinstance(exp, dict):
                    # 构建格式化的经验描述
                    exp_text = f"• {exp.get('position', '')} at {exp.get('company', '')}"
                    if exp.get('duration'):
                        exp_text += f" ({exp.get('duration')})"
                    st.write(exp_text)
                    # 如果有职责描述，显示为子项
                    if exp.get('responsibilities'):
                        for resp in exp['responsibilities']:
                            st.write(f"  - {resp}")
                else:
                    st.write(f"• {exp}")
        else:
            st.write("No experiences listed")
        st.write("")
        
        # 显示其他信息
        st.write("**其他信息:**")
        if structured_resume.get("other_info"):
            # 分类显示其他信息
            personal_info = []
            education = []
            certifications = []
            
            for info in structured_resume["other_info"]:
                # 处理字典格式的信息
                if isinstance(info, dict):
                    info_str = ""
                    # 构建格式化的信息字符串
                    for key, value in info.items():
                        info_str += f"{key}: {value} "
                    info = info_str.strip()
                
                # 现在 info 一定是字符串，可以安全地调用 upper()
                if isinstance(info, str):
                    if "CONTACT" in info.upper() or "NAME" in info.upper():
                        personal_info.append(info)
                    elif "EDUCATION" in info.upper() or "SCHOOL" in info.upper():
                        education.append(info)
                    elif "CERTIFICATION" in info.upper() or "TRAINING" in info.upper():
                        certifications.append(info)
                    else:
                        personal_info.append(info)
            
            # 显示个人信息
            if personal_info:
                st.write("个人信息:")
                for info in personal_info:
                    st.write(f"• {info}")
            
            # 显示教育背景
            if education:
                st.write("教育背景:")
                for edu in education:
                    st.write(f"• {edu}")
            
            # 显示证书和培训
            if certifications:
                st.write("证书和培训:")
                for cert in certifications:
                    st.write(f"• {cert}")
        else:
            st.write("No additional information available")
    else:
        st.warning("No structured resume data available")