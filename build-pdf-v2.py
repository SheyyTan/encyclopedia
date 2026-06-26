# -*- coding: utf-8 -*-
"""Version PDF (à plat, optimisée impression) de la v2 : 12 parties, sans Partie 0."""
import re, io, os
BASE = os.path.dirname(os.path.abspath(__file__))
def read(p):
    with io.open(os.path.join(BASE,p), encoding="utf-8") as f: return f.read()

PARTS = [
 (1,"partie-1-bancaire.html",False,"Produits bancaires & épargne réglementée"),
 (2,"partie-2-fiscalite.html",False,"Fiscalité du patrimoine"),
 (3,"partie-3-enveloppes.html",False,"Enveloppes financières"),
 (4,"partie-4-allocation.html",False,"Allocation d'actifs & instruments"),
 (5,"partie-immo-acquisition.html",True,"Immobilier — acquisition & financement"),
 (6,"partie-5-immobilier.html",False,"Immobilier & immobilier fiscal"),
 (7,"partie-6-matrimonial.html",False,"Régimes & avantages matrimoniaux"),
 (8,"partie-7-transmission.html",False,"Transmission : donation & succession"),
 (9,"partie-societes.html",True,"Sociétés"),
 (10,"partie-comptabilite.html",True,"Comptabilité"),
 (11,"partie-8-entreprise.html",False,"Ingénierie & transmission d'entreprise"),
 (12,"partie-9-synthese.html",False,"Synthèse, cas pratiques & annexes"),
]
OLD2NEW = {1:1,2:2,3:3,4:4,5:6,6:7,7:8,8:11,9:12}
COLORS = {1:"#0f766e",2:"#4338ca",3:"#7c3aed",4:"#b45309",5:"#047857",6:"#15803d",
          7:"#be123c",8:"#1d4ed8",9:"#c2410c",10:"#0e7490",11:"#7e22ce",12:"#475569"}
SOFT = {1:"#dff3f0",2:"#e9e7fb",3:"#f0e8fd",4:"#fbeede",5:"#dcf3ea",6:"#ddf3e3",
        7:"#fbe1e8",8:"#e3ebfd",9:"#fbe7da",10:"#dcf0f6",11:"#f0e2fb",12:"#e8ecf1"}
INK = {1:"#0a554f",2:"#312a9c",3:"#5b21b6",4:"#8a3f07",5:"#03593f",6:"#0f5c2c",
       7:"#8f0d2d",8:"#163fa8",9:"#963209",10:"#0a586e",11:"#5b1799",12:"#33415a"}

def strip_block(css, token):
    while True:
        idx=css.find(token)
        if idx==-1: return css
        b=css.find('{',idx); depth=0; i=b
        while i<len(css):
            if css[i]=='{': depth+=1
            elif css[i]=='}':
                depth-=1
                if depth==0: css=css[:idx]+css[i+1:]; break
            i+=1

css=read("assets/encyclo.css")
css=css.replace('[data-theme="dark"][data-part','[data-theme="dark"] [data-part')
css=strip_block(css,'@media print')
def styles_of(path): return "\n".join(re.findall(r'<style>(.*?)</style>', read(path), re.S))
css+="\n/* annexes */\n"+styles_of("partie-9-synthese.html")
pal=["\n/* palette 12 */"]
for n in range(1,13):
    pal.append('[data-part="%d"]{ --accent:%s; --accent-soft:%s; --accent-ink:%s; }'%(n,COLORS[n],SOFT[n],INK[n]))
css+="\n".join(pal)

