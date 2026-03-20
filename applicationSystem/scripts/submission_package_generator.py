#!/usr/bin/env python3
"""Generate a submission package: markdown files, PDFs, and zip archive.

No third-party dependencies required.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from zipfile import ZIP_DEFLATED, ZipFile


@dataclass
class PackagePaths:
    root: Path
    markdown_dir: Path
    pdf_dir: Path
    zip_path: Path


def sanitize_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_") or "submission"


def markdown_to_plain_text(markdown: str) -> str:
    text = markdown.replace("\r\n", "\n")

    text = re.sub(r"```[\s\S]*?```", lambda m: m.group(0).replace("```", ""), text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"^(#{1,6})\s*(.+)$", lambda m: f"{m.group(2).strip().upper()}\n{'=' * min(len(m.group(2).strip()), 60)}", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "• ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def wrap_plain_text(text: str, width: int = 92) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(line, width=width, break_long_words=False, break_on_hyphens=False)
        lines.extend(wrapped or [""])
    return lines


def escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf_objects(line_pages: list[list[str]]) -> list[str]:
    objects: list[str] = []
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")

    page_count = len(line_pages)
    kids = []
    for i in range(page_count):
        page_obj_num = 3 + i * 2
        kids.append(f"{page_obj_num} 0 R")
    objects.append(f"<< /Type /Pages /Count {page_count} /Kids [{' '.join(kids)}] >>")

    for i, lines in enumerate(line_pages):
        page_obj_num = 3 + i * 2
        content_obj_num = page_obj_num + 1

        page_obj = (
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 612 792] "
            f"/Contents {content_obj_num} 0 R "
            "/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> >> >> >>"
        )
        objects.append(page_obj)

        stream_lines = ["BT", "/F1 11 Tf", "14 TL", "72 742 Td"]
        for idx, line in enumerate(lines):
            if idx > 0:
                stream_lines.append("T*")
            stream_lines.append(f"({escape_pdf_text(line)}) Tj")
        stream_lines.append("ET")
        stream = "\n".join(stream_lines).encode("latin-1", errors="replace")
        content = f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream"
        objects.append(content.decode("latin-1"))

    return objects


def write_simple_pdf(text: str, output_path: Path) -> None:
    wrapped_lines = wrap_plain_text(text)
    lines_per_page = 48
    pages = [wrapped_lines[i:i + lines_per_page] for i in range(0, len(wrapped_lines), lines_per_page)] or [[""]]

    objects = build_pdf_objects(pages)

    pdf = bytearray(b"%PDF-1.4\n")
    xref_offsets = [0]

    for index, obj in enumerate(objects, start=1):
        xref_offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("latin-1"))
        pdf.extend(obj.encode("latin-1"))
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(xref_offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in xref_offsets[1:]:
        pdf.extend(f"{offset:010} 00000 n \n".encode("latin-1"))

    trailer = (
        f"trailer\n<< /Size {len(xref_offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF\n"
    )
    pdf.extend(trailer.encode("latin-1"))

    output_path.write_bytes(pdf)


def build_templates(company: str, role: str, candidate: str) -> dict[str, str]:
    today = datetime.now().strftime("%B %d, %Y")

    return {
        "cover_letter.md": f"""# Cover Letter

{today}

Hiring Team  
{company}

Dear Hiring Team,

I am excited to apply for the {role} position at {company}. I bring practical machine learning engineering experience across data pipelines, model development, and production-ready deployment workflows.

In recent projects, I have delivered end-to-end systems that include data preparation, model training, evaluation, and operational monitoring. I focus on building reliable ML solutions with clean interfaces, measurable performance, and maintainable code.

I would value the opportunity to contribute this execution-focused mindset to {company}. Thank you for your time and consideration.

Sincerely,  
{candidate}
""",
        "resume_customized.md": f"""# {candidate} — Resume (Customized)

## Target Role
- {role} at {company}

## Summary
- Machine Learning Engineer focused on production ML systems, robust data workflows, and practical model iteration.
- Comfortable owning the lifecycle from experimentation to deployment.

## Core Skills
- Python, SQL, feature engineering, model evaluation
- MLOps workflows, reproducibility, monitoring
- API integration, automation, and tooling

