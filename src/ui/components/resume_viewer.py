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
    
    # 显示技能
    st.write("**Skills:**")
    skills = [
        "Network Database Monitoring (Freenas, Centos Database System)",
        "Network Security (Pfsense Firewall)",
        "Computer hardware & software troubleshooting",
        "Network Troubleshooting WAN and LAN",
        "Knowledgeable in Open Source System",
        "Operating System Installation and Software Installation",
        "Networking and Troubleshooting"
    ]
    for i, skill in enumerate(skills, 1):
        st.write(f"{i}. {skill}")
    st.write("")
    
    # 显示工作经验
    st.write("**Experiences:**")
    experiences = [
        "Virtual Assistant Property and Hotel Management at Quarters Lettings (September 2023 – August 2024)",
        "Safety Officer at Currey International Inc (January 2022 - December 2023)",
        "IT & Network Admin Assistant at Currey International Inc (July 2017 - December 2023)",
        "OJT/Trainee at Clark Data Center Incorporated (April – June 2017)"
    ]
    for i, exp in enumerate(experiences, 1):
        st.write(f"{i}. {exp}")
    st.write("")
    
    # 显示其他信息
    st.write("**其他信息:**")
    
    # 个人信息
    st.write("个人信息:")
    personal_info = [
        "姓名: MARK RIVEN M. CRUZ",
        "联系方式: markjanecruz17@gmail.com | 0906 750 9884",
        "目标: 寻求技术支持团队职位，在具有挑战性的环境中进一步发展和利用知识、学习和经验"
    ]
    for i, info in enumerate(personal_info, 1):
        st.write(f"{i}. {info}")
    
    # 教育背景
    st.write("教育背景:")
    education = [
        "Web Developer (Online Course) at Learn Computer Today (2021)",
        "Computer System Servicing NCII at Integrater Computer School Foundation (2017)",
        "Computer Engineering (Undergrad) at Mega Computer College (2014)"
    ]
    for i, edu in enumerate(education, 1):
        st.write(f"{i}. {edu}")
    
    # 证书和培训
    st.write("证书和培训:")
    certifications = [
        "BOSH II - Basic Occupational Safety and Health Officer – Safety Officer 2 (OSHMS360 CORPORATION)",
        "COSH II – Construction Safety and Health Officer – Safety Officer 2 (OSHC RUE 2)",
        "Leadership Training: Life Class, Destiny Class"
    ]
    for i, cert in enumerate(certifications, 1):
        st.write(f"{i}. {cert}")