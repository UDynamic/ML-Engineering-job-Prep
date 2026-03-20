#!/usr/bin/env python3
"""One-command pipeline: raw txt -> normalized job posting md -> submission package."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from convert_raw_job_posts import convert_file
from submission_package_generator import run as generate_submission_package

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    if path.exists():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()


def parse_frontmatter(markdown_text: str) -> Dict[str, str]:
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index: Optional[int] = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break

    if end_index is None:
        return {}

    metadata: Dict[str, str] = {}
    for line in lines[1:end_index]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def normalize_fallback(value: str, fallback: str) -> str:
    clean = value.strip()
    clean = re.sub(r"\s+", " ", clean)
    return clean if clean else fallback


def extract_company_role(job_posting_md: Path, company_override: str | None, role_override: str | None) -> Tuple[str, str]:
    metadata = parse_frontmatter(job_posting_md.read_text(encoding="utf-8"))
    company = company_override or metadata.get("company_en", "")
    role = role_override or metadata.get("role_title", "")
    return (
        normalize_fallback(company, "Unknown Company"),
        normalize_fallback(role, "Unknown Role"),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate full submission outputs directly from raw text job postings."
    )
    parser.add_argument("--candidate", required=True, help="Your full name.")
    parser.add_argument("--raw-dir", default="jobPostings/raw", help="Directory containing raw .txt files.")
    parser.add_argument("--out-dir", default="jobPostings", help="Directory for normalized markdown files.")
    parser.add_argument("--pattern", default="*.txt", help="Glob pattern for raw files (default: *.txt).")
    parser.add_argument("--raw-file", help="Single raw .txt file to process (overrides --pattern).")
    parser.add_argument("--company", help="Optional manual company override for package generation.")
    parser.add_argument("--role", help="Optional manual role override for package generation.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = resolve_project_path(args.raw_dir)
    out_dir = resolve_project_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.raw_file:
        raw_files = [resolve_project_path(args.raw_file)]
    else:
        raw_files = sorted(raw_dir.glob(args.pattern))

    if not raw_files:
        print(f"No files matched {args.pattern} in {raw_dir}")
        return

    generated_jobs: List[Path] = []
    for raw_file in raw_files:
        if not raw_file.exists():
            raise FileNotFoundError(f"Raw job text not found: {raw_file}")
        job_posting_md = convert_file(raw_file=raw_file, out_dir=out_dir)
        generated_jobs.append(job_posting_md)
        print(f"Generated job posting markdown: {job_posting_md}")

    for job_posting_md in generated_jobs:
        company, role = extract_company_role(
            job_posting_md=job_posting_md,
            company_override=args.company,
            role_override=args.role,
        )
        paths = generate_submission_package(
            company=company,
            role=role,
            candidate=args.candidate,
            run_name=None,
            job_posting_md=str(job_posting_md),
        )
        print(f"Created markdown files: {paths.markdown_dir}")
        print(f"Created PDF files: {paths.pdf_dir}")
        print(f"Created zip package: {paths.zip_path}")

    print(f"Done. Processed {len(generated_jobs)} raw file(s).")


if __name__ == "__main__":
    main()
