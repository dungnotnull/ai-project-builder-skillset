#!/usr/bin/env python3
"""Scenario 1: User Supplies a Specific Topic (Happy Path)."""
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Scenario 1: User-Supplied Topic (Happy Path)")
print("=" * 50)

REQUIRED_FILES = [
    "CLAUDE.md",
    "PROJECT-detail.md",
    "PROJECT-DEVELOPMENT-PHASE-TRACKING.md",
    "SECOND-KNOWLEDGE-BRAIN.md",
    "skills/main.md",
]

# 1. Check skill files exist
print("\n[1] Checking skill package files...")
for rel in REQUIRED_FILES:
    p = SKILL_DIR / rel
    if p.exists():
        print(f"  OK: {rel} exists")
    else:
        print(f"  FAIL: Missing {rel}")
        errors += 1

# 2. Check sub-skill files
print("\n[2] Checking sub-skill files...")
subs = sorted((SKILL_DIR / "skills").glob("sub-*.md"))
print(f"  OK: {len(subs)} sub-skills found (need >=3)")
if len(subs) < 3:
    errors += 1

# 3. Validate frontmatter
print("\n[3] Validating frontmatter...")
for f in [SKILL_DIR / "skills/main.md"] + subs:
    content = f.read_text(encoding="utf-8")
    frontmatter_ok = content.startswith("---") and "name:" in content.split("---")[1] if "---" in content else False
    if frontmatter_ok:
        print(f"  OK: frontmatter in {f.name}")
    else:
        print(f"  FAIL: frontmatter missing in {f.name}")
        errors += 1

# 4. Check main.md sections
print("\n[4] Checking main.md sections...")
main_content = (SKILL_DIR / "skills/main.md").read_text(encoding="utf-8")
required_sections = ["## Role & Persona", "## Workflow", "## Sub-Skills", "## Tools", "## Output Format", "## Quality Gates"]
for section in required_sections:
    if section in main_content:
        print(f"  OK: Section '{section}' present")
    else:
        print(f"  FAIL: Section '{section}' missing")
        errors += 1

# 5. Check quality gate defined
print("\n[5] Checking quality gates defined...")
has_quality_gate = any("Quality Gate" in (SKILL_DIR / s).read_text(encoding="utf-8") for s in ["skills/main.md"] + [s.name for s in subs])
if has_quality_gate:
    print("  OK: Quality gates defined in skill files")

print(f"\n{'='*50}")
if errors == 0:
    print("RESULT: ACCEPTED")
    sys.exit(0)
else:
    print(f"RESULT: REJECTED -- {errors} error(s)")
    sys.exit(1)
