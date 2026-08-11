from ..rag.retriever import search


def retrieve_travel_info(
    city: str,
    query: str
):

    results = search(query)


    documents = results.get(
        "documents",
        [[]]
    )[0]


    return {
        "city": city,
        "knowledge": documents
    }