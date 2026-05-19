from app.config import settings


print("API Key 是否读取成功：", bool(settings.DEEPSEEK_API_KEY))
print("Base URL：", settings.DEEPSEEK_BASE_URL)
print("模型名：", settings.DEEPSEEK_MODEL)