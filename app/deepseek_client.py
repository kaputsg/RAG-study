from typing import Optional

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


class DeepSeekClient:
    """
    DeepSeek API 客户端封装。

    这个类的作用：
    1. 创建 DeepSeek API 客户端
    2. 统一发送大模型请求
    3. 统一管理模型名
    4. 请求失败时自动重试
    """

    def __init__(self):
        # 创建 API 客户端
        # api_key 来自 .env
        # base_url 来自 .env
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )

        # 当前使用的模型名
        self.model = settings.DEEPSEEK_MODEL

    @retry(
        stop=stop_after_attempt(3),                 # 最多重试 3 次
        wait=wait_exponential(multiplier=1, min=1, max=6)  # 重试间隔逐渐变长
    )
    def chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 800,
        show_model_name: bool = False
    ) -> str:
        """
        调用大模型进行对话。

        参数：
        user_message：用户输入的问题
        system_message：系统提示词，用来控制模型角色和回答规则
        temperature：控制回答随机性，越低越稳定
        max_tokens：控制最大输出长度
        show_model_name：是否在终端打印当前使用的模型名

        返回：
        模型回答的文本
        """

        messages = []

        # system 用来规定模型身份和回答规则
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })

        # user 是用户真正的问题
        messages.append({
            "role": "user",
            "content": user_message
        })

        #打印当前使用的模型名
        if show_model_name == True:
            print(f"当前模型名是： {self.model}")
        else:
            return

        # 发送请求
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # 取出模型回答
        answer = response.choices[0].message.content

        return answer
    
    


# 创建一个全局对象，其他文件可以直接导入使用
deepseek_client = DeepSeekClient()