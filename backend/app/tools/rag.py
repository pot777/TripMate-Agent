from ..rag.retriever import search


def retrieve_travel_info(
    city: str,
    query: str,
    exclude_high_intensity: bool = False
):
    result = search(
        query=query,
        city=city,
        exclude_high_intensity=exclude_high_intensity
    )

    return {
        "city": city,
        "available": result["found"],
        "knowledge": result["knowledge"],
        "best_distance": result["best_distance"]
    }