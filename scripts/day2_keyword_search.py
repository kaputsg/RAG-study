"""
Day 2：关键词搜索练习

目标：
1. 准备几段知识库文本
2. 输入一个用户问题
3. 根据关键词重合数量计算相关分数
4. 找出最相关的一段资料
"""


documents = [
    "Python 可以用于 Web 后端开发、自动化脚本、数据分析和人工智能应用。",
    "FastAPI 是一个高性能 Python Web 框架，适合开发 API 接口服务。",
    "RAG 是检索增强生成技术，它会先检索知识库资料，再让大模型生成答案。",
    "Vue 是一个前端框架，可以用来构建用户界面。",
    "今天晚上吃什么比较好，可以根据自己的口味选择。"
]


question = "后端服务一般用什么工具开发？"


def calculate_score(question_text, document_text):
    """
    计算用户问题和某一段资料的相关分数。

    当前版本先用最简单的关键词包含判断：
    如果问题里的某个关键词出现在资料里，分数 +1。

    TODO：
    1. 你自己定义一个 keywords 列表
    2. 遍历 keywords
    3. 判断 keyword 是否同时和问题有关，并且出现在 document_text 里
    4. 返回 score
    """

    score = 0

# TODO 1：定义关键词列表
    keywords = ["Python", "后端", "接口", "框架", "FastAPI", "RAG", "Vue", "前端"]

# TODO 2：遍历关键词列表
# 提示：for keyword in keywords:
    for keyword in keywords:
        if keyword in question_text and keyword in document_text:
            score += 1


# TODO 3：如果 keyword 在 question_text 里，并且也在 document_text 里，score += 1
# 提示：if keyword in question_text and keyword in document_text:

    return score


def search(question_text, documents_list):
    """
    从 documents_list 中找出和 question_text 最相关的资料。

    TODO：
    1. 准备 best_document，用来保存当前最相关资料
    2. 准备 best_score，用来保存最高分
    3. 遍历 documents_list
    4. 对每个 document 调用 calculate_score
    5. 如果当前分数更高，就更新 best_document 和 best_score
    6. 返回 best_document 和 best_score
    """

    best_document = None
    best_score = 0

# TODO：遍历 documents_list
    for document in documents_list:
        score = calculate_score(question_text,document)
        print("当前资料：", document)
        print("当前分数：", score)
        print("-" * 30)
        if score > best_score:
            best_score = score
            best_document = document
# TODO：计算每个 document 的 score
# TODO：如果 score > best_score，就更新 best_score 和 best_document

    return best_document, best_score


if __name__ == "__main__":
    result, score = search(question, documents)

    print("用户问题：")
    print(question)

    print("\n最相关资料：")
    print(result)

    print("\n相关分数：")
    print(score)