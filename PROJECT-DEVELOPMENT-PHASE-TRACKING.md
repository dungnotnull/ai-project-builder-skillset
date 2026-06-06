# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — ai-project-builder

## Overview

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| 0 | Research & Architecture | Week 1–2 | ✅ Complete |
| 1 | Core Research Sub-Skills | Week 3–5 | ✅ Complete |
| 2 | Build & Package Sub-Skills | Week 6–8 | ✅ Complete |
| 3 | SECOND-KNOWLEDGE-BRAIN Pipeline | Week 9–10 | ✅ Complete |
| 4 | Testing & Validation | Week 11–12 | ✅ Complete |
| 5 | Integration & Cross-Skill Wiring | Week 13–14 | ✅ Complete |

---

## Phase 0 — Research & Skill Architecture (Week 1–2) ✅ COMPLETE

### Tasks
- [x] Read and analyze 20+ existing AI project builder repos
- [x] Define harness flow (9-stage pipeline)
- [x] Identify all sub-skills and their interfaces
- [x] Design loop-breaker logic for phase execution
- [x] Write CLAUDE.md (skill identity)
- [x] Write PROJECT-detail.md (full technical spec)
- [x] Write PROJECT-DEVELOPMENT-PHASE-TRACKING.md (this file)
- [x] Write SECOND-KNOWLEDGE-BRAIN.md (initial domain knowledge)
- [x] Write all 6 sub-skill stubs
- [x] Write skills/main.md
- [x] Write tools/knowledge_updater.py
- [x] Write tests/test-scenarios.md

### Deliverables
- All 8 required files present in `5/`
- Architecture diagram in PROJECT-detail.md
- Sub-skill catalog with interfaces defined

### Success Criteria
- Harness flow is complete (no missing stages)
- Every sub-skill has: purpose, inputs, outputs, tools, quality gate
- Loop-breaker logic is specified

---

## Phase 1 — Core Research Sub-Skills (Week 3–5) ✅ COMPLETE

### Tasks
- [x] Fully implement `skills/sub-topic-discovery.md`
  - [x] Auto-discover mode: fetch GitHub Trending, ArXiv weekly, HuggingFace Papers
  - [x] Validate mode: score user-supplied topic against the same signals
  - [x] Output: topic struct with novelty score + motivation paragraph
- [x] Fully implement `skills/sub-repo-researcher.md`
  - [x] Build GitHub search query templates for AI topics
  - [x] Scoring rubric: stars (30%), recency (30%), commit activity (20%), docs (20%)
  - [x] Fork-candidate detection logic
  - [x] Output: ranked repo list (top 10, JSON format)
- [x] Fully implement `skills/sub-gap-analyzer.md`
  - [x] Cross-reference repo feature lists against topic requirements
  - [x] Gap severity scoring: Critical / Major / Minor / Nice-to-have
  - [x] Feasibility check against available tools
  - [x] Skill 7 Devil's Advocate validation
  - [x] Output: gap matrix + selected primary gap

### Deliverables
- 3 implemented sub-skill files (topic-discovery, repo-researcher, gap-analyzer)
- Each file: full workflow, tool calls specified, output schema defined, error handling table

### Success Criteria
- Topic discovery returns a structured output within 3 WebSearch calls
- Repo researcher evaluates ≥5 repos per run
- Gap analyzer produces a gap matrix with ≥3 entries and passes devil's advocate

### Estimated Effort: 3 weeks

---

## Phase 2 — Build & Package Sub-Skills (Week 6–8) ✅ COMPLETE

### Tasks
- [x] Fully implement `skills/sub-paper-researcher.md`
  - [x] ArXiv search with topic + gap keywords
  - [x] Semantic Scholar API integration
  - [x] Evidence hierarchy scoring (Systematic Review > RCT > ...)
  - [x] Skill 7 Evidence Hierarchy validation
  - [x] Output: annotated bibliography (>=5 papers with paper_score >= 8)
- [x] Fully implement `skills/sub-skill-packager.md`
  - [x] Template engine for all 8 required files
  - [x] Frontmatter validator
  - [x] Sub-skill stub generator (3 stubs minimum)
  - [x] Error handling table
  - [x] Output: complete skill directory with all files
- [x] Fully implement `skills/sub-phase-executor.md`
  - [x] Phase planning: decompose gap into 4-6 implementation phases
  - [x] Phase execution: run each phase with acceptance test
  - [x] Self-test: execute test file after each phase
  - [x] Fix loop: apply targeted fixes when tests fail
  - [x] Loop-breaker: stop after exactly 5 failed cycles; write blocker report
  - [x] Output: implemented skill or blocker report

### Deliverables
- 3 additional implemented sub-skill files
- End-to-end harness runnable from Stage 1 through Stage 7
- Blocker report template with root cause analysis, all errors, attempted fixes, recommended resolution

### Success Criteria
- sub-skill-packager generates all 8 files for any given topic
- sub-phase-executor successfully completes a 4-phase test case
- Loop-breaker fires correctly after exactly 5 failed cycles

### Estimated Effort: 3 weeks

---

## Phase 3 — SECOND-KNOWLEDGE-BRAIN Pipeline (Week 9–10) ✅ COMPLETE

