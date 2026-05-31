# Resume Application Strategy

## Core Principle
Maintain **one master source of truth** (`testPM3.json`) and generate a **tailored resume per job posting**.

Do **not** send multiple resume styles to the same company for the same role unless explicitly requested.

## Why This Works
- Increases relevance to each job description.
- Improves ATS match rates through targeted keywords.
- Makes recruiter/hiring manager review faster and clearer.
- Keeps your claims consistent across applications.

## Resume Styles (When to Use)

### 1) ATS-Focused Resume
Use when:
- Applying through online portals or large-company systems.
- Job description is broad and keyword-heavy.

Characteristics:
- Clear standard sections.
- Strong keyword alignment (e.g., `Python`, `LLM`, `RAG`, `Reinforcement Learning`, `MLOps`).
- Simple formatting, no complex visual layout.

### 2) Technical-Focused Resume
Use when:
- Role is engineering/research heavy.
- Interviewers are likely senior engineers or ML practitioners.

Characteristics:
- More implementation depth.
- Includes methods, tooling, evaluation approach, and constraints.
- Emphasizes reproducibility and system design decisions.

### 3) Executive-Focused Resume
Use when:
- Role requires ownership, product thinking, or cross-functional leadership.
- Company emphasizes outcomes and business impact.

Characteristics:
- Focus on scope, prioritization, decision-making.
- Highlights measurable outcomes, collaboration, and execution.
- Less low-level detail, more strategic framing.

## One-Resume-Per-Posting Workflow
1. Read the job description and identify required skills/keywords.
2. Choose **one** primary resume style (ATS / Technical / Executive).
3. Pull relevant achievements from `testPM3.json`.
4. Rewrite bullets to match role language and priorities.
5. Keep only the most relevant projects (usually 2–4).
6. Submit one targeted resume + optional portfolio/GitHub links.

## Bullet Writing Formula
Use this pattern:

**Action + System/Method + Scope + Outcome/Impact**

Example template:
- Built [system] using [tools/method], covering [scope], resulting in [impact/metric].

## Practical Rules
- Keep resume to 1 page for most industry roles.
- Prioritize evidence-backed claims.
- Mark unverified claims as placeholders in your master JSON until confirmed.
- Keep dates, titles, and tool names consistent across all documents.
- Never exaggerate metrics; use “self-reported” where needed.

## Quick Selection Heuristic
- If JD is portal-heavy and generic: **ATS**.
- If JD asks for modeling/infra/experimentation: **Technical**.
- If JD asks for ownership/cross-team execution: **Executive**.

## Suggested Next Step (When Ready)
Pick one real job posting and generate one final targeted resume version from `testPM3.json`.
