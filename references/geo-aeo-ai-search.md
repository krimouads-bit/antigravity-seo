# Référence : GEO, AEO & Optimisation pour les Moteurs IA (2026)

Guide méthodologique pour le **Generative Engine Optimization (GEO)** et le **Answer Engine Optimization (AEO)**, ciblant spécifiquement **Google Gemini / AI Overviews**, **Perplexity** et les moteurs de recherche alimentés par LLM.

---

## 1. La Position Officielle de Google sur l'IA Search

Selon le *Google AI Optimization Guide* :
> *"Optimiser pour la recherche générative par IA, c'est optimiser pour l'expérience de recherche globale : c'est donc toujours du SEO."*

Les Google AI Overviews et le mode IA s'appuient sur les **mêmes systèmes fondamentaux d'indexation et de classement** que le Search traditionnel. Une page doit être :
1. Indexable et indexée par Googlebot.
2. Éligible aux extraits enrichis (`max-snippet:-1` ou longueur suffisante).
3. Techniquement accessible et rapide.

---

## 2. Piliers d'Optimisation GEO (Citabilité dans l'IA)

Pour qu'un modèle de langage (comme Gemini ou ChatGPT Search) sélectionne et cite votre contenu dans sa réponse générative :

### 2.1 Citabilité des Passages (*Passage Citability*)
- **Principe** : Les LLM découpent et analysent le texte sous forme de morceaux sémantiques (*chunks*). Si un passage répond directement, précisément et sans fioritures à une question, sa probabilité d'être extrait comme source augmente drastiquement.
- **Règle des 40 à 80 mots** :
  - Immédiatement sous un intertitre interrogatif (`<h2>Qu'est-ce que X ?</h2>` ou `<h3>Comment fonctionne Y ?</h3>`), placer un paragraphe de synthèse autonome de 40 à 80 mots.
  - Définir le concept au présent, sans verbiage d'introduction ("Dans cet article nous allons voir...").
  - Fournir la réponse immédiate, puis approfondir dans les paragraphes suivants.

### 2.2 Densité d'Attribution & Données Primaires
- Les moteurs IA recherchent des faits vérifiables et des sources primaires pour appuyer leurs affirmations et éviter les hallucinations.
- **Bonnes pratiques** :
  - Citer des pourcentages, des dates, des chiffres précis avec leur source méthodologique.
  - Formater les données comparatives sous forme de **tableaux HTML sémantiques** (`<table>`, `<th>`, `<td>`) plutôt qu'en texte fluide : les LLM lisent et extraient les tableaux avec une précision quasi-parfaite.
  - Utiliser des listes ordonnées (`<ol>`) pour les procédures étape par étape.

### 2.3 Alignement avec le Knowledge Graph & Entités
- Ancrer votre marque et vos concepts clés dans l'écosystème d'entités reconnues :
  - Liens réciproques vers vos profils officiels (Wikidata, LinkedIn, GitHub, YouTube).
  - Cohérence stricte du nom de marque, de l'offre et du secteur sur le web.
  - Utilisation du balisage Schema.org `sameAs` et `knowsAbout`.

---

## 3. Démystification des Mythes Répandus

| Mythe | Réalité Factuelle (Google & Tests LLM) |
|:---|:---|
| **"Avoir un fichier `llms.txt` garantit d'apparaître dans Google AI Overviews"** | ❌ **FAUX**. Google Search n'utilise pas le fichier `llms.txt` pour classer ou citer des pages dans Google Search / AI Overviews. Le fichier `llms.txt` est un standard utile pour guider les agents autonomes ou les crawlers spécialisés, mais l'indexation Search passe exclusivement par l'analyse HTML standard. |
| **"Il faut réécrire tout son contenu pour les prompts des IA"** | ❌ **FAUX**. Les modèles de langage modernes comprennent parfaitement la sémantique, les synonymes et le langage naturel. Bourrer un texte de requêtes formatées de type "Prompt" nuit à l'expérience utilisateur et dégrade les signaux E-E-A-T. |
| **"Le SEO classique est mort avec l'arrivée de l'IA"** | ❌ **FAUX**. L'IA synthétise les résultats des sites les plus performants, fiables et rapides. Sans fondations techniques (HTML propre, vitesse, balisage), aucune page n'atteint le seuil d'éligibilité pour être citée. |
