# Submission Package Generator

This project includes a no-dependency generator script that creates:

- `cover_letter.md` + `cover_letter.pdf`
- `resume_customized.md` + `resume_customized.pdf`
- `project_summary.md` + `project_summary.pdf`
- a zip bundle containing all files

## One Command: Raw Text to Full Submission Package

```bash
python3 scripts/raw_to_submission_pipeline.py \
  --candidate "Your Name"
```

This command runs the complete flow:

- `jobPostings/raw/*.txt` -> normalized `jobPostings/*.md`
- generated job posting markdown -> submission `markdown/`, `pdf/`, and `.zip` under `submissions/`

You can also target a single file:

```bash
python3 scripts/raw_to_submission_pipeline.py \
  --candidate "Your Name" \
  --raw-file "jobPostings/raw/2026-03-20_jobinja_company_role_tehran.txt"
```

## Recommended Run (matches job posting filename format)

```bash
python3 scripts/submission_package_generator.py \
  --company "Company Name" \
  --role "Machine Learning Engineer" \
  --candidate "Your Name" \
  --job-posting-md "jobPostings/YYYY-MM-DD_source_company_role_location.md"
```

When `--job-posting-md` is provided, the output folder name is the same as that job posting markdown filename (without `.md`).

## Fallback Run

```bash
python3 scripts/submission_package_generator.py \
  --company "Company Name" \
  --role "Machine Learning Engineer" \
  --candidate "Your Name" \
  --run-name "company_name"
```

## Output

Files are created under:

- `submissions/<job-posting-stem-or-run-name>/markdown/`
- `submissions/<job-posting-stem-or-run-name>/pdf/`
- `submissions/<job-posting-stem-or-run-name>/<job-posting-stem-or-run-name>_submission_package.zip`
