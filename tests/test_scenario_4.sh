#!/bin/bash
# test_scenario_4.sh — Loop-Breaker Fires During Phase Execution
# Validates that the loop-breaker mechanism fires after exactly 5 failures
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Scenario 4: Loop-Breaker Test"
echo "========================================"

errors=0

# 1. Check loop-breaker is defined in sub-phase-executor
echo "[1] Checking loop-breaker definition..."
if grep -q "fail_count >= 5\|Loop-breaker\|loop-breaker" "$SKILL_DIR/skills/sub-phase-executor.md" 2>/dev/null; then
  echo "  OK: Loop-breaker mechanism present"
else
  echo "  FAIL: Loop-breaker missing from sub-phase-executor.md"
  errors=$((errors+1))
fi

# 2. Check max cycle count is exactly 5
echo "[2] Checking max cycle count..."
if grep -q "5 failed cycles\|fail_count.*5\|exactly 5" "$SKILL_DIR/skills/sub-phase-executor.md" 2>/dev/null; then
  echo "  OK: Loop-breaker fires at exactly 5 cycles"
else
  echo "  FAIL: Loop-breaker cycle count not 5"
  errors=$((errors+1))
fi

# 3. Check blocker-report.md template exists
echo "[3] Checking blocker report template..."
if grep -q "blocker-report.md\|Blocker Report" "$SKILL_DIR/skills/sub-phase-executor.md" 2>/dev/null; then
  echo "  OK: Blocker report template present"
else
  echo "  FAIL: Blocker report template missing"
  errors=$((errors+1))
fi

# 4. Check blocker report required fields
echo "[4] Checking blocker report required sections..."
report_fields=("Root Cause" "All Errors" "Attempted Fixes" "Recommended Resolution")
for field in "${report_fields[@]}"; do
  if grep -q "$field" "$SKILL_DIR/skills/sub-phase-executor.md" 2>/dev/null; then
    echo "  OK: Blocker report includes '$field'"
  else
    echo "  FAIL: Blocker report missing '$field'"
    errors=$((errors+1))
  fi
done

# 5. Check harness stops on BLOCKED
echo "[5] Checking BLOCKED stops pipeline..."
if grep -q "BLOCKED\|STOP.*loop\|stop entire pipeline" "$SKILL_DIR/skills/sub-phase-executor.md" 2>/dev/null; then
  echo "  OK: Pipeline stops on BLOCKED result"
else
  echo "  WARN: Stop-on-BLOCKED behavior not explicit"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "RESULT: ACCEPTED"
  exit 0
else
  echo "RESULT: REJECTED — $errors error(s) found"
  exit 1
fi
