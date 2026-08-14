from .embedding import encode_text
from .vector_store import collection


DISTANCE_THRESHOLD = 0.9


def search(
    query: str,
    city: str,
    top_k=3,
    exclude_high_intensity: bool = False
):
    query_vector = encode_text(query)

    where_filter = {
        "city": city
    }

    if exclude_high_intensity:
        where_filter = {
            "$and": [
                {"city": city},
                {"intensity": {"$ne": "高"}}
            ]
        }

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where_filter,
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
            "city": "哈尔滨",
            "query": "适合带父母轻松游览的景点",
            "exclude_high_intensity": True
        },
        {
            "city": "哈尔滨",
            "query": "哈尔滨刺激好玩的景点",
            "exclude_high_intensity": False
        }
    ]

    for item in tests:

        result = search(
            query=item["query"],
            city=item["city"],
            exclude_high_intensity=item["exclude_high_intensity"]
        )

        print("City:", item["city"])
        print("Query:", item["query"])
        print(
            "Exclude High:",
            item["exclude_high_intensity"]
        )
        print("Found:", result["found"])
        print("Best Distance:", result["best_distance"])
        print("Knowledge:")

        for doc in result["knowledge"]:
            print(doc)
            print("---")

        print("================")