# -*- coding: utf-8 -*-
"""Génère une version 'à plat' optimisée impression -> Encyclopedie-Patrimoine-PRINT.html"""
import re, io, os
BASE = os.path.dirname(os.path.abspath(__file__))
def read(p):
    with io.open(os.path.join(BASE,p), encoding="utf-8") as f: return f.read()

PARTS = [
    ("0","partie-0-cadre.html","Cadre, métiers & réglementation"),
    ("1","partie-1-bancaire.html","Produits bancaires & épargne réglementée"),
    ("2","partie-2-fiscalite.html","Fiscalité du patrimoine"),
    ("3","partie-3-enveloppes.html","Enveloppes financières"),
    ("4","partie-4-allocation.html","Allocation d'actifs & instruments"),
    ("5","partie-5-immobilier.html","Immobilier & immobilier fiscal"),
    ("6","partie-6-matrimonial.html","Régimes & avantages matrimoniaux"),
    ("7","partie-7-transmission.html","Transmission : donation & succession"),
    ("8","partie-8-entreprise.html","Ingénierie & transmission d'entreprise"),
    ("9","partie-9-synthese.html","Synthèse, cas pratiques & annexes"),
]

def strip_block(css, token):
    while True:
        idx = css.find(token)
        if idx == -1: return css
        b = css.find('{', idx); depth=0; i=b
        while i < len(css):
            if css[i]=='{': depth+=1
            elif css[i]=='}':
                depth-=1
                if depth==0:
                    css = css[:idx] + css[i+1:]; break
            i+=1

css = read("assets/encyclo.css")
css = css.replace('[data-theme="dark"][data-part', '[data-theme="dark"] [data-part')
css = strip_block(css, '@media print')          # on pilote l'impression nous-mêmes
def styles_of(path): return "\n".join(re.findall(r'<style>(.*?)</style>', read(path), re.S))
css += "\n/* annexes */\n" + styles_of("partie-9-synthese.html")

PRINT_CSS = r"""
/* ====== mise en page PDF ====== */
@page{ size:A4; margin:15mm 14mm 16mm; }
html,body{ background:#fff !important; }
body{ font-size:10.6pt; line-height:1.5; }
.content{ padding:0 !important; }
.container{ max-width:none !important; margin:0 !important; }

/* sauts de page entre grandes sections */
.pdf-cover{ break-after:page; }
.pdf-toc{ break-after:page; }
.pdf-part{ break-before:page; }

/* --- anti-chevauchement : blocs insécables --- */
.callout,.calc,.figure,.mini,.def,.timeline li,.pill,.ref{ break-inside:avoid; }
.figure svg,svg,img{ break-inside:avoid; }
.part-hero{ break-inside:avoid; break-after:avoid; }
/* tableaux : la table peut couvrir plusieurs pages mais chaque ligne reste entière + en-tête répété */
.table-wrap{ break-inside:auto; overflow:visible !important; box-shadow:none; }
.table-wrap::-webkit-scrollbar{ display:none; }
table{ break-inside:auto; font-size:9.3pt; }
td.num,th.num{ font-size:8.8pt; }
thead{ display:table-header-group; }
tfoot{ display:table-footer-group; }
tr,td,th{ break-inside:avoid; }
caption{ break-after:avoid; }
/* titres solidaires du contenu qui suit */
h2.chapter,h3.section,h4.notion,.mini h5,dt,caption{ break-after:avoid; break-inside:avoid; }
/* cohésion des paragraphes : jamais 1-2 lignes orphelines à cheval */
p,li,dd,dt{ orphans:3; widows:3; }
.lead{ orphans:3; widows:3; }

/* couleurs fidèles dans le PDF */
*{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }

/* le hero garde sa couleur ; on enlève juste l'ombre */
.part-hero{ box-shadow:none; }
.notion-card,.table-wrap,.mini,.callout{ box-shadow:none; }

/* espace avant chaque titre de chapitre pour respirer */
h2.chapter{ margin-top:24px; }

/* ====== page de garde ====== */
.pdf-cover{ min-height:262mm; display:flex; flex-direction:column; justify-content:center;
  padding:30mm 6mm; color:#fff; border-radius:0;
  background:radial-gradient(120% 130% at 0% 0%, #2c5b8f 0%, #1b3c63 55%, #0f2742 100%); }
.pdf-cover .kick{ letter-spacing:.24em; text-transform:uppercase; font-size:11pt; opacity:.82; font-weight:600; }
.pdf-cover h1{ font-size:34pt; line-height:1.08; margin:.3em 0 .2em; letter-spacing:-.02em; max-width:20ch; }
.pdf-cover .sub{ font-size:13pt; opacity:.92; max-width:60ch; }
.pdf-cover .cov-meta{ margin-top:22px; font-size:10.5pt; opacity:.9; }
.pdf-cover .cov-disc{ margin-top:30px; font-size:9pt; opacity:.8; max-width:70ch; border-top:1px solid rgba(255,255,255,.3); padding-top:12px; }

/* ====== sommaire ====== */
.pdf-toc h2{ font-size:20pt; color:#1b3c63; margin:0 0 4px; }
.pdf-toc .toc-part{ margin:14px 0 4px; }
.pdf-toc .toc-part > a{ font-weight:800; font-size:13pt; color:#16263a; text-decoration:none; }
.pdf-toc .toc-part .pno{ display:inline-block; min-width:34px; color:#2c5b8f; font-variant-numeric:tabular-nums; }
.pdf-toc ul{ list-style:none; margin:2px 0 0; padding:0 0 0 34px; }
.pdf-toc ul li{ font-size:10.5pt; padding:1.5px 0; color:#33415a; }
.pdf-toc ul li .n{ display:inline-block; min-width:36px; color:#5b6573; font-variant-numeric:tabular-nums; }
.pdf-toc a{ color:inherit; text-decoration:none; }

/* part opener color tab inherits data-part accent */
.pdf-part .part-hero{ margin-top:0; }
"""

