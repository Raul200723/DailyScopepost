import json
import re
from pathlib import Path

import httpx
from newspaper import Article

from app.fetch_news import get_news

ARTICLES_PATH = Path(__file__).resolve().parent / "content" / "articles"
IMAGES_PATH = Path(__file__).resolve().parent / "content" / "images"

ARTICLES_PATH.mkdir(parents=True, exist_ok=True)
IMAGES_PATH.mkdir(parents=True, exist_ok=True)


def slugify(text: str):

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "-", text)

    return text.strip("-")


def clean_text(text: str):

    if not text:

        return ""

    text = text.replace("\r", "")

    text = re.sub(r"\n{2,}", "\n\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    paragraphs = []

    for p in text.split("\n"):

        p = p.strip()

        if len(p) > 60:

            paragraphs.append(p)

    return "\n\n".join(paragraphs)


def get_full_article(url: str):

    try:

        article = Article(url)

        article.download()

        article.parse()

        text = clean_text(article.text)

        if len(text) > 800:

            return text

    except Exception:

        pass

    return ""


async def download_image(client, url, path):

    if not url:

        return

    try:

        response = await client.get(url, timeout=20)

        if response.status_code == 200:

            path.write_bytes(response.content)

    except Exception:

        pass


async def generate_articles():

    news = await get_news()

    async with httpx.AsyncClient(
        follow_redirects=True
    ) as client:

        for item in news:

            slug = slugify(item["title"])

            image_name = f"{slug}.webp"

            image_path = IMAGES_PATH / image_name

            await download_image(
                client,
                item.get("image"),
                image_path
            )

            full_text = get_full_article(item["url"])

            if not full_text:

                full_text = item.get(
                    "content",
                    item["description"]
                )

            article = {

                "slug": slug,

                "title": item["title"],

                "description": item["description"],

                "content": full_text,

                "published": item["publishedAt"],

                "image": (
                    f"/content/images/{image_name}"
                    if image_path.exists()
                    else "/static/images/no-image.webp"
                ),

                "url": item["url"]

            }

            with open(
                ARTICLES_PATH / f"{slug}.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    article,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

    print("Noticias generadas correctamente.")