/* DailyScopePost — main.js
   Vanilla JS, no dependencies. Handles: mobile nav drawer, header search
   overlay, and the cookie consent banner. */

(function () {
  "use strict";

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---------- Mobile nav drawer ---------- */
  var hamburger = qs("[data-hamburger]");
  var drawer = qs("[data-mobile-drawer]");
  var drawerClose = qs("[data-drawer-close]");
  var drawerBackdrop = qs("[data-drawer-backdrop]");

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add("open");
    document.body.style.overflow = "hidden";
    if (hamburger) hamburger.setAttribute("aria-expanded", "true");
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    document.body.style.overflow = "";
    if (hamburger) hamburger.setAttribute("aria-expanded", "false");
  }
  if (hamburger) hamburger.addEventListener("click", openDrawer);
  if (drawerClose) drawerClose.addEventListener("click", closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeDrawer(); closeSearch(); }
  });

  /* ---------- Header search overlay ---------- */
  var searchBtn = qs("[data-search-open]");
  var searchOverlay = qs("[data-search-overlay]");
  var searchOverlayClose = qs("[data-search-close]");
  var searchOverlayInput = qs("[data-search-overlay-input]");
  var searchOverlayForm = qs("[data-search-overlay-form]");

  function openSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.add("open");
    document.body.style.overflow = "hidden";
    setTimeout(function () { if (searchOverlayInput) searchOverlayInput.focus(); }, 50);
  }
  function closeSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.remove("open");
    document.body.style.overflow = "";
  }
  if (searchBtn) searchBtn.addEventListener("click", openSearch);
  if (searchOverlayClose) searchOverlayClose.addEventListener("click", closeSearch);
  if (searchOverlay) {
    searchOverlay.addEventListener("click", function (e) {
      if (e.target === searchOverlay) closeSearch();
    });
  }
  if (searchOverlayForm) {
    searchOverlayForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = (searchOverlayInput && searchOverlayInput.value || "").trim();
      var base = document.body.getAttribute("data-root") || "";
      window.location.href = base + "search.html" + (q ? ("?q=" + encodeURIComponent(q)) : "");
    });
  }

  /* ---------- Cookie consent banner ---------- */
  var COOKIE_KEY = "dsp_cookie_consent";
  var banner = qs("[data-cookie-banner]");
  var acceptBtn = qs("[data-cookie-accept]");
  var rejectBtn = qs("[data-cookie-reject]");

  function getConsent() {
    try { return localStorage.getItem(COOKIE_KEY); } catch (e) { return null; }
  }
  function setConsent(value) {
    try { localStorage.setItem(COOKIE_KEY, value); } catch (e) { /* ignore */ }
  }
  if (banner && !getConsent()) {
    banner.classList.add("visible");
  }
  if (acceptBtn) acceptBtn.addEventListener("click", function () {
    setConsent("accepted");
    if (banner) banner.classList.remove("visible");
    /* Placeholder hook: initialize analytics/ads consent here once IDs are configured. */
  });
  if (rejectBtn) rejectBtn.addEventListener("click", function () {
    setConsent("rejected");
    if (banner) banner.classList.remove("visible");
  });

  /* ---------- Dynamic topbar date ---------- */
  var topbarDateEls = document.querySelectorAll("[data-topbar-date]");
  if (topbarDateEls.length) {
    var todayFormatted = new Date().toLocaleDateString("en-US", {
      weekday: "long", year: "numeric", month: "long", day: "numeric"
    });
    topbarDateEls.forEach(function (el) {
      el.textContent = todayFormatted + " \u00B7 U.S. Edition";
    });
  }
})();
/* DailyScopePost — search.js
   Lightweight client-side search over a local JSON index. No external
   API calls. Matches on title, excerpt, category, author, and tags. */

(function () {
  "use strict";

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var root = document.body.getAttribute("data-root") || "";
  var input = qs("[data-search-input]");
  var resultsEl = qs("[data-search-results]");
  var countEl = qs("[data-search-count]");
  var emptyEl = qs("[data-search-empty]");
  var INDEX = null;

  function params() {
    return new URLSearchParams(window.location.search);
  }

  function loadIndex(cb) {
    if (INDEX) return cb(INDEX);
    fetch(root + "search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { INDEX = data; cb(data); })
      .catch(function () { INDEX = []; cb([]); });
  }

  function score(item, terms) {
    var haystack = (item.title + " " + item.excerpt + " " + item.category + " " +
      item.author + " " + (item.tags || []).join(" ")).toLowerCase();
    var s = 0;
    terms.forEach(function (t) {
      if (!t) return;
      if (item.title.toLowerCase().indexOf(t) !== -1) s += 5;
      if (item.category.toLowerCase().indexOf(t) !== -1) s += 3;
      if (item.author.toLowerCase().indexOf(t) !== -1) s += 2;
      if (haystack.indexOf(t) !== -1) s += 1;
    });
    return s;
  }

  function render(query) {
    if (!resultsEl) return;
    resultsEl.innerHTML = "";
    var q = (query || "").trim().toLowerCase();

    if (!q) {
      if (countEl) countEl.textContent = "";
      if (emptyEl) emptyEl.style.display = "none";
      return;
    }

    var terms = q.split(/\s+/).filter(Boolean);
    var matches = INDEX
      .map(function (item) { return { item: item, s: score(item, terms) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .map(function (r) { return r.item; });

    if (countEl) {
      countEl.textContent = matches.length
        ? matches.length + " result" + (matches.length === 1 ? "" : "s") + " for \u201c" + escapeHtml(query) + "\u201d"
        : "";
    }

    if (!matches.length) {
      if (emptyEl) emptyEl.style.display = "block";
      return;
    }
    if (emptyEl) emptyEl.style.display = "none";

    matches.forEach(function (item) {
      var li = el("li");
      li.innerHTML =
        '<div class="thumb"><img src="' + root + item.image.replace(/^\//, "") + '" alt="" width="92" height="68" loading="lazy"></div>' +
        '<div>' +
        '<span class="tag tag-' + item.categorySlug + '">' + escapeHtml(item.category) + '</span>' +
        '<h3><a href="' + root + item.url + '">' + escapeHtml(item.title) + '</a></h3>' +
        '<p class="excerpt" style="font-size:13.5px;color:var(--ink-soft);margin:4px 0">' + escapeHtml(item.excerpt) + '</p>' +
        '<div class="meta-row"><span>' + escapeHtml(item.author) + '</span><span class="dot"></span><span>' + escapeHtml(item.date) + '</span></div>' +
        '</div>';
      resultsEl.appendChild(li);
    });
  }

  if (input) {
    loadIndex(function () {
      var initial = params().get("q") || "";
      input.value = initial;
      render(initial);
    });
    input.addEventListener("input", function () {
      render(input.value);
      var url = new URL(window.location.href);
      if (input.value) url.searchParams.set("q", input.value); else url.searchParams.delete("q");
      window.history.replaceState({}, "", url);
    });
  }
})();
