# -*- coding: utf-8 -*-
"""Assemble la v2 (sans Partie 0, +3 nouvelles parties, renumérotée) -> Encyclopedie-Patrimoine.html"""
import re, io, os
BASE = os.path.dirname(os.path.abspath(__file__))
def read(p):
    with io.open(os.path.join(BASE,p), encoding="utf-8") as f: return f.read()

# (new_num, source_file, is_new, color, label, hub_desc, hub_tags)
PARTS = [
 (1,"partie-1-bancaire.html",False,"Produits bancaires &amp; épargne",
   "Livrets, plans d'épargne logement et comptes à terme : l'épargne de précaution.",["Livret A · LEP","PEL · CEL","DAT","PFU"]),
 (2,"partie-2-fiscalite.html",False,"Fiscalité du patrimoine",
   "IR et quotient, flat tax, prélèvements sociaux, IFI, IS, plus-values.",["IR","PFU 30 %","IFI","Plus-values"]),
 (3,"partie-3-enveloppes.html",False,"Enveloppes financières",
   "CTO, PEA, assurance-vie FR + Luxembourg, capitalisation, PER.",["PEA","Assurance-vie","PER","Capi."]),
 (4,"partie-4-allocation.html",False,"Allocation d'actifs &amp; instruments",
   "Classes d'actifs, ETF, produits structurés, private equity, SCPI.",["ETF","Structurés","Private equity","SCPI"]),
 (5,"partie-immo-acquisition.html",True,"Immobilier — acquisition &amp; financement",
   "Acheter à crédit : capacité d'emprunt, amortissement, assurance, garanties.",["Crédit","Amortissement","Assurance","Rendement"]),
 (6,"partie-5-immobilier.html",False,"Immobilier &amp; immobilier fiscal",
   "SCI, démembrement, LMNP/LMP, déficit foncier, Malraux, Monuments Historiques.",["LMNP","Déficit foncier","Malraux","Nue-propriété"]),
 (7,"partie-6-matrimonial.html",False,"Régimes &amp; avantages matrimoniaux",
   "Régimes, préciput, clause alsacienne, donation entre époux, PACS.",["Communauté","Préciput","Clause alsacienne","Donation"]),
 (8,"partie-7-transmission.html",False,"Transmission : donation &amp; succession",
   "Dévolution, réserve, abattements, barème DMTG, démembrement, assurance-vie.",["Abattements","DMTG","Donation-partage","990 I"]),
 (9,"partie-societes.html",True,"Sociétés",
   "Formes de sociétés, statut social du dirigeant (TNS / assimilé salarié), IR/IS, dividendes.",["EURL · SARL","SASU · SAS","TNS","Dividendes"]),
 (10,"partie-comptabilite.html",True,"Comptabilité",
   "Bilan (actif, passif), compte de résultat, ratios, ce qui fait la rentabilité.",["Bilan","Résultat","BFR","Rentabilité"]),
 (11,"partie-8-entreprise.html",False,"Ingénierie &amp; transmission d'entreprise",
   "Pacte Dutreil, apport-cession, holding, OBO, donation avant cession.",["Dutreil","Apport-cession","OBO","Holding"]),
 (12,"partie-9-synthese.html",False,"Synthèse, cas pratiques &amp; annexes",
   "Cas intégrés, arbres de décision, check-lists, glossaire, index des articles.",["Cas pratiques","Check-lists","Glossaire","Index CGI"]),
]

# mapping ancien numéro -> nouveau (pour les renvois textuels "Partie X" dans les fichiers existants)
OLD2NEW = {1:1,2:2,3:3,4:4,5:6,6:7,7:8,8:11,9:12}

