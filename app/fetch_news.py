import httpx

from app.config import GNEWS_API_KEY
from app.config import LANGUAGE
from app.config import COUNTRY


async def get_news():

    url = (
        f"https://gnews.io/api/v4/top-headlines"
        f"?country={COUNTRY}"
        f"&lang={LANGUAGE}"
        f"&max=15"
        f"&apikey={GNEWS_API_KEY}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(url)

        response.raise_for_status()

        data = response.json()

    return data["articles"]