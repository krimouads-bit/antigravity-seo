<#
.SYNOPSIS
    Antigravity SEO Analyzer (Native Windows PowerShell)
    Audit SEO technique, E-E-A-T, Schema.org JSON-LD (2026), GEO et Agent Readiness.
#>

param(
    [string]$Url,
    [string]$File,
    [ValidateSet("markdown", "json")][string]$Format = "markdown"
)

$ErrorActionPreference = "Stop"

if (-not $Url -and -not $File) {
    Write-Error "Vous devez specifier soit -Url soit -File."
    exit 1
}

$html = ""
$statusCode = 200
$latencyMs = 0

if ($Url) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 (Antigravity-SEO/1.0)"
    $sw.Stop()
    $latencyMs = $sw.ElapsedMilliseconds
    $statusCode = $response.StatusCode
    $html = $response.Content
    $targetName = $Url
} else {
    if (-not (Test-Path $File)) {
        Write-Error "Fichier local introuvable : $File"
        exit 1
    }
    $html = Get-Content -Path $File -Raw -Encoding utf8
    $targetName = $File
}

# Extraction On-Page
$title = ""
if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
    $title = $matches[1].Trim()
}

$description = ""
if ($html -match '(?is)<meta[^>]+name=["'']description["''][^>]+content=["'']([^"'']*)["'']' -or $html -match '(?is)<meta[^>]+content=["'']([^"'']*)["''][^>]+name=["'']description["'']') {
    $description = $matches[1].Trim()
}

$canonical = ""
if ($html -match '(?is)<link[^>]+rel=["'']canonical["''][^>]+href=["'']([^"'']*)["'']' -or $html -match '(?is)<link[^>]+href=["'']([^"'']*)["''][^>]+rel=["'']canonical["'']') {
    $canonical = $matches[1].Trim()
}

$robots = ""
if ($html -match '(?is)<meta[^>]+name=["'']robots["''][^>]+content=["'']([^"'']*)["'']') {
    $robots = $matches[1].Trim()
}

# Headings
$h1Matches = [regex]::Matches($html, '(?is)<h1[^>]*>(.*?)</h1>')
$h1Count = $h1Matches.Count
$h1Text = if ($h1Count -gt 0) { ($h1Matches[0].Groups[1].Value -replace '<[^>]+>', '').Trim() } else { "" }

$h2Matches = [regex]::Matches($html, '(?is)<h2[^>]*>(.*?)</h2>')
$h2Count = $h2Matches.Count

$questionH2Count = 0
foreach ($m in $h2Matches) {
    $txt = ($m.Groups[1].Value -replace '<[^>]+>', '').Trim()
    if ($txt -match '(?i)(comment|pourquoi|qu''est-ce|quel|quelle|how|what|why|\?)') {
        $questionH2Count++
    }
}

# Images & Alt
$imgMatches = [regex]::Matches($html, '(?is)<img\b([^>]*)>')
$totalImages = $imgMatches.Count
$missingAltCount = 0
foreach ($img in $imgMatches) {
    $attrs = $img.Groups[1].Value
    if ($attrs -notmatch 'alt\s*=\s*["''][^"'']+["'']') {
        $missingAltCount++
    }
}

# Schema.org JSON-LD
$jsonLdMatches = [regex]::Matches($html, '(?is)<script[^>]+type=["'']application/ld\+json["''][^>]*>(.*?)</script>')
$jsonLdCount = $jsonLdMatches.Count
$schemaEntities = @()
$deprecatedSchemas = @()
$hasGraph = $false

$deprecatedList = @("faqpage", "howto", "specialannouncement", "estimatedsalary", "learningvideo")

foreach ($block in $jsonLdMatches) {
    $raw = $block.Groups[1].Value.Trim()
    try {
        $parsed = ConvertFrom-Json $raw -ErrorAction SilentlyContinue
        if ($parsed.'@graph') {
            $hasGraph = $true
            foreach ($item in $parsed.'@graph') {
                if ($item.'@type') {
                    $t = [string]$item.'@type'
                    $schemaEntities += $t
                    if ($deprecatedList -contains $t.ToLower()) { $deprecatedSchemas += $t }
                }
            }
        } elseif ($parsed.'@type') {
            $t = [string]$parsed.'@type'
            $schemaEntities += $t
            if ($deprecatedList -contains $t.ToLower()) { $deprecatedSchemas += $t }
        }
    } catch {}
}

# Calcul du Score (0-100)
$techScore = 25
$onpageScore = 20
$schemaScore = 20
$eeatScore = 20
$geoScore = 15
$deductions = @()

if (-not $canonical) {
    $techScore -= 8
    $deductions += "Absence de balise canonique (-8)"
}
if ($robots -match '(?i)noindex') {
    $techScore -= 15
    $deductions += "Directives robots noindex actives (-15)"
}

if (-not $title) {
    $onpageScore -= 8
    $deductions += "Balise <title> absente (-8)"
} elseif ($title.Length -lt 30 -or $title.Length -gt 65) {
    $onpageScore -= 3
    $deductions += "Longueur de la balise <title> non optimale ($($title.Length) car.) (-3)"
}

if (-not $description) {
    $onpageScore -= 6
    $deductions += "Meta description absente (-6)"
}

if ($h1Count -eq 0) {
    $onpageScore -= 6
    $deductions += "Aucun titre <h1> trouve (-6)"
} elseif ($h1Count -gt 1) {
    $onpageScore -= 3
    $deductions += "Plusieurs titres <h1> ($h1Count) detectes (-3)"
}

