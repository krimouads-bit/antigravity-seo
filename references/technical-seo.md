# Référence : SEO Technique & Core Web Vitals (2026)

Guide de référence pour l'audit SEO technique, calibré sur les normes actuelles de Google Search et Chrome UX.

---

## 1. Core Web Vitals (Normes 2026)

Google a fait évoluer ses indicateurs de performance clés. FID (First Input Delay) est définitivement obsolète et a été retiré des rapports Chrome User Experience Report (CrUX) et PageSpeed Insights.

| Métrique | Nom Complet | Seuil Bon (Vert) | Seuil À Améliorer (Orange) | Seuil Mauvais (Rouge) | Description & Focus |
|:---|:---|:---:|:---:|:---:|:---|
| **INP** | Interaction to Next Paint | **< 200 ms** | 200 ms - 500 ms | > 500 ms | Remplace FID depuis mars 2024. Mesure la latence globale de toutes les interactions de la page (clics, touches clavier, taps). Principal coupable : longs blocs de JavaScript sur le thread principal. |
| **LCP** | Largest Contentful Paint | **< 2.5 s** | 2.5 s - 4.0 s | > 4.0 s | Temps d'affichage du plus grand bloc de contenu visible (image hero, vidéo poster, grand bloc de texte). Subdivisé en TTFB, délai de chargement, durée de chargement et délai de rendu. |
| **CLS** | Cumulative Layout Shift | **< 0.1** | 0.1 - 0.25 | > 0.25 | Stabilité visuelle. Mesure les décalages inattendus d'éléments lors du chargement. Coupables : images sans dimensions fixes (`width`/`height`), polices web non préchargées (FOUT/FOIT), bannières injectées dynamiquement. |

### Vérifications Pratiques CWV
1. **Images & Médias** :
   - Dimensions explicites (`width="800" height="600"`) ou `aspect-ratio` CSS sur toutes les balises `<img>` et `<video>`.
   - `loading="lazy"` sur les images hors-écran, **MAIS JAMAIS** sur l'image LCP (au-dessus de la ligne de flottaison).
   - Utiliser des formats modernes : WebP ou AVIF avec balise `<picture>`.
   - `fetchpriority="high"` sur l'image hero candidate LCP.
2. **JavaScript & Réactivité (INP)** :
   - Fractionner les longues tâches (`Long Tasks` > 50ms) avec `scheduler.yield()` ou `setTimeout()`.
   - Éviter les écouteurs d'événements lourds et synchrones sur les boutons et inputs.
   - Différer les scripts non critiques (`defer` ou `async`).

---

## 2. Indexabilité & Directives d'Exploration

### Balises Robots
- **Meta Robots dans le HTML** :
  ```html
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  ```
  - `noindex` : exclut la page de l'index Google. Vérifier l'absence accidentelle en production.
  - `nofollow` : empêche la transmission de PageRank via les liens.
  - `noarchive` : n'a plus d'impact majeur depuis le retrait du cache Google (2024).
  - `max-image-preview:large` : **Obligatoire** pour être éligible aux grandes images dans Google Discover et AI Overviews.

### Fichier robots.txt
- Accessible à la racine : `https://domaine.com/robots.txt` avec un code HTTP 200.
- Ne pas bloquer l'accès aux assets CSS, JS et images nécessaires au rendu de Googlebot.
- Déclaration de la sitemap :
  ```text
  User-agent: *
  Allow: /
  Disallow: /admin/
  Disallow: /api/private/

  Sitemap: https://domaine.com/sitemap.xml
  ```

### Balise Canonique (`rel="canonical"`)
- Chaque page indexable doit déclarer une balise canonique auto-référente absolue :
  ```html
  <link rel="canonical" href="https://domaine.com/page-cible">
  ```
- Vérifier :
  - Pas d'URL relative (`href="/page"` est déconseillé ; toujours utiliser l'URL absolue HTTPS).
  - Pas de chaîne de redirection (l'URL canonique doit répondre en 200 direct).
  - Cohérence avec les paramètres d'URL (tracking UTM, tris, filtres doivent pointer vers la version propre).

---

## 3. Structure Sémantique & On-Page

### Hiérarchie des Titres
- **Un seul `<h1>`** par page, résumant le sujet principal avec les termes clés naturels.
- Structure logique : `<h1>` > `<h2>` > `<h3>` sans sauts de niveau arbitraires.
- Intégrer des formulations interrogatives dans les `<h2>`/`<h3>` pour capter les requêtes d'intention et les AI Overviews.

### Meta Tags Essentiels
- **Balise `<title>`** :
  - Longueur recommandée : 50 à 60 caractères (ou ~580 pixels).
  - Format idéal : `Mot-clé Principal - Bénéfice / Sous-thème | Nom de Marque`.
  - Unique par page.
- **Meta Description** :
  - Longueur recommandée : 120 à 155 caractères.
  - Doit comporter un appel à l'action implicite et répondre précisément à l'intention.
- **Viewport** :
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ```

### Protocole Open Graph & Social Cards
```html
<meta property="og:type" content="article">
<meta property="og:title" content="Titre de la Page">
<meta property="og:description" content="Description engageante">
<meta property="og:image" content="https://domaine.com/assets/og-image.jpg">
<meta property="og:url" content="https://domaine.com/page-cible">
<meta name="twitter:card" content="summary_large_image">
```
