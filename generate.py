import asyncio
import shutil

from pathlib import Path

from app.generate_articles import generate_articles
from app.build_static import render

ROOT = Path(__file__).parent

DIST = ROOT / "dist"


def prepare_dist():

    if DIST.exists():

        shutil.rmtree(DIST)

    DIST.mkdir()

    (DIST / "article").mkdir()


async def main():

    prepare_dist()

    await generate_articles()

    render()

    print("Sitio estático generado correctamente.")


if __name__ == "__main__":

    asyncio.run(main())

import shutil

for file in [
    "robots.txt",
    "sitemap.xml",
    "ads.txt",
    "CNAME"
]:
    shutil.copy(file, DIST / file)

import shutil

FILES_TO_COPY = [
    "robots.txt",
    "sitemap.xml",
    "ads.txt",
    "CNAME",
    "google51e4758e124c73e2.html"
]

for file in FILES_TO_COPY:

    source = ROOT / file

    if source.exists():

        shutil.copy(
            source,
            DIST / file
        )