COLORS = {  # num: (accent, soft, ink, darkAccent, darkSoft, darkInk)
 1:("#0f766e","#dff3f0","#0a554f","#2dd4bf","#0c2b28","#7ff0e3"),
 2:("#4338ca","#e9e7fb","#312a9c","#818cf8","#1a1b35","#c3c8ff"),
 3:("#7c3aed","#f0e8fd","#5b21b6","#a78bfa","#231634","#d6c6ff"),
 4:("#b45309","#fbeede","#8a3f07","#fbbf24","#2a1f0a","#ffe2a3"),
 5:("#047857","#dcf3ea","#03593f","#34d399","#0c2a20","#9bf0cf"),
 6:("#15803d","#ddf3e3","#0f5c2c","#4ade80","#0c2616","#b4f3c6"),
 7:("#be123c","#fbe1e8","#8f0d2d","#fb7185","#330d18","#ffc0cb"),
 8:("#1d4ed8","#e3ebfd","#163fa8","#60a5fa","#0f203f","#bdd6ff"),
 9:("#c2410c","#fbe7da","#963209","#fb923c","#2a1408","#ffcda3"),
 10:("#0e7490","#dcf0f6","#0a586e","#22d3ee","#0a2730","#9aeaf8"),
 11:("#7e22ce","#f0e2fb","#5b1799","#c084fc","#220c33","#e3c6ff"),
 12:("#475569","#e8ecf1","#33415a","#94a3b8","#1a2029","#cbd5e1"),
}

# ---------- CSS ----------
css = read("assets/encyclo.css")
css = strip = css.replace('[data-theme="dark"][data-part', '[data-theme="dark"] [data-part')
def styles_of(path): return "\n".join(re.findall(r'<style>(.*?)</style>', read(path), re.S))
css += "\n/* hub */\n" + styles_of("index.html")
css += "\n/* annexes */\n" + styles_of("partie-9-synthese.html")
# palette 12 couleurs (override)
pal = ["\n/* === palette 12 parties === */"]
for n,(a,s,ink,da,ds,di) in COLORS.items():
    pal.append('[data-part="%d"]{ --accent:%s; --accent-soft:%s; --accent-ink:%s; }'%(n,a,s,ink))
    pal.append('[data-theme="dark"] [data-part="%d"]{ --accent:%s; --accent-soft:%s; --accent-ink:%s; }'%(n,da,ds,di))
css += "\n".join(pal)
css += "\n/* router */\n.part-page{ display:none; } .part-page.active{ display:block; }\n"

def fix_internal(s):
    s = s.replace('href="index.html"', 'href="#hub"')
    s = re.sub(r'href="partie-[^"#]*\.html(#[^"]*)?"', '#', s)
    return s

def remap_parties(text):
    def repl(m):
        pref=m.group(1); body=m.group(2)
        body2=re.sub(r'\d+', lambda mm: str(OLD2NEW.get(int(mm.group(0)), int(mm.group(0)))), body)
        return pref+body2
    return re.sub(r'(Parties?\s+)(\d+(?:\s*(?:et|,|&|à)\s*\d+)*)', repl, text)

def build_sidebar(num, main):
    # extraire chapitres / sections
    items = re.findall(r'<h([23]) class="(chapter|section)" id="(p%d-[a-z0-9]+)"[^>]*>(.*?)</h[23]>'%num, main, re.S)
    lis=[]
    for lvl,cls,hid,title in items:
        title=re.sub(r'<[^>]+>','',title).strip()
        m=re.match(r'p%d-c(\d+)(?:s(\d+))?'%num, hid)
        if not m: continue
        if m.group(2):
            n="%d.%s.%s"%(num,m.group(1),m.group(2)); lis.append('<li><a class="lvl3" href="#%s">%s · %s</a></li>'%(hid,n,title))
        else:
            n="%d.%s"%(num,m.group(1)); lis.append('<li><a href="#%s">%s · %s</a></li>'%(hid,n,title))
    # nav prev/next
    prev='<li><a href="#part-%d">← Partie %d</a></li>'%(num-1,num-1) if num>1 else ''
    nxt='<li><a href="#part-%d">Partie %d →</a></li>'%(num+1,num+1) if num<12 else ''
    return ('<aside class="sidebar"><h4>Partie %d — Sommaire</h4><nav><ul class="toc">%s</ul>'
            '<h4>Naviguer</h4><ul class="toc"><li><a href="#hub">Sommaire général</a></li>%s%s</ul></nav></aside>'
            %(num,"".join(lis),prev,nxt))

