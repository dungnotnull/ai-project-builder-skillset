# Completion Report — {Skill Name}

## Topic & Gap
- **Topic**: {topic}
- **Gap Addressed**: {gap description}
- **Gap Type**: Coverage | Quality | Integration
- **Gap Score**: {score}/9

## Research Summary
- **Repos Evaluated**: {N} (top 3: {name} stars, ...)
- **Papers Cited**: {N} (top 3: {title} ({year}, {venue}) — DOI: {doi})
- **Evidence Quality**: {strong | adequate | limited}

## Implementation
- **Phases Completed**: {N}/{N}
- **Phase Results**:
  - P1 — {name}: PASS | FAIL
  - P2 — {name}: PASS | FAIL
  - P3 — {name}: PASS | FAIL
  - P4 — {name}: PASS | FAIL
  - {P5} — {name}: PASS | FAIL
- **Loop-Breaker Fired**: Yes | No
  - If Yes: Blocker report at `{path}/blocker-report.md`

## Generated Files
| File | Size | Status |
|------|------|--------|
| CLAUDE.md | {N} bytes | ok |
| PROJECT-detail.md | {N} bytes | ok |
| PROJECT-DEVELOPMENT-PHASE-TRACKING.md | {N} bytes | ok |
| SECOND-KNOWLEDGE-BRAIN.md | {N} bytes | ok |
| skills/main.md | {N} bytes | ok |
| skills/sub-*.md | {N} files | ok |
| tools/knowledge_updater.py | {N} bytes | ok |
| tests/test-scenarios.md | {N} bytes | ok |

## Quality Gate Results
- [ ] Topic novelty_score >= 6: {passed | failed}
- [ ] >= 5 repos evaluated: {passed | failed}
- [ ] Primary gap confirmed absent across top-5: {passed | failed}
- [ ] >= 5 papers with paper_score >= 8: {passed | failed}
- [ ] All 8 skill files present and non-empty: {passed | failed}
- [ ] All .md files have valid frontmatter: {passed | failed}
- [ ] All phase tests PASS: {passed | failed}
- [ ] report.md written: {passed | failed}

## Next Steps for Maintainer
1. Review the generated skill package at `{path}`
2. If blocker report exists, address the root cause before first use
3. Configure knowledge_updater.py cron schedule for weekly updates
4. Run `python tests/test_regression.py` after any modification
5. Deploy the skill to your Claude Code skills directory
