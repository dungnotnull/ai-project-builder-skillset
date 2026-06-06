#!/bin/bash
# test_scenario_1.sh — User Supplies a Specific Topic (Happy Path)
# Validates the full pipeline for "multimodal RAG with PDF, images, and tables"
set -e

SKILL_DIR="${1:-.}"
echo "========================================"
echo "Scenario 1: User-Supplied Topic (Happy Path)"
echo "========================================"

errors=0

# 1. Check skill files exist
echo "[1] Checking skill package files..."
for f in "$SKILL_DIR/CLAUDE.md" "$SKILL_DIR/PROJECT-detail.md" "$SKILL_DIR/PROJECT-DEVELOPMENT-PHASE-TRACKING.md" "$SKILL_DIR/SECOND-KNOWLEDGE-BRAIN.md" "$SKILL_DIR/skills/main.md"; do
  if [ ! -f "$f" ]; then
    echo "  FAIL: Missing $f"
    errors=$((errors+1))
  else
    echo "  OK: $f exists"
  fi
done

# 2. Check sub-skill files
echo "[2] Checking sub-skill files..."
count=0
for f in "$SKILL_DIR/skills"/sub-*.md; do
  if [ -f "$f" ]; then
    count=$((count+1))
  fi
done
if [ "$count" -lt 3 ]; then
  echo "  FAIL: Expected ≥3 sub-skills, found $count"
  errors=$((errors+1))
else
  echo "  OK: $count sub-skills found"
fi

# 3. Validate frontmatter on all skill .md files
echo "[3] Validating frontmatter..."
for f in "$SKILL_DIR/skills/main.md" "$SKILL_DIR/skills"/sub-*.md; do
  if [ -f "$f" ]; then
    if head -5 "$f" | grep -q "^name:" && head -5 "$f" | grep -q "^description:"; then
      echo "  OK: frontmatter in $(basename $f)"
    else
      echo "  FAIL: frontmatter missing in $(basename $f)"
      errors=$((errors+1))
    fi
  fi
done

# 4. Check main.md has all 6 required sections
echo "[4] Checking main.md sections..."
for section in "## Role & Persona" "## Workflow" "## Sub-Skills" "## Tools" "## Output Format" "## Quality Gates"; do
  if grep -q "$section" "$SKILL_DIR/skills/main.md" 2>/dev/null; then
    echo "  OK: Section '$section' present"
  else
    echo "  FAIL: Section '$section' missing"
    errors=$((errors+1))
  fi
done

# 5. Check report.md placeholder (for generated reports)
echo "[5] Checking quality gates defined..."
if grep -q "report.md" "$SKILL_DIR/skills/main.md" 2>/dev/null; then
  echo "  OK: report.md referenced in harness"
else
  echo "  WARN: report.md not referenced in main.md"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "RESULT: ACCEPTED — All acceptance criteria met"
  exit 0
else
  echo "RESULT: REJECTED — $errors error(s) found"
  exit 1
fi
