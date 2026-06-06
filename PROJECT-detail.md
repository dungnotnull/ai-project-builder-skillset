# PROJECT-detail.md — ai-project-builder

## Executive Summary

`ai-project-builder` is an autonomous AI skill harness that discovers compelling AI topics, researches the existing open-source landscape on GitHub, finds genuine gaps or improvement opportunities, grounds the work in peer-reviewed papers and authoritative documentation, and then generates a complete, production-grade Claude skill package. It executes each implementation phase in a self-testing loop until the delivered skill passes all quality gates. The result is a fully automated pipeline from topic to production skill.

---

## Problem Statement

Building a new Claude skill currently requires a developer to:
1. Stay current with fast-moving AI research and open-source trends
2. Manually survey dozens of GitHub repos to avoid duplicate effort
3. Identify which gaps are genuinely worth filling
4. Read relevant papers and extract applicable methods
5. Design and scaffold the skill architecture
6. Implement, test, debug, and iterate across multiple phases

Each of these steps is time-consuming, expertise-dependent, and error-prone when done manually. `ai-project-builder` automates the entire pipeline, applying structured evidence-based reasoning at each stage, producing a complete, self-tested skill package autonomously.

---

## Target Users & Use Cases

**Primary users**: Claude Code users who want to rapidly create new skills for emerging AI topics.

| Trigger | Skill Response |
|---------|---------------|
| User says "build a skill for multimodal RAG" | Executes full pipeline on that topic |
| User says "find me an interesting AI topic to build" | Auto-discovers top trending topic, presents it, then builds |
| User says "I want to improve the existing open-source TTS repos" | Researches TTS repos, finds improvement gaps, builds skill targeting those gaps |
| Cron schedule fires | Auto-discovers newest trending topic, builds skill, delivers completion report |

---

## Harness Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ai-project-builder                    │
│                     main.md (harness)                   │
└─────────────────┬───────────────────────────────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 1: Topic Intake   │ ← sub-topic-discovery.md
     │ User input OR auto-find │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 2: Repo Research  │ ← sub-repo-researcher.md
     │ GitHub search + scoring │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 3: Gap Analysis   │ ← sub-gap-analyzer.md
     │ What's missing/weak?    │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 4: Paper Research │ ← sub-paper-researcher.md
     │ ArXiv + Semantic Scholar│
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 5: Skill Package  │ ← sub-skill-packager.md
     │ Generate 4-file combo   │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Stage 6: Phase Loop     │ ← sub-phase-executor.md
     │ Plan → Execute → Test   │
     │ → Fix → Retest (loop)   │
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Quality Gate Review     │ ← main.md checklist
     └────────────┬────────────┘
                  │
     ┌────────────▼────────────┐
     │ Completion Report       │
     └─────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-topic-discovery.md
- **Purpose**: Discover or validate an AI topic worth building a skill for
- **Inputs**: Optional user-supplied topic string; if none, auto-discover
- **Outputs**: Confirmed topic, domain context, novelty score, motivation paragraph
- **Tools**: WebSearch, WebFetch
- **Quality Gate**: Topic must have (a) active research interest in past 6 months, (b) at least one gap not fully addressed by existing repos

### sub-repo-researcher.md
- **Purpose**: Exhaustive GitHub search for existing repos on the topic
- **Inputs**: Confirmed topic from Stage 1
- **Outputs**: Ranked repo list (name, URL, stars, last commit, summary, code quality score), fork candidates
- **Tools**: WebSearch (GitHub search queries), WebFetch (README, package.json, requirements.txt)
- **Quality Gate**: Minimum 5 repos evaluated; each scored on stars, recency (< 18 months), activity (commits/month), documentation quality

### sub-gap-analyzer.md
- **Purpose**: Identify genuine gaps — areas no repo covers well, or opportunities to improve
- **Inputs**: Ranked repo list from Stage 2, topic requirements
- **Outputs**: Gap matrix (gap description, severity, novelty, feasibility); selected primary gap for implementation
- **Tools**: Read, Grep, WebSearch
- **Quality Gate**: Selected gap must be (a) confirmed absent across top 5 repos, (b) feasible within 4 phases

### sub-paper-researcher.md
- **Purpose**: Find and rank relevant papers/docs to ground the implementation
- **Inputs**: Confirmed topic + selected gap from Stage 3
- **Outputs**: Annotated bibliography (title, authors, year, venue, DOI, abstract, applicable methods)
- **Tools**: WebSearch, WebFetch
- **Quality Gate**: Minimum 5 papers; at least 2 from peer-reviewed venues (ArXiv with CS categories, NeurIPS, ICML, ACL, CVPR, etc.)

