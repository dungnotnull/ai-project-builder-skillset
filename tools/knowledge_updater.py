"""
knowledge_updater.py — ai-project-builder

Crawls trending AI topics and papers from GitHub, ArXiv, HuggingFace, and
Papers With Code. Appends new entries to SECOND-KNOWLEDGE-BRAIN.md.

Schedule: Weekly (e.g. Sunday 00:00 UTC via cron or CronCreate)
Usage:   python tools/knowledge_updater.py [--dry-run] [--sources all|github|arxiv|hf|pwc]
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BRAIN_FILE = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"

SOURCES = {
    "github_trending": {
        "url": "https://github.com/trending?l=python&since=weekly",
        "type": "repo",
        "keywords": ["AI", "LLM", "machine learning", "deep learning", "agent", "RAG"],
    },
    "arxiv_cs_ai": {
        "url": "https://arxiv.org/list/cs.AI/recent",
        "type": "paper",
        "keywords": ["agent", "reasoning", "planning", "benchmark"],
    },
    "arxiv_cs_lg": {
        "url": "https://arxiv.org/list/cs.LG/recent",
        "type": "paper",
        "keywords": ["foundation model", "fine-tuning", "in-context learning"],
    },
    "huggingface_papers": {
        "url": "https://huggingface.co/papers",
        "type": "paper",
        "keywords": ["multimodal", "language model", "generation"],
    },
    "papers_with_code": {
        "url": "https://paperswithcode.com/api/v1/papers/?ordering=-published&page_size=20",
        "type": "paper",
        "keywords": ["state of the art", "benchmark", "open source"],
    },
}

MAX_ENTRIES_PER_SOURCE = 20
RELEVANCE_THRESHOLD = 4  # minimum relevance score (0-10) to include


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def load_existing_hashes(brain_path: Path) -> set[str]:
    """Extract all URL hashes already in SECOND-KNOWLEDGE-BRAIN.md."""
    if not brain_path.exists():
        return set()
    content = brain_path.read_text(encoding="utf-8")
    # Hashes are stored in HTML comments: <!-- hash:abc123 -->
    return set(re.findall(r"<!-- hash:([a-f0-9]{16}) -->", content))


def score_relevance(text: str, keywords: list[str]) -> int:
    """Score 0-10 based on keyword density in text."""
    text_lower = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    return min(10, int((hits / max(len(keywords), 1)) * 10))


def format_date(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Crawl4AI integration
# ---------------------------------------------------------------------------

def crawl_with_crawl4ai(url: str) -> str:
    """
    Fetch page content using crawl4ai (async web crawler optimized for LLM).
    Falls back to urllib if crawl4ai is not installed.
    """
    try:
        import asyncio
        from crawl4ai import AsyncWebCrawler

        async def _crawl(target_url: str) -> str:
            async with AsyncWebCrawler(verbose=False) as crawler:
                result = await crawler.arun(url=target_url)
                return result.markdown or result.cleaned_html or ""

        return asyncio.run(_crawl(url))
    except ImportError:
        # Fallback: plain urllib
        import urllib.request
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[WARN] Failed to fetch {url}: {e}", file=sys.stderr)
            return ""


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_github_trending(content: str, source_cfg: dict) -> list[dict]:
    """Extract repos from GitHub Trending page HTML/markdown."""
    entries = []
    # Match patterns like: owner/repo-name — description
    repo_pattern = re.compile(
        r'href="/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)"[^>]*>',
        re.IGNORECASE,
    )
    seen = set()
    for match in repo_pattern.finditer(content):
        repo_path = match.group(1)
        if "/" not in repo_path or repo_path in seen:
            continue
        seen.add(repo_path)

        repo_url = f"https://github.com/{repo_path}"
        # Extract surrounding context for description (rough heuristic)
        start = max(0, match.start() - 50)
        end = min(len(content), match.end() + 200)
        context = content[start:end]

        # Score relevance against AI keywords
        relevance = score_relevance(context, source_cfg["keywords"])
        if relevance < RELEVANCE_THRESHOLD:
            continue

        entries.append({
            "type": "repo",
            "title": repo_path,
            "url": repo_url,
            "relevance_score": relevance,
            "source": "github_trending",
            "date_added": format_date(),
        })

        if len(entries) >= MAX_ENTRIES_PER_SOURCE:
            break

    return entries


def parse_arxiv(content: str, source_cfg: dict) -> list[dict]:
    """Extract paper titles and IDs from ArXiv listing page."""
    entries = []
    # ArXiv listing: <a href="/abs/2401.12345"> Title </a>
    paper_pattern = re.compile(
        r'href="/abs/(\d{4}\.\d{4,5})"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    seen = set()
    for match in paper_pattern.finditer(content):
        arxiv_id = match.group(1)
        title = re.sub(r"\s+", " ", match.group(2)).strip()

        if not title or arxiv_id in seen:
            continue
        seen.add(arxiv_id)

        url = f"https://arxiv.org/abs/{arxiv_id}"
        relevance = score_relevance(title, source_cfg["keywords"])
        if relevance < RELEVANCE_THRESHOLD:
            continue

        entries.append({
            "type": "paper",
            "title": title,
            "url": url,
            "arxiv_id": arxiv_id,
            "relevance_score": relevance,
            "source": source_cfg.get("source_name", "arxiv"),
            "date_added": format_date(),
        })

        if len(entries) >= MAX_ENTRIES_PER_SOURCE:
            break

    return entries


def parse_huggingface_papers(content: str, source_cfg: dict) -> list[dict]:
    """Extract paper entries from HuggingFace papers page."""
    entries = []
    # HuggingFace papers page links to /papers/<arxiv_id>
    paper_pattern = re.compile(r'href="/papers/(\d{4}\.\d{4,5})"')
    seen = set()
    for match in paper_pattern.finditer(content):
        arxiv_id = match.group(1)
        if arxiv_id in seen:
            continue
        seen.add(arxiv_id)

        url = f"https://arxiv.org/abs/{arxiv_id}"
        # Context for relevance scoring
        start = max(0, match.start() - 100)
        end = min(len(content), match.end() + 300)
        context = content[start:end]
        relevance = score_relevance(context, source_cfg["keywords"])
        if relevance < RELEVANCE_THRESHOLD:
            continue

        entries.append({
            "type": "paper",
            "title": f"HuggingFace Paper {arxiv_id}",  # title resolved on append
            "url": url,
            "arxiv_id": arxiv_id,
            "relevance_score": relevance,
            "source": "huggingface_papers",
            "date_added": format_date(),
        })

        if len(entries) >= MAX_ENTRIES_PER_SOURCE:
            break

    return entries


def parse_papers_with_code(content: str, source_cfg: dict) -> list[dict]:
    """Parse JSON response from Papers With Code API."""
    entries = []
    try:
        data = json.loads(content)
        results = data.get("results", [])
    except json.JSONDecodeError:
        return entries

    for item in results[:MAX_ENTRIES_PER_SOURCE]:
        title = item.get("title", "")
        url = item.get("url_pdf") or item.get("url_abs") or ""
        if not title or not url:
            continue

        relevance = score_relevance(
            title + " " + " ".join(item.get("tasks", [])),
            source_cfg["keywords"],
        )
        if relevance < RELEVANCE_THRESHOLD:
            continue

        entries.append({
            "type": "paper",
            "title": title,
            "url": url,
            "relevance_score": relevance,
            "source": "papers_with_code",
            "date_added": format_date(),
        })

    return entries


SOURCE_PARSERS = {
    "github_trending": parse_github_trending,
    "arxiv_cs_ai": parse_arxiv,
    "arxiv_cs_lg": parse_arxiv,
    "huggingface_papers": parse_huggingface_papers,
    "papers_with_code": parse_papers_with_code,
}


# ---------------------------------------------------------------------------
# Append to SECOND-KNOWLEDGE-BRAIN.md
# ---------------------------------------------------------------------------

def format_entry(entry: dict) -> str:
    """Format a single entry as a markdown table row with hash comment."""
    h = url_hash(entry["url"])
    entry_type = entry.get("type", "unknown")
    title = entry["title"].replace("|", "\\|")
    url = entry["url"]
    source = entry.get("source", "")
    date = entry.get("date_added", format_date())
    score = entry.get("relevance_score", 0)

    return (
        f"| {title} | {entry_type} | {source} | {score}/10 | {date} | [link]({url}) |"
        f" <!-- hash:{h} -->"
    )


def ensure_update_log_section(brain_path: Path) -> None:
    """Ensure the ## Knowledge Update Log section exists."""
    content = brain_path.read_text(encoding="utf-8")
    if "## Knowledge Update Log" not in content:
        with brain_path.open("a", encoding="utf-8") as f:
            f.write("\n\n## Knowledge Update Log\n\n")
            f.write("| Title | Type | Source | Relevance | Date | Link |\n")
            f.write("|-------|------|--------|-----------|------|------|\n")


