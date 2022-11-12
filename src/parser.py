import json
import urllib3
import contextlib
from datetime import datetime

with contextlib.suppress(Exception):
    urllib3.disable_warnings()


def parse(query):
    session = urllib3.PoolManager()
    def_params = dict(
        category="general",
        q=query,
        language="ru-RU",
        format="json",
        engines=['google', 'wikipedia', 'bing', 'wikidata', 'duckduckgo', 'yahoo', 'yandex'],
    )

    url = "https://searx.thegpm.org/search?"

    start_time = datetime.now()

    raw_results = json.loads(
        session.request("GET", url, fields={**def_params}).data.decode("UTF-8")
    )["results"]

    results = []
    for result in raw_results:
        content = ""
        if "content" in result:
            content = result["content"]
        results.append(
            {
                "title": result["title"],
                "url": result["url"],
                "description": content,
            }
        )
    results = {
        "results": results,
        "time": str(datetime.now() - start_time),
        "query": query
    }

    return results