### sub-skill-packager.md
- **Purpose**: Generate the complete Claude skill package (all 4 required .md files + sub-skills)
- **Inputs**: Topic, gap analysis, papers, project name
- **Outputs**: Full directory with CLAUDE.md, PROJECT-detail.md, SECOND-KNOWLEDGE-BRAIN.md, skills/main.md, skills/sub-*.md
- **Tools**: Write, Read, Glob
- **Quality Gate**: All 8 required files present; frontmatter valid; harness flow complete

### sub-phase-executor.md
- **Purpose**: Break the skill implementation into phases; execute each; self-test; fix in a loop
- **Inputs**: Generated skill package from Stage 5
- **Outputs**: Implemented, tested, and passing skill (or detailed blocker report after N cycles)
- **Tools**: Bash, Read, Write, Grep
- **Quality Gate**: All phase tests pass; loop-breaker triggers after 5 failed cycles with error report

---

## Skill File Format Specification

### Frontmatter Schema
```yaml
---
name: skill-name          # kebab-case, unique
description: One-line summary shown in /help
---
```

### Required Sections (main.md)
1. `## Role & Persona` — who Claude becomes
2. `## Workflow (Harness Flow)` — numbered step-by-step
3. `## Sub-skills Available` — list of sub-skill files
4. `## Tools` — WebSearch, WebFetch, Bash, Read, Write, etc.
5. `## Output Format` — exact deliverable structure
6. `## Quality Gates` — pre-flight checklist

---

## E2E Execution Flow

```
START
  ├─ [1] Read user input → topic provided?
  │         YES → validate topic (sub-topic-discovery: validate mode)
  │         NO  → auto-discover (sub-topic-discovery: discover mode)
  ├─ [2] Invoke sub-repo-researcher → build ranked repo list
  ├─ [3] Invoke sub-gap-analyzer → select primary gap
  ├─ [4] Invoke sub-paper-researcher → build annotated bibliography
  ├─ [5] Invoke sub-skill-packager → generate full skill package
  ├─ [6] Invoke sub-phase-executor (PLAN) → define phases with tasks/tests
  ├─ [7] Loop: sub-phase-executor (EXECUTE)
  │         ├─ Execute current phase
  │         ├─ Run self-tests
  │         ├─ All pass? → advance to next phase
  │         └─ Fail? → apply fixes → retest → loop (max 5 cycles)
  │                  5 cycles exceeded? → emit blocker report → STOP
  ├─ [8] Quality gate check (main.md checklist)
  └─ [9] Write completion report → DONE
```

---

## SECOND-KNOWLEDGE-BRAIN Integration

- **Sources**: ArXiv (cs.AI, cs.LG, cs.CL), GitHub Trending (Python, weekly), HuggingFace Papers, Papers With Code SOTA
- **Crawl config**: `tools/knowledge_updater.py` — weekly cron, fetches top 20 entries per source
- **Append format**: Frontmatter-tagged entries with date, source, relevance score
- **Dedup**: Skip entries where DOI or GitHub URL already present in the brain

---

## Quality Gates (Pre-Final-Output Checklist)

- [ ] Topic is novel and has demonstrable gap in existing repos
- [ ] At least 5 repos evaluated and scored
- [ ] Gap confirmed absent across top-5 repos
- [ ] At least 5 papers cited with DOI/URL
- [ ] All 8 skill package files present and non-empty
- [ ] Harness frontmatter valid (name + description fields)
- [ ] All phase tests pass (or blocker report issued if loop-breaker fired)
- [ ] Completion report written to `report.md` inside the generated skill folder

---

## Test Scenarios

See `tests/test-scenarios.md` for the full test case catalog.

---

## Key Design Decisions

1. **Loop-breaker at 5 cycles**: Prevents infinite self-testing loops; emits an actionable blocker report instead of silent failure.
2. **Auto-discovery mode**: When no topic is given, pulls from GitHub Trending + ArXiv weekly digest — the most live signal of what's actually being built and researched.
3. **Fork-candidate flagging**: The repo researcher specifically identifies repos suitable for forking as implementation base, not just reference — accelerates phase execution.
4. **Skill 7 integration**: Paper research and gap analysis invoke `research-first-reasoning` as the evidence-enforcement engine to ensure claims are grounded.
5. **Phase isolation**: Each phase generates its own test file and runs independently — partial completion is recoverable without restarting the full harness.
6. **Completion report**: Always written as `report.md` in the output skill folder — gives the user a human-readable summary without needing to inspect all files.
