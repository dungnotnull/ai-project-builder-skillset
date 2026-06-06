#!/usr/bin/env python3
"""Scenario 5: Sub-Skill Failure Mid-Flow (Error Recovery)."""
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Scenario 5: Sub-Skill Failure (Mid-Flow)")
print("=" * 50)

paper_researcher = SKILL_DIR / "skills" / "sub-paper-researcher.md"
content = paper_researcher.read_text(encoding="utf-8")

# 1. Check papers_below_minimum flag
print("\n[1] Checking papers_below_minimum flag...")
if "papers_below_minimum" in content:
    print("  OK: papers_below_minimum flag present")
else:
    print("  FAIL: papers_below_minimum flag missing")
    errors += 1

# 2. Check query broadening
print("\n[2] Checking query broadening...")
if "broaden" in content.lower() or "expand" in content.lower():
    print("  OK: Query broadening logic present")
else:
    print("  FAIL: Query broadening missing")
    errors += 1

# 3. Check harness does NOT abort on <5 papers
print("\n[3] Checking non-abort on low paper count...")
if "does NOT abort" in content or "papers_below_minimum" in content:
    print("  OK: Harness continues with < 5 papers")
else:
    print("  WARN: Non-abort behavior not explicit")

# 4. Check quality gate flags shortfall without blocking
print("\n[4] Checking quality gate flags shortfall...")
if "flag" in content.lower() and ("shortfall" in content.lower() or "minimum" in content.lower()):
    print("  OK: Shortfall flagging present")
else:
    print("  WARN: Shortfall flagging not explicit")

# 5. Check limited evidence documentation
print("\n[5] Checking limited evidence documentation...")
if "papers_below_minimum" in content or "evidence" in content.lower():
    print("  OK: Limited evidence documented")
else:
    print("  WARN: Limited-paper documentation not explicit")

print(f"\n{'='*50}")
if errors == 0:
    print("RESULT: ACCEPTED")
    sys.exit(0)
else:
    print(f"RESULT: REJECTED — {errors} error(s)")
    sys.exit(1)
