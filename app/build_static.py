import json
import shutil

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"

ARTICLES_DIR = (
    BASE_DIR /
    "content" /
    "articles"
)

STATIC_DIR = BASE_DIR / "static"

DIST_DIR = BASE_DIR.parent / "dist"


env = Environment(
    loader=FileSystemLoader(
        str(TEMPLATES_DIR)
    )
)


def clean_dist():

    if DIST_DIR.exists():

        shutil.rmtree(
            DIST_DIR
        )

    DIST_DIR.mkdir(
        exist_ok=True
    )


def copy_static():

    destination = DIST_DIR / "static"

    shutil.copytree(
        STATIC_DIR,
        destination,
        dirs_exist_ok=True
    )


def load_articles():

    articles = []

    for file in ARTICLES_DIR.glob("*.json"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            article = json.load(f)

            articles.append(article)


    articles.sort(
        key=lambda x: x.get(
            "published",
            ""
        ),
        reverse=True
    )


    return articles



def render_template(
    template_name,
    output,
    **context
):

    template = env.get_template(
        template_name
    )


    html = template.render(
        **context
    )


    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    output.write_text(
        html,
        encoding="utf-8"
    )



def build_home(
    articles
):

    render_template(
    "index.html",
    DIST_DIR / "index.html",
    articles=articles,
    asset_path=""
)



def build_articles(
    articles
):

    article_folder = (
        DIST_DIR /
        "article"
    )


    for article in articles:


        filename = (
            article["slug"]
            +
            ".html"
        )


        render_template(
    "article.html",
    article_folder / filename,
    article=article,
    asset_path="../"
)



def build_pages():

    pages = {

        "about.html": "about.html",

        "contact.html": "contact.html",

        "privacy.html": "privacy.html",

        "terms.html": "terms.html",

        "cookies.html": "cookies.html",

    }


    for output, template in pages.items():

        template_path = (
            TEMPLATES_DIR /
            template
        )


        if template_path.exists():

            render_template(
                template,
                DIST_DIR / output,
                canonical=(
                    "https://dailyscopepost.com/"
                    +
                    output
                )
            )

        else:

            print(
                f"No existe plantilla: {template}"
            )



def render():

    print(
        "Generando sitio estático..."
    )


    clean_dist()


    copy_static()


    articles = load_articles()


    build_home(
        articles
    )


    build_articles(
        articles
    )


    build_pages()


    print(
        "Sitio generado en /dist"
    )