## Experience Highlights
- Built and iterated ML pipelines with clear evaluation criteria and reproducible runs.
- Improved system reliability through input validation, better observability, and cleaner interfaces.
- Collaborated across product and engineering constraints to deliver measurable outcomes.

## Projects
- End-to-end ML application systems for role-targeted submissions.
- Workflow automation scripts for packaging, reporting, and review.

## Links
- GitHub: <add-link>
- Portfolio: <add-link>
- LinkedIn: <add-link>
""",
        "project_summary.md": f"""# Project Summary

## Why This Package Exists
- Provide a concise overview of ML engineering work relevant to {role} at {company}.

## Project 1: Application Submission System
- Designed a structured workflow for role-specific application materials.
- Automated generation of markdown artifacts and final delivery bundles.
- Reduced manual handoff time and improved consistency across submissions.

## Project 2: Model Workflow Template
- Created reusable conventions for data preparation, training, and evaluation.
- Emphasized reproducibility and clear metrics for decision-making.

## Project 3: Deployment Readiness Practices
- Documented practical checks for reliability, logging, and maintainability.
- Focused on production-minded engineering tradeoffs.

## Outcome
- Demonstrates practical execution, automation mindset, and end-to-end ownership.
""",
    }


def resolve_output_folder(run_name: Optional[str], company: str, job_posting_md: Optional[str]) -> str:
    if job_posting_md:
        job_posting_path = Path(job_posting_md)
        if not job_posting_path.exists():
            raise FileNotFoundError(f"Job posting markdown not found: {job_posting_md}")
        if job_posting_path.suffix.lower() != ".md":
            raise ValueError("--job-posting-md must point to a markdown (.md) file")
        return sanitize_name(job_posting_path.stem)

    return sanitize_name(run_name or company)


def prepare_paths(base_dir: Path, company: str, run_name: str | None, job_posting_md: Optional[str]) -> PackagePaths:
    folder = resolve_output_folder(run_name=run_name, company=company, job_posting_md=job_posting_md)
    root = base_dir / folder
    markdown_dir = root / "markdown"
    pdf_dir = root / "pdf"
    zip_path = root / f"{folder}_submission_package.zip"

    markdown_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    return PackagePaths(root=root, markdown_dir=markdown_dir, pdf_dir=pdf_dir, zip_path=zip_path)


def create_zip(paths: PackagePaths) -> None:
    with ZipFile(paths.zip_path, "w", ZIP_DEFLATED) as archive:
        for md_file in sorted(paths.markdown_dir.glob("*.md")):
            archive.write(md_file, arcname=f"markdown/{md_file.name}")
        for pdf_file in sorted(paths.pdf_dir.glob("*.pdf")):
            archive.write(pdf_file, arcname=f"pdf/{pdf_file.name}")


def run(company: str, role: str, candidate: str, run_name: str | None, job_posting_md: Optional[str]) -> PackagePaths:
    base_dir = Path("submissions")
    paths = prepare_paths(base_dir=base_dir, company=company, run_name=run_name, job_posting_md=job_posting_md)

    templates = build_templates(company=company, role=role, candidate=candidate)

    for file_name, markdown_content in templates.items():
        md_path = paths.markdown_dir / file_name
        md_path.write_text(markdown_content.strip() + "\n", encoding="utf-8")

        plain = markdown_to_plain_text(markdown_content)
        pdf_path = paths.pdf_dir / file_name.replace(".md", ".pdf")
        write_simple_pdf(plain, pdf_path)

    create_zip(paths)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate markdown, PDFs, and zip package for job submissions.")
    parser.add_argument("--company", required=True, help="Target company name.")
    parser.add_argument("--role", required=True, help="Target role title.")
    parser.add_argument("--candidate", required=True, help="Your full name.")
    parser.add_argument("--run-name", help="Optional output folder name under submissions/ (ignored when --job-posting-md is set).")
    parser.add_argument("--job-posting-md", help="Path to job posting markdown in jobPostings/. Output folder and zip use this filename stem.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = run(
        company=args.company,
        role=args.role,
        candidate=args.candidate,
        run_name=args.run_name,
        job_posting_md=args.job_posting_md,
    )

    print(f"Created markdown files: {paths.markdown_dir}")
    print(f"Created PDF files: {paths.pdf_dir}")
    print(f"Created zip package: {paths.zip_path}")


if __name__ == "__main__":
    main()
