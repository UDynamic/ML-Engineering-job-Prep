# Submission Package Generator

This project includes a no-dependency generator script that creates:

- `cover_letter.md` + `cover_letter.pdf`
- `resume_customized.md` + `resume_customized.pdf`
- `project_summary.md` + `project_summary.pdf`
- a zip bundle containing all files

## Run

```bash
python3 scripts/submission_package_generator.py \
  --company "Company Name" \
  --role "Machine Learning Engineer" \
  --candidate "Your Name" \
  --run-name "company_name"
```

## Output

Files are created under:

- `submissions/<run-name>/markdown/`
- `submissions/<run-name>/pdf/`
- `submissions/<run-name>/<run-name>_submission_package.zip`
