#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 检查配置
python check_config.py

# 运行应用
streamlit run src/ui/app.py 