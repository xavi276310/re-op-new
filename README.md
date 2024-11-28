# re-op-new

该项目是一个简历匹配与编辑工具，旨在帮助用户分析和优化简历，以提高求职成功率。用户可以上传简历，系统会分析简历内容并提供修改建议，以便更好地匹配职位要求。
技术栈：
前端：使用 Streamlit 框架构建用户界面，提供简洁的交互体验。
后端：使用 Python 作为主要编程语言，结合 Flask 进行API处理。
数据处理：使用 Pandas 进行数据处理和分析。
AI分析：集成 OpenAI API 进行简历内容分析和建议生成。

# 代码流程
1. 用户上传简历
用户通过界面上传简历文件（PDF格式）。
相关代码文件：src/ui/app.py（处理文件上传的逻辑）

2. 简历解析
使用 ResumeParser 组件提取上传的PDF简历中的文本和图像，并将其结构化为技能、工作经验和其他信息。
相关代码文件：src/core/resume_parser.py（简历解析逻辑）

3. AI分析
将解析后的简历内容和用户输入的岗位描述传递给 AIClient。
AIClient 构建请求的 prompt，并调用 OpenAI API 进行分析。
接收分析结果并解析为可用的格式。
相关代码文件：src/core/ai_client.py（与AI交互的逻辑）

4. 结果展示
将分析结果展示在用户界面，包括建议增加、删除和修改的技能。
用户可以查看建议并选择是否应用这些修改。
相关代码文件：src/ui/components/resume_viewer.py（展示分析结果的逻辑）

5. 保存和导出
用户可以选择保存修改后的简历，并导出修改建议为文件。
相关代码文件：src/ui/app.py（处理保存和导出功能的逻辑）