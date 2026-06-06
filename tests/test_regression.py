#!/usr/bin/env python3
"""Regression Test Suite for ai-project-builder.

Run after any change to main.md or any sub-skill file.
Usage: python tests/test_regression.py [skill_dir]
"""
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors = 0

print("=" * 50)
print("Regression Test Suite — ai-project-builder")
print("=" * 50)

# Run each scenario test
scenarios = [
    ("Scenario 1: User-Supplied Topic", "test_scenario_1.py"),
    ("Scenario 2: Auto-Discovery Mode", "test_scenario_2.py"),
    ("Scenario 3: Few GitHub Repos (Edge Case)", "test_scenario_3.py"),
    ("Scenario 4: Loop-Breaker Test", "test_scenario_4.py"),
    ("Scenario 5: Sub-Skill Failure (Mid-Flow)", "test_scenario_5.py"),
]

for name, script in scenarios:
    print(f"\n--- Running {name} ---")
    script_path = SKILL_DIR / "tests" / script
    result = subprocess.run(
        [sys.executable, str(script_path), str(SKILL_DIR)],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"FAIL: {name}")
        errors += 1
    else:
        print(f"PASS: {name}")

# --- Additional Regression Checks ---
print("\n--- Additional Regression Checks ---")

# R1: main.md has all 6 required sections
print("  Checking main.md sections...")
main_content = (SKILL_DIR / "skills/main.md").read_text(encoding="utf-8")
required_sections = ["## Role & Persona", "## Workflow", "## Sub-Skills", "## Tools", "## Output Format", "## Quality Gates"]
all_sections = all(s in main_content for s in required_sections)
print(f"  {'OK' if all_sections else 'FAIL'}: main.md has all 6 required sections")
if not all_sections:
    errors += 1

# R2: All sub-*.md files have valid frontmatter
print("  Checking sub-skill frontmatter...")
subs = sorted((SKILL_DIR / "skills").glob("sub-*.md"))
frontmatter_ok = True
for f in subs:
    content = f.read_text(encoding="utf-8")
    has_fm = content.startswith("---") and "name:" in content.split("---")[1] if "---" in content else False
    if not has_fm:
        print(f"  FAIL: {f.name} missing frontmatter")
        frontmatter_ok = False
        errors += 1
if frontmatter_ok:
    print("  OK: All sub-skill files have valid frontmatter")

# R3: knowledge_updater.py --validate works
print("  Checking knowledge_updater.py...")
result = subprocess.run(
    [sys.executable, str(SKILL_DIR / "tools/knowledge_updater.py"), "--dry-run", "--validate"],
    capture_output=True, text=True
)
if "integrity OK" in result.stdout:
    print("  OK: knowledge_updater.py validates")
else:
    print("  WARN: knowledge_updater.py validation check")
    print("  ", result.stdout.strip())

# R4: SECOND-KNOWLEDGE-BRAIN.md has all required sections
print("  Checking SECOND-KNOWLEDGE-BRAIN.md sections...")
brain_content = (SKILL_DIR / "SECOND-KNOWLEDGE-BRAIN.md").read_text(encoding="utf-8")
required_brain = [
    "Core Concepts", "Key Research Papers", "State-of-the-Art Methods",
    "Authoritative Data Sources", "Analytical Frameworks", "Self-Update Protocol"
]
brain_ok = all(s in brain_content for s in required_brain)
if brain_ok:
    print("  OK: All required sections present")
else:
    missing = [s for s in required_brain if s not in brain_content]
    print(f"  FAIL: Missing sections: {missing}")
    errors += 1

# R5: validate_skill_files.py passes
print("  Running validate_skill_files.py...")
result = subprocess.run(
    [sys.executable, str(SKILL_DIR / "tools/validate_skill_files.py")],
    capture_output=True, text=True
)
if "ALL CHECKS PASSED" in result.stdout:
    print("  OK: validate_skill_files.py passes")
else:
    print("  FAIL: validate_skill_files.py reported errors")
    errors += 1

# Summary
print(f"\n{'='*50}")
if errors == 0:
    print("REGRESSION RESULT: ALL CHECKS PASSED")
    sys.exit(0)
else:
    print(f"REGRESSION RESULT: {errors} error(s) found")
    sys.exit(1)
