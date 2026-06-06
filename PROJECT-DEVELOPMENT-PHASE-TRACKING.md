# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — ai-project-builder

## Overview

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| 0 | Research & Architecture | Week 1–2 | ✅ Complete |
| 1 | Core Research Sub-Skills | Week 3–5 | 🔲 Not Started |
| 2 | Build & Package Sub-Skills | Week 6–8 | 🔲 Not Started |
| 3 | SECOND-KNOWLEDGE-BRAIN Pipeline | Week 9–10 | 🔲 Not Started |
| 4 | Testing & Validation | Week 11–12 | 🔲 Not Started |
| 5 | Integration & Cross-Skill Wiring | Week 13–14 | 🔲 Not Started |

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

## Phase 1 — Core Research Sub-Skills (Week 3–5) 🔲

### Tasks
- [ ] Fully implement `skills/sub-topic-discovery.md`
  - [ ] Auto-discover mode: fetch GitHub Trending, ArXiv weekly, HuggingFace Papers
  - [ ] Validate mode: score user-supplied topic against the same signals
  - [ ] Output: topic struct with novelty score + motivation paragraph
- [ ] Fully implement `skills/sub-repo-researcher.md`
  - [ ] Build GitHub search query templates for AI topics
  - [ ] Scoring rubric: stars (30%), recency (30%), commit activity (20%), docs (20%)
  - [ ] Fork-candidate detection logic
  - [ ] Output: ranked repo list (top 10, JSON format)
- [ ] Fully implement `skills/sub-gap-analyzer.md`
  - [ ] Cross-reference repo feature lists against topic requirements
  - [ ] Gap severity scoring: Critical / Major / Minor / Nice-to-have
  - [ ] Feasibility check against available tools
  - [ ] Output: gap matrix + selected primary gap

### Deliverables
- 3 implemented sub-skill files (topic-discovery, repo-researcher, gap-analyzer)
- Each file: full workflow, tool calls specified, output schema defined

### Success Criteria
- Topic discovery returns a structured output within 3 WebSearch calls
- Repo researcher evaluates ≥5 repos per run
- Gap analyzer produces a gap matrix with ≥3 entries

### Estimated Effort: 3 weeks

---

## Phase 2 — Build & Package Sub-Skills (Week 6–8) 🔲

### Tasks
- [ ] Fully implement `skills/sub-paper-researcher.md`
  - [ ] ArXiv search with topic + gap keywords
  - [ ] Semantic Scholar API integration
  - [ ] Evidence hierarchy scoring (Systematic Review > RCT > …)
  - [ ] Output: annotated bibliography (≥5 papers)
- [ ] Fully implement `skills/sub-skill-packager.md`
  - [ ] Template engine for all 8 required files
  - [ ] Frontmatter validator
  - [ ] Sub-skill stub generator (3 stubs minimum)
  - [ ] Output: complete skill directory with all files
- [ ] Fully implement `skills/sub-phase-executor.md`
  - [ ] Phase planning: decompose gap into 4–6 implementation phases
  - [ ] Phase execution: run each phase as a Bash script or tool sequence
  - [ ] Self-test: execute test file after each phase
  - [ ] Fix loop: apply targeted fixes when tests fail
  - [ ] Loop-breaker: stop after 5 failed cycles; write blocker report
  - [ ] Output: implemented skill or blocker report

### Deliverables
- 3 additional implemented sub-skill files
- End-to-end harness runnable from Stage 1 through Stage 7

### Success Criteria
- sub-skill-packager generates all 8 files for any given topic
- sub-phase-executor successfully completes a 3-phase test case
- Loop-breaker fires correctly when all 5 cycles fail

### Estimated Effort: 3 weeks

---

## Phase 3 — SECOND-KNOWLEDGE-BRAIN Pipeline (Week 9–10) 🔲

### Tasks
- [ ] Implement `tools/knowledge_updater.py`
  - [ ] crawl4ai integration for ArXiv, GitHub Trending, HuggingFace Papers
  - [ ] Parser: extract title, authors, year, URL, abstract, relevance score
  - [ ] Deduplication: SHA256 of URL/DOI as key; skip if already present
  - [ ] Append to SECOND-KNOWLEDGE-BRAIN.md with date stamp
  - [ ] Config file: sources, keywords, frequency
- [ ] Set up weekly cron trigger (via CronCreate or system cron)
- [ ] Validate knowledge base growth: run once manually, verify 20+ new entries added

### Deliverables
- `tools/knowledge_updater.py` — fully functional crawl pipeline
- Updated `SECOND-KNOWLEDGE-BRAIN.md` with first crawl results

### Success Criteria
- Crawler runs end-to-end without errors
- Adds ≥10 new entries per source per crawl
- No duplicate entries after 2 consecutive runs

### Estimated Effort: 2 weeks

---

## Phase 4 — Testing & Validation (Week 11–12) 🔲

### Tasks
- [ ] Run all 5 test scenarios from `tests/test-scenarios.md`
- [ ] Scenario 1: User supplies a specific topic → full pipeline to completion report
- [ ] Scenario 2: Auto-discovery mode → harness selects topic autonomously
- [ ] Scenario 3: Topic with no GitHub repos → graceful degradation
- [ ] Scenario 4: Loop-breaker triggers → blocker report written correctly
- [ ] Scenario 5: Sub-skill failure mid-flow → error handling and recovery
- [ ] Fix all failures discovered during testing
- [ ] Re-run all scenarios to confirm passing

### Deliverables
- Test run logs for all 5 scenarios
- All bugs fixed and documented

### Success Criteria
- All 5 scenarios pass their acceptance criteria
- Loop-breaker test confirms max 5 cycles before report

### Estimated Effort: 2 weeks

---

## Phase 5 — Integration & Cross-Skill Wiring (Week 13–14) 🔲

### Tasks
- [ ] Wire Skill 7 (research-first-reasoning) into sub-paper-researcher.md
  - [ ] sub-paper-researcher invokes `Skill("research-first-reasoning")` for evidence enforcement
  - [ ] Ensure evidence hierarchy is applied to all cited papers
- [ ] Wire Skill 7 into sub-gap-analyzer.md
  - [ ] Gap analysis conclusions require research-first validation before proceeding
- [ ] Integration test: run full harness end-to-end with Skill 7 active
- [ ] Update SECOND-KNOWLEDGE-BRAIN.md with integration patterns
- [ ] Write final completion report template to `tests/completion-report-template.md`

### Deliverables
- Integrated harness with Skill 7 evidence enforcement
- Integration test passing
- Completion report template

### Success Criteria
- Paper research outputs include evidence hierarchy scores
- Gap analysis conclusions are research-validated before skill packaging begins
- Full E2E test passes in < 45 minutes wall-clock time

### Estimated Effort: 2 weeks

---

## Milestone Summary

| Milestone | Deliverable | Target |
|-----------|-------------|--------|
| M0 | All 8 files scaffolded | Week 2 ✅ |
| M1 | Research sub-skills functional | Week 5 |
| M2 | Full harness runnable end-to-end | Week 8 |
| M3 | Self-improving knowledge pipeline live | Week 10 |
| M4 | All test scenarios passing | Week 12 |
| M5 | Cross-skill integration complete | Week 14 |
