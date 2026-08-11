import json
import os

import chromadb

from .embedding import encode_text


CHROMA_PATH = "./chroma_db"

DOCUMENT_PATH = "./app/rag/documents/chengdu.json"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name="travel_knowledge"
)


def format_document(item):

    suitable_for = "、".join(
        item["suitable_for"]
    )

    return f"""
景点名称：{item["name"]}。
所在城市：{item["city"]}。
类型：{item["type"]}。
游玩强度：{item["intensity"]}。
适合人群：{suitable_for}。
建议游玩时间：{item["duration"]}。
注意事项：{item["tips"]}。
"""


def load_documents():

    with open(
        DOCUMENT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def build_vector_store():

    documents = load_documents()

    texts = []
    ids = []
    metadatas = []
    embeddings = []


    for index,item in enumerate(documents):

        text = format_document(item)

        vector = encode_text(text)

        texts.append(text)

        ids.append(
            str(index)
        )

        metadatas.append(
            {
                "city":item["city"],
                "name":item["name"]
            }
        )

        embeddings.append(vector)



    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )


    print(
        f"Added {len(documents)} documents"
    )



if __name__ == "__main__":

    build_vector_store()

    print(
        "Collection count:",
        collection.count()
    )