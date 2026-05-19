import os
from dotenv import load_dotenv


# 加载项目根目录下的 .env 文件
load_dotenv()


class Settings:
    """
    项目配置类。

    作用：
    1. 从 .env 文件读取 DeepSeek 配置
    2. 统一管理 API Key、base_url、模型名
    3. 避免在业务代码里写死配置
    """

    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    @classmethod
    def validate(cls):
        """
        检查关键配置是否存在。

        如果 API Key 没有填写，就直接报错。
        这样可以让问题尽早暴露。
        """
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("缺少 DEEPSEEK_API_KEY，请检查 .env 文件。")


# 创建全局配置对象
settings = Settings()

# 程序启动时先检查配置
settings.validate()