---
name: antigravity-seo
description: >-
  Use this skill when the user asks for an SEO audit, technical SEO analysis,
  content quality evaluation (E-E-A-T), Schema.org / JSON-LD validation,
  Generative Engine Optimization (GEO/AEO for Gemini & AI Overviews), or agentic
  readiness audit (Lighthouse Agentic Browsing, WebMCP, llms.txt). Optimized for
  Antigravity and Google Gemini.
---

# Antigravity SEO — Expert SEO & GEO Skill for Antigravity & Gemini

Skill d'audit et d'optimisation SEO de nouvelle génération, conçu exclusivement
pour **Antigravity** et propulsé par **Google Gemini**. Il couvre le SEO technique,
l'E-E-A-T, les microdonnées Schema.org (2026), le GEO (Generative Engine Optimization)
pour Google AI Overviews / Gemini, et la préparation aux agents autonomes
(Lighthouse Agentic Browsing, WebMCP).

---

## 🎯 Quand activer cette Skill

Activez cette skill dès que l'utilisateur demande :
- Un audit SEO complet d'un site web ou d'une page spécifique.
- Une analyse technique SEO (Core Web Vitals INP/LCP/CLS, indexabilité, robots, canoniques).
- Une évaluation E-E-A-T et de qualité éditoriale (Search Quality Rater Guidelines).
- La détection, validation ou génération de balisage Schema.org / JSON-LD.
- Une optimisation GEO/AEO (citabilité dans Google AI Overviews, Gemini, Perplexity).
- Une vérification de conformité "Agent Readiness" (Agentic Browsing, `llms.txt`, WebMCP).
- L'audit SEO d'un projet local (code source HTML/Blade/PHP/JS avant mise en production).

---

## 🧭 Workflow d'Audit en 5 Phases

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  1. Collecte &  │───>│  2. Technique & │───>│ 3. E-E-A-T &    │───>│ 4. GEO & Agent  │───>│ 5. Synthèse &   │
│   Inspection    │    │    Balisage     │    │   Contenu       │    │    Readiness    │    │ Plan d'Action   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Phase 1 — Collecte & Inspection
1. **Cible en ligne (URL)** :
   - Exécuter le script d'analyse rapide :
     ```powershell
     python scripts/seo_analyzer.py --url "<URL>" --format json
     ```
   - Si la page est une SPA (React, Vue, client-side heavy) ou requiert l'inspection visuelle du rendu :
     utiliser `browser_subagent` ou `read_url_content`.
2. **Cible locale (code source du projet)** :
   - Analyser les vues (Blade, HTML, templates), les routes, `robots.txt` et `sitemap.xml`.
   - Exécuter le script en mode local :
     ```powershell
     python scripts/seo_analyzer.py --file "<chemin_vers_fichier>" --format json
     ```

### Phase 2 — Audit Technique & Schema.org
Consulter la référence : [technical-seo.md](./references/technical-seo.md) et [schema-jsonld.md](./references/schema-jsonld.md).
1. **Core Web Vitals 2026** :
   - **INP** (Interaction to Next Paint) : cible < 200ms (remplace définitivement FID).
   - **LCP** (Largest Contentful Paint) : cible < 2.5s.
   - **CLS** (Cumulative Layout Shift) : cible < 0.1.
2. **Indexabilité & Infrastructure** :
   - Code réponse HTTP (200, 301, 404, 500).
   - Directives Robots (`meta name="robots"` et `robots.txt`).
   - Balise canonique (`canonical`) : auto-référente, absolue, sans chaîne de redirection.
   - Hiérarchie des titres : un seul `<h1>`, imbrication logique `<h2>`-`<h6>` sans saut.
   - Open Graph & Twitter Cards.
3. **Validation Schema.org JSON-LD (Normes Google 2026)** :
   - Vérifier la présence de blocs `<script type="application/ld+json">`.
   - Types actifs recommandés : `Organization`, `WebSite`, `Article`, `Product`, `LocalBusiness`, `SoftwareApplication`.
   - ⚠️ **Types dépréciés par Google à proscrire** :
     - `FAQPage` : résultats enrichis retirés par Google le 7 mai 2026.
     - `HowTo` : retiré en septembre 2023.
     - `SpecialAnnouncement`, `EstimatedSalary`, `LearningVideo` : retirés en 2025.

