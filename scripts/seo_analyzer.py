#!/usr/bin/env python3
"""
Antigravity SEO Analyzer (Zero-Dependency)
Analyzes an online URL or local HTML file for Technical SEO, E-E-A-T signals,
Schema.org JSON-LD compliance (2026), GEO (AI Citability), and Agent Readiness.

Compatible with Python 3.8+ (standard library only).
"""

import sys
import os
import re
import json
import argparse
import time
import ssl
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        
        self.meta_tags = []
        self.links = []
        
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.current_heading = None
        self.heading_buffer = []
        
        self.images = []
        self.forms = []
        self.current_form = None
        self.inputs = []
        self.labels = []
        
        self.json_ld_blocks = []
        self.in_json_ld = False
        self.json_ld_buffer = []
        
        self.semantic_tags = {"header": 0, "nav": 0, "main": 0, "article": 0, "section": 0, "footer": 0}
        self.text_content = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        
        if tag in self.semantic_tags:
            self.semantic_tags[tag] += 1
            
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.meta_tags.append(attr_dict)
        elif tag == "link":
            self.links.append(attr_dict)
        elif tag in ("h1", "h2", "h3"):
            self.current_heading = tag
            self.heading_buffer = []
        elif tag == "img":
            self.images.append({
                "src": attr_dict.get("src", ""),
                "alt": attr_dict.get("alt", None),
                "loading": attr_dict.get("loading", ""),
                "width": attr_dict.get("width", ""),
                "height": attr_dict.get("height", "")
            })
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_buffer = []
        elif tag == "input":
            self.inputs.append({
                "type": attr_dict.get("type", "text"),
                "name": attr_dict.get("name", ""),
                "id": attr_dict.get("id", ""),
                "aria-label": attr_dict.get("aria-label", "")
            })
        elif tag == "label":
            self.labels.append({
                "for": attr_dict.get("for", "")
            })

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2", "h3"):
            text = " ".join(self.heading_buffer).strip()
            if tag == "h1":
                self.h1.append(text)
            elif tag == "h2":
                self.h2.append(text)
            elif tag == "h3":
                self.h3.append(text)
            self.current_heading = None
            self.heading_buffer = []
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            raw_json = "".join(self.json_ld_buffer).strip()
            if raw_json:
                self.json_ld_blocks.append(raw_json)
            self.json_ld_buffer = []

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.current_heading:
            self.heading_buffer.append(data)
        elif self.in_json_ld:
            self.json_ld_buffer.append(data)
        if self.current_tag not in ("script", "style"):
            clean = data.strip()
            if clean:
                self.text_content.append(clean)


