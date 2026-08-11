# DailyScopePost

An independent, U.S.-focused digital news publication. This is a **100% static
website** — plain HTML, CSS, and vanilla JavaScript. There is no build step,
no framework, no server, and no database. You can open any `.html` file
directly in a browser, edit it in VS Code, and see your changes immediately.

---

## 1. What's in this project

```
dailyscopepost/
├── index.html                  Homepage
├── us-news.html                Category pages (9 total)
├── politics.html
├── business.html
├── technology.html
├── science.html
├── health.html
├── world.html
├── money.html
├── lifestyle.html
├── explainers.html             Cross-category evergreen explainers hub
│
├── articles/                   20 full article pages
│   └── article-slug.html
│
├── authors/                    6 author profile pages
│   └── author-slug.html
│
├── css/
│   └── style.css               Single stylesheet — the whole design system
│
├── js/
│   └── script.js               Mobile nav, search overlay, cookie banner,
│                                and the client-side search logic
│
├── images/
│   ├── articles/                Article hero images (SVG placeholders)
│   ├── authors/                 Author avatars (SVG placeholders)
│   └── icons/                   Favicon, logo, fallback image
│
├── about.html, contact.html, editorial-policy.html, fact-checking.html,
├── corrections.html, privacy-policy.html, terms.html, cookie-policy.html,
├── disclaimer.html              Trust / legal / editorial pages
│
├── search.html                  Client-side search page
├── search-index.json            Local search index (no external API)
├── 404.html                     Custom not-found page
│
├── robots.txt
├── sitemap.xml
├── ads.txt                      Placeholder — see section 6 below
└── CNAME                        GitHub Pages custom domain file
```

Every page is a **complete, standalone HTML file**. The header, navigation,
footer, and cookie banner markup is duplicated across every page on purpose —
there's no template engine stitching things together at request time. This
is intentional: it keeps the project simple to host anywhere and easy to
hand-edit, at the cost of some repeated markup.

---

## 2. How to add a new article

1. Duplicate the article file closest in topic to your new one, e.g.:
   ```
   cp articles/what-is-inflation.html articles/your-new-article.html
   ```
2. Open the new file and update, from top to bottom:
   - `<title>` and `<meta name="description">`
   - `<link rel="canonical">` — update the path to match your new filename
   - The Open Graph (`og:*`) and Twitter meta tags
   - The `<script type="application/ld+json">` blocks (there are two: an
     `Article`/`NewsArticle` block and a `BreadcrumbList` block) — update
     `headline`, `description`, `image`, `datePublished`, `dateModified`,
     `author`, and the breadcrumb `item` URLs
   - The breadcrumb HTML near the top of `<main>`
   - The category tag, `<h1>`, dek, byline (name/avatar/link), published
     date, hero image `src`/`alt`, and caption/credit
   - The article body itself
   - The "Key Takeaways" box and "Common Questions" (FAQ) section, or
     delete them if not relevant
   - The author box at the bottom
   - The "Related Stories" cards (link to 2–3 genuinely related articles)
3. Add a hero image to `images/articles/` (see section 5 below).
4. Add a card linking to the new article on the relevant category page
   (e.g. `money.html`) and, if it should be featured, on `index.html`.
5. Add an entry to `search-index.json` so the new article is searchable:
   ```json
   {
     "title": "...", "url": "articles/your-new-article.html",
     "excerpt": "...", "category": "Money", "categorySlug": "money",
     "author": "Author Name", "tags": ["Tag1", "Tag2"],
     "image": "/images/articles/your-image.svg", "date": "Aug 09, 2026"
   }
   ```
6. Add a `<url>` entry to `sitemap.xml`.

No build command is required — save the file and it's live.

---

## 3. How to edit categories

Categories are just the 9 top-level `.html` files (`us-news.html`,
`politics.html`, etc.). To change a category's name, description, or which
articles appear in it, edit that file directly — the intro copy is near the
top, and article cards follow below. The category list also appears in the
navigation and footer of **every** page, so if you rename a category, update
the `<nav>` and `<footer>` blocks across all files (a project-wide
find-and-replace in VS Code works well for this).

---

## 4. How to update authors

Each author has one profile page in `authors/`. To edit an author's bio,
title, or coverage areas, open their file directly. To change how an author
appears elsewhere (byline, author box), you'll need to update those sections
on each of their articles — search your editor for the author's name or
avatar filename to find every reference.

