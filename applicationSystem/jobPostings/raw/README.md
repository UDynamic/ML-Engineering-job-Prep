# Raw Job Posts

Place raw text job postings here as `.txt` files.

## Recommended filename

Use this format so metadata is inferred from filename:

`YYYY-MM-DD_source_company_role_location.txt`

Example:

`2026-03-20_jobinja_pishro-ebtekar-danesh_data-science-engineer_tehran.txt`

## Convert to normalized markdown

```bash
python3 scripts/convert_raw_job_posts.py
```

Generated files are saved in `jobPostings/` as:

`YYYY-MM-DD_source_company_role_location.md`
