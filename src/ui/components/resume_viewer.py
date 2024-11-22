import sys
import os
import streamlit as st
from PIL import Image
import io

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def show_resume_preview(resume_text, resume_images):
    """显示简历预览"""
    st.subheader("简历预览")
    
    # 显示文本内容
    with st.expander("文本内容", expanded=True):
        st.text(resume_text)
    
    # 显示图片预览
    if resume_images:
        with st.expander("图片预览"):
            for i, img_data in enumerate(resume_images):
                img = Image.open(io.BytesIO(img_data))
                st.image(img, caption=f"Page {i+1}") 