To add a new author:
1. Copy an existing file in `authors/` as a starting point.
2. Add an avatar SVG to `images/authors/`.
3. Update articles' bylines and author boxes to reference the new author.

---

## 5. How to replace images

All images currently ship as **SVG placeholders** — simple duotone graphics
in the site's brand colors with a topic icon, clearly not real photography.
They're there so the site doesn't look empty, and so you can see the layout
and aspect ratios working correctly.

To replace one:
1. Export/save your real photo as `.webp` (preferred) or `.jpg`, ideally at
   a 16:9 ratio for article heroes (e.g. 1600×900).
2. Drop it into `images/articles/` (or `images/authors/` for headshots).
3. Update the `src` attribute wherever that image is referenced (hero image,
   any card thumbnails, Open Graph `og:image` tag, and the structured data
   `image` field).
4. Update the `alt` text to describe the real photo, and update the caption
   / credit line with the actual photographer or source.

Keep `width`/`height` attributes on `<img>` tags accurate to the new file's
dimensions — this prevents layout shift (good for Core Web Vitals).

---

## 6. Before you go live

- **ads.txt** — Replace `pub-XXXXXXXXXXXXXXXX` with your real Google AdSense
  publisher ID once your AdSense account is approved (find it under
  Account → Account information in AdSense).
- **Analytics** — This build does not include any analytics snippet by
  default. When you're ready, add your Google Analytics (GA4) tag and/or
  Google Search Console verification meta tag to the `<head>` of every page
  (or at minimum `index.html` for Search Console verification).
- **AdSense script** — Add the AdSense loader script to the `<head>` of
  every page once approved, and consider activating the reserved ad slots
  already marked in the markup (search for `class="ad-slot"` in
  `css/style.css` / the category and article pages) with real `<ins>` ad
  units.
- **Contact emails** — `contact.html` uses placeholder addresses like
  `hello@dailyscopepost.com`. Replace with real, monitored inboxes.
- **Cookie consent** — `js/script.js` includes a lightweight accept/reject
  banner that stores the choice in `localStorage`. It's built so you can
  swap in a full consent management platform (CMP) later without redesigning
  the page — look for the `cookie-banner` functions in `js/script.js`.
- **CNAME** — Already set to `dailyscopepost.com` for GitHub Pages. Update
  or remove if you're using a different domain or host.

---

## 7. Deploying to GitHub Pages

1. Push this entire folder to a GitHub repository (the repo root should be
   this folder, i.e. `index.html` sits at the repo root).
2. In the repo, go to **Settings → Pages**.
3. Under "Build and deployment," set Source to **Deploy from a branch**,
   and pick the branch/folder containing these files (typically `main` /
   `root`).
4. If using the custom domain, make sure your DNS points to GitHub Pages and
   that the `CNAME` file (already included) matches your domain.
5. GitHub Pages will serve the site directly — no build step runs. All paths
   in this project are relative and have been verified to work both at the
   domain root and from one level deep (`articles/`, `authors/`).

This project also works on any other static host (Netlify, Cloudflare Pages,
S3 + CloudFront, etc.) — just upload the folder as-is.

---

## 8. Local preview

To preview the site locally before deploying, from this folder run:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000/` in a browser. (This is just for local
preview — it is not required for hosting or for the site to function.)

---

## 9. Design system quick reference

All colors, fonts, spacing, and component styles live in `css/style.css` as
CSS custom properties at the top of the file (`:root { --ink: ...; }`).
Change a value there and it updates sitewide. Category tag colors
(`--cat-us-news`, `--cat-money`, etc.) are also defined there.

- Headlines: Georgia/serif system stack (`--font-display`)
- Body text: system UI sans-serif stack (`--font-body`)
- No external font or icon requests — everything renders from system fonts
  and inline SVG, which keeps the site fast and avoids extra network
  requests.

---

## 10. What's intentionally *not* included

- No analytics IDs, ad publisher IDs, or API keys are hard-coded anywhere.
- No tracking scripts run until you add them.
- No article claims to be breaking news reporting — the 20 included articles
  are evergreen explainers and general-interest guides, clearly written as
  such, per the site's own Editorial Policy (`editorial-policy.html`).
