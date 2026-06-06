#!/usr/bin/env python3
"""Scenario 4: Loop-Breaker Fires During Phase Execution."""
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Scenario 4: Loop-Breaker Test")
print("=" * 50)

executor = SKILL_DIR / "skills" / "sub-phase-executor.md"
content = executor.read_text(encoding="utf-8")

# 1. Check loop-breaker defined
print("\n[1] Checking loop-breaker definition...")
if "loop-breaker" in content.lower() or "Loop" in content:
    print("  OK: Loop-breaker mechanism present")
else:
    print("  FAIL: Loop-breaker missing")
    errors += 1

# 2. Check max cycle count is exactly 5
print("\n[2] Checking max cycle count (exactly 5)...")
import re
cycle_matches = re.findall(r'fail_count\s*>=\s*5|5\s+failed\s+cycles|fail_count\s*<\s*5', content, re.IGNORECASE)
if cycle_matches:
    print("  OK: Loop-breaker fires at exactly 5 cycles")
else:
    print("  FAIL: Loop-breaker cycle count not exactly 5")
    errors += 1

# 3. Check blocker-report.md template
print("\n[3] Checking blocker report template...")
if "blocker-report.md" in content or "Blocker Report" in content:
    print("  OK: Blocker report template present")
else:
    print("  FAIL: Blocker report template missing")
    errors += 1

# 4. Check blocker report required fields
print("\n[4] Checking blocker report fields...")
required_fields = ["Root Cause", "All Errors", "Attempted Fixes", "Recommended Resolution"]
for field in required_fields:
    if field in content:
        print(f"  OK: Blocker report includes '{field}'")
    else:
        print(f"  FAIL: Blocker report missing '{field}'")
        errors += 1

# 5. Check BLOCKED stops pipeline
print("\n[5] Checking BLOCKED stops pipeline...")
if "BLOCKED" in content or "STOP" in content:
    print("  OK: Pipeline stops on BLOCKED result")
else:
    print("  WARN: Stop-on-BLOCKED not explicit")

print(f"\n{'='*50}")
if errors == 0:
    print("RESULT: ACCEPTED")
    sys.exit(0)
else:
    print(f"RESULT: REJECTED — {errors} error(s)")
    sys.exit(1)