def fix_links(s):
    s = s.replace('href="index.html"', 'href="#"')
    s = re.sub(r'href="partie-\d+-[^"#]*\.html(#[^"]*)?"', '#', s)
    return s

def strip_nongreedy(s, tag_open_re):
    return re.sub(tag_open_re, '', s, flags=re.S)

toc_rows = []
parts_html = []
for num, path, label in PARTS:
    html = read(path)
    main = re.search(r'(<main class="content"[^>]*>.*</main>)', html, re.S).group(1)
    # retirer la navigation propre à l'écran
    main = re.sub(r'<nav class="breadcrumb">.*?</nav>', '', main, flags=re.S)
    main = re.sub(r'<nav class="part-nav">.*?</nav>', '', main, flags=re.S)
    main = re.sub(r'<div class="foot">.*?</div>', '', main, flags=re.S)
    # namespacing des ancres
    main = re.sub(r'id="(c\d[^"]*)"', r'id="p%s-\1"' % num, main)
    main = fix_links(main)
    parts_html.append('<section class="pdf-part" data-part="%s">\n%s\n</section>' % (num, main))
    # ---- collecte sommaire (chapitres + sections) ----
    items = re.findall(r'<h([23]) class="(chapter|section)" id="(p\d+-[a-z0-9]+)"[^>]*>(.*?)</h[23]>', main, re.S)
    rows = []
    for lvl, cls, hid, title in items:
        title = re.sub(r'<[^>]+>', '', title).strip()
        m = re.match(r'p(\d+)-c(\d+)(?:s(\d+))?', hid)
        if not m: continue
        if m.group(3):
            n = "%s.%s.%s" % (m.group(1), m.group(2), m.group(3))
            rows.append('<li><span class="n">%s</span> <a href="#%s">%s</a></li>' % (n, hid, title))
        else:
            n = "%s.%s" % (m.group(1), m.group(2))
            rows.append('<li><span class="n">%s</span> <a href="#%s">%s</a></li>' % (n, hid, title))
    toc_rows.append('<div class="toc-part"><span class="pno">%s</span><a href="#part-anchor-%s">Partie %s — %s</a><ul>%s</ul></div>'
                    % (num, num, num, label, "".join(rows)))
    # ancre de partie (sur le hero)
    parts_html[-1] = parts_html[-1].replace('<section class="pdf-part" data-part="%s">' % num,
                                            '<section class="pdf-part" id="part-anchor-%s" data-part="%s">' % (num, num))

COVER = u'''<section class="pdf-cover" data-part="0">
  <div class="kick">Référence professionnelle · LF 2026 / revenus 2025</div>
  <h1>Encyclopédie de la Gestion de Patrimoine</h1>
  <div class="sub">France · niveau conseiller expert (CIF/COA). Fiscalité, enveloppes financières, immobilier, ingénierie patrimoniale, transmission et entreprise — définitions, calculs détaillés, cas chiffrés et articles du CGI.</div>
  <div class="cov-meta">10 parties · glossaire · index des articles cités · édition du 25 juin 2026</div>
  <div class="cov-disc">Document pédagogique et technique. Reflète l'état du droit connu au 25/06/2026 (LF 2026, revenus 2025). Ne constitue ni un conseil personnalisé ni une consultation opposable. Les barèmes, taux et plafonds évoluent : vérifier le texte en vigueur (BOFiP, Légifrance) avant toute décision.</div>
</section>'''

TOC = u'<section class="pdf-toc" data-part="0"><h2>Sommaire</h2>%s</section>' % "".join(toc_rows)

DOC = u'''<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
<meta charset="UTF-8">
<title>Encyclopédie de la Gestion de Patrimoine — France (CIF/COA)</title>
<style>
%s
%s
</style>
</head>
<body data-part="0">
%s
%s
%s
</body>
</html>''' % (css, PRINT_CSS, COVER, TOC, "\n\n".join(parts_html))

out = os.path.join(BASE, "Encyclopedie-Patrimoine-PRINT.html")
with io.open(out, "w", encoding="utf-8") as f: f.write(DOC)
print("OK ->", out)
print("Taille: %.0f Ko" % (len(DOC.encode('utf-8'))/1024))
