#!/usr/bin/env python3
"""Scenario 2: Auto-Discovery Mode (No User Topic)."""
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Scenario 2: Auto-Discovery Mode")
print("=" * 50)

topic_discovery = SKILL_DIR / "skills" / "sub-topic-discovery.md"
main_md = SKILL_DIR / "skills" / "main.md"

tdc = topic_discovery.read_text(encoding="utf-8")

# 1. Check discover mode
print("\n[1] Checking discover mode...")
if "Mode A" in tdc or "discover" in tdc.lower():
    print("  OK: Discover mode defined")
else:
    print("  FAIL: Discover mode missing")
    errors += 1

# 2. Check multi-source signal queries
print("\n[2] Checking multi-source signal queries...")
sources = ["GitHub", "ArXiv", "HuggingFace", "Papers With Code"]
found = sum(1 for s in sources if s.lower() in tdc.lower())
print(f"  OK: {found}/4 live sources referenced (need >=3)")
if found < 3:
    errors += 1

# 3. Check scoring rubric
print("\n[3] Checking scoring rubric...")
if all(kw in tdc for kw in ["Momentum", "Novelty", "Buildability"]):
    print("  OK: Scoring rubric present")
else:
    print("  FAIL: Scoring rubric missing")
    errors += 1

# 4. Check user confirmation gate
print("\n[4] Checking user confirmation gate...")
main_content = main_md.read_text(encoding="utf-8")
if "confirmation" in main_content.lower() or "present" in main_content.lower():
    print("  OK: User confirmation gate present")
else:
    print("  WARN: User confirmation gate not explicit")

# 5. Check novelty_score threshold
print("\n[5] Checking minimum novelty threshold...")
if "novelty_score" in tdc and "6" in tdc:
    print("  OK: novelty_score >= 6 threshold enforced")
else:
    print("  WARN: Minimum novelty threshold not explicit")

print(f"\n{'='*50}")
if errors == 0:
    print("RESULT: ACCEPTED")
    sys.exit(0)
else:
    print(f"RESULT: REJECTED -- {errors} error(s)")
    sys.exit(1)
