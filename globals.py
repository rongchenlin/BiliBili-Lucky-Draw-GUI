import os
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()
# 读取变量
max_checks = int(os.getenv("max_checks"))
home_url = os.getenv("home_url")



