from .embedding import encode_text
from .vector_store import collection


DISTANCE_THRESHOLD = 0.9


def search(query: str, city: str, top_k=3):

    query_vector = encode_text(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={
            "city": city
        },
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    if not documents:
        return {
            "found": False,
            "knowledge": [],
            "best_distance": None
        }

    best_distance = distances[0]

    if best_distance >= DISTANCE_THRESHOLD:
        return {
            "found": False,
            "knowledge": [],
            "best_distance": best_distance
        }

    return {
        "found": True,
        "knowledge": documents,
        "best_distance": best_distance
    }


if __name__ == "__main__":

    tests = [
        {
            "city": "成都",
            "query": "适合老人旅游的地方"
        },
        {
            "city": "哈尔滨",
            "query": "冬天有哪些冰雪景点"
        }
    ]

    for item in tests:

        result = search(
            query=item["query"],
            city=item["city"]
        )

        print("City:", item["city"])
        print("Query:", item["query"])
        print("Found:", result["found"])
        print("Best Distance:", result["best_distance"])
        print("Knowledge:", result["knowledge"])
        print("================")