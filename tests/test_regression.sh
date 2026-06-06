#!/bin/bash
# test_regression.sh — Regression Test Suite
# Run after any change to main.md or any sub-skill file
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Regression Test Suite — ai-project-builder"
echo "========================================"

errors=0

# Ensure scripts are executable (Windows-compatible)
chmod +x "$SKILL_DIR/tests/test_scenario_1.sh" "$SKILL_DIR/tests/test_scenario_2.sh" "$SKILL_DIR/tests/test_scenario_3.sh" "$SKILL_DIR/tests/test_scenario_4.sh" "$SKILL_DIR/tests/test_scenario_5.sh" 2>/dev/null || true

# Run each scenario test
echo ""
for scenario in 1 2 3 4 5; do
  echo "--- Running Scenario $scenario ---"
  if bash "$SKILL_DIR/tests/test_scenario_$scenario.sh" "$SKILL_DIR"; then
    echo "Scenario $scenario: PASS"
  else
    echo "Scenario $scenario: FAIL"
    errors=$((errors+1))
  fi
  echo ""
done

# Regression checks
echo "--- Additional Regression Checks ---"

# R1: main.md has all 6 required sections
if grep -q "## Role & Persona" "$SKILL_DIR/skills/main.md" && \
   grep -q "## Workflow" "$SKILL_DIR/skills/main.md" && \
   grep -q "## Sub-Skills" "$SKILL_DIR/skills/main.md" && \
   grep -q "## Tools" "$SKILL_DIR/skills/main.md" && \
   grep -q "## Output Format" "$SKILL_DIR/skills/main.md" && \
   grep -q "## Quality Gates" "$SKILL_DIR/skills/main.md"; then
  echo "  OK: main.md has all 6 required sections"
else
  echo "  FAIL: main.md missing required sections"
  errors=$((errors+1))
fi

# R2: All sub-*.md files have valid frontmatter
echo "  Checking sub-skill frontmatter..."
for f in "$SKILL_DIR/skills"/sub-*.md; do
  if head -5 "$f" | grep -q "^name:" && head -5 "$f" | grep -q "^description:"; then
    true
  else
    echo "  FAIL: $(basename $f) missing frontmatter"
    errors=$((errors+1))
  fi
done

# R3: knowledge_updater.py dry-run validation
echo "  Checking knowledge_updater.py..."
if python "$SKILL_DIR/tools/knowledge_updater.py" --dry-run --validate 2>&1 | grep -q "integrity OK"; then
  echo "  OK: knowledge_updater.py validates"
else
  echo "  WARN: knowledge_updater.py validation warning"
fi

# R4: SECOND-KNOWLEDGE-BRAIN.md has all required sections
echo "  Checking SECOND-KNOWLEDGE-BRAIN.md sections..."
for section in "Core Concepts" "Key Research Papers" "State-of-the-Art Methods" "Authoritative Data Sources" "Analytical Frameworks" "Self-Update Protocol"; do
  if grep -q "$section" "$SKILL_DIR/SECOND-KNOWLEDGE-BRAIN.md"; then
    true
  else
    echo "  FAIL: SECOND-KNOWLEDGE-BRAIN.md missing '$section'"
    errors=$((errors+1))
  fi
done

# R5: validate_skill_files.py passes
echo "  Running validate_skill_files.py..."
if python "$SKILL_DIR/tools/validate_skill_files.py" 2>&1 | grep -q "ALL CHECKS PASSED"; then
  echo "  OK: validate_skill_files.py passes"
else
  echo "  FAIL: validate_skill_files.py reported errors"
  errors=$((errors+1))
fi

# Summary
echo ""
echo "========================================"
if [ "$errors" -eq 0 ]; then
  echo "REGRESSION RESULT: ALL CHECKS PASSED"
  exit 0
else
  echo "REGRESSION RESULT: $errors error(s) found"
  exit 1
fi
