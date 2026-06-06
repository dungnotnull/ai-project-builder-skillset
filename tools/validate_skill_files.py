#!/usr/bin/env python3
"""
validate_skill_files.py — ai-project-builder

Validates all skill .md files for:
- File existence (8 required files)
- Frontmatter (name: and description: fields)
- Required sections presence
- Cross-reference consistency

Usage:
    python tools/validate_skill_files.py [--dir SKILL_DIR]
"""

import os
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "CLAUDE.md",
    "PROJECT-detail.md",
    "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "SECOND-KNOWLEDGE-BRAIN.md",
    "skills/main.md",
]

SUB_SKILL_GLOB = "skills/sub-*.md"

REQUIRED_MAIN_SECTIONS = [
    "## Role & Persona",
    "## Workflow",
    "## Sub-Skills",
    "## Tools",
    "## Output Format",
    "## Quality Gates",
]

REQUIRED_SUB_SECTIONS = [
    "## Role & Persona",
    "## Workflow",
    "## Tools",
    "## Quality Gate",
]

FRONTMATTER_RE = re.compile(r"^---\s*\nname:\s*(.+)\ndescription:\s*(.+)\n---", re.MULTILINE)


def validate_file_exists(path: Path) -> bool:
    if not path.exists():
        print(f"  FAIL: Missing required file: {path}")
        return False
    if path.stat().st_size == 0:
        print(f"  FAIL: File is empty: {path}")
        return False
    return True


def validate_frontmatter(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.search(content)
    if not match:
        print(f"  FAIL: Missing or invalid frontmatter (name: + description:) in {path}")
        return False
    name, desc = match.group(1).strip(), match.group(2).strip()
    if not name or not desc:
        print(f"  FAIL: Empty name or description in frontmatter of {path}")
        return False
    return True


def validate_sections(path: Path, required: list[str], file_type: str = "file") -> bool:
    content = path.read_text(encoding="utf-8")
    all_ok = True
    for section in required:
        if section not in content:
            print(f"  FAIL: Missing section '{section}' in {path}")
            all_ok = False
    return all_ok


def run(skill_dir: str = ".") -> int:
    base = Path(skill_dir).resolve()
    print(f"Validating skill package in: {base}")
    print()

    errors = 0

    # --- Step 1: Check required files ---
    print("[1] Required Files")
    for rel in REQUIRED_FILES:
        path = base / rel
        if not validate_file_exists(path):
            errors += 1
        else:
            print(f"  OK: {rel}")

    # Check sub-skill files (3–5 expected)
    sub_skills = sorted(base.glob(SUB_SKILL_GLOB))
    print(f"\n[2] Sub-Skill Files (found {len(sub_skills)})")
    if len(sub_skills) < 3:
        print(f"  FAIL: Expected at least 3 sub-skills, found {len(sub_skills)}")
        errors += 1
    else:
        for f in sub_skills:
            print(f"  OK: {f.relative_to(base)}")

    # --- Step 3: Validate frontmatter (skill .md files only) ---
    print(f"\n[3] Frontmatter Validation (skill .md files only)")
    skill_files = [base / "skills/main.md"] + list(sub_skills)
    for f in skill_files:
        if f.exists():
            if not validate_frontmatter(f):
                errors += 1
            else:
                print(f"  OK: frontmatter in {f.relative_to(base)}")

    # --- Step 4: Validate sections ---
    print(f"\n[4] Section Validation")
    main_md = base / "skills/main.md"
    if main_md.exists():
        if not validate_sections(main_md, REQUIRED_MAIN_SECTIONS, "main.md"):
            errors += 1
        else:
            print(f"  OK: main.md has all {len(REQUIRED_MAIN_SECTIONS)} required sections")

    for f in sub_skills:
        if not validate_sections(f, REQUIRED_SUB_SECTIONS, f.name):
            errors += 1
        else:
            print(f"  OK: {f.relative_to(base)} has all {len(REQUIRED_SUB_SECTIONS)} required sections")

    # --- Step 5: Check CLAUDE.md references ---
    print(f"\n[5] Cross-Reference Check")
    claude_md = base / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        for ref in ["PROJECT-detail.md", "PROJECT-DEVELOPMENT-PHASE-TRACKING.md", "SECOND-KNOWLEDGE-BRAIN.md"]:
            if ref in content:
                print(f"  OK: CLAUDE.md references {ref}")
            else:
                print(f"  WARN: CLAUDE.md missing reference to {ref}")

    # --- Summary ---
    print(f"\n{'='*50}")
    if errors == 0:
        print("RESULT: ALL CHECKS PASSED")
        return 0
    else:
        print(f"RESULT: {errors} error(s) found")
        return 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate Claude skill package files")
    parser.add_argument("--dir", default=".", help="Skill package root directory")
    args = parser.parse_args()
    sys.exit(run(skill_dir=args.dir))
