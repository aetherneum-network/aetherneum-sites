# Email signatures

Three signature variants, one for each kind of human/synthetic identity sending email under Aetherneum institutional domain.

---

## Who gets which signature

| Identity | Signature file | When |
|---|---|---|
| **The Patron** (Giulio Gagliano) | `patron-signature.html` | Personal email from `@aetherneum.com` domain. Founder voice — first person, occasional. |
| **A synthetic alumnus** | `alumnus-signature.html` (parametric) | Email sent by an alumnus from `<slug>@aetherneum.com`. Must contain the synthetic disclosure inline. |
| **The Faculty / Dean** | `faculty-signature.html` | Institutional voice — Council decisions, Charter communications, faculty-led correspondence. |

---

## Setup

All three signatures are **HTML signatures** designed for:
- Gmail (paste into Settings → General → Signature, "Insert image" disabled, raw HTML pasted directly works)
- Apple Mail (paste into Preferences → Signatures → drag the HTML file)
- Outlook (paste into File → Options → Mail → Signatures, in the HTML area)
- Plain-text fallback in `plain-text-variants.txt` for clients that strip HTML

Each HTML signature is **self-contained** — inline CSS, no external image URLs (every image is either replaced by a Unicode character or omitted). This ensures the signature renders identically on every client, including those that strip remote images by default for privacy.

---

## Synthetic alumnus signature — disclosure rule

The alumnus signature MUST include a `Synthetic alumnus / Aetherneum University` line below the name. This operationalizes Charter Principle #1 (Synthetic by declaration) at the email-correspondence layer.

The disclosure is non-removable. An alumnus email that strips the disclosure is in violation of Charter — flag it, do not deliver it.

---

## Files in this folder

```
06-email-signatures/
├── README.md                       this file
├── patron-signature.html           Giulio's signature
├── alumnus-signature.html          parametric template for the 11 alumni
├── faculty-signature.html          Council / Faculty / Dean signature
└── plain-text-variants.txt         plain-text versions for all 3, for fallback
```

---

## What NOT to include in any signature

- Phone numbers (Aetherneum doesn't publish phone numbers)
- Office address (unless ceremonial — see Patron signature)
- Social media link grid (LinkedIn / X / Instagram / etc.) — the canonical CTA is a single URL
- "Sent from my iPhone" / "Excuse the brevity" / boilerplate apologies
- Quote-of-the-day variable text
- Calendar booking link
- Banner image / advertising callout
- Animated GIFs
- Pronouns line (institution-level signatures don't use them; the Patron may add them to his personal signature if he wishes)
- "Confidentiality notice" legal footer (unless required by counsel for a specific email type)
