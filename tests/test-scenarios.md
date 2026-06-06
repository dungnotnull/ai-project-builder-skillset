# test-scenarios.md — ai-project-builder

Five concrete end-to-end test scenarios covering normal flow, edge cases, error handling, and integration.

---

## Scenario 1 — User Supplies a Specific Topic (Happy Path)

**Trigger**: User invokes `/ai-project-builder "multimodal RAG with PDF, images, and tables"`

**Preconditions**
- WebSearch tool is available
- WebFetch tool is available
- Write tool is available

**Execution Flow**
1. Stage 1: `sub-topic-discovery` runs in validate mode
   - Searches GitHub for "multimodal RAG" repos
   - Searches ArXiv for recent papers
   - Returns novelty_score ≥ 6

2. Stage 2: `sub-repo-researcher` finds ≥ 5 repos
   - Expected: repos like LlamaIndex, LangChain RAG extensions, ColPali, MTEB
   - At least 1 fork candidate with permissive license

3. Stage 3: `sub-gap-analyzer` builds requirements matrix (≥ 8 requirements)
   - Expected gap: No repo combines PDF + image + table retrieval in a single unified pipeline with citation attribution
   - Gap type: Coverage or Integration
   - Gap score ≥ 4 (Medium × Medium or better)

4. Stage 4: `sub-paper-researcher` finds ≥ 5 papers
   - Expected: ColPali (ECCV 2024), RAG Survey (ACL 2024), PDFPlumber, etc.
   - At least 2 peer-reviewed papers

5. Stage 5: `sub-skill-packager` generates all 8 files
   - Skill name: `multimodal-rag-builder` (or similar)
   - All files present and non-empty

6. Stage 6–7: Phase plan has 4 phases; all execute and PASS

7. Stage 8–9: Quality gates pass; `report.md` written

**Acceptance Criteria**
- [ ] novelty_score ≥ 6
- [ ] ≥ 5 repos evaluated
- [ ] Gap matrix has ≥ 3 gaps identified
- [ ] Primary gap has gap_score ≥ 4
- [ ] ≥ 5 papers with paper_score ≥ 8
- [ ] All 8 skill files written to output directory
- [ ] All phase tests PASS
- [ ] `report.md` exists and has all 6 required sections

---

## Scenario 2 — Auto-Discovery Mode (No User Topic)

**Trigger**: User invokes `/ai-project-builder` with no arguments

**Preconditions**
- Same as Scenario 1

**Execution Flow**
1. Stage 1: `sub-topic-discovery` runs in discover mode
   - Fetches GitHub Trending (Python, weekly)
   - Fetches ArXiv cs.AI recent
   - Fetches HuggingFace Papers
   - Scores all candidates; selects top (score ≥ 6)
   - Presents topic to user with motivation paragraph

2. User confirms topic (simulated: "yes, proceed")

3. Harness continues through Stages 2–9 as in Scenario 1

**Acceptance Criteria**
- [ ] Auto-discovery queries ≥ 3 live sources
- [ ] Selected topic has novelty_score ≥ 6
- [ ] Motivation paragraph cites ≥ 2 evidence URLs
- [ ] Harness presents topic for user confirmation before proceeding
- [ ] Rest of pipeline completes successfully (same criteria as Scenario 1)

---

## Scenario 3 — Topic With Very Few GitHub Repos (Edge Case)

**Trigger**: User invokes `/ai-project-builder "neuro-symbolic AI for robot navigation"`

**Preconditions**
- WebSearch returns < 5 repos matching the topic exactly

**Execution Flow**
1. Stage 1: Topic validates (novelty_score ≥ 6 from ArXiv papers even if GitHub is sparse)

2. Stage 2: `sub-repo-researcher` finds < 5 repos matching the topic directly
   - Harness should broaden search to related terms: "neuro-symbolic", "symbolic AI", "robot planning"
   - Still produces a ranked list of best available repos (may be < 5)
   - Flags topic as "early-stage" in output