sections=[]
for num, src, is_new, label, desc, tags in PARTS:
    html=read(src)
    main=re.search(r'(<main class="content"[^>]*>.*</main>)', html, re.S).group(1)
    # nav écran -> on retire (sidebar régénérée, breadcrumb régénéré)
    main=re.sub(r'<nav class="breadcrumb">.*?</nav>','',main,flags=re.S)
    main=re.sub(r'<nav class="part-nav">.*?</nav>','',main,flags=re.S)
    main=re.sub(r'<div class="foot">.*?</div>','',main,flags=re.S)
    main=re.sub(r'\s*data-crumb="[^"]*"','',main)             # crumb géré par le texte du lien
    # forcer le bon numéro d'affichage
    main=re.sub(r"--partno:'[^']*'","--partno:'%d'"%num, main)
    # namespacing des ancres
    main=re.sub(r'id="(c\d[^"]*)"', r'id="p%d-\1"'%num, main)
    main=re.sub(r'href="#(c\d[^"]*)"', r'href="#p%d-\1"'%num, main)
    if not is_new:
        main=remap_parties(main)
    main=main.replace('(Partie 0)','(cadre réglementaire)')   # la Partie 0 n'existe plus en v2
    main=fix_internal(main)
    # breadcrumb régénéré juste après l'ouverture du container
    crumb=('<nav class="breadcrumb"><a href="#hub">Accueil</a><span class="sep">/</span>'
           '<a href="#part-%d">Partie %d</a><span class="sep">/</span>'
           '<span class="crumb-current">%s</span></nav>'%(num,num,label.replace('&amp;','&')))
    main=main.replace('<div class="container">','<div class="container">\n'+crumb, 1)
    sidebar=build_sidebar(num, main)
    sections.append('<section class="part-page" id="part-%d" data-part="%d">\n<div class="layout">%s<div class="scrim"></div>%s</div>\n</section>'
                    %(num,num,sidebar,main))

# ---------- HUB ----------
ICON='<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 4h11l3 3v13H5z"/><path d="M9 9h6M9 13h6M9 17h4"/></svg>'
cards=[]
for num, src, is_new, label, desc, tags in PARTS:
    c=COLORS[num][0]
    tagli="".join('<li>%s</li>'%t for t in tags)
    badge='Partie %d'%num + (' · 🆕' if is_new else '')
    cards.append('<a class="part-card" href="#part-%d" style="--pc:%s" data-search="%s %s">%s<div class="pnum">%s</div><h3>%s</h3><p>%s</p><ul>%s</ul></a>'
                 %(num,c,label,desc,ICON,badge,label,desc,tagli))

legend="".join('<span class="lg"><span class="dot" style="background:%s"></span>%d</span>'%(COLORS[n][0],n) for n in range(1,13))

HUB='''<section class="part-page" id="hub" data-part="2">
<main class="content"><div class="container">
  <section class="cover">
    <div class="kicker">Référence professionnelle · LF 2026 / revenus 2025</div>
    <h1>L'encyclopédie illustrée de la gestion de patrimoine</h1>
    <p class="sub">Du fondamental à l'expertise : fiscalité, enveloppes, immobilier, sociétés, comptabilité, transmission et entreprise. Définitions, calculs, cas chiffrés et articles du CGI. Édition « en devenir d'être indépendant ».</p>
    <div class="meta"><span class="chip">⚖️ Articles CGI</span><span class="chip">🧮 Cas chiffrés</span><span class="chip">📊 Tableaux</span><span class="chip">🏢 Sociétés &amp; compta</span><span class="chip">📴 Hors-ligne</span></div>
  </section>
  <div class="section-title">Code couleur des parties</div>
  <div class="legend" data-search="legende couleurs">%s</div>
  <div class="section-title">Sommaire général</div>
  <div class="parts">%s</div>
  <div id="noResults" class="no-results">Aucune partie ne correspond à votre recherche.</div>
  <div class="foot"><p class="disclaimer"><b>⚠️ Avertissement.</b> Ressource pédagogique à jour au 26/06/2026 (LF 2026). Ne constitue pas un conseil personnalisé. Vérifiez les textes en vigueur (BOFiP, Légifrance) avant toute décision.</p></div>
</div></main>
</section>'''%(legend,"".join(cards))

