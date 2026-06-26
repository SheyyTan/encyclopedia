/* =====================================================================
   ENCYCLOPÉDIE — GESTION DE PATRIMOINE FRANCE
   Logique partagée : thème, scroll-spy, recherche live, ariane,
   back-to-top, progression. Vanilla JS, zéro dépendance.
   ===================================================================== */
(function () {
  "use strict";

  /* ---------- Thème clair/sombre persistant ---------- */
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem("encyclo-theme");
    if (saved) root.setAttribute("data-theme", saved);
    else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)
      root.setAttribute("data-theme", "dark");
  } catch (e) {}

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    /* ----- Toggle thème ----- */
    var themeBtn = document.getElementById("themeToggle");
    if (themeBtn) themeBtn.addEventListener("click", function () {
      var now = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", now);
      try { localStorage.setItem("encyclo-theme", now); } catch (e) {}
    });

    /* ----- Menu mobile ----- */
    var navToggle = document.querySelector(".nav-toggle");
    var scrim = document.querySelector(".scrim");
    function closeNav() { document.body.classList.remove("nav-open"); }
    if (navToggle) navToggle.addEventListener("click", function () { document.body.classList.toggle("nav-open"); });
    if (scrim) scrim.addEventListener("click", closeNav);

    /* ----- Back to top + barre de progression ----- */
    var toTop = document.getElementById("toTop");
    var progress = document.getElementById("progress");
    function onScroll() {
      var st = window.scrollY || document.documentElement.scrollTop;
      if (toTop) toTop.classList.toggle("show", st > 500);
      if (progress) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.width = (h > 0 ? (st / h) * 100 : 0) + "%";
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

    /* ----- Scroll-spy + fil d'Ariane ----- */
    var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
    var crumbCurrent = document.getElementById("crumb-current");
    var targets = tocLinks.map(function (a) {
      var el = document.getElementById(a.getAttribute("href").slice(1));
      return el ? { a: a, el: el } : null;
    }).filter(Boolean);

    function spy() {
      var pos = (window.scrollY || 0) + 96;
      var current = null;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].el.offsetTop <= pos) current = targets[i];
      }
      tocLinks.forEach(function (a) { a.classList.remove("active"); });
      if (current) {
        current.a.classList.add("active");
        // garder le lien actif visible dans la sidebar
        var sb = current.a.closest(".sidebar");
        if (sb) {
          var r = current.a.getBoundingClientRect(), rs = sb.getBoundingClientRect();
          if (r.top < rs.top + 60 || r.bottom > rs.bottom - 20) {
            current.a.scrollIntoView({ block: "nearest" });
          }
        }
        if (crumbCurrent) {
          var h = current.el.querySelector("a, .crumb-label") ? null : null;
          crumbCurrent.textContent = (current.el.getAttribute("data-crumb") || current.a.textContent).trim();
        }
      }
    }
    window.addEventListener("scroll", spy, { passive: true });
    spy();

    tocLinks.forEach(function (a) {
      a.addEventListener("click", function () { if (window.innerWidth <= 980) closeNav(); });
    });

    /* ----- Recherche live ----- */
    var input = document.getElementById("searchInput");
    if (input) {
      // unités filtrables : cartes-notion, callouts, sections, tableaux, mini-cards
      var units = Array.prototype.slice.call(
        document.querySelectorAll("[data-search]")
      );
      var noRes = document.getElementById("noResults");
      var debounce;

      function clearMarks(el) {
        var marks = el.querySelectorAll("mark.hit");
        marks.forEach(function (m) {
          var t = document.createTextNode(m.textContent);
          m.parentNode.replaceChild(t, m);
        });
      }
      function markText(el, q) {
        var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
        var nodes = [], n;
        while ((n = walker.nextNode())) nodes.push(n);
        var rx = new RegExp("(" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
        nodes.forEach(function (node) {
          if (!node.nodeValue.trim()) return;
          if (node.parentNode && /^(MARK|SCRIPT|STYLE)$/.test(node.parentNode.nodeName)) return;
          if (!rx.test(node.nodeValue)) return;
          rx.lastIndex = 0;
          var span = document.createElement("span");
          span.innerHTML = node.nodeValue.replace(rx, '<mark class="hit">$1</mark>');
          node.parentNode.replaceChild(span, node);
        });
      }

      function run() {
        var q = input.value.trim().toLowerCase();
        units.forEach(clearMarks);
        if (!q) {
          document.body.classList.remove("searching");
          units.forEach(function (u) { u.classList.remove("search-hidden"); });
          document.querySelectorAll("h2.chapter, h3.section").forEach(function (h) { h.classList.remove("search-hidden"); });
          if (noRes) noRes.style.display = "none";
          return;
        }
        document.body.classList.add("searching");
        var any = false;
        units.forEach(function (u) {
          var hit = (u.getAttribute("data-search") + " " + u.textContent).toLowerCase().indexOf(q) !== -1;
          u.classList.toggle("search-hidden", !hit);
          if (hit) { any = true; markText(u, q); }
        });
        if (noRes) noRes.style.display = any ? "none" : "block";
      }
      input.addEventListener("input", function () {
        clearTimeout(debounce); debounce = setTimeout(run, 130);
      });
      // raccourci "/" pour focus recherche
      document.addEventListener("keydown", function (e) {
        if (e.key === "/" && document.activeElement !== input) { e.preventDefault(); input.focus(); }
        if (e.key === "Escape" && document.activeElement === input) { input.value = ""; run(); input.blur(); }
      });
    }
  });
})();
