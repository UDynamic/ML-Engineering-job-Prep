# Application System — Integrated Onboarding Guide

This is the **single source of truth** for this project’s workflow.
If a future session has no chat history, reading this file should be enough to continue end-to-end execution.

---

## 1) Mission

Convert raw job posting text into a complete submission package with consistent, repeatable commands:

1. `raw .txt` job posting intake
2. normalized `jobPostings/*.md` generation
3. submission artifact generation (`markdown/`, `pdf/`, `.zip`)

---

## 2) Repository Layout

From `applicationSystem/`:

- `README.md` (this file)
- `docs/`
  - `application_strategy.md`
  - `jobPostingFormat.md`
  - `packageGenerator.md` (pointer to this README)
  - `textToMdInstructions.md` (pointer to this README)
  - `personalMappings/`
- `jobPostings/`
  - `raw/` for input `.txt`
  - normalized posting `.md` files at `jobPostings/*.md`
- `scripts/`
  - `convert_raw_job_posts.py`
  - `submission_package_generator.py`
  - `raw_to_submission_pipeline.py`
- `submissions/`
  - generated packages, one folder per posting/run

---

## 3) End-to-End Process

### Step A — Add raw job post text

Place `.txt` files in `jobPostings/raw/`.

Recommended filename format for better metadata extraction:

`YYYY-MM-DD_source_company_role_location.txt`

Example:

`2026-03-20_jobinja_pishro-ebtekar-danesh_data-science-engineer_tehran.txt`

### Step B — Normalize raw text into job posting markdown

Script: `scripts/convert_raw_job_posts.py`

- Reads raw text files
- Extracts metadata from filename/body/frontmatter
- Applies fallbacks when fields are missing
- Writes canonical posting markdown files in `jobPostings/`

### Step C — Build submission package from a posting

Script: `scripts/submission_package_generator.py`

- Generates `cover_letter`, `resume_customized`, `project_summary`
- Creates both markdown and PDF versions
- Bundles outputs into a zip file

### Step D — One-command pipeline (daily default)

Script: `scripts/raw_to_submission_pipeline.py`

Runs full chain:

- `jobPostings/raw/*.txt` → `jobPostings/*.md`
- each generated posting → `submissions/<run>/markdown`, `submissions/<run>/pdf`, `<run>_submission_package.zip`

---

## 4) Command Reference (Complete)

Run all commands from `applicationSystem/` root.

### 4.1 Discover options

```bash
python3 scripts/convert_raw_job_posts.py --help
python3 scripts/submission_package_generator.py --help
python3 scripts/raw_to_submission_pipeline.py --help
```

### 4.2 Raw text → normalized markdown only

```bash
python3 scripts/convert_raw_job_posts.py
```

With explicit flags:

```bash
python3 scripts/convert_raw_job_posts.py \
  --raw-dir "jobPostings/raw" \
  --out-dir "jobPostings" \
  --pattern "*.txt"
```

### 4.3 Posting markdown → submission package only

Preferred (`--job-posting-md` controls run naming):

```bash
python3 scripts/submission_package_generator.py \
  --company "Company Name" \
  --role "Machine Learning Engineer" \
  --candidate "Your Name" \
  --job-posting-md "jobPostings/YYYY-MM-DD_source_company_role_location.md"
```

Fallback mode:

```bash
python3 scripts/submission_package_generator.py \
  --company "Company Name" \
  --role "Machine Learning Engineer" \
  --candidate "Your Name" \
  --run-name "company_name"
```

### 4.4 One-command full pipeline (recommended)

All raw files:

```bash
python3 scripts/raw_to_submission_pipeline.py \
  --candidate "Your Name"
```

Single raw file:

```bash
python3 scripts/raw_to_submission_pipeline.py \
  --candidate "Your Name" \
  --raw-file "jobPostings/raw/some_post.txt"
```

Single file + manual company/role override:

```bash
python3 scripts/raw_to_submission_pipeline.py \
  --candidate "Your Name" \
  --raw-file "jobPostings/raw/some_post.txt" \
  --company "Company Name" \
  --role "Machine Learning Engineer"
```

---

## 5) Process Contracts (Inputs / Outputs)

### `scripts/convert_raw_job_posts.py`

- **Input:** `jobPostings/raw/*.txt`
- **Output:** `jobPostings/YYYY-MM-DD_source_company_role_location.md`
- **Duplicate naming:** adds `_2`, `_3`, ... when needed

### `scripts/submission_package_generator.py`

- **Input:** company, role, candidate (+ optional `--job-posting-md`)
- **Output:**
  - `submissions/<run>/markdown/*.md`
  - `submissions/<run>/pdf/*.pdf`
  - `submissions/<run>/<run>_submission_package.zip`
- **Run folder naming priority:**
  1. stem of `--job-posting-md`
  2. `--run-name`
  3. sanitized company name

### `scripts/raw_to_submission_pipeline.py`

- **Input:** raw files + `--candidate`
- **Output:** both normalized posting markdown + complete submission package
- **Company/role source priority:**
  1. CLI override (`--company`, `--role`)
  2. frontmatter in generated posting markdown
  3. fallback `Unknown Company` / `Unknown Role`

---

## 6) Working Rules

- Use `raw_to_submission_pipeline.py` for normal daily operation.
- Use the two lower-level scripts for debugging or partial reruns.
- Keep raw inputs only in `jobPostings/raw/`.
- Treat `submissions/` as generated artifacts.
- Validate with `--help` first when unsure about flags.

---

## 7) Quick Start

If you just want the full flow:

```bash
python3 scripts/raw_to_submission_pipeline.py --candidate "Your Name"
```

Then inspect outputs:

- `jobPostings/*.md`
- `submissions/<generated-folder>/markdown/`
- `submissions/<generated-folder>/pdf/`
- `submissions/<generated-folder>/<generated-folder>_submission_package.zip`

---

## 8) Session Handoff Checklist

1. Read `README.md` at project root.
2. Confirm objective: convert-only or full package.
3. Run relevant `--help` command(s).
4. Execute the command(s) from Section 4.
5. Verify outputs in `jobPostings/` and `submissions/`.

