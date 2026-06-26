# Encyclopédie de la Gestion de Patrimoine

Encyclopédie illustrée et exhaustive de la gestion de patrimoine en France
(niveau conseiller expert CIF/COA) : fiscalité, enveloppes financières,
immobilier, sociétés, comptabilité, transmission et ingénierie patrimoniale.

## 🌐 Site en ligne

La page d'accueil (`index.html`) **est** l'encyclopédie : un fichier unique,
autonome, qui fonctionne sur téléphone, tablette et ordinateur.

Partagez simplement le lien GitHub Pages — vos lecteurs ont **toujours la
dernière version**, sans rien télécharger.

- **Version interactive** : `index.html`
- **Version PDF** (téléchargeable / imprimable) : `Encyclopedie-Patrimoine.pdf`

## ✍️ Mettre à jour le contenu

1. Modifier le contenu dans les fichiers sources `partie-*.html`
   (ou demander la modification).
2. Régénérer les versions :
   ```bash
   python build-v2.py        # régénère index.html (+ Encyclopedie-Patrimoine.html)
   python build-pdf-v2.py    # régénère le HTML d'impression -> puis conversion PDF
   ```
3. Publier :
   ```bash
   git add -A
   git commit -m "Mise à jour du contenu"
   git push
   ```
4. Le site se met à jour automatiquement en ~1 minute.

## 🗂️ Structure

| Fichier | Rôle |
|---|---|
| `index.html` | Le site (encyclopédie monofichier, 12 parties) |
| `Encyclopedie-Patrimoine.pdf` | Version PDF |
| `partie-*.html` | Sources de chaque partie (servent au build) |
| `assets/encyclo.css`, `assets/encyclo.js` | Design system partagé |
| `build-v2.py` | Assemble le site `index.html` |
| `build-pdf-v2.py` | Assemble la version imprimable (puis PDF) |

## ⚠️ Avertissement

Ressource pédagogique et technique. Reflète l'état du droit à sa date d'édition
(LF 2026, revenus 2025). Ne constitue ni un conseil personnalisé ni une
consultation opposable. Vérifier les textes en vigueur (BOFiP, Légifrance)
avant toute décision.
