#!/usr/bin/env python3
import os
from pathlib import Path
import toml

def check_config():
    """检查配置文件是否存在并且包含必要的配置项"""
    streamlit_dir = Path(".streamlit")
    secrets_file = streamlit_dir / "secrets.toml"
    
    if not streamlit_dir.exists():
        print("创建 .streamlit 目录...")
        streamlit_dir.mkdir()
    
    if not secrets_file.exists():
        print("创建 secrets.toml 文件...")
        config = {
            "api_key": os.getenv("OPENAI_API_KEY", "sk-Mo4A5sf0JAXZKMYgaP4V0GSd61yPCRMEFNsbDklc4m9LGUB0"),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.deepbricks.ai/v1/"),
            "max_tokens": 2000,
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        }
        
        with open(secrets_file, "w") as f:
            toml.dump(config, f)
        
        print("配置文件已创建！")
    else:
        print("配置文件已存在。")

if __name__ == "__main__":
    check_config() 