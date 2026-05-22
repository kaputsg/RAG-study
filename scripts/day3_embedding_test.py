"""
Day 3：真实 Embedding 模型测试

目标：
1. 加载 BGE 中文 embedding 模型
2. 把一段中文文本转换成真实向量
3. 查看向量长度和前几个数值
"""

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def main():
    text = "FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务。"

    # TODO 1：加载模型
    # 提示：model = SentenceTransformer(MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)

    # TODO 2：把 text 转成向量
    # 提示：embedding = model.encode(text)
    embedding = model.encode(text)

    # TODO 3：打印原始文本
    print("原始文本：")
    print("FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务")

    # TODO 4：打印 embedding 的类型
    # 提示：type(embedding)
    print("embedding 类型: ")
    print(type(embedding))

    # TODO 5：打印 embedding 的长度
    # 提示：len(embedding)
    print("embedding 长度：")
    print(len(embedding))

    # TODO 6：打印前 10 个数字
    # 提示：embedding[:10]
    print("embedding 前10个数字：")
    print(embedding[:10])


if __name__ == "__main__":
    main()