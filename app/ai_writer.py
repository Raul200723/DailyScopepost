from openai import OpenAI

from app.config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)


def rewrite_article(title: str, description: str, content: str) -> str:

    prompt = f"""
You are a professional journalist.

Rewrite the following news article.

Requirements:

- Write in fluent English.
- Between 700 and 1000 words.
- Do NOT invent facts.
- Keep all important information.
- Use your own words.
- Add headings.
- Use short paragraphs.
- Neutral journalistic tone.
- Do not mention OpenAI.
- Finish with:

Source: Original news publisher.

TITLE:
{title}

DESCRIPTION:
{description}

CONTENT:
{content}
"""

    response = client.responses.create(

        model="gpt-5.1-mini",

        input=prompt,

        temperature=0.3

    )

    return response.output_text.strip()