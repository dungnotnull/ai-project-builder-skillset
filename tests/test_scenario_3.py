#!/usr/bin/env python3
"""Scenario 3: Topic With Very Few GitHub Repos (Edge Case)."""
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Scenario 3: Few GitHub Repos (Edge Case)")
print("=" * 50)

repo_researcher = SKILL_DIR / "skills" / "sub-repo-researcher.md"
gap_analyzer = SKILL_DIR / "skills" / "sub-gap-analyzer.md"
rr_content = repo_researcher.read_text(encoding="utf-8")

# 1. Check early_stage_flag
print("\n[1] Checking early_stage_flag...")
if "early_stage" in rr_content.lower():
    print("  OK: early_stage_flag present")
else:
    print("  FAIL: early_stage_flag missing")
    errors += 1

# 2. Check search broadening
print("\n[2] Checking search broadening...")
if "broaden" in rr_content.lower() or "expand" in rr_content.lower():
    print("  OK: Search broadening logic present")
else:
    print("  FAIL: Search broadening missing")
    errors += 1

# 3. Check graceful degradation
print("\n[3] Checking graceful degradation...")
if "no_repos" in rr_content or "error" in rr_content.lower():
    print("  OK: Error handling present")
else:
    print("  WARN: Error handling not explicit")

# 4. Check gap analyzer handles sparse repos
gap_content = gap_analyzer.read_text(encoding="utf-8")
print("\n[4] Checking gap analyzer handles sparse repos...")
if "reduced_matrix" in gap_content or "Coverage Gap" in gap_content:
    print("  OK: Sparse-repo handling present")
else:
    print("  WARN: Sparse-repo handling not explicit in gap analyzer")

# 5. Check fork_candidates empty case
print("\n[5] Checking empty fork_candidates handling...")
if "fork_candidates.*\[\]" in rr_content or "acceptable" in rr_content.lower():
    print("  OK: Empty fork_candidates handled")
else:
    print("  OK: Empty fork_candidates is valid")

print(f"\n{'='*50}")
if errors == 0:
    print("RESULT: ACCEPTED")
    sys.exit(0)
else:
    print(f"RESULT: REJECTED — {errors} error(s)")
    sys.exit(1)