3. Stage 3: `sub-gap-analyzer` identifies Coverage Gap (no repo addresses this combination)
   - Coverage gaps dominate because the topic is truly novel

4. Harness continues through remaining stages with the best available research

**Acceptance Criteria**
- [ ] Harness does NOT abort when < 5 repos are found
- [ ] repo_researcher broadens search terms and documents this in output
- [ ] Output JSON includes `"early_stage_flag": true` when < 5 repos found
- [ ] Gap matrix shows Coverage Gap as primary type
- [ ] Skill package is still generated successfully
- [ ] report.md notes the limited prior art context

---

## Scenario 4 — Loop-Breaker Fires During Phase Execution

**Trigger**: Phase execution test script fails 5 consecutive times (simulated by injecting a broken test)

**Setup**
- Manually inject a broken `tests/test_p2.sh` that always exits 1:
  ```bash
  #!/bin/bash
  echo "INTENTIONAL FAIL"
  exit 1
  ```

**Execution Flow**
1. Stages 1–5 complete normally
2. Phase plan created with Phase P2 having the broken test
3. `sub-phase-executor` executes P2:
   - Attempt 1: test fails → apply fix → retest
   - Attempt 2: test still fails → apply fix → retest
   - Attempts 3–5: same pattern
   - After 5th failure: loop-breaker fires

4. `blocker-report.md` written to skill directory

**Acceptance Criteria**
- [ ] Loop iterates exactly 5 times before firing (not 4, not 6)
- [ ] `blocker-report.md` exists in skill directory
- [ ] Blocker report contains: phase_id, root_cause_analysis, all 5 error messages, attempted fixes, recommended resolution
- [ ] Harness outputs `{result: "BLOCKED", blocker_report: "<path>"}` to user
- [ ] Harness STOPS (does not continue to next phase after loop-breaker)
- [ ] User is notified with a clear message including the path to the blocker report

---

## Scenario 5 — Sub-Skill Failure Mid-Flow (Error Recovery)

**Trigger**: `sub-paper-researcher` returns fewer than 5 papers (e.g., topic is very new)

**Simulated Condition**
- WebSearch returns only 3 papers matching the topic
- All 3 have paper_score ≥ 8

**Execution Flow**
1. Stages 1–3 complete normally

2. Stage 4: `sub-paper-researcher` finds only 3 papers
   - Quality gate: "minimum 5 papers" NOT met
   - Sub-skill should: broaden search queries (remove topic-specific terms, search only for gap keywords)
   - If still < 5 after broadening: accept 3 papers and flag the shortfall

3. Harness continues with 3 papers but:
   - Quality gate at Stage 8 catches the shortfall
   - Report.md notes: "Paper research: 3 papers found (below 5 minimum); broadened search applied"

**Acceptance Criteria**
- [ ] Harness does NOT abort when paper count < 5
- [ ] sub-paper-researcher attempts query broadening before declaring shortfall
- [ ] Shortfall is documented in the output JSON (`"papers_below_minimum": true`)
- [ ] Stage 8 quality gate flags the shortfall but does NOT block report.md generation
- [ ] report.md explicitly notes the shortfall and suggests manual paper curation
- [ ] User receives a warning (not an error) about the limited paper evidence

---

## Regression Test Checklist

Run after any change to main.md or any sub-skill file:

- [ ] `skills/main.md` has all 6 required sections (Role, Workflow, Sub-skills, Tools, Output Format, Quality Gates)
- [ ] All `skills/sub-*.md` files have valid frontmatter (`name:` and `description:`)
- [ ] `tools/knowledge_updater.py` runs with `--dry-run` without error
- [ ] All 5 scenarios above pass their acceptance criteria
- [ ] `SECOND-KNOWLEDGE-BRAIN.md` has all 6 required sections (Core Concepts, Key Research Papers, SOTA, Data Sources, Analytical Frameworks, Self-Update Protocol)
