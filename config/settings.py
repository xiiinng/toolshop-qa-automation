
import os

from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
load_dotenv()

# API 基础地址
BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://api.practicesoftwaretesting.com"
)

# 接口请求超时时间（秒）
TIMEOUT = 10