def fetch_url(url, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 (Antigravity-SEO-Analyzer/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    req = Request(url, headers=headers)
    start_time = time.time()
    try:
        with urlopen(req, timeout=timeout, context=ctx) as response:
            latency_ms = round((time.time() - start_time) * 1000)
            status_code = response.getcode()
            content = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            return {
                "success": True,
                "status_code": status_code,
                "latency_ms": latency_ms,
                "content_type": content_type,
                "html": content,
                "final_url": response.geturl()
            }
    except HTTPError as e:
        latency_ms = round((time.time() - start_time) * 1000)
        return {
            "success": False,
            "status_code": e.code,
            "latency_ms": latency_ms,
            "error": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "latency_ms": 0,
            "error": str(e)
        }


def analyze_html(html, target_url=""):
    parser = SEOHTMLParser()
    try:
        parser.feed(html)
    except Exception:
        pass
        
    title = parser.title.strip()
    
    # Meta tags extraction
    description = ""
    robots = ""
    canonical = ""
    og_data = {}
    twitter_data = {}
    
    for meta in parser.meta_tags:
        name = meta.get("name", "").lower()
        prop = meta.get("property", "").lower()
        content = meta.get("content", "")
        
        if name == "description":
            description = content
        elif name == "robots":
            robots = content
        elif prop.startswith("og:"):
            og_data[prop] = content
        elif name.startswith("twitter:"):
            twitter_data[name] = content
            
    for link in parser.links:
        rel = link.get("rel", "").lower()
        if "canonical" in rel:
            canonical = link.get("href", "")
            
    # Schema JSON-LD analysis
    schema_entities = []
    schema_errors = []
    deprecated_schemas = []
    has_graph = False
    
    deprecated_list = ["faqpage", "howto", "specialannouncement", "estimatedsalary", "learningvideo"]
    
    for raw_block in parser.json_ld_blocks:
        try:
            parsed = json.loads(raw_block)
            if isinstance(parsed, dict):
                if "@graph" in parsed:
                    has_graph = True
                    for item in parsed["@graph"]:
                        stype = item.get("@type", "Unknown")
                        schema_entities.append(stype)
                        if str(stype).lower() in deprecated_list:
                            deprecated_schemas.append(stype)
                else:
                    stype = parsed.get("@type", "Unknown")
                    schema_entities.append(stype)
                    if str(stype).lower() in deprecated_list:
                        deprecated_schemas.append(stype)
            elif isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict):
                        stype = item.get("@type", "Unknown")
                        schema_entities.append(stype)
                        if str(stype).lower() in deprecated_list:
                            deprecated_schemas.append(stype)
        except Exception as e:
            schema_errors.append(f"Erreur de syntaxe JSON-LD: {str(e)[:80]}")
            
    # Images analysis
    total_images = len(parser.images)
    missing_alt = [img for img in parser.images if img["alt"] is None or img["alt"].strip() == ""]
    
    # Headings hierarchy
    h1_count = len(parser.h1)
    h2_count = len(parser.h2)
    h3_count = len(parser.h3)
    
    # Text length & GEO check
    all_text = " ".join(parser.text_content)
    words = re.findall(r'\b\w+\b', all_text)
    word_count = len(words)
    
    # Check for question headings (GEO readiness)
    question_h2 = [h for h in parser.h2 if any(q in h.lower() for q in ["comment", "pourquoi", "qu'est-ce", "quel", "quelle", "how", "what", "why", "?"])]
    
    # Forms and accessibility (Agent Readiness)
    unlabeled_inputs = []
    label_fors = {lbl["for"] for lbl in parser.labels if lbl["for"]}
    for inp in parser.inputs:
        if inp["type"] not in ("hidden", "submit", "button"):
            if inp["id"] not in label_fors and not inp["aria-label"]:
                unlabeled_inputs.append(inp)

    # Scoring Algorithm (0-100)
    score_breakdown = {
        "technical": 25,
        "onpage": 20,
        "schema": 20,
        "eeat": 20,
        "geo_agent": 15
    }
    deductions = []
    
    # Technical Deductions (Max 25)
    tech_score = 25
    if not canonical:
        tech_score -= 8
        deductions.append("Absence de balise canonique (-8)")
    elif target_url and canonical and not canonical.startswith("http"):
        tech_score -= 4
        deductions.append("Balise canonique non absolue (-4)")
        
    if "noindex" in robots.lower():
        tech_score -= 15
        deductions.append("Balise robots noindex active (-15)")
        
    # On-Page Deductions (Max 20)
    onpage_score = 20
    if not title:
        onpage_score -= 8
        deductions.append("Balise <title> manquante (-8)")
    elif len(title) < 30 or len(title) > 65:
        onpage_score -= 3
        deductions.append(f"Longueur <title> non optimale ({len(title)} car.) (-3)")
        
    if not description:
        onpage_score -= 6
        deductions.append("Meta description manquante (-6)")
    elif len(description) < 70 or len(description) > 165:
        onpage_score -= 2
        deductions.append(f"Longueur meta description non optimale ({len(description)} car.) (-2)")
        
    if h1_count == 0:
        onpage_score -= 6
        deductions.append("Aucun titre <h1> trouvé (-6)")
    elif h1_count > 1:
        onpage_score -= 3
        deductions.append(f"Plusieurs titres <h1> ({h1_count}) détectés (-3)")
        
    if missing_alt:
        ratio = len(missing_alt) / max(total_images, 1)
        pen = min(5, int(ratio * 5) + 1)
        onpage_score -= pen
        deductions.append(f"{len(missing_alt)}/{total_images} images sans attribut alt (-{pen})")
        
    # Schema Deductions (Max 20)
    schema_score = 20
    if not parser.json_ld_blocks:
        schema_score -= 15
        deductions.append("Aucun bloc Schema.org JSON-LD détecté (-15)")
    else:
        if schema_errors:
            schema_score -= 8
            deductions.append("Erreur de syntaxe dans le JSON-LD (-8)")
        if deprecated_schemas:
            schema_score -= 5
            deductions.append(f"Schémas dépréciés détectés ({', '.join(deprecated_schemas)}) (-5)")
        if not has_graph:
            schema_score -= 2
            deductions.append("Pas de graphe connecté (@graph) (-2)")
            
    # E-E-A-T Deductions (Max 20)
    eeat_score = 20
    if word_count < 300:
        eeat_score -= 8
        deductions.append(f"Contenu textuel très court ({word_count} mots) (-8)")
    elif word_count < 600:
        eeat_score -= 4
        deductions.append(f"Contenu textuel modéré ({word_count} mots) (-4)")
        
    has_author_signal = any("author" in str(x).lower() for x in (schema_entities + parser.meta_tags))
    if not has_author_signal:
        eeat_score -= 5
        deductions.append("Aucun signal d'auteur explicite détecté (-5)")
        
    # GEO & Agent Readiness (Max 15)
    geo_score = 15
    if h2_count == 0:
        geo_score -= 5
        deductions.append("Absence de sous-titres <h2> pour structurer les passages (-5)")
    elif not question_h2 and h2_count > 0:
        geo_score -= 2
        deductions.append("Aucun sous-titre interrogatif pour capter les AI Overviews (-2)")
        
    if unlabeled_inputs:
        geo_score -= 3
        deductions.append(f"{len(unlabeled_inputs)} champs sans label explicite (Agent Readiness) (-3)")
        
    total_score = max(0, min(100, tech_score + onpage_score + schema_score + eeat_score + geo_score))
    
    return {
        "url": target_url,
        "total_score": total_score,
        "score_details": {
            "technical": max(0, tech_score),
            "onpage": max(0, onpage_score),
            "schema": max(0, schema_score),
            "eeat": max(0, eeat_score),
            "geo_agent": max(0, geo_score)
        },
        "deductions": deductions,
        "onpage": {
            "title": title,
            "title_length": len(title),
            "description": description,
            "description_length": len(description),
            "canonical": canonical,
            "robots": robots,
            "h1": parser.h1,
            "h2_count": h2_count,
            "h2_sample": parser.h2[:5],
            "question_headings": question_h2,
            "word_count": word_count
        },
        "images": {
            "total": total_images,
            "missing_alt_count": len(missing_alt),
            "missing_alt_sample": [img["src"] for img in missing_alt[:3]]
        },
        "schema": {
            "blocks_count": len(parser.json_ld_blocks),
            "entities": schema_entities,
            "has_graph": has_graph,
            "deprecated_types": deprecated_schemas,
            "errors": schema_errors
        },
        "agent_readiness": {
            "semantic_tags": parser.semantic_tags,
            "unlabeled_inputs_count": len(unlabeled_inputs),
            "og_tags_count": len(og_data),
            "twitter_tags_count": len(twitter_data)
        }
    }


def format_markdown_report(data, latency_ms=0, status_code=200):
    url = data.get("url", "Document HTML")
    score = data["total_score"]
    
    if score >= 90:
        grade = "🟢 Excellent"
    elif score >= 75:
        grade = "🟡 Bon"
    elif score >= 50:
        grade = "🟠 Moyen"
    else:
        grade = "🔴 Critique"

    sd = data["score_details"]
    op = data["onpage"]
    sc = data["schema"]
    im = data["images"]
    ar = data["agent_readiness"]

    md = f"""# Rapport d'Audit SEO & GEO — {url}

**Date de l'audit :** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** **{score} / 100** — {grade}  
**Statut HTTP :** {status_code} | **Latence Réseau (TTFB approx.) :** {latency_ms} ms

---

## 📊 Répartition du Score par Pilier

| Pilier | Score | Max | Statut |
|:---|:---:|:---:|:---|
| **1. SEO Technique & Performance** | **{sd['technical']}** | 25 | {'✅ Conforme' if sd['technical'] >= 20 else '⚠️ À corriger'} |
| **2. Structure On-Page & Sémantique** | **{sd['onpage']}** | 20 | {'✅ Conforme' if sd['onpage'] >= 16 else '⚠️ À corriger'} |
| **3. Microdonnées Schema.org (2026)** | **{sd['schema']}** | 20 | {'✅ Conforme' if sd['schema'] >= 15 else '⚠️ À corriger'} |
| **4. E-E-A-T & Qualité Éditoriale** | **{sd['eeat']}** | 20 | {'✅ Conforme' if sd['eeat'] >= 15 else '⚠️ À corriger'} |
| **5. GEO & Agent Readiness** | **{sd['geo_agent']}** | 15 | {'✅ Conforme' if sd['geo_agent'] >= 12 else '⚠️ À corriger'} |

---

## 🔍 Synthèse des Constats Clés

### Balises On-Page
- **Titre (`<title>`)** : `{op['title'] or 'NON DÉFINI'}` ({op['title_length']} caractères)
- **Meta Description** : `{op['description'] or 'NON DÉFINIE'}` ({op['description_length']} caractères)
- **Canonique** : `{op['canonical'] or 'NON DÉFINIE'}`
- **Directives Robots** : `{op['robots'] or 'index, follow (par défaut)'}`
- **Hiérarchie Titres** : H1: {len(op['h1'])} | H2: {op['h2_count']} | Mots: {op['word_count']}

### Données Structurées Schema.org
- **Blocs JSON-LD détectés** : {sc['blocks_count']}
- **Entités identifiées** : {', '.join(sc['entities']) if sc['entities'] else 'Aucune'}
- **Graphe Connecté (`@graph`)** : {'Oui ✅' if sc['has_graph'] else 'Non (blocs isolés) ⚠️'}
- **Schémas Dépréciés (2026)** : {', '.join(sc['deprecated_types']) if sc['deprecated_types'] else 'Aucun ✅'}

### Médias & Accessibilité Agents
- **Images totales** : {im['total']} (dont **{im['missing_alt_count']} sans attribut alt**)
- **Balises sémantiques HTML5** : header: {ar['semantic_tags']['header']}, nav: {ar['semantic_tags']['nav']}, main: {ar['semantic_tags']['main']}, article: {ar['semantic_tags']['article']}
- **Champs de formulaire sans label** : {ar['unlabeled_inputs_count']}

---

## 🛠️ Plan d'Action & Recommandations Priorisées
"""
    if data["deductions"]:
        for i, ded in enumerate(data["deductions"], 1):
            md += f"{i}. **{ded}**\n"
    else:
        md += "Aucun problème majeur identifié. Le document respecte les standards.\n"

    return md


def main():
    parser = argparse.ArgumentParser(description="Antigravity SEO Analyzer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL publique à auditer")
    group.add_argument("--file", help="Chemin vers un fichier HTML local")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Format de sortie")
    
    args = parser.parse_args()
    
    if args.url:
        res = fetch_url(args.url)
        if not res["success"]:
            print(f"Erreur lors de la requête vers {args.url}: {res.get('error')}", file=sys.stderr)
            sys.exit(1)
        audit = analyze_html(res["html"], target_url=res.get("final_url", args.url))
        latency = res["latency_ms"]
        status = res["status_code"]
    else:
        if not os.path.exists(args.file):
            print(f"Fichier introuvable : {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        audit = analyze_html(html, target_url=args.file)
        latency = 0
        status = 200

    if args.format == "json":
        print(json.dumps(audit, indent=2, ensure_ascii=False))
    else:
        print(format_markdown_report(audit, latency_ms=latency, status_code=status))


if __name__ == "__main__":
    main()