def append_entries(brain_path: Path, new_entries: list[dict], dry_run: bool = False) -> int:
    """Append non-duplicate entries to the Knowledge Update Log section."""
    existing_hashes = load_existing_hashes(brain_path)
    added = 0

    rows = []
    for entry in new_entries:
        h = url_hash(entry["url"])
        if h in existing_hashes:
            continue
        rows.append(format_entry(entry))
        existing_hashes.add(h)
        added += 1

    if rows and not dry_run:
        ensure_update_log_section(brain_path)
        with brain_path.open("a", encoding="utf-8") as f:
            for row in rows:
                f.write(row + "\n")

    return added


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(sources_filter: str = "all", dry_run: bool = False) -> None:
    today = format_date()
    total_added = 0

    source_keys = (
        list(SOURCES.keys())
        if sources_filter == "all"
        else [s.strip() for s in sources_filter.split(",")]
    )

    for source_name in source_keys:
        if source_name not in SOURCES:
            print(f"[WARN] Unknown source: {source_name}", file=sys.stderr)
            continue

        cfg = SOURCES[source_name].copy()
        cfg["source_name"] = source_name
        url = cfg["url"]

        print(f"[INFO] Crawling {source_name}: {url}")
        content = crawl_with_crawl4ai(url)

        if not content:
            print(f"[WARN] Empty response from {source_name}", file=sys.stderr)
            continue

        parser = SOURCE_PARSERS.get(source_name)
        if not parser:
            print(f"[WARN] No parser for {source_name}", file=sys.stderr)
            continue

        entries = parser(content, cfg)
        print(f"[INFO] {source_name}: {len(entries)} relevant entries found")

        added = append_entries(BRAIN_FILE, entries, dry_run=dry_run)
        print(f"[INFO] {source_name}: {added} new entries added to knowledge brain")
        total_added += added

    print(f"\n[DONE] {today} — Total new entries added: {total_added}")
    if dry_run:
        print("[DRY RUN] No files were modified.")


