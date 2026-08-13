from tavily import TavilyClient

from ..config import TAVILY_API_KEY


client = TavilyClient(
    api_key=TAVILY_API_KEY
)


def search_web(query: str, max_results: int = 5):

    try:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
            include_answer=False
        )

        results = []

        for item in response.get("results", []):

            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                    "score": item.get("score")
                }
            )

        if not results:

            return {
                "available": False,
                "query": query,
                "results": [],
                "message": "未搜索到相关网页信息"
            }

        return {
            "available": True,
            "query": query,
            "results": results
        }


    except Exception as e:

        return {
            "available": False,
            "query": query,
            "results": [],
            "error": str(e)
        }

if __name__ == "__main__":

    result = search_web(
        "哈尔滨冬季适合家庭游玩的冰雪景点"
    )

    print(result)