### Tasks
- [x] Implement `tools/knowledge_updater.py`
  - [x] crawl4ai integration for ArXiv, GitHub Trending, HuggingFace Papers
  - [x] Parser: extract title, authors, year, URL, abstract, relevance score
  - [x] Deduplication: SHA256 of URL/DOI as key; skip if already present
  - [x] Append to SECOND-KNOWLEDGE-BRAIN.md with date stamp
  - [x] Config file: SOURCES dict with keywords per source
  - [x] `--validate` flag for integrity checks
- [x] Implement `tools/validate_skill_files.py` — file existence, frontmatter, section, cross-reference validation
- [x] Validate knowledge base integrity: `--validate` passes all checks

### Deliverables
- `tools/knowledge_updater.py` — fully functional crawl pipeline with dry-run and validate modes
- `tools/validate_skill_files.py` — 5-step validation for any skill package
- `SECOND-KNOWLEDGE-BRAIN.md` — passes validation (7 required sections present)

### Success Criteria
- knowledge_updater.py runs with `--dry-run --validate` without errors
- validate_skill_files.py reports "ALL CHECKS PASSED"
- All 7 required sections present in SECOND-KNOWLEDGE-BRAIN.md

### Estimated Effort: 2 weeks

---

## Phase 4 — Testing & Validation (Week 11–12) ✅ COMPLETE

### Tasks
- [x] Write 5 concrete Python test scripts (test_scenario_1.py through test_scenario_5.py)
- [x] Scenario 1: User supplies a specific topic -> full pipeline to completion report
- [x] Scenario 2: Auto-discovery mode -> harness selects topic autonomously
- [x] Scenario 3: Topic with no GitHub repos -> graceful degradation (early_stage_flag, search broadening)
- [x] Scenario 4: Loop-breaker triggers -> blocker report written correctly (exactly 5 cycles, all required fields)
- [x] Scenario 5: Sub-skill failure mid-flow -> error handling and recovery (papers_below_minimum, query broadening)
- [x] Write `tests/test_regression.py` — unified regression runner covering all 5 scenarios + additional checks
- [x] Write `tools/validate_skill_files.py` — 5-step validation: files, frontmatter, sections, cross-refs
- [x] Fix all failures discovered during testing (Windows CP1258 unicode encoding, frontmatter on non-skill files)
- [x] Re-run all scenarios to confirm passing

### Deliverables
- Test run logs for all 5 scenarios (Python, cross-platform)
- Regression test suite — one command: `python tests/test_regression.py`
- validate_skill_files.py — one command: `python tools/validate_skill_files.py`

### Success Criteria
- All 5 scenarios pass their acceptance criteria (confirmed: ALL PASS)
- Loop-breaker test confirms max 5 cycles before report (confirmed: exactly 5)
- validate_skill_files.py reports "ALL CHECKS PASSED" (confirmed: PASSED)
- Regression suite exits 0 (confirmed: ALL CHECKS PASSED)

### Estimated Effort: 2 weeks

---

## Phase 5 — Integration & Cross-Skill Wiring (Week 13–14) ✅ COMPLETE

### Tasks
- [x] Wire Skill 7 (research-first-reasoning) into sub-paper-researcher.md
  - [x] sub-paper-researcher invokes Skill 7 Evidence Hierarchy enforcement (Step 7)
  - [x] Evidence hierarchy applied to all cited papers (Tiers 1-7 with scores)
  - [x] All papers validated via Skill 7 reasoning before inclusion
- [x] Wire Skill 7 into sub-gap-analyzer.md
  - [x] Gap analysis conclusions require Skill 7 Devil's Advocate validation before proceeding
  - [x] Top-2 gaps challenged: "why not filled?" + "why not worth filling?" + counter-argument
- [x] Wire Skill 7 into main.md harness flow
  - [x] Stage 3: Explicit Skill 7 Devil's Advocate invocation
  - [x] Stage 4: Explicit Skill 7 Evidence Hierarchy enforcement note
- [x] Update SECOND-KNOWLEDGE-BRAIN.md with Skill 7 analytical frameworks (8 methods mapped)
- [x] Write completion report template to `tests/completion-report-template.md`

### Deliverables
- Integrated harness with Skill 7 evidence enforcement at Stages 3-4
- Integration test passing (regression suite confirms all 5 scenarios PASS)
- Completion report template

### Success Criteria
- Paper research outputs include evidence hierarchy scores (confirmed: evidence_tier + paper_score in schema)
- Gap analysis conclusions are research-validated before skill packaging begins (confirmed: devils_advocate_cleared gate)
- Full regression test passes (confirmed: ALL CHECKS PASSED)

### Estimated Effort: 2 weeks

---

## Milestone Summary

| Milestone | Deliverable | Target | Status |
|-----------|-------------|--------|--------|
| M0 | All 8 files scaffolded | Week 2 | ✅ Complete |
| M1 | Research sub-skills functional | Week 5 | ✅ Complete |
| M2 | Full harness runnable end-to-end | Week 8 | ✅ Complete |
| M3 | Self-improving knowledge pipeline live | Week 10 | ✅ Complete |
| M4 | All test scenarios passing | Week 12 | ✅ Complete |
| M5 | Cross-skill integration complete | Week 14 | ✅ Complete |
