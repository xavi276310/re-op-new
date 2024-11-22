import os
from pathlib import Path
import streamlit.web.cli as stcli
import sys

# 设置项目根目录
ROOT_DIR = Path(__file__).parent
os.environ["PYTHONPATH"] = str(ROOT_DIR)

if __name__ == "__main__":
    sys.path.insert(0, str(ROOT_DIR))
    sys.argv = ["streamlit", "run", str(ROOT_DIR / "src" / "ui" / "app.py")]
    sys.exit(stcli.main()) 