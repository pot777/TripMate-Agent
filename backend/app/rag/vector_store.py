# vector_store.py
import json
import logging
from pathlib import Path

import chromadb

from ..config import CHROMA_DB_PATH
from .embedding import encode_text


logger = logging.getLogger(__name__)

CHROMA_PATH = CHROMA_DB_PATH

DOCUMENT_PATH = Path(__file__).resolve().parent / "documents" / "chengdu.json"


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
                "city": item["city"],
                "name": item["name"],
                "type": item["type"],
                "intensity": item["intensity"],
                "suitable_for": "、".join(item["suitable_for"])
            }
        )

        embeddings.append(vector)



    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )


    logger.info("Added %s seed documents to the travel knowledge store", len(documents))


def ensure_vector_store_initialized():
    document_count = collection.count()

    if document_count > 0:
        logger.info(
            "Travel knowledge store already initialized with %s documents",
            document_count
        )
        return

    logger.info("Travel knowledge store is empty; loading seed documents")
    build_vector_store()



if __name__ == "__main__":

    build_vector_store()

    print(
        "Collection count:",
        collection.count()
    )
