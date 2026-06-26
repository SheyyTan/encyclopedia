# -*- coding: utf-8 -*-
"""Assemble l'encyclopédie multi-fichiers en UN seul HTML autonome."""
import re, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
def read(p):
    with io.open(os.path.join(BASE,p), encoding="utf-8") as f: return f.read()

PARTS = [
    ("0","partie-0-cadre.html"),
    ("1","partie-1-bancaire.html"),
    ("2","partie-2-fiscalite.html"),
    ("3","partie-3-enveloppes.html"),
    ("4","partie-4-allocation.html"),
    ("5","partie-5-immobilier.html"),
    ("6","partie-6-matrimonial.html"),
    ("7","partie-7-transmission.html"),
    ("8","partie-8-entreprise.html"),
    ("9","partie-9-synthese.html"),
]

# ---- CSS partagé (dark part-colors -> descendant combinator) ----
css = read("assets/encyclo.css")
css = css.replace('[data-theme="dark"][data-part', '[data-theme="dark"] [data-part')

def styles_of(path):
    return "\n".join(re.findall(r'<style>(.*?)</style>', read(path), re.S))
css += "\n/* --- styles hub (index) --- */\n" + styles_of("index.html")
css += "\n/* --- styles annexes (P9) --- */\n" + styles_of("partie-9-synthese.html")
# styles single-file (router)
css += """
/* --- monofichier : router --- */
.part-page{ display:none; }
.part-page.active{ display:block; }
"""

def fix_links(s):
    s = s.replace('href="index.html"', 'href="#hub"')
    s = re.sub(r'href="partie-(\d+)-[^"#]*\.html(#[^"]*)?"', r'href="#part-\1"', s)
    return s

# ---- HUB (depuis index.html) ----
idx = read("index.html")
hub_main = re.search(r'(<main class="content">.*</main>)', idx, re.S).group(1)
hub_main = fix_links(hub_main)
hub = '<section class="part-page" id="hub" data-part="0">\n' + hub_main + '\n</section>'

# ---- PARTIES ----
sections = [hub]
for num, path in PARTS:
    html = read(path)
    layout = re.search(r'<div class="layout">(.*)</div>\s*<button id="toTop"', html, re.S).group(1)
    # crumb-current -> classe (évite ids dupliqués)
    layout = layout.replace('id="crumb-current"', 'class="crumb-current"')
    # namespacing des ancres c... -> pN-c...
    layout = re.sub(r'id="(c\d[^"]*)"', r'id="p%s-\1"' % num, layout)
    layout = re.sub(r'href="#(c\d[^"]*)"', r'href="#p%s-\1"' % num, layout)
    # liens inter-fichiers -> internes
    layout = fix_links(layout)
    sec = ('<section class="part-page" id="part-%s" data-part="%s">\n'
           '<div class="layout">%s</div>\n</section>') % (num, num, layout)
    sections.append(sec)

body_sections = "\n\n".join(sections)

# ---- chrome partagé (topbar / progress / toTop / script) ----
TOPBAR = '''<div id="progress"></div>
<header class="topbar">
  <button class="icon-btn nav-toggle" aria-label="Sommaire"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <a class="brand" href="#hub" style="color:inherit">
    <svg class="logo" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="7" fill="#2c5b8f"/><path d="M9 22V10l7 5 7-5v12" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span>Encyclopédie du Patrimoine<small id="brandSub">France · CIF/COA expert</small></span>
  </a>
  <div class="spacer"></div>
  <div class="search-box">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    <input id="searchInput" type="search" placeholder="Rechercher dans la partie…  ( / )" autocomplete="off" aria-label="Recherche">
  </div>
  <button class="icon-btn" id="themeToggle" title="Basculer clair / sombre" aria-label="Thème">
    <svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19"/></svg>
    <svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8z"/></svg>
  </button>
</header>'''

TOTOP = '''<button id="toTop" title="Retour en haut" aria-label="Retour en haut"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>'''

