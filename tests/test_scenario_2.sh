#!/bin/bash
# test_scenario_2.sh — Auto-Discovery Mode (No User Topic)
# Validates that the harness can operate with no pre-supplied topic
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Scenario 2: Auto-Discovery Mode"
echo "========================================"

errors=0

# 1. Check sub-topic-discovery has discover mode defined
echo "[1] Checking discover mode in sub-topic-discovery..."
if grep -q "Mode A: Discover\|mode:discover\|mode=discover" "$SKILL_DIR/skills/sub-topic-discovery.md" 2>/dev/null; then
  echo "  OK: Discover mode defined"
else
  echo "  FAIL: Discover mode missing from sub-topic-discovery.md"
  errors=$((errors+1))
fi

# 2. Check that auto-discovery queries multiple sources
echo "[2] Checking multi-source signal queries..."
sources=0
for src in "GitHub" "ArXiv" "HuggingFace" "Papers With Code"; do
  if grep -qi "$src" "$SKILL_DIR/skills/sub-topic-discovery.md" 2>/dev/null; then
    sources=$((sources+1))
  fi
done
if [ "$sources" -ge 3 ]; then
  echo "  OK: $sources/4 live sources referenced"
else
  echo "  FAIL: Only $sources/4 live sources — need ≥3"
  errors=$((errors+1))
fi

# 3. Check scoring rubric exists
echo "[3] Checking scoring rubric..."
if grep -q "Momentum\|Novelty\|Buildability" "$SKILL_DIR/skills/sub-topic-discovery.md" 2>/dev/null; then
  echo "  OK: Scoring rubric (Momentum/Novelty/Buildability) present"
else
  echo "  FAIL: Scoring rubric missing"
  errors=$((errors+1))
fi

# 4. Check user confirmation gate exists
echo "[4] Checking user confirmation gate..."
if grep -qi "user confirmation\|pause for confirmation\|present to user" "$SKILL_DIR/skills/main.md" 2>/dev/null; then
  echo "  OK: User confirmation gate present"
else
  echo "  WARN: User confirmation gate not explicit in harness"
fi

# 5. Check novelty_score minimum threshold
echo "[5] Checking minimum novelty threshold..."
if grep -q "novelty_score.*≥ 6\|minimum.*6\|score.*≥ 6" "$SKILL_DIR/skills/sub-topic-discovery.md" 2>/dev/null; then
  echo "  OK: novelty_score ≥ 6 threshold enforced"
else
  echo "  WARN: Minimum novelty threshold not explicit"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "RESULT: ACCEPTED"
  exit 0
else
  echo "RESULT: REJECTED — $errors error(s) found"
  exit 1
fi
