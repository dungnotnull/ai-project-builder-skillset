#!/bin/bash
# test_scenario_5.sh — Sub-Skill Failure Mid-Flow (Error Recovery)
# Validates that paper researcher handles < 5 papers gracefully
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Scenario 5: Sub-Skill Failure (Mid-Flow)"
echo "========================================"

errors=0

# 1. Check papers_below_minimum flag exists
echo "[1] Checking papers_below_minimum flag..."
if grep -q "papers_below_minimum" "$SKILL_DIR/skills/sub-paper-researcher.md" 2>/dev/null; then
  echo "  OK: papers_below_minimum flag present"
else
  echo "  FAIL: papers_below_minimum flag missing"
  errors=$((errors+1))
fi

# 2. Check query broadening
echo "[2] Checking query broadening on low results..."
if grep -q "broaden\|expand.*search\|remove.*topic.*specific" "$SKILL_DIR/skills/sub-paper-researcher.md" 2>/dev/null; then
  echo "  OK: Query broadening logic present"
else
  echo "  FAIL: Query broadening missing"
  errors=$((errors+1))
fi

# 3. Check harness does NOT abort on <5 papers
echo "[3] Checking non-abort on low paper count..."
if grep -q "does NOT abort\|below minimum\|papers_below_minimum" "$SKILL_DIR/skills/sub-paper-researcher.md" 2>/dev/null; then
  echo "  OK: Harness continues with < 5 papers"
else
  echo "  WARN: Non-abort behavior not explicit"
fi

# 4. Check quality gate flags shortfall but continues
echo "[4] Checking quality gate flags shortfall..."
if grep -q "flag.*shortfall\|does NOT block\|flags.*shortfall" "$SKILL_DIR/skills/sub-paper-researcher.md" 2>/dev/null; then
  echo "  OK: Quality gate flags shortfall without blocking"
else
  echo "  WARN: Shortfall-flag-no-block pattern not explicit"
fi

# 5. Check report.md notes limited evidence
echo "[5] Checking limited evidence documentation..."
if grep -q "Papers Below Minimum\|papers_below_minimum\|limited paper.*evidence" "$SKILL_DIR/skills/sub-paper-researcher.md" 2>/dev/null; then
  echo "  OK: Limited evidence documented"
else
  echo "  WARN: Limited-paper documentation not explicit"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "RESULT: ACCEPTED"
  exit 0
else
  echo "RESULT: REJECTED — $errors error(s) found"
  exit 1
fi
