from pathlib import Path

from app.article_loader import get_articles
from app.article_loader import get_article
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import APP_NAME

app = FastAPI(title=APP_NAME)

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

app.mount(
    "/content",
    StaticFiles(directory=str(BASE_DIR / "content")),
    name="content"
)


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_title": "DailyScope | Latest US News",
            "meta_description": "Latest breaking news from the United States and around the world.",
            "articles": get_articles()
        }
    )


@app.get("/article/{slug}")
async def article(request: Request, slug: str):

    article = get_article(slug)

    if article is None:
        raise HTTPException(404)

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "article": article
        }
    )

@app.get("/about")
async def about(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )


@app.get("/contact")
async def contact(request: Request):

    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )


@app.get("/privacy")
async def privacy(request: Request):

    return templates.TemplateResponse(
        "privacy.html",
        {"request": request}
    )


@app.get("/terms")
async def terms(request: Request):

    return templates.TemplateResponse(
        "terms.html",
        {"request": request}
    )


@app.get("/cookies")
async def cookies(request: Request):

    return templates.TemplateResponse(
        "cookies.html",
        {"request": request}
    )

