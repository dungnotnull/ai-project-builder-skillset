<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/ai--project--builder-v1.0.0-6C5CE7?style=for-the-badge&logo=claude&logoColor=white&labelColor=2D2D2D">
    <img alt="ai-project-builder" src="https://img.shields.io/badge/ai--project--builder-v1.0.0-6C5CE7?style=for-the-badge&logo=claude&logoColor=white&labelColor=2D2D2D">
  </picture>
</p>

<p align="center">
  <b>Autonomous AI Topic Discovery, GitHub Gap Analysis & End-to-End Claude Skill Package Builder</b>
</p>

<p align="center">
  <a href="#-overview"><img src="https://img.shields.io/badge/Overview-6C5CE7?style=flat-square" /></a>
  <a href="#-architecture"><img src="https://img.shields.io/badge/Architecture-00CEC9?style=flat-square" /></a>
  <a href="#-sub-skills"><img src="https://img.shields.io/badge/Sub--Skills-FDCB6E?style=flat-square" /></a>
  <a href="#-quality-gates"><img src="https://img.shields.io/badge/Quality%20Gates-E17055?style=flat-square" /></a>
  <a href="#-testing"><img src="https://img.shields.io/badge/Testing-00B894?style=flat-square" /></a>
  <a href="#-project-structure"><img src="https://img.shields.io/badge/Structure-636E72?style=flat-square" /></a>
</p>

---

## Overview

The AI landscape evolves so fast that by the time you discover a promising topic, research existing repos, find a gap, gather papers, design a skill, and implement it — the opportunity window has narrowed.

**ai-project-builder** is a Claude Code skill harness that automates the entire pipeline:

1. **Discovers** compelling AI topics (or accepts one from you)
2. **Researches** GitHub's open-source ecosystem for prior art
3. **Identifies** genuine gaps or improvement opportunities
4. **Grounds** the plan in authoritative, peer-reviewed papers
5. **Generates** a complete, production-grade Claude skill package
6. **Executes** each implementation phase in a self-testing loop until the delivered skill passes all quality gates

The result is a **fully validated, production-grade skill** delivered autonomously — from topic to completion, no manual intervention required.

---

## How It Works

```
┌──────────────────────────────────────────────────────┐
│                  ai-project-builder                   │
│                    main.md (harness)                  │
└──────────────────┬────────────────────────────────────┘
                   │
      ┌────────────▼────────────┐
      │  1. Topic Intake        │
      │  User input OR auto-find│
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  2. GitHub Repo Research│
      │  Search + quality score │
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  3. Gap Analysis        │
      │  Coverage/Quality/Integ │   ◄── Skill 7 Devil's Advocate
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  4. Paper Research      │
      │  ArXiv + Semantic Scholar│  ◄── Skill 7 Evidence Hierarchy
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  5. Skill Package       │
      │  Generate all 8 files   │
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  6. Phase Loop          │
      │  Plan → Execute → Test  │
      │  → Fix → Retest (×5 max)│
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  7. Quality Gate Review │
      │  Pre-flight checklist   │
      └────────────┬────────────┘
                   │
      ┌────────────▼────────────┐
      │  8. Completion Report   │
      └─────────────────────────┘
```

### Loop-Breaker

The fix loop iterates a maximum of **5 cycles**. If the acceptance test fails 5 consecutive times, a detailed **blocker report** is written with root cause analysis, all observed errors, attempted fixes, and a recommended resolution. The pipeline stops — no infinite loops, no silent failures.

---

## Sub-Skills

Six composable sub-skills, each with a defined interface contract, error handling table, and quality gate:

| Sub-Skill | Purpose | Quality Gate |
|-----------|---------|-------------|
| [`sub-topic-discovery`](skills/sub-topic-discovery.md) | Auto-discover or validate trending AI topics from GitHub, ArXiv, HuggingFace, Papers With Code | `novelty_score >= 6`, `gap_signal != "none"` |
| [`sub-repo-researcher`](skills/sub-repo-researcher.md) | Search GitHub, score repos by stars/recency/activity/docs, flag fork candidates | >= 5 repos evaluated, quality scoring rubric applied |
| [`sub-gap-analyzer`](skills/sub-gap-analyzer.md) | Build requirements matrix, cross-reference top repos, identify Coverage/Quality/Integration gaps | >= 8 requirements, `devils_advocate_cleared: true`, `gap_score >= 4` |
| [`sub-paper-researcher`](skills/sub-paper-researcher.md) | Find & rank papers with evidence hierarchy scoring, Skill 7 enforcement | >= 5 papers with `paper_score >= 8`, >= 2 from peer-reviewed venues |
| [`sub-skill-packager`](skills/sub-skill-packager.md) | Generate the complete 8-file skill package with templates & validation | All files present, `frontmatter_valid: true`, `package_ready: true` |
| [`sub-phase-executor`](skills/sub-phase-executor.md) | Decompose into 4-6 phases, execute with self-test loop, emit blocker report at 5 failures | Phase plan with runnable tests, loop-breaker fires at exactly 5 cycles |

---

## Quality Gates

Before any output is delivered, every item on this checklist is verified:

