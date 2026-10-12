# Référence : Agentic Browsing & Préparation aux Agents IA

Guide pour auditer et optimiser les applications web et sites de contenu pour l'interaction avec les agents autonomes d'IA (navigateurs autonomes, assistants de shopping, moteurs d'action, et *Lighthouse Agentic Browsing*).

---

## 1. Qu'est-ce que l'Agentic Readiness ?

L'Agentic Readiness désigne la capacité d'un site à être parcouru, compris et utilisé de manière fluide par un agent autonome (qu'il s'agisse d'un navigateur headless piloté par LLM, d'un assistant comme Antigravity, ou d'un bot d'extraction).

---

## 2. Critères de la Catégorie "Agentic Browsing" (Lighthouse)

La catégorie *Agentic Browsing* évalue la clarté et l'accessibilité de l'interface pour les agents IA :

1. **Accessibilité Sémantique & ARIA** :
   - Présence d'un `role` et d'un `aria-label` descriptif sur tous les éléments cliquables sans texte visible (icônes, boutons fermer).
   - Utilisation des balises HTML natives (`<button>`, `<a href>`, `<input>`, `<select>`) plutôt que des `<div>` avec écouteurs de clics JavaScript arbitraires.
2. **Formulaires & Intrants Déterministes** :
   - Chaque champ de formulaire possède un `<label for="...">` explicite associé à l'`id` du champ.
   - Les attributs `name`, `type` et `autocomplete` sont renseignés conformément aux standards (`email`, `tel`, `address-line1`, etc.).
3. **Absence de Barrières Bloquantes sans Fallback** :
   - Les pop-ups modales et overlays intempestifs bloquent souvent la navigation des agents. Prévoir une touche de fermeture accessible ou éviter l'affichage forcé avant interaction utilisateur.
4. **Rendu Textuel Non Obfusqué** :
   - Les textes critiques doivent être présents dans le DOM (pas dessinés dans un `<canvas>` ou intégrés dans des images bitmap sans alternative textuelle).

---

## 3. Mise en Place du Standard `llms.txt`

Le fichier `llms.txt` (placé à la racine `https://domaine.com/llms.txt`) permet de fournir un résumé structuré en Markdown de votre site, facilitant la tâche des modèles de langage et des agents d'exploration.

### Structure Recommandée (`/llms.txt`) :
```markdown
# Nom du Site / Projet

> Description concise en une phrase de ce que fait l'application ou l'entreprise.

## Présentation
Résumé synthétique des fonctionnalités, produits ou services proposés.

## Liens Clés
- [Documentation Technique](https://domaine.com/docs): Guide complet d'utilisation.
- [API Reference](https://domaine.com/api): Spécifications des endpoints.
- [Tarifs](https://domaine.com/pricing): Détail des plans et abonnements.
- [À Propos & Équipe](https://domaine.com/about): Informations sur l'entreprise et la gouvernance.

## Directives pour les Agents IA
- Les requêtes d'action peuvent être envoyées via l'API REST documentée sur `/api/v1`.
- Les données de stock et de prix en temps réel sont disponibles sur `/api/public/catalog.json`.
```

---

## 4. WebMCP & Protocoles d'Intégration d'Outils

Pour les applications web interactives, l'intégration de points de terminaison standardisés au protocole MCP (*Model Context Protocol*) permet aux agents IA (comme Antigravity et Claude) d'interagir directement avec votre logique métier sans devoir simuler des clics complexes dans le navigateur.
