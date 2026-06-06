# CLAUDE.md — ai-project-builder

## Skill Identity

- **Name**: ai-project-builder
- **Tagline**: Autonomous AI topic discovery, GitHub gap analysis, and end-to-end skill package builder
- **Current Phase**: All 6 Phases Complete — Production Ready
- **Domain**: AI Topic Discovery & Open-Source Project Builder

---

## The Problem This Skill Solves

The AI landscape evolves so fast that by the time a developer discovers a promising topic, researches existing repos, finds a gap, gathers papers, designs a skill, and implements it — the opportunity window has narrowed. This skill automates the entire pipeline: it periodically discovers compelling AI topics (or accepts one from the user), researches GitHub's open-source ecosystem for prior art, identifies genuine gaps or improvement opportunities, grounds the plan in authoritative papers, then creates a complete Claude skill package and executes each implementation phase in a self-testing loop until the skill is production-ready. The result is a fully validated, production-grade skill delivered autonomously.

---

## Harness Flow Summary

```
[1] TOPIC INTAKE / DISCOVERY
      ↓ sub-topic-discovery.md
[2] GITHUB REPO RESEARCH
      ↓ sub-repo-researcher.md
[3] GAP ANALYSIS
      ↓ sub-gap-analyzer.md
[4] PAPER & DOCUMENT RESEARCH
      ↓ sub-paper-researcher.md
[5] SKILL PACKAGE CREATION (4-file combo)
      ↓ sub-skill-packager.md
[6] PHASE PLANNING
      ↓ sub-phase-executor.md (plan stage)
[7] PHASE EXECUTION LOOP (self-test → fix → retest)
      ↓ sub-phase-executor.md (execute stage)
[8] QUALITY GATE / FINAL REVIEW
      ↓ main.md (quality gate check)
[9] COMPLETION REPORT
```

---

## Sub-Skills List

| File                             | One-line Description                                                                                                       |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `skills/sub-topic-discovery.md`  | Auto-discover or validate trending AI topics from ArXiv, HuggingFace, GitHub Trending, Papers With Code                    |
| `skills/sub-repo-researcher.md`  | Search GitHub for existing repos on the topic; score by stars, recency, activity, and code quality                         |
| `skills/sub-gap-analyzer.md`     | Cross-reference repos against topic requirements; identify uncovered angles, weak implementations, and novel opportunities |
| `skills/sub-paper-researcher.md` | Find and rank relevant papers/docs from ArXiv, Semantic Scholar, HuggingFace; extract key methods                          |
| `skills/sub-skill-packager.md`   | Generate the full Claude skill package (CLAUDE.md + PROJECT-detail.md + SECOND-KNOWLEDGE-BRAIN.md + skills/main.md)        |
| `skills/sub-phase-executor.md`   | Plan implementation phases; execute each phase; run self-tests; apply fixes in a loop until complete                       |

---

## Tools Required

- **WebSearch** — topic discovery, GitHub search, paper search
- **WebFetch** — fetch GitHub README, ArXiv abstracts, HuggingFace model cards
- **Read** — read existing skill files and knowledge base
- **Write** — write all generated skill package files
- **Bash** — run tests, invoke crawl4ai pipeline, execute code checks
- **Glob / Grep** — scan generated skill files for completeness

---

## Knowledge Sources for Self-Update

- **ArXiv categories**: cs.AI, cs.LG, cs.CL, cs.CV, cs.RO, stat.ML
- **GitHub Trending**: `https://github.com/trending?l=python&since=weekly`
- **Papers With Code**: `https://paperswithcode.com/sota`
- **HuggingFace Papers**: `https://huggingface.co/papers`
- **Semantic Scholar**: `https://api.semanticscholar.org/graph/v1/paper/search`

---

## Supporting Python Tools

- `tools/knowledge_updater.py` — crawl4ai pipeline that fetches trending AI topics and top papers weekly; appends new entries to `SECOND-KNOWLEDGE-BRAIN.md`

---

## Active Development Tasks

- [x] Phase 1: Implement sub-topic-discovery.md
- [x] Phase 1: Implement sub-repo-researcher.md
- [x] Phase 1: Implement sub-gap-analyzer.md
- [x] Phase 2: Implement sub-paper-researcher.md
- [x] Phase 2: Implement sub-skill-packager.md
- [x] Phase 2: Implement sub-phase-executor.md
- [x] Phase 3: Build tools/knowledge_updater.py + validate_skill_files.py
- [x] Phase 4: Run all test-scenarios.md cases — ALL 5 SCENARIOS PASS
- [x] Phase 5: Wire Skill 7 (research-first-reasoning) as evidence enforcement engine
- [ ] Phase 4: Run all test-scenarios.md cases
- [ ] Phase 5: Wire Skill 7 (research-first-reasoning) as evidence enforcement engine

---

## Reference Files

- Full technical spec: `PROJECT-detail.md`
- Build roadmap: `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- Domain knowledge: `SECOND-KNOWLEDGE-BRAIN.md`
- Test cases: `tests/test-scenarios.md`