- **Novelty**: Topic has `novelty_score >= 6`
- **Coverage**: Minimum 5 repos evaluated and scored
- **Gap Validation**: Primary gap confirmed absent across top 5 repos
- **Evidence**: Minimum 5 papers with `paper_score >= 8`, >= 2 peer-reviewed
- **Completeness**: All 8 skill files present and non-empty
- **Frontmatter**: All `.md` files have valid `name:` and `description:` fields
- **Tests**: All phase tests PASS (or blocker report written if loop-breaker fired)
- **Report**: `report.md` written to the skill directory

---

## Testing

Five end-to-end test scenarios, implemented as cross-platform Python scripts:

| # | Scenario | Script | Validates |
|---|----------|--------|-----------|
| 1 | **User supplies a specific topic** | `test_scenario_1.py` | Happy path: all files, frontmatter, sections, quality gates |
| 2 | **Auto-discovery mode** | `test_scenario_2.py` | Discover mode, multi-source scoring, user confirmation, novelty threshold |
| 3 | **Topic with few GitHub repos** | `test_scenario_3.py` | `early_stage_flag`, search broadening, graceful degradation |
| 4 | **Loop-breaker fires** | `test_scenario_4.py` | Exactly 5 cycles, blocker report with all required fields, pipeline stop |
| 5 | **Sub-skill failure mid-flow** | `test_scenario_5.py` | `papers_below_minimum`, query broadening, non-abort on low results |

All tests and quality checks are runnable in a single command:

```bash
python tests/test_regression.py      # 5 scenarios + regression checks
python tools/validate_skill_files.py  # 5-step structural validation
```

---

## Tools

### [`tools/knowledge_updater.py`](tools/knowledge_updater.py)
Crawl4AI-based pipeline that fetches trending AI topics from GitHub, ArXiv, HuggingFace, and Papers With Code. Appends deduplicated entries to `SECOND-KNOWLEDGE-BRAIN.md`. Features `--dry-run` and `--validate` flags.

```bash
python tools/knowledge_updater.py --dry-run --sources all  # Preview new entries
python tools/knowledge_updater.py --validate                 # Check brain integrity
```

### [`tools/validate_skill_files.py`](tools/validate_skill_files.py)
5-step validation for any generated skill package:
1. Required file existence (8 files)
2. Sub-skill count (>= 3)
3. Frontmatter validation (`name:` + `description:`)
4. Required section presence (6 for main.md, 4 for sub-skills)
5. Cross-reference consistency (CLAUDE.md references)

```bash
python tools/validate_skill_files.py                    # Validate current project
python tools/validate_skill_files.py --dir ./my-skill   # Validate a generated skill
```

---

## Project Structure

```
ai-project-builder/
├── CLAUDE.md                          # Skill identity & harness flow
├── PROJECT-detail.md                  # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Build roadmap (0-5 ✅)
├── SECOND-KNOWLEDGE-BRAIN.md          # Self-improving domain knowledge base
├── .gitignore
│
├── skills/
│   ├── main.md                        # Primary harness (9-stage flow)
│   ├── sub-topic-discovery.md         # Stage 1: Topic intake
│   ├── sub-repo-researcher.md         # Stage 2: GitHub research
│   ├── sub-gap-analyzer.md            # Stage 3: Gap analysis
│   ├── sub-paper-researcher.md        # Stage 4: Paper research
│   ├── sub-skill-packager.md          # Stage 5: Skill generation
│   └── sub-phase-executor.md          # Stage 6-7: Phase execution
│
├── tools/
│   ├── knowledge_updater.py           # Weekly crawl & append pipeline
│   └── validate_skill_files.py        # 5-step skill package validator
│
└── tests/
    ├── test-scenarios.md              # Scenario specs (reference doc)
    ├── completion-report-template.md  # Output report template
    ├── test_regression.py             # Unified regression runner
    ├── test_scenario_1.py             # Happy path tests
    ├── test_scenario_2.py             # Auto-discovery tests
    ├── test_scenario_3.py             # Edge case: sparse repos
    ├── test_scenario_4.py             # Loop-breaker tests
    └── test_scenario_5.py             # Error recovery tests
```

---

## Skill 7 Integration

This project integrates **Skill 7 (research-first-reasoning)** at two critical decision points:

| Stage | Skill 7 Method | Application |
|-------|---------------|-------------|
| Gap Analysis | **Devil's Advocate** | Before selecting the primary gap, challenges it: "Why hasn't anyone done this?", "Might this NOT be worth filling?" — only proceeds if the counter-argument holds |
| Paper Research | **Evidence Hierarchy** | Validates each paper's venue classification, cross-checks citation counts, flags mislabeled sources — guarantees all citations are peer-reviewed or explicitly noted otherwise |

---

## Design Decisions

1. **Loop-breaker at 5 cycles** — Prevents infinite self-testing loops; emits an actionable blocker report with root cause analysis instead of silent failure.

2. **Auto-discovery from live signals** — When no topic is given, pulls from GitHub Trending + ArXiv weekly digest + HuggingFace Papers, scoring each candidate on Momentum, Novelty, and Buildability.

3. **Fork-candidate flagging** — The repo researcher identifies repos suitable for forking as implementation base, not just reference — accelerates phase execution.

4. **Phase isolation** — Each phase generates its own runnable acceptance test. Partial completion is recoverable without restarting the full harness.

5. **Completion report** — Always written as `report.md` in the output skill folder, giving the user a human-readable summary without needing to inspect all files.

---

## License

MIT
