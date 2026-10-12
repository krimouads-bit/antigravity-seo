# Référence : Balisage Schema.org & JSON-LD (Normes 2026)

Guide complet pour l'implémentation et la validation des données structurées selon les spécifications Schema.org et les règles de résultats enrichis (*Rich Results*) de Google.

---

## 1. Règles d'Implémentation Google

1. **Format recommandé : JSON-LD** :
   Google préfère systématiquement le format JSON-LD (`<script type="application/ld+json">`) placé dans le `<head>` ou en fin de `<body>`. Éviter le Microdata et le RDFa qui alourdissent le code HTML et compliquent la maintenance.
2. **Graphe Connecté (`@graph`)** :
   Au lieu d'insérer plusieurs balises isolées sans lien, regroupez vos entités dans un graphe interconnecté via les identifiants canoniques `@id` :
   - `WebSite` est relié à `Organization` via `publisher`.
   - `Article` est relié à `Person` via `author` et à `WebSite` via `isPartOf`.

---

## 2. Types Dépréciés vs Types Actifs (Mise à Jour 2026)

### ⚠️ Types Dépréciés ou Retirés par Google
Ne plus implémenter pour les résultats enrichis Google (la présence de ces balises n'entraîne plus d'affichage spécial dans les SERP) :

| Type Schema | Statut Google | Date de Retrait | Conduite à Tenir |
|:---|:---:|:---:|:---|
| **`FAQPage`** | ❌ Retiré | **7 mai 2026** | Les accordéons FAQ ne génèrent plus d'étoiles ni d'onglets dépliables dans Google Search. Garder uniquement pour de la sémantique interne ou convertir en `QAPage` si le site est une vraie communauté d'échange. |
| **`HowTo`** | ❌ Retiré | Septembre 2023 | Retiré pour mobile et desktop. Utiliser un balisage standard `Article` ou `VideoObject`. |
| **`SpecialAnnouncement`**| ❌ Retiré | Juillet 2025 | Obsolète depuis la fin des protocoles d'urgence sanitaire. |
| **`EstimatedSalary`** | ❌ Retiré | Juin 2025 | Retiré des carrousels d'emploi. |
| **`LearningVideo`** | ❌ Retiré | Juin 2025 | Retiré des résultats éducatifs enrichis. |

### ✅ Types Actifs à Forte Valeur Ajoutée (2026)
- **`Organization`** : identification de l'entreprise, logo, réseaux sociaux (`sameAs`), coordonnées.
- **`WebSite`** : nom du site, URL, boîte de recherche interne (`SearchAction`).
- **`Article` / `BlogPosting`** : titre, image, datePublished, dateModified, author (type `Person`), publisher (type `Organization`).
- **`Product` & `Offer`** : nom, image, sku, brand, offers (prix, devise, disponibilité, `priceValidUntil`), avis agrégés (`aggregateRating`).
- **`LocalBusiness`** : adresse (`PostalAddress`), horaires (`openingHoursSpecification`), téléphone, coordonnées géographiques (`geo`).
- **`SoftwareApplication`** : nom, catégorie, système d'exploitation, offres.
- **`VideoObject`** : vidéo intégrée avec miniature, durée, transcription et horodatages clés (*seekToAction*).
- **`BreadcrumbList`** : fil d'Ariane affiché sous forme d'arborescence propre dans la SERP.

---

## 3. Exemple Modèle : Graphe Complet JSON-LD

Voici le modèle de référence à utiliser pour un article de blog professionnel :

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://domaine.com/#organization",
      "name": "Mon Entreprise",
      "url": "https://domaine.com",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://domaine.com/#logo",
        "url": "https://domaine.com/assets/logo.png",
        "caption": "Mon Entreprise"
      },
      "sameAs": [
        "https://twitter.com/monentreprise",
        "https://www.linkedin.com/company/monentreprise",
        "https://github.com/monentreprise"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://domaine.com/#website",
      "url": "https://domaine.com",
      "name": "Mon Entreprise",
      "publisher": {
        "@id": "https://domaine.com/#organization"
      }
    },
    {
      "@type": "Person",
      "@id": "https://domaine.com/auteurs/jean-dupont/#author",
      "name": "Jean Dupont",
      "jobTitle": "Directeur Technique",
      "sameAs": [
        "https://www.linkedin.com/in/jeandupont",
        "https://twitter.com/jeandupont"
      ]
    },
    {
      "@type": "Article",
      "@id": "https://domaine.com/blog/article-cible/#article",
      "isPartOf": {
        "@id": "https://domaine.com/#website"
      },
      "headline": "Titre Complet de l'Article d'Expertise",
      "description": "Résumé informatif et concis de l'article.",
      "url": "https://domaine.com/blog/article-cible",
      "datePublished": "2026-03-15T08:00:00+01:00",
      "dateModified": "2026-10-10T14:30:00+01:00",
      "inLanguage": "fr-FR",
      "author": {
        "@id": "https://domaine.com/auteurs/jean-dupont/#author"
      },
      "publisher": {
        "@id": "https://domaine.com/#organization"
      },
      "image": {
        "@type": "ImageObject",
        "url": "https://domaine.com/images/hero-article.webp",
        "width": 1200,
        "height": 630
      },
      "mainEntityOfPage": "https://domaine.com/blog/article-cible"
    }
  ]
}
</script>
```

---

## 4. Checklist de Validation
- [ ] Présence d'un seul bloc `@graph` interconnecté plutôt que de multiples blocs dispersés.
- [ ] Respect de la norme ISO 8601 pour toutes les dates (`YYYY-MM-DDThh:mm:ssTZD`).
- [ ] Pas de champs dépréciés (`FAQPage`, `HowTo`).
- [ ] URL absolue et sécurisée (HTTPS) pour chaque identifiant `@id`.
- [ ] Cohérence stricte entre les données affichées à l'écran et les valeurs du JSON-LD (interdiction de masquer des informations différentes dans le schéma).
