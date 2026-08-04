import json
from pathlib import Path


ARTICLES_PATH = (
    Path(__file__)
    .resolve()
    .parent
    / "content"
    / "articles"
)


def get_articles():

    articles = []

    for file in ARTICLES_PATH.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:

            article = json.load(f)

            articles.append(article)

    articles.sort(
        key=lambda x: x["published"],
        reverse=True
    )

    return articles


def get_article(slug):

    articles = get_articles()

    for article in articles:

        if article["slug"] == slug:

            return article

    return None