PRINT_CSS=r"""
@page{ size:A4; margin:15mm 14mm 16mm; }
html,body{ background:#fff !important; }
body{ font-size:10.3pt; line-height:1.45; }
.content{ padding:0 !important; } .container{ max-width:none !important; margin:0 !important; }
/* compaction (moins de blanc, plus de contenu par page) */
.notion-card{ padding:12px 17px; margin:11px 0; }
.callout{ padding:10px 14px; margin:10px 0; }
.figure{ margin:11px 0; } .table-wrap{ margin:11px 0; } .calc{ margin:10px 0; padding:11px 13px; }
.def{ margin:8px 0; } p{ margin:.45em 0; } ul,ol{ margin:.5em 0; }
.part-hero{ padding:22px 24px 20px; margin:2px 0 16px; }
.part-hero h1{ margin:.2em 0 .15em; } .lead{ margin:.4em 0 .8em; }
.pdf-cover{ break-after:page; } .pdf-toc{ break-after:page; } .pdf-part{ break-before:page; }
.notion-card,.callout,.calc,.figure,.mini,.def,.timeline li,.pill,.ref{ break-inside:avoid; }
.figure svg,svg,img{ break-inside:avoid; }
.part-hero{ break-inside:avoid; break-after:avoid; box-shadow:none; }
/* un tableau ne se coupe pas juste après son en-tête : il bascule entier (sauf s'il dépasse une page) */
.table-wrap{ break-inside:avoid; overflow:visible !important; box-shadow:none; }
.table-wrap::-webkit-scrollbar{ display:none; }
table{ break-inside:avoid; font-size:9.3pt; } td.num,th.num{ font-size:8.8pt; }
thead{ break-after:avoid; }
thead{ display:table-header-group; } tfoot{ display:table-footer-group; }
tr,td,th{ break-inside:avoid; } caption{ break-after:avoid; }
h2.chapter,h3.section,h4.notion,.mini h5,dt,caption{ break-after:avoid; break-inside:avoid; }
/* un paragraphe / item ne se coupe jamais à cheval sur deux pages : il bascule entier */
p,li,dd,dt,.lead,.def,blockquote{ orphans:4; widows:4; break-inside:avoid; }
.calc .row{ break-inside:avoid; }
*{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.notion-card,.mini,.callout{ box-shadow:none; }
h2.chapter{ margin-top:14px; }
.pdf-cover{ min-height:250mm; display:flex; flex-direction:column; justify-content:center; padding:30mm 6mm; color:#fff;
  background:radial-gradient(120% 130% at 0% 0%, #2c5b8f 0%, #1b3c63 55%, #0f2742 100%); }
.pdf-cover .kick{ letter-spacing:.24em; text-transform:uppercase; font-size:11pt; opacity:.82; font-weight:600; }
.pdf-cover h1{ font-size:33pt; line-height:1.08; margin:.3em 0 .2em; letter-spacing:-.02em; max-width:20ch; }
.pdf-cover .sub{ font-size:12.5pt; opacity:.92; max-width:62ch; }
.pdf-cover .cov-meta{ margin-top:22px; font-size:10.5pt; opacity:.9; }
.pdf-cover .cov-disc{ margin-top:28px; font-size:9pt; opacity:.8; max-width:70ch; border-top:1px solid rgba(255,255,255,.3); padding-top:12px; }
.pdf-toc h2{ font-size:20pt; color:#1b3c63; margin:0 0 4px; }
.pdf-toc .toc-part{ margin:13px 0 4px; }
.pdf-toc .toc-part > a{ font-weight:800; font-size:13pt; color:#16263a; text-decoration:none; }
.pdf-toc .toc-part .pno{ display:inline-block; min-width:36px; color:#2c5b8f; font-variant-numeric:tabular-nums; }
.pdf-toc ul{ list-style:none; margin:2px 0 0; padding:0 0 0 36px; }
.pdf-toc ul li{ font-size:10.4pt; padding:1.5px 0; color:#33415a; }
.pdf-toc ul li .n{ display:inline-block; min-width:38px; color:#5b6573; font-variant-numeric:tabular-nums; }
.pdf-toc a{ color:inherit; text-decoration:none; }
"""

def remap_parties(text):
    def repl(m):
        pref=m.group(1); body=m.group(2)
        body2=re.sub(r'\d+', lambda mm: str(OLD2NEW.get(int(mm.group(0)), int(mm.group(0)))), body)
        return pref+body2
    return re.sub(r'(Parties?\s+)(\d+(?:\s*(?:et|,|&|à)\s*\d+)*)', repl, text)

