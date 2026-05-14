#!/usr/bin/env python3
"""
update-activity.py — Live Activity feed generator for university.aetherneum.com.

Fetches the most recent public commits across aetherneum-network/* repositories,
maps each commit author to an alumnus profile (via email <first>.<last>@aetherneum.com),
and rewrites the ACTIVITY_FEED block of the served `index.html`.

Run by cron every ~10 minutes. Idempotent: if no new commit since last run, file is
left untouched (mtime preserved).

Auth: anonymous (60 req/h cap), sufficient for 10-minute cadence.

Failure policy: if the GitHub API is unreachable or the response is malformed, the
script logs the error and EXITS WITHOUT TOUCHING THE FILE. Never replaces real content
with a "site temporarily unavailable" placeholder.

Configuration via env vars (path-aware, deployment-agnostic):
  INDEX_HTML       — path to the index.html to rewrite (default: ./university-aetherneum-com/index.html)
  ACTIVITY_LOG     — path to the run log (default: ./activity.log)
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ORG = "aetherneum-network"
INDEX_HTML = Path(os.environ.get("INDEX_HTML", "./university-aetherneum-com/index.html"))
LOG_FILE = Path(os.environ.get("ACTIVITY_LOG", "./activity.log"))
MAX_ITEMS = 12
COMMITS_PER_REPO = 6
USER_AGENT = "aetherneum-university-activity/1.0"

# Map alumnus first.last → slug for linking to /alumni/<slug>.html
ALUMNI_SLUGS = {
    "marco.aurelius":     "marco-aurelius",
    "lucia.solari":       "lucia-solari",
    "riku.aetherian":     "riku-aetherian",
    "adrian.volta":       "adrian-volta",
    "davide.ferri":       "davide-ferri",
    "elena.tessera":      "elena-tessera",
    "yara.indrani":       "yara-indrani",
    "sofia.lume":         "sofia-lume",
    "noa.cifratti":       "noa-cifratti",
    "tariq.al-khwarizmi": "tariq-al-khwarizmi",
    "costanza.notari":    "costanza-notari",
}
DEAN_EMAIL = "aetherneum@aetherneum.com"  # Dean / org-level commits


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    sys.stderr.write(line)


def http_get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def relative_time(iso_ts):
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except Exception:
        return ""
    delta = datetime.now(timezone.utc) - dt
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def author_view(commit):
    """Resolve commit author identity. Returns (display_name, alumni_href_or_None)."""
    a = commit.get("commit", {}).get("author") or {}
    email = (a.get("email") or "").lower().strip()
    name = a.get("name") or "Aetherneum Network"
    if email == DEAN_EMAIL:
        return ("Aetherneum (Dean)", None)
    local = email.split("@", 1)[0] if "@" in email else ""
    slug = ALUMNI_SLUGS.get(local)
    if slug:
        return (name, f"/alumni/{slug}.html")
    # Unknown authors (legacy accounts, patron commits, etc.)
    return (name, None)


def fetch_public_repos():
    return http_get_json(f"https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public&sort=pushed&direction=desc")


def fetch_commits(repo_name):
    try:
        return http_get_json(f"https://api.github.com/repos/{ORG}/{repo_name}/commits?per_page={COMMITS_PER_REPO}")
    except urllib.error.HTTPError as e:
        log(f"commits fetch failed for {repo_name}: HTTP {e.code}")
        return []
    except Exception as e:
        log(f"commits fetch failed for {repo_name}: {e!r}")
        return []


def gather_activity():
    repos = fetch_public_repos()
    items = []
    for repo in repos:
        name = repo.get("name")
        if not name or repo.get("archived") or repo.get("disabled"):
            continue
        for c in fetch_commits(name):
            commit_dt = (c.get("commit") or {}).get("author", {}).get("date", "")
            display, href = author_view(c)
            items.append({
                "repo": name,
                "repo_url": repo.get("html_url"),
                "sha": (c.get("sha") or "")[:7],
                "url": c.get("html_url"),
                "message": (c.get("commit") or {}).get("message", "").split("\n", 1)[0],
                "author_name": display,
                "author_href": href,
                "date": commit_dt,
                "when": relative_time(commit_dt),
            })
    items.sort(key=lambda x: x["date"], reverse=True)
    return items[:MAX_ITEMS]


def render(items):
    if not items:
        return '<p style="opacity: 0.6; font-family: var(--mono); font-size: 0.9rem;">No activity available — retrying on next cron tick.</p>'

    rows = []
    for it in items:
        author_html = (
            f'<a href="{escape(it["author_href"])}" style="color: var(--cyan); text-decoration: none; font-weight: 500;">{escape(it["author_name"])}</a>'
            if it["author_href"]
            else f'<span style="color: var(--cyan); font-weight: 500;">{escape(it["author_name"])}</span>'
        )
        repo_html = (
            f'<a href="{escape(it["repo_url"] or "")}" style="color: var(--cyan-glow); text-decoration: none; font-family: var(--mono); font-size: 0.9em;">{escape(it["repo"])}</a>'
        )
        sha_html = (
            f'<a href="{escape(it["url"] or "")}" style="font-family: var(--mono); font-size: 0.75rem; opacity: 0.55; text-decoration: none;">{escape(it["sha"])} ↗</a>'
        )
        rows.append(
            '<li style="border-left: 2px solid var(--cyan); padding: 0.6rem 0 0.6rem 1rem; margin-bottom: 1rem; list-style: none;">'
            f'  <div style="font-family: var(--mono); font-size: 0.75rem; opacity: 0.55; letter-spacing: 0.1em; text-transform: uppercase;">{escape(it["when"])} · {repo_html}</div>'
            f'  <div style="margin-top: 0.35rem;">{author_html} <span style="opacity: 0.55;">committed</span></div>'
            f'  <div style="margin-top: 0.3rem; opacity: 0.88;">{escape(it["message"])}</div>'
            f'  <div style="margin-top: 0.25rem;">{sha_html}</div>'
            '</li>'
        )
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return (
        '<ul style="padding: 0; margin: 0;">' + "".join(rows) + "</ul>"
        f'<p style="font-family: var(--mono); font-size: 0.7rem; opacity: 0.4; margin-top: 1rem; text-align: right;">last refresh: {generated}</p>'
    )


def main():
    try:
        items = gather_activity()
    except Exception as e:
        log(f"FATAL gather_activity: {e!r}")
        return 2

    if not INDEX_HTML.exists():
        log(f"FATAL index missing: {INDEX_HTML}")
        return 3

    html = INDEX_HTML.read_text(encoding="utf-8")
    begin_marker = "<!-- ACTIVITY_FEED_BEGIN -->"
    end_marker = "<!-- ACTIVITY_FEED_END -->"
    if begin_marker not in html or end_marker not in html:
        log(f"FATAL markers not found in {INDEX_HTML}")
        return 4

    new_block = render(items)
    pattern = re.compile(
        re.escape(begin_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{begin_marker}\n{new_block}\n{end_marker}"
    new_html = pattern.sub(replacement, html, count=1)

    if new_html == html:
        log(f"no changes (idempotent run)")
        return 0

    # Atomic write
    tmp = INDEX_HTML.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(INDEX_HTML)
    log(f"updated with {len(items)} activity items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
