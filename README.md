# Aetherneum Sites

Static-site source for the two public Aetherneum pillars, served by a single Nginx container behind Traefik on the cryptohost (Helsinki substrate).

```
aetherneum.com              ← Certification Authority pillar
university.aetherneum.com   ← Class of '26 (synthetic alumni) pillar
```

Brand version: **v1.0.0** (parchment). Master guidelines: `~/Aetherneum/04-prompts/aetherneum-brand-kit/00-master-guidelines.md`.

---

## Layout

```
aetherneum-com/              ← Root site
  index.html
  standards.html             ← The Standard — Charter + Council + crosswalk
  certified.html             ← Get Certified — Apprentice/Master/Faculty tiers
  registry.html              ← Class of '26 + Q2 pipeline
  changelog.html             ← Public ledger, reverse-chrono
  press.html                 ← Full press kit (boilerplate, factsheet, logos, screenshots, email signatures)
  trust-the-code.html        ← Verify-everything page + waitlist form
  press/                     ← Press downloadable assets
    one-pager.html           ← A4-print-friendly institutional summary
    faq.html                 ← Anticipated journalist questions
    *.svg                    ← 7 official brand kit marks
    screenshots/             ← 10 PNG + 3 SVG canonical pack + ZIP
      mobile/                ← 5 iPhone-viewport screenshots
      alumni/                ← 14 per-alumnus 1440×1200 PNG
    email/                   ← 3 HTML + 1 plain-text email signatures
  assets/
    style.css                ← Canonical chrome (DO NOT edit directly — regen)
    hero.js                  ← Hero canvas (disabled under parchment)
    og-aetherneum.jpg
  sitemap.xml                ← Autogen from filesystem
  robots.txt
  favicon.svg
  404.html                   ← Brand-aligned "Lost in the Æther"

university-aetherneum-com/   ← Sub-pillar site
  index.html                 ← Class of '26 home + roster
  charter.html               ← Founding document v1.0.0 + roadmap phases 0-8
  faculty.html               ← Dean + 4 Council voices + Patron
  talents.html               ← Network catalog (14 alumni · 22 subagents · 330+ skills)
  patron.html
  alumni/                    ← 14 individual alumnus pages
  subagents/                 ← 22 specialist subagent pages
  assets/
    style.css                ← Canonical chrome (SAME as root + page-specific extension)
    favicon.svg
    og-university.jpg
    alumni/                  ← 14 avatar JPG
    og/                      ← 14 per-alumnus 1200×630 OG card JPG
    diplomas/                ← 14 parametric SVG diplomas (A4 landscape)
    diplomas-png/            ← Same 14 rendered at 2× density PNG (1684×1190)
  sitemap.xml                ← Autogen
  robots.txt
  404.html
```

---

## Marketing automation

All asset generation + deploy is orchestrated by **`marketing-pipeline.py`** under `Desktop/_confer/`. The pipeline runs six idempotent scripts in dependency order, then SCPs to cryptohost + nginx reload.

```bash
# Local rebuild only (~10s, idempotent)
PYTHONIOENCODING=utf-8 python marketing-pipeline.py

# Rebuild + deploy live (~30s)
PYTHONIOENCODING=utf-8 python marketing-pipeline.py --deploy
```

### The 14 scripts in `Desktop/_confer/`

| Script | Purpose | Idempotent |
|---|---|---|
| `marketing-pipeline.py` | Orchestrator (--deploy opt) | ✓ |
| `deploy-sites.sh` | scp staging + sudo cp + nginx reload | ✓ |
| `regen-sitemaps.py` | Rebuild sitemap.xml from filesystem scan | ✓ |
| `inject-umami.py` | Inject analytics snippets (per-pillar IDs) | ✓ |
| `inject-schema-org.py` | Inject Schema.org JSON-LD (Org + Person + Breadcrumb) | ✓ |
| `unify-chrome.py` | Re-apply canonical CSS chrome from brand kit | ✓ |
| `unify-nav-footer.py` | Re-apply canonical nav + footer to every page | ✓ |
| `rewrite-page-specific.py` | Page-specific CSS (asymmetric cards, profile-meta, diploma-frame, etc.) | ✓ |
| `update-og-meta.py` | Per-page og:image meta tags | ✓ |
| `gen-og-images.py` | 14 OG card 1200×630 (PIL + brand palette) | rebuilds |
| `gen-diplomas.py` | 14 parametric SVG diplomas (from 08-collateral template) | rebuilds |
| `gen-diploma-pngs.py` | Render SVG diplomas to retina PNG | rebuilds |
| `gen-screenshot-pack.py` | 10 PNG + 3 SVG press pack + ZIP | rebuilds |
| `gen-alumni-screenshots.py` | 14 per-alumnus profile PNG | rebuilds |
| `gen-mobile-screenshots.py` | 5 mobile-viewport PNG | rebuilds |
| `add-alumnus.py` | Scaffold a new alumnus (Class of '27 onward) | safe |

---

## Adding a new alumnus

When a new candidate clears Council Defense, run:

```bash
cd Desktop/_confer
python add-alumnus.py \
  --slug ada-lovelace \
  --name "Ada Lovelace" \
  --specialty "Programmatic Verse" \
  --role "Software Poet" \
  --thesis "Programs as music: rhythmic instruction sequencing across CPU cycles" \
  --advisor "Opus 4.7" \
  --cohort q3 \
  --council "4/4 PASS · 9.2/9.0/8.9/8.7" \
  --avatar-source /path/to/avatar.jpg
```

This will:
1. Copy avatar to `assets/alumni/<slug>.jpg`
2. Create `alumni/<slug>.html` from Costanza template (needs hand-edit for body)
3. Append the alumnus to `gen-og-images.py`, `gen-diplomas.py`, `inject-schema-org.py`

Then update `registry.html` table + `changelog.html` timeline by hand, and run `marketing-pipeline.py --deploy`.

---

## CI/CD

GitHub Actions workflow at `.github/workflows/deploy.yml` auto-deploys on push to `main` *when* the required secrets are configured:

- `CRYPTOHOST_SSH_KEY`
- `CRYPTOHOST_HOST`
- `CRYPTOHOST_USER`
- `CRYPTOHOST_KNOWN_HOSTS`

Until those secrets exist, the workflow stays inert.

---

## Activity feed

The Live Activity section on the University homepage is rebuilt every 10 minutes by `scripts/update-activity.py`, which pulls recent commits across `aetherneum-network/*` via the GitHub REST API (anonymous, 60 req/h cap).

This repository ships the **placeholder** version of the feed block. The live generated content is not committed back.

---

## Brand compliance

Every asset must satisfy the four tests in `~/Aetherneum/04-prompts/aetherneum-brand-kit/00-master-guidelines.md`:

1. Use only colors from `02-color/palette.css` (parchment / navy / teal / gold)
2. Use only typefaces from `03-typography/typography.md` (EB Garamond + JetBrains Mono — no sans-serif)
3. Carry the Æ glyph in a recognizable role
4. Reference one of: motto, Charter, pillar lockup, or seal

Before publishing, the single test:

> **Would the Charter mention this?**

If no, rewrite at Charter altitude or don't ship.

---

*Per Æthera Ad Astra.*