def fix_links(s):
    s=s.replace('href="index.html"','href="#"')
    s=re.sub(r'href="partie-[^"#]*\.html(#[^"]*)?"','#',s)
    return s

toc_rows=[]; parts_html=[]
for num, src, is_new, label in PARTS:
    html=read(src)
    main=re.search(r'(<main class="content"[^>]*>.*</main>)', html, re.S).group(1)
    main=re.sub(r'<nav class="breadcrumb">.*?</nav>','',main,flags=re.S)
    main=re.sub(r'<nav class="part-nav">.*?</nav>','',main,flags=re.S)
    main=re.sub(r'<div class="foot">.*?</div>','',main,flags=re.S)
    main=re.sub(r'\s*data-crumb="[^"]*"','',main)
    main=re.sub(r"--partno:'[^']*'","--partno:'%d'"%num, main)
    main=re.sub(r'id="(c\d[^"]*)"', r'id="p%d-\1"'%num, main)
    if not is_new: main=remap_parties(main)
    main=main.replace('(Partie 0)','(cadre réglementaire)')
    main=fix_links(main)
    parts_html.append('<section class="pdf-part" id="part-anchor-%d" data-part="%d">\n%s\n</section>'%(num,num,main))
    # TOC
    items=re.findall(r'<h([23]) class="(chapter|section)" id="(p%d-[a-z0-9]+)"[^>]*>(.*?)</h[23]>'%num, main, re.S)
    rows=[]
    for lvl,cls,hid,title in items:
        title=re.sub(r'<[^>]+>','',title).strip()
        m=re.match(r'p%d-c(\d+)(?:s(\d+))?'%num, hid)
        if not m: continue
        n=("%d.%s.%s"%(num,m.group(1),m.group(2))) if m.group(2) else ("%d.%s"%(num,m.group(1)))
        rows.append('<li><span class="n">%s</span> <a href="#%s">%s</a></li>'%(n,hid,title))
    toc_rows.append('<div class="toc-part"><span class="pno">%d</span><a href="#part-anchor-%d">Partie %d — %s</a><ul>%s</ul></div>'
                    %(num,num,num,label,"".join(rows)))

COVER=u'''<section class="pdf-cover" data-part="2">
  <div class="kick">Référence professionnelle · LF 2026 / revenus 2025</div>
  <h1>Encyclopédie de la Gestion de Patrimoine</h1>
  <div class="sub">France · niveau conseiller expert (CIF/COA). Fiscalité, enveloppes, immobilier, sociétés, comptabilité, ingénierie patrimoniale et transmission — définitions, calculs détaillés, cas chiffrés et articles du CGI. Édition « en devenir d'être indépendant ».</div>
  <div class="cov-meta">12 parties · glossaire · index des articles cités · édition du 26 juin 2026</div>
  <div class="cov-disc">Document pédagogique et technique. Reflète l'état du droit connu au 26/06/2026 (LF 2026, revenus 2025). Ne constitue ni un conseil personnalisé ni une consultation opposable. Les barèmes, taux et plafonds évoluent : vérifier le texte en vigueur (BOFiP, Légifrance) avant toute décision.</div>
</section>'''
TOC=u'<section class="pdf-toc" data-part="2"><h2>Sommaire</h2>%s</section>'%"".join(toc_rows)

DOC=u'''<!DOCTYPE html><html lang="fr" data-theme="light"><head><meta charset="UTF-8">
<title>Encyclopédie de la Gestion de Patrimoine — France (CIF/COA)</title>
<style>
%s
%s
</style></head><body data-part="2">
%s
%s
%s
</body></html>'''%(css,PRINT_CSS,COVER,TOC,"\n\n".join(parts_html))

out=os.path.join(BASE,"Encyclopedie-Patrimoine-PRINT.html")
with io.open(out,"w",encoding="utf-8") as f: f.write(DOC)
print("OK ->",out); print("Taille: %.0f Ko"%(len(DOC.encode('utf-8'))/1024))
