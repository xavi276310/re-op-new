import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

def get_api_keys():
    """获取API密钥"""
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY")
    }

def load_config():
    """加载配置"""
    return {
        "DEFAULT_MAX_TOKENS": 1000,
        "MODEL_NAME": "gpt-3.5-turbo",
        "TEMPERATURE": 0.7
    } 