import json

from ..llm import chat_raw
from .embedding import encode_text
from .vector_store import collection, format_document


def extract_knowledge(city: str, web_results: list):

    prompt = f"""
你是一个旅游知识抽取器。

请根据下面的网页搜索结果，提取适合加入旅游知识库的景点信息。

目标城市：
{city}

网页搜索结果：
{web_results}

要求：

1. 只提取与目标城市直接相关的景点。
2. 忽略广告、酒店、旅行团、机票等营销信息。
3. 不要提取明显属于其他城市的内容。
4. 如果信息不足，不要编造。
5. 每个景点输出以下字段：

name：景点名称
city：城市
type：景点类型
intensity：游玩强度，只能是“低”“中等”“高”
suitable_for：适合人群列表
duration：建议游玩时间
tips：游玩建议

6. 最多提取5个景点。
7. 只能输出JSON数组，不要输出Markdown，不要输出解释。

输出格式：

[
  {{
    "name": "景点名称",
    "city": "{city}",
    "type": "历史文化",
    "intensity": "低",
    "suitable_for": ["老人", "家庭"],
    "duration": "2小时",
    "tips": "游玩建议"
  }}
]
"""

    response = chat_raw(prompt)

    print("====== KNOWLEDGE EXTRACTION RAW ======")
    print(response)
    print("======================================")

    try:
        items = json.loads(response)

    except json.JSONDecodeError:
        return []

    # 基础清洗：只保留目标城市
    valid_items = []

    for item in items:

        if not isinstance(item, dict):
            continue

        if item.get("city") != city:
            continue

        if not item.get("name"):
            continue

        valid_items.append(item)

    return valid_items


def build_document_id(item: dict):

    city = item["city"].strip()
    name = item["name"].strip()

    return f"{city}_{name}"


def write_knowledge(items: list):

    if not items:
        return {
            "written": 0,
            "ids": []
        }

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for item in items:

        if not item.get("name") or not item.get("city"):
            continue

        document_id = build_document_id(item)

        text = format_document(item)

        vector = encode_text(text)

        ids.append(document_id)
        documents.append(text)
        embeddings.append(vector)

        metadatas.append(
            {
                "city": item["city"],
                "name": item["name"],
                "type": item["type"],
                "intensity": item["intensity"],
                "suitable_for": "、".join(item["suitable_for"])
            }
        )

    if not ids:
        return {
            "written": 0,
            "ids": []
        }

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "written": len(ids),
        "ids": ids
    }


def expand_knowledge(
    city: str,
    query: str,
    web_results: list
):

    items = extract_knowledge(
        city=city,
        web_results=web_results
    )

    if not items:

        return {
            "expanded": False,
            "query": query,
            "extracted": 0,
            "written": 0,
            "ids": []
        }

    write_result = write_knowledge(items)

    return {
        "expanded": write_result["written"] > 0,
        "query": query,
        "extracted": len(items),
        "written": write_result["written"],
        "ids": write_result["ids"]
    }


if __name__ == "__main__":

    test_results = [
        {
            "title": "哈尔滨旅游攻略",
            "content": """
            中央大街是哈尔滨著名步行街，
            适合老人和家庭轻松游览，
            建议游玩2小时。

            圣索菲亚大教堂是哈尔滨著名历史建筑，
            适合文化参观和拍照。
            """
        }
    ]

    result = expand_knowledge(
        city="哈尔滨",
        query="哈尔滨适合带父母旅游的景点",
        web_results=test_results
    )

    print(result)