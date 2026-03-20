# Submission Package Generator

This project includes a no-dependency generator script that creates:

- `cover_letter.md` + `cover_letter.pdf`
- `resume_customized.md` + `resume_customized.pdf`
- `project_summary.md` + `project_summary.pdf`
- a zip bundle containing all files

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
