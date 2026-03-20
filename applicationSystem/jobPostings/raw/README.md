# Raw Job Posts

Place raw text job postings here as `.txt` files.
You can use any filename (for example: `New Text Document.txt`).

## Optional filename (best metadata)

If you use this format, metadata is inferred from filename:

`YYYY-MM-DD_source_company_role_location.txt`

Example:

`2026-03-20_jobinja_pishro-ebtekar-danesh_data-science-engineer_tehran.txt`

## Convert to normalized markdown

```bash
python3 scripts/convert_raw_job_posts.py
```

Generated files are saved in `jobPostings/` as:

`YYYY-MM-DD_source_company_role_location.md`

If metadata is missing in the raw text, the script uses safe fallbacks and still generates valid files.
