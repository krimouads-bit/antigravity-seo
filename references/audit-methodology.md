# Référence : Méthodologie d'Audit & Scoring Falsifiable

Méthodologie standardisée de notation et de formulation des recommandations pour l'ensemble des audits produits par la skill **Antigravity SEO**.

---

## 1. Grille de Notation Pondérée (Score Global sur 100)

Chaque audit calcule un score global sur 100 points, réparti sur les 5 piliers clés du SEO moderne :

| Pilier | Pondération | Critères Évalués |
|:---|:---:|:---|
| **1. SEO Technique & Performance** | **25 %** | Code statut HTTP, validité canonique, robots.txt, Core Web Vitals (INP < 200ms, LCP < 2.5s, CLS < 0.1), HTTPS, absence d'erreurs console bloquantes. |
| **2. Structure On-Page & Sémantique** | **20 %** | Balises `<title>`, meta description, unicité du `<h1>`, hiérarchie des `<h2>`-`<h6>`, attributs `alt` des images, maillage interne. |
| **3. Microdonnées Schema.org** | **20 %** | Présence de JSON-LD valide, graphe interconnecté (`@graph`), types actifs conformes (Organization, Article, Product, etc.), absence de schémas dépréciés (`FAQPage`, `HowTo`). |
| **4. E-E-A-T & Qualité Éditoriale** | **20 %** | Transparence de l'auteur (page bio, liens de preuve), fraîcheur des dates (datePublished/dateModified), pages légales (mentions, confidentialité), originalité des données et de l'expérience démontrée. |
| **5. GEO & Agent Readiness** | **15 %** | Citabilité des passages (paragraphes de synthèse 40-80 mots), présence d'un `llms.txt` ou d'un rendu textuel accessible pour les agents IA, conformité accessibilité/formulaires. |

### Barème d'Appréciation
- **90 - 100** : 🟢 **Excellent** (Prêt pour la compétition de premier plan, éligible aux AI Overviews).
- **75 - 89** : 🟡 **Bon** (Bases solides, quelques optimisations ciblées requises).
- **50 - 74** : 🟠 **Moyen** (Freins techniques ou manque d'autorité/schema détectés).
- **0 - 49** : 🔴 **Critique** (Pénalités probables, problèmes majeurs d'indexation ou de performance).

---

## 2. Le Principe de Falsifiabilité des Recommandations

Pour éliminer les recommandations vagues, "génériques" ou purement promotionnelles, chaque action préconisée **DOIT** obligatoirement comporter 4 composantes :

1. **Observation Factuelle** : Preuve mesurée directement dans le code ou le rendu (ex: *"La balise canonique pointe vers une URL HTTP non sécurisée générant une redirection 301"*).
2. **Action Corrective Recommandée** : Modification technique exacte à apporter (ex: *"Remplacer `http://...` par `https://...` dans la balise `link rel='canonical'` du template Blade `layouts.app`"*).
3. **Indicateur Avancé (*Leading Indicator*)** : Ce qui doit changer immédiatement après le déploiement (ex: *"Le crawler HTTP ou l'outil d'inspection d'URL de Google Search Console valide le statut canonique en 200 direct sans redirection"*).
4. **Test d'Échec Explicite (*Falsifiability Check*)** : *"Comment sait-on que l'action a échoué ?"* (ex: *"Si après 14 jours, Search Console signale toujours 'Page avec redirection' ou sélectionne une autre URL canonique choisie par Google, la règle de réécriture Nginx/Apache est en conflit avec la balise"*).

---

## 3. Matrice de Priorisation des Tâches

Les constats sont classés selon une matrice à 4 niveaux d'urgence :

| Niveau | Impact Métier | Délai Recommandé | Exemples Typiques |
|:---|:---|:---:|:---|
| 🚨 **Critique** | Empêche l'indexation ou bloque complètement les moteurs | Immédiat (24h) | `noindex` par erreur sur des pages de vente, boucle de redirection 301, site non sécurisé HTTPS, page blanche pour les bots JS. |
| ⚠️ **Élevé** | Dégrade significativement le classement ou la citabilité | 1 semaine | Balise canonique erronée, absence de balisage Schema.org, LCP > 4s, INP catastrophique, balises `<title>` dupliquées en masse. |
| ℹ️ **Moyen** | Opportunité d'optimisation concurrentielle | 2 à 4 semaines | Enrichissement des passages clés pour les AI Overviews, ajout du maillage interne contextuel, mise en place de `llms.txt`. |
| 💡 **Faible** | Peaufinage de détail ou micro-optimisation | Backlog | Retouche mineure de meta descriptions, mise à jour de liens sociaux secondaires dans Schema.org. |
