import sys
import os
from pathlib import Path
import streamlit as st
import json

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.ai_client import AIClient
from src.core.resume_parser import ResumeParser
from src.ui.components.resume_viewer import show_resume_preview
from src.utils.resume_generator import ResumeGenerator

def get_api_credentials():
    """获取API凭证"""
    try:
        # 首先尝试从 Streamlit Cloud secrets 获取凭证
        api_key = st.secrets["api_credentials"]["api_key"]
        base_url = st.secrets["api_credentials"]["base_url"]
    except Exception as e:
        # 如果失败，尝试从环境变量获取
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            st.error("API凭证未正确配置。请在Streamlit Cloud中配置secrets或设置环境变量。")
            st.stop()
    
    return api_key, base_url

def main():
    st.title("Resume Matcher & Editor")
    
    # 初始化session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'resume_images' not in st.session_state:
        st.session_state.resume_images = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    
    # 获取API凭证
    api_key, base_url = get_api_credentials()
    
    # 岗位描述输入
    st.header("岗位描述")
    job_description = st.text_area(
        "请输入岗位描述",
        value="",  # 不使用session_state中的值
        height=200,
        help="请输入完整的岗位描述，包括职位要求、技能要求等"
    )
    
    # 文件上传
    st.header("简历上传")
    uploaded_file = st.file_uploader("上传简历(PDF格式)", type="pdf", key="resume_uploader")
    
    # 当文件上传器的值改变时，清除之前的分析结果
    if uploaded_file is not None and 'last_uploaded_file' in st.session_state:
        if uploaded_file.name != st.session_state.last_uploaded_file:
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            st.session_state.resume_text = None
            st.session_state.resume_images = None
            st.session_state.job_description = ""
            if 'modifications' in st.session_state:
                st.session_state.modifications = {
                    'skills_to_add': {},
                    'content_to_remove': set(),
                    'content_to_modify': {}
                }  
    
    # 记录当前上传的文件名
    if uploaded_file is not None:
        st.session_state.last_uploaded_file = uploaded_file.name
    
    # 开始分析按钮
    if uploaded_file and job_description and st.button("开始分析"):
        with st.spinner('正在分析简历...'):
            # 每次分析前都更新岗位描述
            st.session_state.job_description = job_description
            
            # 初始化AI客户端
            ai_client = AIClient(api_key, base_url)
            
            # 解析简历
            resume_text, resume_images = ResumeParser.extract_text_and_image(uploaded_file)
            
            # 结构化处理简历内容
            structured_resume = ai_client.structure_resume(resume_text)
            if structured_resume:
                st.session_state.resume_text = resume_text
                st.session_state.resume_images = resume_images
                st.session_state.structured_resume = structured_resume
                
                # 显示结构化的简历内容
                st.subheader("简历内容")
                
                # 显示技能
                st.write("**技能**")
                for skill_group in structured_resume['skills']:
                    st.write(f"*{skill_group['category']}*")
                    for skill in skill_group['items']:
                        st.write(f"- {skill}")
                
                # 显示工作经验
                st.write("**工作经验**")
                for exp in structured_resume['experience']:
                    st.write(f"**{exp['title']} @ {exp['company']}**")
                    st.write(f"*{exp['duration']}*")
                    for resp in exp['responsibilities']:
                        st.write(f"- {resp}")
                
                # 显示其他信息
                st.write("**其他信息**")
                other_info = structured_resume['other_info']
                if 'education' in other_info:
                    st.write("*教育背景*")
                    for edu in other_info['education']:
                        st.write(f"- {edu['degree']} @ {edu['school']} ({edu['duration']})")
                
                # AI分析
                analysis = json.loads(ai_client.analyze_resume(json.dumps(structured_resume), job_description))
                st.session_state.analysis_results = analysis
                st.session_state.analysis_complete = True
                
                # 重置修改状态
                st.session_state.modifications = {
                    'skills_to_add': {},
                    'content_to_remove': set(),
                    'content_to_modify': {}
                }
    
    # 如果分析完成，显示结果和重新分析按钮
    if st.session_state.analysis_complete:
        # 显示重新分析按钮
        if st.button("重新分析", key="reset_button"):
            # 完全重置所有 session_state 变量
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            st.session_state.resume_text = None
            st.session_state.resume_images = None
            st.session_state.job_description = ""  # 重置岗位描述
            st.session_state.modifications = {
                'skills_to_add': {},
                'content_to_remove': set(),
                'content_to_modify': {}
            }
            # 清除文件上传器的状态
            if 'resume_uploader' in st.session_state:
                del st.session_state.resume_uploader
            st.experimental_rerun()
        
        # 显示简历预览
        show_resume_preview(st.session_state.resume_text, st.session_state.resume_images)
        
        analysis = st.session_state.analysis_results
        
        # 显示分析结果和编辑选项
        st.header("1. 建议增加的技能")
        for skill in analysis["skills_to_add"]:
            with st.expander(f"✨ {skill['skill']}", expanded=True):
                st.write("**为什么需要这个技能：**")
                st.write(skill['reason'])
                st.write("**建议展示方式：**")
                st.write(skill['suggestion'])
                
                skill_key = f"skill_{skill['skill']}"
                if st.checkbox("添加这个技能", key=f"checkbox_{skill_key}"):
                    experience = st.text_area(
                        "请按建议编写相关经验:",
                        value=st.session_state.modifications['skills_to_add'].get(skill['skill'], ''),
                        key=skill_key,
                        help="参考上面的建议展示方式编写"
                    )
                    if experience:
                        st.session_state.modifications['skills_to_add'][skill['skill']] = experience

        st.header("2. 建议删除的内容")
        for content in analysis["content_to_remove"]:
            with st.expander(f"🔍 需要考虑删除的内容", expanded=True):
                st.write("**原文内容：**")
                st.write(content['content'])
                st.write("**建议删除原因：**")
                st.write(content['reason'])
                
                content_key = content['content']
                if st.checkbox("删除这部分内容", key=f"remove_{content_key}"):
                    st.session_state.modifications['content_to_remove'].add(content['content'])

        st.header("3. 建议修改的内容")
        for modify in analysis["content_to_modify"]:
            with st.expander(f"📝 建议优化的内容", expanded=True):
                st.write("**原始内容：**")
                st.write(modify['original'])
                st.write("**建议修改为：**")
                st.write(modify['suggested'])
                st.write("**修改原因：**")
                st.write(modify['reason'])
                if 'keywords' in modify:
                    st.write("**关键词：**")
                    st.write(modify['keywords'])
                
                modify_key = modify['original']
                if st.checkbox("修改这部分内容", key=f"modify_checkbox_{modify_key}"):
                    modified_text = st.text_area(
                        "自定义修改:",
                        value=st.session_state.modifications['content_to_modify'].get(
                            modify['original'], modify['suggested']
                        ),
                        key=f"modify_text_{modify_key}",
                        help="你可以直接使用建议的修改，或者自己编写"
                    )
                    if modified_text:
                        st.session_state.modifications['content_to_modify'][modify['original']] = modified_text

        # 保存按钮
        if st.button("保存修改", key="save_button"):
            try:
                # 准备用于显示的修改内容（将set转换为list）
                display_modifications = {
                    'skills_to_add': st.session_state.modifications['skills_to_add'],
                    'content_to_remove': list(st.session_state.modifications['content_to_remove']),
                    'content_to_modify': st.session_state.modifications['content_to_modify']
                }
                
                # 获取原PDF数据
                if uploaded_file is not None:
                    # 使用 getbuffer() 而不是 getvalue()
                    pdf_bytes = uploaded_file.getbuffer()
                    
                    # 生成修改后的简历
                    doc_path, json_path = ResumeGenerator.generate_modified_resume(
                        pdf_bytes,
                        st.session_state.modifications
                    )
                    
                    # 显示成功消息
                    st.success("修改已保存!")
                    
                    # 显示修改内容预览
                    st.write("修改内容预览:")
                    st.json(display_modifications)
                    
                    # 提供下载链接
                    try:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            doc_content = f.read()
                        
                        st.download_button(
                            label="下载修改后的简历",
                            data=doc_content,
                            file_name="modified_resume.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"读取生成的文件时出错: {str(e)}")
                else:
                    st.error("请先上传简历文件")
                    
            except Exception as e:
                st.error(f"保存修改时出错: {str(e)}")
                st.error("请确保文件仍然可用，可能需要重新上传文件。")

if __name__ == "__main__":
    main() 