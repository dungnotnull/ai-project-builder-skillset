#!/bin/bash
# test_scenario_3.sh — Topic With Very Few GitHub Repos (Edge Case)
# Validates graceful degradation when GitHub search returns < 5 repos
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Scenario 3: Few GitHub Repos (Edge Case)"
echo "========================================"

errors=0

# 1. Check early_stage_flag mechanism exists
echo "[1] Checking early_stage_flag..."
if grep -q "early_stage" "$SKILL_DIR/skills/sub-repo-researcher.md" 2>/dev/null; then
  echo "  OK: early_stage_flag present"
else
  echo "  FAIL: early_stage_flag missing from sub-repo-researcher.md"
  errors=$((errors+1))
fi

# 2. Check broadening search behavior
echo "[2] Checking search broadening logic..."
if grep -q "broaden\|expand search\|related terms" "$SKILL_DIR/skills/sub-repo-researcher.md" 2>/dev/null; then
  echo "  OK: Search broadening logic present"
else
  echo "  FAIL: Search broadening missing"
  errors=$((errors+1))
fi

# 3. Check harness does NOT abort on <5 repos
echo "[3] Checking < 5 repo handling..."
if grep -q "error.*no_repos\|early_stage.*flag.*true" "$SKILL_DIR/skills/sub-repo-researcher.md" 2>/dev/null; then
  echo "  OK: Harness continues gracefully on low repo count"
else
  echo "  WARN: Graceful degradation on low repo count not explicit"
fi

# 4. Check Coverage Gap detection path
echo "[4] Checking gap analyzer handles sparse repos..."
if grep -q "Coverage Gap\|reduced_matrix" "$SKILL_DIR/skills/sub-gap-analyzer.md" 2>/dev/null; then
  echo "  OK: Coverage Gap + reduced_matrix handling present"
else
  echo "  WARN: Sparse-repo handling not explicit in gap analyzer"
fi

# 5. Check forking from ground-up path
echo "[5] Checking build-from-scratch path..."
if grep -q "fork_candidates.*\[\].*acceptable\|build from scratch" "$SKILL_DIR/skills/sub-repo-researcher.md" 2>/dev/null; then
  echo "  OK: Empty fork_candidates handled"
else
  echo "  WARN: Empty fork_candidates handling not explicit"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "RESULT: ACCEPTED"
  exit 0
else
  echo "RESULT: REJECTED — $errors error(s) found"
  exit 1
fi
