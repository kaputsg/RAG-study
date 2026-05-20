"""
Day 2：假向量搜索练习

目标：
1. 用人工方式把文本映射成“语义向量”
2. 计算问题向量和文档向量的相似度
3. 找出最相关资料
"""
features = ["Python", "后端", "接口", "前端", "RAG", "生活"]

feature_keywords = {
    "Python": ["Python"],
    "后端": ["后端", "服务端", "Web"],
    "接口": ["接口", "API", "服务"],
    "前端": ["前端", "Vue", "界面"],
    "RAG": ["RAG", "检索增强", "知识库"],
    "生活": ["吃什么", "口味", "晚上"]
}

raw_documents = [
    "Python 可以用于 Web 后端开发、自动化脚本、数据分析和人工智能应用。",
    "FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务。",
    "RAG 是检索增强生成技术，它会先检索知识库资料，再让大模型生成答案。",
    "Vue 是一个前端框架，可以用来构建用户界面。",
    "今天晚上吃什么比较好，可以根据自己的口味选择。"
]


question = "后端服务一般用什么工具开发？"

# 问题向量：
# Python、后端、接口、前端、RAG、生活

def text_to_fake_vector(text):
    """
    把文本转换成假向量。

    规则：
    1. 遍历 features
    2. 取出每个 feature 对应的关键词列表
    3. 如果任意关键词出现在 text 中，这一位就是 1
    4. 否则这一位就是 0
    5. 返回 vector
    """

    vector = []

# TODO 1：遍历 features
# TODO 2：取出当前 feature 对应的关键词列表
# TODO 3：准备 found = False
# TODO 4：遍历关键词列表
            # 如果 keyword in text:
                # found = True
# TODO 5：如果 found 是 True，vector.append(1)
# 否则 vector.append(0)
    
    for feature in features:
        keywords = feature_keywords[feature]
        found = False

        for keyword in keywords:
            if keyword in text:
                found = True
                break

        if found:
            vector.append(1)
        else:
            vector.append(0)


    return vector

def build_documents(raw_documents):
    """
    把原始文本列表转换成带向量的文档列表。

    输入：
    [
        "文档1",
        "文档2"
    ]

    输出：
    [
        {"text": "文档1", "vector": [...]},
        {"text": "文档2", "vector": [...]}
    ]
    """

    documents_with_vectors = []

    # TODO 1：遍历 raw_documents

        # TODO 2：对每个 text 调用 text_to_fake_vector(text)，得到 vector

        # TODO 3：构造一个字典 {"text": text, "vector": vector}

        # TODO 4：把字典 append 到 documents_with_vectors
    for text in raw_documents:
        vector = text_to_fake_vector(text)
        document = {"text": text, "vector": vector}
        documents_with_vectors.append(document)

    return documents_with_vectors


def calculate_similarity(vector1, vector2):
    """
    计算两个向量的相似度。

    当前先用最简单的点积：
    对应位置相乘，然后全部加起来。

    例子：
    [1, 1, 1, 0] 和 [1, 1, 0, 0]
    分数 = 1*1 + 1*1 + 1*0 + 0*0 = 2

    TODO：
    1. 准备 score = 0
    2. 遍历两个向量的下标
    3. 每一位相乘后加到 score
    4. 返回 score
    """

# TODO：你自己写
    score = 0
    for i in range(len(vector1)):
        score += vector1[i] * vector2[i]
        
    return score


def search(question_vector, documents_list):
    """
    根据问题向量，从 documents_list 中找出最相关的文档。

    TODO：
    1. 准备 best_document
    2. 准备 best_score
    3. 遍历 documents_list
    4. 取出每个文档的 vector
    5. 调用 calculate_similarity()
    6. 打印每个文档的分数，方便 debug
    7. 更新最高分文档
    8. 返回 best_document 和 best_score
    """

# TODO：你自己写
    best_document = None
    best_score = 0
    for document in documents_list:
        vector = document["vector"]
        score = calculate_similarity(question_vector,vector)
        print("当前资料：", document["text"])
        print("当前分数：", score)
        print("-" * 30)
        if score > best_score:
            best_score = score
            best_document = document["text"]
    return best_document, best_score
    


if __name__ == "__main__":
    documents = build_documents(raw_documents)
    question_vector = text_to_fake_vector(question)
    print("问题向量：", question_vector)

    result, score = search(question_vector, documents)

    print("\n用户问题：")
    print(question)

    print("\n最相关资料：")
    print(result)

    print("\n相似度分数：")
    print(score)