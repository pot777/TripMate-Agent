from ..rag.retriever import search


def retrieve_travel_info(
    city: str,
    query: str
):

    result = search(
        query=query,
        city=city
    )

    
    return {
        "city": city,
        "available": result["found"],
        "knowledge": result["knowledge"],
        "best_distance": result["best_distance"]
    }