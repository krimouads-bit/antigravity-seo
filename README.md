# 🚀 Antigravity SEO

> **The Next-Generation SEO & GEO Skill for [Antigravity](https://antigravity.google) & Google Gemini.**  
> Technical SEO · Core Web Vitals (INP/LCP/CLS) · E-E-A-T · Schema.org JSON-LD (2026 Standards) · GEO (AI Overviews & Gemini Citability) · Agentic Browsing & `llms.txt`.

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://antigravity.google)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.5-8E75C2)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20External-brightgreen)](#scripts)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#installation)

---

## 🌟 Why Antigravity SEO?

Most traditional SEO audit tools are still anchored in 2020: they measure outdated metrics (like FID instead of INP), fail to account for Google's latest rich-result deprecations (such as the removal of `FAQPage` rich results in May 2026), and ignore the reality of **AI Search (GEO / AEO)**.

**Antigravity SEO** is purpose-built from the ground up for the **Antigravity agentic environment** and **Google Gemini**:

- 🤖 **Designed Exclusively for Antigravity & Gemini**: Leverages Antigravity's native tools (`browser_subagent`, `run_command`, `read_url_content`) to perform in-depth DOM inspections, headless crawls, and local source code audits.
- ⚡ **2026 Core Web Vitals Compliance**: Real-world evaluation of **INP** (< 200ms), **LCP** (< 2.5s), and **CLS** (< 0.1).
- 🏷️ **Schema.org 2026 Standards**: Immediate detection of deprecated schemas (`FAQPage`, `HowTo`, `SpecialAnnouncement`) and generation of modern, connected `@graph` JSON-LD models.
- 🧠 **GEO / AEO Citability Engine**: Evaluates passage citability (40–80 words standalone response blocks) for Google AI Overviews, Gemini, and Perplexity.
- 🌐 **Agent Readiness**: Verifies semantic form markup, ARIA access, and `llms.txt` formatting for autonomous AI agents.
- 🎯 **Falsifiable Action Plans**: Every recommendation includes a concrete observation, leading indicator, and an explicit test to detect failure.

---

## 📁 Repository Structure

```text
antigravity-seo/
├── SKILL.md                          # Master Antigravity skill specification
├── README.md                         # Project documentation & GitHub guide
├── LICENSE                           # MIT License
├── references/                       # Progressive disclosure manuals
│   ├── technical-seo.md              # Technical SEO, Core Web Vitals (INP/LCP/CLS)
│   ├── eeat-framework.md             # E-E-A-T & Google Search Quality Rater Guidelines
│   ├── schema-jsonld.md              # Schema.org JSON-LD 2026 rich results & deprecations
│   ├── geo-aeo-ai-search.md          # Generative Engine Optimization (AI Overviews)
│   ├── agentic-browsing.md           # Lighthouse Agentic Browsing & llms.txt readiness
│   └── audit-methodology.md          # 0-100 Scoring rubric & falsifiable action matrix
├── scripts/                          # Zero-dependency audit utilities
│   ├── seo_analyzer.ps1              # Native Windows PowerShell analyzer (instant execution)
│   └── seo_analyzer.py               # Cross-platform Python 3.8+ analyzer (standard library)
└── examples/
    └── sample-audit-report.md        # Comprehensive example audit report
```

---

## 🚀 Installation on Antigravity

You can install **Antigravity SEO** either globally across your entire machine or specifically within a single project workspace.

### Option A — Global Installation (Recommended)

To make Antigravity SEO available across all your projects on this computer:

#### Windows (PowerShell):
```powershell
# Clone directly into your global Antigravity skills directory:
git clone https://github.com/krimouads-bit/antigravity-seo.git "$env:USERPROFILE\.gemini\config\skills\antigravity-seo"
```

#### macOS / Linux:
```bash
git clone https://github.com/krimouads-bit/antigravity-seo.git ~/.gemini/config/skills/antigravity-seo
```

*Antigravity automatically discovers and activates the skill via progressive disclosure!*

---

### Option B — Workspace Project Installation

To include Antigravity SEO directly in a repository and share it with your team:

```bash
# Inside your project root:
mkdir -p .agents/skills
git clone https://github.com/krimouads-bit/antigravity-seo.git .agents/skills/antigravity-seo
```

---

## 💡 How to Use with Antigravity

Once installed, simply prompt Antigravity in natural language:

### 1. Audit a Public Website
> *"Fais un audit SEO complet de https://mon-site.com avec antigravity-seo"*  
> *"Audit https://example.com for technical SEO, Schema.org, and GEO readiness"*

### 2. Audit Local Code (Laravel, Blade, HTML, Vue, React)
> *"Audit les vues Blade et le balisage SEO de notre projet avant le déploiement"*  
> *"Check if our index.html meets the 2026 Schema.org and E-E-A-T guidelines"*

### 3. Generate 2026-Compliant Schema JSON-LD
> *"Génère un graphe Schema.org JSON-LD connecté pour notre SaaS de facturation"*

### 4. Optimize for Google AI Overviews (GEO)
> *"Optimise cet article de blog pour qu'il soit cité dans les Google AI Overviews et Gemini"*

---

## 🛠️ CLI Standalone Tools

The skill includes two standalone, zero-dependency tools for instant audits:

### Native PowerShell (Windows):
```powershell
# Online URL:
powershell -ExecutionPolicy Bypass -File scripts/seo_analyzer.ps1 -Url "https://example.com"

# Local file:
powershell -ExecutionPolicy Bypass -File scripts/seo_analyzer.ps1 -File "public/index.html"

# Output as JSON:
powershell -ExecutionPolicy Bypass -File scripts/seo_analyzer.ps1 -Url "https://example.com" -Format json
```

### Python 3 (Cross-Platform):
```bash
python scripts/seo_analyzer.py --url "https://example.com"
python scripts/seo_analyzer.py --file "resources/views/welcome.blade.php" --format json
```

---

## 📊 0-100 Weighted Scoring Rubric

| Pillar | Weight | Key Evaluations |
|:---|:---:|:---|
| **1. Technical SEO & Performance** | **25%** | Status codes, canonical tags, robots.txt, Core Web Vitals (INP < 200ms, LCP < 2.5s, CLS < 0.1), HTTPS. |
| **2. On-Page Structure & Semantics** | **20%** | `<title>`, meta description, single `<h1>`, logical heading hierarchy, image `alt` coverage. |
| **3. Schema.org JSON-LD (2026)** | **20%** | Valid syntax, `@graph` interconnected entities, zero deprecated schemas (`FAQPage`, `HowTo`). |
| **4. E-E-A-T & Quality Signals** | **20%** | Transparent authorship, verifiable credentials, publication/update timestamps, primary data. |
| **5. GEO & Agent Readiness** | **15%** | Standalone 40-80 words citation passages, `llms.txt`, semantic form markup, ARIA roles. |

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

## 🤝 Contributing

Contributions, feedback, and pull requests are welcome! If you have recommendations for Google Search updates, Gemini advancements, or new schema patterns, feel free to open an issue or PR.
