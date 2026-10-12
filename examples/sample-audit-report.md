# Exemple de Rapport d'Audit Complet : SaaS / Application Web

**Cible analysée :** `https://mon-saas-exemple.com`  
**Date de l'audit :** 2026-10-12 14:45:00  
**Audit produit par :** Antigravity SEO (Gemini 2.5 / DeepMind)  
**Score Global :** **68 / 100** — 🟠 Moyen

---

## 1. Score Pondéré par Pilier

| Pilier | Score | Max | Statut | Synthèse |
|:---|:---:|:---:|:---:|:---|
| **1. SEO Technique & Performance** | **19** | 25 | ⚠️ À corriger | TTFB correct (280ms), mais CLS à 0.14 et chaîne de redirection sur la canonique. |
| **2. Structure On-Page & Sémantique** | **14** | 20 | ⚠️ À corriger | Titre et méta présents mais multiples `<h1>` détectés sur la page d'accueil. |
| **3. Microdonnées Schema.org (2026)** | **10** | 20 | 🔴 Critique | Utilisation de `FAQPage` déprécié par Google ; manque `SoftwareApplication` et `@graph`. |
| **4. E-E-A-T & Qualité Éditoriale** | **15** | 20 | 🟡 Bon | Présence de cas clients et de tarification claire ; biographie d'auteur sommaire. |
| **5. GEO & Agent Readiness** | **10** | 15 | ⚠️ À corriger | Absence de `llms.txt` et aucun passage synthétique (40-80 mots) pour les AI Overviews. |

---

## 2. Analyse Technique & Core Web Vitals (2026)

### Core Web Vitals
- **INP (Interaction to Next Paint)** : **140 ms** 🟢 *Bon* (Seuil < 200 ms respecté). Les composants interactifs réagissent rapidement.
- **LCP (Largest Contentful Paint)** : **2.2 s** 🟢 *Bon* (Seuil < 2.5 s respecté). L'image hero est optimisée en WebP.
- **CLS (Cumulative Layout Shift)** : **0.14** 🟠 *À améliorer* (Seuil < 0.1 dépassé). Les polices personnalisées causent un léger décalage visuel (FOUT) lors du chargement initial.

### Directives d'Indexation
- **Robots** : `index, follow, max-image-preview:large` présent.
- **Balise canonique** : Déclarée en `http://mon-saas-exemple.com/` (HTTP non sécurisé) au lieu de `https://mon-saas-exemple.com`. Génère une boucle inutile de redirection 301.

---

## 3. Données Structurées Schema.org (Normes 2026)

### ⚠️ Problèmes Détectés
1. **Schéma Déprécié `FAQPage`** : La page intègre un bloc `FAQPage`. Google a retiré les résultats enrichis FAQ depuis le **7 mai 2026**. Ce balisage n'apporte plus aucun affichage étendu dans les SERP.
2. **Entité SaaS Manquante** : Absence du schéma `SoftwareApplication` / `WebApplication` indispensable pour afficher les fonctionnalités logicielles, les prix d'abonnement et la note moyenne dans les résultats de recherche.
3. **Absence de `@graph` unifié** : Les balises `Organization` et `WebSite` sont dans des scripts séparés sans référence `@id` croisée.

---

## 4. GEO & Citabilité dans Google AI Overviews / Gemini

### Diagnostic Citabilité
- Le contenu explique bien le logiciel, mais sous forme de longs blocs promotionnels continus.
- **Manque de passages autonomes (40-80 mots)** : Aucun bloc synthétique ne répond directement aux requêtes fréquentes telles que *"Comment automatiser ses rapports avec un logiciel SaaS ?"*.
- **Agent Readiness** : Le site ne propose pas de route `https://mon-saas-exemple.com/llms.txt` pour permettre aux assistants IA d'extraire rapidement les fonctionnalités et tarifs officiels.

---

## 5. Plan d'Action Falsifiable & Priorisé

### 🚨 Priorité 1 — Critique (Sous 48h)
- **Observation** : La balise canonique pointe vers une URL HTTP non sécurisée.
- **Action** : Remplacer l'URL canonique par la version HTTPS stricte `https://mon-saas-exemple.com`.
- **Indicateur Avancé** : L'outil d'inspection de Google Search Console valide l'URL canonique déclarée comme l'URL canonique sélectionnée par Google sans redirection.
- **Test d'Échec** : Si GSC continue d'indiquer "URL déclarée par l'internaute différente de l'URL choisie par Google" après 7 jours.

### ⚠️ Priorité 2 — Élevé (Sous 1 semaine)
- **Observation** : Présence du schéma obsolète `FAQPage` et absence de `SoftwareApplication`.
- **Action** : Supprimer `FAQPage` et injecter un graphe unifié JSON-LD contenant `Organization`, `WebSite` et `SoftwareApplication` avec les propriétés `applicationCategory`, `operatingSystem` et `offers`.
- **Indicateur Avancé** : Le Validateur de Résultats Enrichis de Google ne remonte aucun avertissement et identifie l'entité logicielle.
- **Test d'Échec** : Si le validateur signale des erreurs de syntaxe JSON ou des propriétés obligatoires manquantes sur `offers`.

### ℹ️ Priorité 3 — Moyen (Sous 3 semaines)
- **Observation** : CLS supérieur à 0.1 causé par le swap de police web.
- **Action** : Ajouter `font-display: optional` ou précharger la police critique avec `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- **Indicateur Avancé** : CLS mesuré sous 0.05 dans PageSpeed Insights (Lab data).
- **Test d'Échec** : Si le rapport CrUX après 28 jours conserve un score CLS > 0.1 sur le 75e percentile.
