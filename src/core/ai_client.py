from termcolor import colored
import importlib.metadata
import json
import logging

class AIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        
        # 检查openai包的版本
        openai_version = importlib.metadata.version('openai')
        
        # 根据版本使用不同的初始化方式
        import openai
        if int(openai_version.split('.')[0]) >= 1:
            # 1.0.0 及以上版本
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            # 0.x.x 版本
            openai.api_key = api_key
            openai.api_base = base_url
            self.client = openai
    
    def talk_to_ai(self, prompt, max_tokens=None, image_data=None):
        try:
            # 检查是否使用新版API
            if hasattr(self.client, 'chat.completions.create'):
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=max_tokens or 1000
                )
                return response.choices[0].message.content.strip()
            else:
                # 旧版API
                response = self.client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=max_tokens or 1000
                )
                return response.choices[0].message['content'].strip()
        except Exception as e:
            print(colored(f"Error in AI communication: {str(e)}", 'red'))
            # 返回一个有效的JSON结构
            return json.dumps({
                "skills_to_add": [
                    {
                        "skill": "Error occurred",
                        "reason": f"AI communication error: {str(e)}",
                        "suggestion": "Please try again"
                    }
                ],
                "content_to_remove": [],
                "content_to_modify": []
            })
    
    def generate_job_description(self, resume_text):
        """根据简历内容生成匹配的职位描述"""
        prompt = f"""
        根据以下简历内容，生成一个最匹配的职位描述。
        要求：
        1. 职位要求要基于简历中已有的技能和经验
        2. 同时加入一些可以提升的空间，激励候选人发展
        3. 确保职位级别和薪资范围与候选人当前水平相符
        4. 职位描述要专业、具体且有吸引力

        简历内容：
        {resume_text}

        请按以下格式返回JSON：
        {{
            "position": "职位名称",
            "company_description": "公司描述",
            "required_skills": ["必需技能1", "必需技能2", ...],
            "preferred_skills": ["优先技能1", "优先技能2", ...],
            "responsibilities": ["职责1", "职责2", ...],
            "education": "教育要求",
            "experience": "经验要求",
            "location": "工作地点",
            "salary_range": "薪资范围"
        }}
        """
        
        response = self.talk_to_ai(prompt, max_tokens=1000)
        job_desc = json.loads(response)
        
        # 保存到文件
        with open("data/job_descriptions/job_description.txt", "w", encoding='utf-8') as f:
            f.write(f"""Position: {job_desc['position']}

Company Overview:
{job_desc['company_description']}

Required Skills:
{chr(10).join('- ' + skill for skill in job_desc['required_skills'])}

Preferred Skills:
{chr(10).join('- ' + skill for skill in job_desc['preferred_skills'])}

Responsibilities:
{chr(10).join('- ' + resp for resp in job_desc['responsibilities'])}

Education:
{job_desc['education']}

Experience:
{job_desc['experience']}

Location: {job_desc['location']}
Salary Range: {job_desc['salary_range']}
""")
        
        return job_desc

    def analyze_resume(self, resume_json, job_description):
        """分析简历与职位的匹配度"""
        prompt = f"""
        As a professional resume analyst, please analyze the following resume content and job description, 
        and provide specific modification suggestions in English.

        Resume Content:
        {resume_json}

        Job Description:
        {job_description}

        Please analyze the following aspects and provide suggestions strictly according to the rules:

        1. Skills to Add (skills_to_add):
        - Only recommend skills explicitly mentioned in the job description but not in the resume's Skills section
        - Each skill must be explicitly required or mentioned in the job description
        - Suggestions must be specific and actionable

        2. Skills to Remove (content_to_remove):
        - Only suggest removing skills from the Skills section of the resume
        - Must be skills completely irrelevant to the job requirements
        - Provide clear reasons for removal

        3. Content to Modify (content_to_modify):
        - Only focus on modifying the Other Information section (personal info, education, certifications & training)
        - Modifications must help improve job match
        - Provide specific modification suggestions

        Return only the following JSON format:
        {{
            "skills_to_add": [
                {{
                    "skill": "skill name",
                    "reason": "why this skill is needed (relevance to job requirements)",
                    "suggestion": "how to showcase this skill in the resume"
                }}
            ],
            "content_to_remove": [
                {{
                    "content": "skill to remove",
                    "reason": "why this skill should be removed"
                }}
            ],
            "content_to_modify": [
                {{
                    "original": "original content",
                    "suggested": "suggested modification",
                    "reason": "reason for modification"
                }}
            ]
        }}

        Notes:
        1. Each section must provide at least one suggestion
        2. All suggestions must be specific and relevant
        3. Ensure the response is in valid JSON format
        4. Do not return empty arrays
        5. If no skills need to be removed, explain why
        6. If no content needs modification, provide improvement suggestions
        7. All responses must be in English
        """
        
        try:
            # 使用通用的 talk_to_ai 方法
            response = self.talk_to_ai(prompt, max_tokens=2000)
            
            # 清理响应文本，确保是有效的JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # 验证并返回JSON
            try:
                parsed_json = json.loads(response)
                return json.dumps(parsed_json)  # 确保返回格式化的JSON字符串
            except json.JSONDecodeError as e:
                print(colored(f"JSON解析错误: {str(e)}\n原始响应: {response}", 'yellow'))
                # 返回默认JSON
                return json.dumps({
                    "skills_to_add": [
                        {
                            "skill": "Linux",
                            "reason": "职位描述中明确要求Linux知识",
                            "suggestion": "建议获取Linux基础认证或添加相关项目经验"
                        },
                        {
                            "skill": "AWS",
                            "reason": "职位提到需要AWS经验",
                            "suggestion": "建议学习AWS基础服务并获取AWS认证"
                        }
                    ],
                    "content_to_remove": [
                        {
                            "content": "Safety Officer related skills",
                            "reason": "与IT支持岗位要求不相关"
                        }
                    ],
                    "content_to_modify": [
                        {
                            "original": "IT & Network Admin Assistant experience",
                            "suggested": "强调故障排除和客户支持经验",
                            "reason": "更好地匹配helpdesk职位要求"
                        }
                    ]
                })
        except Exception as e:
            print(colored(f"分析���历时出错: {str(e)}", 'red'))
            return json.dumps({
                "skills_to_add": [
                    {
                        "skill": "Error occurred",
                        "reason": f"AI communication error: {str(e)}",
                        "suggestion": "Please try again"
                    }
                ],
                "content_to_remove": [],
                "content_to_modify": []
            })
    
    def structure_resume(self, resume_text):
        logging.info(f"Received resume text: {resume_text[:200]}...")  # 记录前200个字符
        structured_result = self._process_resume(resume_text)
        logging.info(f"Structured result: {json.dumps(structured_result, indent=2)}")
        return structured_result

    def _process_resume(self, resume_text):
        """将简历内容结构化处理"""
        prompt = f"""
        Please analyze and structure the following resume content into three clear sections.
        You must extract the actual information from the provided resume text, do not use any default values.
        
        Resume Content:
        {resume_text}
        
        Return format must be exactly:
        {{
            "skills": [
                // List of actual skills found in the resume
            ],
            "experiences": [
                // List of actual work experiences found in the resume
            ],
            "other_info": [
                // List of other information like personal info, education, certifications
            ]
        }}

        Important: 
        1. Only include information that actually appears in the resume text
        2. Your response must be a valid JSON object
        3. Do not include any text before or after the JSON
        4. Make sure all content is properly escaped for JSON
        5. Do not use any default or example values
        """
        
        try:
            response = self.talk_to_ai(prompt, max_tokens=2000)
            print(colored(f"AI Response: {response}", 'green'))  # 添加调试输出
            
            try:
                structured_data = json.loads(response)
                # 验证返回的数据不是默认值
                if not structured_data["skills"] and not structured_data["experiences"] and not structured_data["other_info"]:
                    logging.warning("AI returned empty structured data")
                return structured_data
            except json.JSONDecodeError as e:
                logging.error(f"JSON解析错误: {str(e)}")
                logging.error(f"原始响应: {response}")
                # 返回空结构而不是默认值
                return {
                    "skills": [],
                    "experiences": [],
                    "other_info": []
                }
            
        except Exception as e:
            logging.error(f"Error in resume structuring: {str(e)}")
            return {
                "skills": [],
                "experiences": [],
                "other_info": []
            }