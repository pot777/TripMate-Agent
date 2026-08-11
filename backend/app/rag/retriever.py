from .embedding import encode_text
from .vector_store import collection


def search(query: str, top_k=3):

    # 1. 将用户问题转换成向量
    query_vector = encode_text(query)


    # 2. 查询向量数据库
    results = collection.query(
        query_embeddings=[
            query_vector
        ],
        n_results=top_k
    )


    return results



if __name__ == "__main__":

    query = "成都适合老人旅游的地方"


    results = search(query)


    print("Query:")
    print(query)

    print("================")

    for i, doc in enumerate(
        results["documents"][0]
    ):

        print(
            f"Result {i+1}:"
        )

        print(doc)

        print("----------------")