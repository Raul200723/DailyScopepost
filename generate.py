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