# ---------- chrome + script ----------
TOPBAR='''<div id="progress"></div>
<header class="topbar">
  <button class="icon-btn nav-toggle" aria-label="Sommaire"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <a class="brand" href="#hub" style="color:inherit">
    <svg class="logo" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="7" fill="#2c5b8f"/><path d="M9 22V10l7 5 7-5v12" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span>Encyclopédie du Patrimoine<small id="brandSub">France · CIF/COA expert</small></span>
  </a>
  <div class="spacer"></div>
  <div class="search-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    <input id="searchInput" type="search" placeholder="Rechercher…  ( / )" autocomplete="off" aria-label="Recherche"></div>
  <a class="icon-btn" href="Encyclopedie-Patrimoine.pdf" download title="Télécharger l'encyclopédie en PDF" aria-label="Télécharger en PDF">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M8 11l4 4 4-4M5 21h14"/></svg>
  </a>
  <button class="icon-btn" id="themeToggle" title="Clair / sombre" aria-label="Thème">
    <svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19"/></svg>
    <svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8z"/></svg>
  </button>
</header>'''

TOTOP='<button id="toTop" title="Retour en haut" aria-label="Retour en haut"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>'

SCRIPT=r'''<script>
(function(){"use strict";
 var root=document.documentElement;
 try{var s=localStorage.getItem('encyclo-theme'); if(s)root.setAttribute('data-theme',s); else if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)root.setAttribute('data-theme','dark');}catch(e){}
 function ready(fn){document.readyState!=='loading'?fn():document.addEventListener('DOMContentLoaded',fn);}
 ready(function(){
  var pages=[].slice.call(document.querySelectorAll('.part-page'));
  function active(){return document.querySelector('.part-page.active');}
  function showPart(id,anchor){var ok=false;pages.forEach(function(p){var on=p.id===id;p.classList.toggle('active',on);if(on)ok=true;});
    if(!ok){document.getElementById('hub').classList.add('active');id='hub';}
    var sub=document.getElementById('brandSub'),ap=document.getElementById(id),h1=ap?ap.querySelector('.part-hero h1'):null;
    if(sub)sub.textContent=h1?h1.textContent:'France · CIF/COA expert';
    document.body.classList.remove('nav-open');
    if(anchor){var el=document.getElementById(anchor); if(el){el.scrollIntoView();return;}} window.scrollTo(0,0);}
  function route(){var h=(location.hash||'').slice(1);
    if(!h||h==='hub'){showPart('hub');return;} if(/^part-\d+$/.test(h)){showPart(h);return;}
    var m=h.match(/^p(\d+)-/); if(m){showPart('part-'+m[1],h);return;} showPart('hub');}
  window.addEventListener('hashchange',function(){var i=document.getElementById('searchInput');if(i){i.value='';document.body.classList.remove('searching');}route();spy();});
  route();
  var tb=document.getElementById('themeToggle'); if(tb)tb.addEventListener('click',function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('encyclo-theme',n);}catch(e){}});
  var nt=document.querySelector('.nav-toggle'); if(nt)nt.addEventListener('click',function(){document.body.classList.toggle('nav-open');});
  [].forEach.call(document.querySelectorAll('.scrim'),function(s){s.addEventListener('click',function(){document.body.classList.remove('nav-open');});});
  document.addEventListener('click',function(e){var a=e.target.closest?e.target.closest('.toc a'):null; if(a&&window.innerWidth<=980)document.body.classList.remove('nav-open');});
  var toTop=document.getElementById('toTop'),prog=document.getElementById('progress');
  function onScroll(){var st=window.scrollY||0; if(toTop)toTop.classList.toggle('show',st>500); if(prog){var hh=document.documentElement.scrollHeight-window.innerHeight;prog.style.width=(hh>0?(st/hh*100):0)+'%';} spy();}
  window.addEventListener('scroll',onScroll,{passive:true}); if(toTop)toTop.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  function spy(){var ap=active(); if(!ap)return; var links=[].slice.call(ap.querySelectorAll('.toc a[href^="#"]')),cur=null;
    links.forEach(function(a){var t=document.getElementById(a.getAttribute('href').slice(1)); if(t&&ap.contains(t)&&t.getBoundingClientRect().top<=170)cur=a;});
    links.forEach(function(a){a.classList.remove('active');});
    if(cur){cur.classList.add('active'); var cc=ap.querySelector('.crumb-current'); if(cc)cc.textContent=cur.textContent.trim();}}
  var input=document.getElementById('searchInput'),deb;
  function clearMarks(el){[].forEach.call(el.querySelectorAll('mark.hit'),function(m){var t=document.createTextNode(m.textContent);m.parentNode.replaceChild(t,m);});}
  function mark(el,q){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null),n,ns=[];while(n=w.nextNode())ns.push(n);
    var rx=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
    ns.forEach(function(node){if(!node.nodeValue.trim())return; if(node.parentNode&&/^(MARK|SCRIPT|STYLE)$/.test(node.parentNode.nodeName))return;
      if(!rx.test(node.nodeValue))return; rx.lastIndex=0; var sp=document.createElement('span'); sp.innerHTML=node.nodeValue.replace(rx,'<mark class="hit">$1</mark>'); node.parentNode.replaceChild(sp,node);});}
  function runSearch(){var ap=active(); if(!ap)return; var units=[].slice.call(ap.querySelectorAll('[data-search]')),q=input.value.trim().toLowerCase(),nr=ap.querySelector('#noResults');
    units.forEach(clearMarks);
    if(!q){document.body.classList.remove('searching');units.forEach(function(u){u.classList.remove('search-hidden');});if(nr)nr.style.display='none';return;}
    document.body.classList.add('searching'); var any=false;
    units.forEach(function(u){var hit=(u.getAttribute('data-search')+' '+u.textContent).toLowerCase().indexOf(q)!==-1;u.classList.toggle('search-hidden',!hit);if(hit){any=true;mark(u,q);}});
    if(nr)nr.style.display=any?'none':'block';}
  if(input){input.addEventListener('input',function(){clearTimeout(deb);deb=setTimeout(runSearch,130);});
    document.addEventListener('keydown',function(e){if(e.key==='/'&&document.activeElement!==input){e.preventDefault();input.focus();} if(e.key==='Escape'&&document.activeElement===input){input.value='';runSearch();input.blur();}});}
  onScroll();
 });
})();
</script>'''

DOC=u'''<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Encyclopédie de la Gestion de Patrimoine — France (CIF/COA)</title>
<meta name="description" content="Encyclopédie illustrée de la gestion de patrimoine en France : fiscalité, enveloppes, immobilier, sociétés, comptabilité, transmission. Fichier unique autonome.">
<style>
%s
</style>
</head>
<body data-part="2">
%s
%s

%s
%s
%s
</body>
</html>''' % (css, TOPBAR, HUB, "\n\n".join(sections), TOTOP, SCRIPT)

for name in ("index.html","Encyclopedie-Patrimoine.html"):
    with io.open(os.path.join(BASE,name),"w",encoding="utf-8") as f: f.write(DOC)
print("OK -> index.html + Encyclopedie-Patrimoine.html"); print("Taille: %.0f Ko"%(len(DOC.encode('utf-8'))/1024)); print("Parties:",len(sections))