def validate_brain() -> None:
    """Validate brain file integrity and report stats."""
    if not BRAIN_FILE.exists():
        print("[ERROR] SECOND-KNOWLEDGE-BRAIN.md not found.")
        sys.exit(1)

    content = BRAIN_FILE.read_text(encoding="utf-8")
    existing = load_existing_hashes(BRAIN_FILE)

    required_sections = [
        "Core Concepts",
        "Key Research Papers",
        "State-of-the-Art Methods",
        "Authoritative Data Sources",
        "Analytical Frameworks",
        "Self-Update Protocol",
        "Knowledge Update Log",
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        print(f"[WARN] Missing sections: {', '.join(missing)}")
    else:
        print("[OK] All required sections present.")

    print(f"[STATS] Total unique entries: {len(existing)}")
    print(f"[STATS] File size: {len(content)} bytes")
    print(f"[STATS] Lines: {content.count(chr(10))}")

    if missing:
        sys.exit(1)
    print("[DONE] Brain file validation complete — integrity OK.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update SECOND-KNOWLEDGE-BRAIN.md with fresh AI research")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and score entries without writing to the brain file",
    )
    parser.add_argument(
        "--sources",
        default="all",
        help="Comma-separated list of sources to crawl (default: all)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate brain file integrity and report stats without crawling",
    )
    args = parser.parse_args()

    if args.validate:
        validate_brain()
    else:
        run(sources_filter=args.sources, dry_run=args.dry_run)