SCRIPT = r'''<script>
(function(){"use strict";
  var root=document.documentElement;
  try{var s=localStorage.getItem('encyclo-theme'); if(s)root.setAttribute('data-theme',s);
      else if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)root.setAttribute('data-theme','dark');}catch(e){}
  function ready(fn){document.readyState!=='loading'?fn():document.addEventListener('DOMContentLoaded',fn);}
  ready(function(){
    var pages=[].slice.call(document.querySelectorAll('.part-page'));
    function active(){return document.querySelector('.part-page.active');}
    function showPart(id,anchor){
      var ok=false; pages.forEach(function(p){var on=p.id===id;p.classList.toggle('active',on);if(on)ok=true;});
      if(!ok){document.getElementById('hub').classList.add('active');id='hub';}
      var sub=document.getElementById('brandSub'); var ap=document.getElementById(id);
      var h1=ap?ap.querySelector('.part-hero h1'):null;
      if(sub)sub.textContent=h1?h1.textContent:'France · CIF/COA expert';
      document.body.classList.remove('nav-open');
      if(anchor){var el=document.getElementById(anchor); if(el){el.scrollIntoView();return;}}
      window.scrollTo(0,0);
    }
    function route(){
      var h=(location.hash||'').slice(1);
      if(!h||h==='hub'){showPart('hub');return;}
      if(/^part-\d+$/.test(h)){showPart(h);return;}
      var m=h.match(/^p(\d+)-/); if(m){showPart('part-'+m[1],h);return;}
      showPart('hub');
    }
    window.addEventListener('hashchange',function(){var inp=document.getElementById('searchInput');if(inp){inp.value='';document.body.classList.remove('searching');}route();spy();});
    route();

    var tb=document.getElementById('themeToggle');
    if(tb)tb.addEventListener('click',function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('encyclo-theme',n);}catch(e){}});
    var nt=document.querySelector('.nav-toggle');
    if(nt)nt.addEventListener('click',function(){document.body.classList.toggle('nav-open');});
    [].forEach.call(document.querySelectorAll('.scrim'),function(s){s.addEventListener('click',function(){document.body.classList.remove('nav-open');});});
    document.addEventListener('click',function(e){var a=e.target.closest?e.target.closest('.toc a'):null; if(a&&window.innerWidth<=980)document.body.classList.remove('nav-open');});

    var toTop=document.getElementById('toTop'),prog=document.getElementById('progress');
    function onScroll(){var st=window.scrollY||0; if(toTop)toTop.classList.toggle('show',st>500);
      if(prog){var hh=document.documentElement.scrollHeight-window.innerHeight; prog.style.width=(hh>0?(st/hh*100):0)+'%';} spy();}
    window.addEventListener('scroll',onScroll,{passive:true});
    if(toTop)toTop.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});

    function spy(){var ap=active(); if(!ap)return;
      var links=[].slice.call(ap.querySelectorAll('.toc a[href^="#"]')),cur=null;
      links.forEach(function(a){var t=document.getElementById(a.getAttribute('href').slice(1)); if(t&&ap.contains(t)&&t.getBoundingClientRect().top<=170)cur=a;});
      links.forEach(function(a){a.classList.remove('active');});
      if(cur){cur.classList.add('active'); var cc=ap.querySelector('.crumb-current'),tgt=document.getElementById(cur.getAttribute('href').slice(1));
        if(cc&&tgt)cc.textContent=(tgt.getAttribute('data-crumb')||cur.textContent).trim();}
    }

    var input=document.getElementById('searchInput'),deb;
    function clearMarks(el){[].forEach.call(el.querySelectorAll('mark.hit'),function(m){var t=document.createTextNode(m.textContent);m.parentNode.replaceChild(t,m);});}
    function mark(el,q){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null),n,ns=[];while(n=w.nextNode())ns.push(n);
      var rx=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
      ns.forEach(function(node){if(!node.nodeValue.trim())return; if(node.parentNode&&/^(MARK|SCRIPT|STYLE)$/.test(node.parentNode.nodeName))return;
        if(!rx.test(node.nodeValue))return; rx.lastIndex=0; var sp=document.createElement('span');
        sp.innerHTML=node.nodeValue.replace(rx,'<mark class="hit">$1</mark>'); node.parentNode.replaceChild(sp,node);});}
    function runSearch(){var ap=active(); if(!ap)return; var units=[].slice.call(ap.querySelectorAll('[data-search]')),q=input.value.trim().toLowerCase();
      units.forEach(clearMarks);
      if(!q){document.body.classList.remove('searching');units.forEach(function(u){u.classList.remove('search-hidden');});return;}
      document.body.classList.add('searching');
      units.forEach(function(u){var hit=(u.getAttribute('data-search')+' '+u.textContent).toLowerCase().indexOf(q)!==-1; u.classList.toggle('search-hidden',!hit); if(hit)mark(u,q);});}
    if(input){input.addEventListener('input',function(){clearTimeout(deb);deb=setTimeout(runSearch,130);});
      document.addEventListener('keydown',function(e){if(e.key==='/'&&document.activeElement!==input){e.preventDefault();input.focus();}
        if(e.key==='Escape'&&document.activeElement===input){input.value='';runSearch();input.blur();}});}
    onScroll();
  });
})();
</script>'''

DOC = u'''<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Encyclopédie de la Gestion de Patrimoine — France (CIF/COA)</title>
<meta name="description" content="Encyclopédie illustrée et exhaustive de la gestion de patrimoine en France : fiscalité, enveloppes, immobilier, transmission, ingénierie. Fichier unique autonome.">
<style>
%s
</style>
</head>
<body data-part="0">
%s
%s
%s
%s
</body>
</html>''' % (css, TOPBAR, body_sections, TOTOP, SCRIPT)

out = os.path.join(BASE, "Encyclopedie-Patrimoine.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(DOC)
print("OK ->", out)
print("Taille: %.0f Ko" % (len(DOC.encode("utf-8"))/1024))
print("Sections:", len(sections))