### Phase 3 — Audit Éditorial & E-E-A-T
Consulter la référence : [eeat-framework.md](./references/eeat-framework.md).
1. **Critère "Who / How / Why" (Helpful Content Guide)** :
   - **Who** : auteur identifié avec biographie, liens sociaux/professionnels, expertise visible.
   - **How** : méthodologie de recherche, données sources, transparence sur les tests ou outils.
   - **Why** : le contenu sert-il d'abord l'internaute ou est-il calibré uniquement pour les moteurs ?
2. **4 Piliers E-E-A-T (Search Quality Rater Guidelines)** :
   - **Experience** (Expérience vécue) : photos originales, retours d'usage concrets, études de cas réelles.
   - **Expertise** (Compétence technique) : profondeur conceptuelle, vocabulaire métier exact.
   - **Authoritativeness** (Autorité) : citations externes de référence, mentions dans l'écosystème.
   - **Trustworthiness** (Confiance - Pilier le plus pondéré) : mentions légales, politique de confidentialité, HTTPS, dates de publication et de mise à jour visibles.

### Phase 4 — GEO & Agent Readiness (IA & Gemini)
Consulter la référence : [geo-aeo-ai-search.md](./references/geo-aeo-ai-search.md) et [agentic-browsing.md](./references/agentic-browsing.md).
1. **GEO / AEO (Google AI Overviews & Gemini)** :
   - **Citabilité des passages** : blocs de réponses concises et autonomes (40-80 mots) répondant directement aux requêtes intentionnelles sous des `<h2>`/`<h3>` interrogatifs.
   - **Densité d'attribution** : faits sourcés avec ancrage clair facilitant l'extraction par les LLMs.
   - **Démystification** : `llms.txt` n'est pas un levier d'indexation pour Google Search classique, mais un standard de clarté pour les agents d'assistance.
2. **Agent Readiness** :
   - Structure sémantique respectant les critères *Lighthouse Agentic Browsing*.
   - Rendu textuel propre sans dépendance stricte aux interactions JS bloquantes.
   - Disponibilité d'une route `llms.txt` ou d'une version Markdown structurée pour les agents IA.

### Phase 5 — Restitution & Plan d'Action Falsifiable
Consulter la référence : [audit-methodology.md](./references/audit-methodology.md).
Produire systématiquement un rapport structuré respectant le format standard :
1. **Score Global 0-100** avec grille pondérée.
2. **Matrice des Recommandations Priorisées** (Critique, Élevé, Moyen, Faible).
3. **Principe de Falsifiabilité** pour chaque recommandation :
   - Observation concrète (preuve directe).
   - Action corrective précise.
   - Indicateur avancé (*leading indicator*).
   - Test d'échec explicite (*"Comment sait-on que la mesure a échoué ?"*).

---

## 🛠️ Outils & Scripts Inclus

Le skill fournit un analyseur autonome multiplateforme dans `scripts/` :
- `scripts/seo_analyzer.py` : Analyseur zéro-dépendance (Python standard) capable d'analyser une URL ou un fichier HTML local, d'extraire toutes les balises SEO, de valider le JSON-LD, de vérifier les Core Web Vitals lab et de générer un rapport JSON ou Markdown.

Exemple d'exécution via Antigravity :
```powershell
python scripts/seo_analyzer.py --url "https://example.com"
```

---

## 📋 Références Détaillées

- [SEO Technique & Core Web Vitals](./references/technical-seo.md)
- [Guide E-E-A-T & Évaluation de Contenu](./references/eeat-framework.md)
- [Balisage Schema.org & JSON-LD 2026](./references/schema-jsonld.md)
- [GEO, AEO & Optimisation pour l'IA (Gemini/AI Overviews)](./references/geo-aeo-ai-search.md)
- [Agentic Browsing & Préparation aux Agents IA](./references/agentic-browsing.md)
- [Méthodologie d'Audit & Scoring Falsifiable](./references/audit-methodology.md)
- [Exemple de Rapport d'Audit](./examples/sample-audit-report.md)
