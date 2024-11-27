from termcolor import colored
import importlib.metadata
import json

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

    def analyze_resume(self, resume_text, job_desc):
        """分析简历与岗位要求的匹配度并提供建议"""
        prompt = f"""
        Please analyze the resume against the job requirements and provide improvement suggestions.
        You must return a valid JSON object in the exact format shown below.

        Job Requirements:
        {job_desc}

        Resume Content:
        {resume_text}

        Return format must be exactly:
        {{
            "skills_to_add": [
                {{
                    "skill": "Cashiering",
                    "reason": "The job requires cashiering skills, but it's not mentioned in your resume",
                    "suggestion": "Highlight any experience handling cash transactions or managing payments"
                }},
                {{
                    "skill": "Customer Service",
                    "reason": "Strong customer service skills are essential for this position",
                    "suggestion": "Emphasize your experience interacting with customers and handling their needs"
                }},
                {{
                    "skill": "Waitering",
                    "reason": "Core requirement for the position, but not explicitly shown in resume",
                    "suggestion": "Describe your restaurant experience in terms of serving customers and handling orders"
                }}
            ],
            "content_to_remove": [
                {{
                    "content": "I used to be a tailor employee",
                    "reason": "This experience is not relevant to the restaurant service position"
                }},
                {{
                    "content": "read a book",
                    "reason": "This hobby is not relevant to the position and takes up space"
                }}
            ],
            "content_to_modify": [
                {{
                    "original": "cleaning kitchen ingredients",
                    "suggested": "Responsible for maintaining a clean and organized kitchen environment, including cleaning cooking ingredients and washing dishes to support efficient restaurant operations",
                    "reason": "This modification better demonstrates your understanding of kitchen operations and teamwork"
                }},
                {{
                    "original": "washing dishes",
                    "suggested": "Maintained high standards of cleanliness by efficiently managing dishwashing operations and ensuring proper sanitation protocols",
                    "reason": "This shows a more professional approach to kitchen duties"
                }}
            ]
        }}

        Important: Your response must be a valid JSON object exactly matching this format.
        Do not include any additional text before or after the JSON object.
        """
        
        try:
            response = self.talk_to_ai(prompt, max_tokens=2000)
            try:
                # 尝试解析JSON
                analysis = json.loads(response)
                # 验证返回的JSON格式是否正确
                if not all(key in analysis for key in ['skills_to_add', 'content_to_remove', 'content_to_modify']):
                    raise ValueError("Missing required fields in response")
                return json.dumps(analysis)
            except (json.JSONDecodeError, ValueError) as e:
                print(colored(f"Error parsing AI response: {str(e)}", 'red'))
                print(colored(f"Raw response: {response}", 'yellow'))
                # 返回一个示例分析结果
                return json.dumps({
                    "skills_to_add": [
                        {
                            "skill": "Cashiering",
                            "reason": "The job requires cashiering skills, but it's not mentioned in your resume",
                            "suggestion": "Highlight any experience handling cash transactions or managing payments"
                        }
                    ],
                    "content_to_remove": [
                        {
                            "content": "I used to be a tailor employee",
                            "reason": "This experience is not relevant to the restaurant service position"
                        }
                    ],
                    "content_to_modify": [
                        {
                            "original": "cleaning kitchen ingredients",
                            "suggested": "Responsible for maintaining a clean and organized kitchen environment",
                            "reason": "This shows a more professional approach to kitchen duties"
                        }
                    ]
                })
        except Exception as e:
            print(colored(f"Error in resume analysis: {str(e)}", 'red'))
            return json.dumps({
                "skills_to_add": [
                    {
                        "skill": "Error occurred",
                        "reason": f"Analysis error: {str(e)}",
                        "suggestion": "Please try again"
                    }
                ],
                "content_to_remove": [],
                "content_to_modify": []
            })
    
    def structure_resume(self, resume_text):
        """将简历内容结构化处理"""
        prompt = f"""
        Please analyze and structure the following resume content into clear sections.
        
        Resume Content:
        {resume_text}
        
        Please return a JSON object with the following structure:
        {{
            "skills": [
                {{
                    "category": "Technical Skills/Soft Skills/Language Skills",
                    "items": ["skill 1", "skill 2", ...]
                }}
            ],
            "experience": [
                {{
                    "title": "job title",
                    "company": "company name",
                    "duration": "time period",
                    "responsibilities": ["responsibility 1", "responsibility 2", ...]
                }}
            ],
            "other_info": {{
                "education": [
                    {{
                        "degree": "degree name",
                        "school": "school name",
                        "duration": "time period"
                    }}
                ],
                "personal_info": {{
                    "name": "candidate name",
                    "contact": ["contact info 1", "contact info 2", ...]
                }},
                "additional_info": ["other relevant information"]
            }}
        }}
        """
        
        try:
            response = self.talk_to_ai(prompt, max_tokens=2000)
            return json.loads(response)
        except Exception as e:
            print(colored(f"Error in resume structuring: {str(e)}", 'red'))
            return None