if ($missingAltCount -gt 0) {
    $pen = [Math]::Min(5, [int]($missingAltCount / [Math]::Max($totalImages, 1) * 5) + 1)
    $onpageScore -= $pen
    $deductions += "$missingAltCount/$totalImages images sans attribut alt (-$pen)"
}

if ($jsonLdCount -eq 0) {
    $schemaScore -= 15
    $deductions += "Aucun balisage Schema.org JSON-LD detecte (-15)"
} else {
    if ($deprecatedSchemas.Count -gt 0) {
        $schemaScore -= 5
        $deductions += "Schemas deprecies detectes ($($deprecatedSchemas -join ', ')) (-5)"
    }
}

if ($h2Count -eq 0) {
    $geoScore -= 5
    $deductions += "Absence de sous-titres <h2> (-5)"
} elseif ($questionH2Count -eq 0) {
    $geoScore -= 2
    $deductions += "Aucun sous-titre interrogatif pour capter les AI Overviews (-2)"
}

$techScore = [Math]::Max(0, $techScore)
$onpageScore = [Math]::Max(0, $onpageScore)
$schemaScore = [Math]::Max(0, $schemaScore)
$eeatScore = [Math]::Max(0, $eeatScore)
$geoScore = [Math]::Max(0, $geoScore)
$totalScore = $techScore + $onpageScore + $schemaScore + $eeatScore + $geoScore

$resultObj = [PSCustomObject]@{
    Url = $targetName
    StatusCode = $statusCode
    LatencyMs = $latencyMs
    TotalScore = $totalScore
    ScoreDetails = [PSCustomObject]@{
        Technical = $techScore
        OnPage = $onpageScore
        Schema = $schemaScore
        EEAT = $eeatScore
        GeoAgent = $geoScore
    }
    Deductions = $deductions
    OnPage = [PSCustomObject]@{
        Title = $title
        TitleLength = $title.Length
        Description = $description
        DescriptionLength = $description.Length
        Canonical = $canonical
        Robots = $robots
        H1Count = $h1Count
        H1Text = $h1Text
        H2Count = $h2Count
        QuestionH2Count = $questionH2Count
    }
    Schema = [PSCustomObject]@{
        JsonLdBlocks = $jsonLdCount
        Entities = $schemaEntities
        HasGraph = $hasGraph
        Deprecated = $deprecatedSchemas
    }
    Images = [PSCustomObject]@{
        Total = $totalImages
        MissingAlt = $missingAltCount
    }
}

if ($Format -eq "json") {
    $resultObj | ConvertTo-Json -Depth 5
} else {
    $grade = if ($totalScore -ge 90) { "Excellent" } elseif ($totalScore -ge 75) { "Bon" } elseif ($totalScore -ge 50) { "Moyen" } else { "Critique" }
    
    $lines = @()
    $lines += "# Rapport d'Audit Antigravity SEO - $targetName"
    $lines += ""
    $lines += "**Date de l'audit :** " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
    $lines += "**Score Global :** **$totalScore / 100** ($grade)"
    $lines += "**Statut HTTP :** $statusCode | **Latence Reseau :** $latencyMs ms"
    $lines += ""
    $lines += "---"
    $lines += ""
    $lines += "## Repartition du Score par Pilier"
    $lines += ""
    $lines += "| Pilier | Score | Max | Statut |"
    $lines += "|:---|:---:|:---:|:---|"
    $lines += "| **1. SEO Technique & Performance** | **$techScore** | 25 | $(if ($techScore -ge 20) { 'Conforme' } else { 'A corriger' }) |"
    $lines += "| **2. Structure On-Page & Semantique** | **$onpageScore** | 20 | $(if ($onpageScore -ge 16) { 'Conforme' } else { 'A corriger' }) |"
    $lines += "| **3. Microdonnees Schema.org (2026)** | **$schemaScore** | 20 | $(if ($schemaScore -ge 15) { 'Conforme' } else { 'A corriger' }) |"
    $lines += "| **4. E-E-A-T & Qualite Editoriale** | **$eeatScore** | 20 | $(if ($eeatScore -ge 15) { 'Conforme' } else { 'A corriger' }) |"
    $lines += "| **5. GEO & Agent Readiness** | **$geoScore** | 15 | $(if ($geoScore -ge 12) { 'Conforme' } else { 'A corriger' }) |"
    $lines += ""
    $lines += "---"
    $lines += ""
    $lines += "## Synthese des Constats Cles"
    $lines += ""
    $lines += "- **Titre (<title>)** : $(if ($title) { "$title ($($title.Length) car.)" } else { 'NON DEFINI' })"
    $lines += "- **Meta Description** : $(if ($description) { "$description ($($description.Length) car.)" } else { 'NON DEFINIE' })"
    $lines += "- **Balise Canonique** : $(if ($canonical) { $canonical } else { 'NON DEFINIE' })"
    $lines += "- **Directives Robots** : $(if ($robots) { $robots } else { 'index, follow (par defaut)' })"
    $lines += "- **Structure Titres** : H1: $h1Count | H2: $h2Count (dont $questionH2Count interrogatifs)"
    $lines += "- **Donnees Structurees** : $jsonLdCount bloc(s) JSON-LD | Entites: $($schemaEntities -join ', ')"
    $lines += "- **Images** : $totalImages image(s) (dont $missingAltCount sans balise alt)"
    $lines += ""
    $lines += "---"
    $lines += ""
    $lines += "## Plan d'Action Recommande"
    $lines += ""
    
    if ($deductions.Count -gt 0) {
        $idx = 1
        foreach ($d in $deductions) {
            $lines += "$idx. **$d**"
            $idx++
        }
    } else {
        $lines += "Aucune anomalie critique detectee. La page respecte les standards."
    }
    
    $lines -join "`n"
}
