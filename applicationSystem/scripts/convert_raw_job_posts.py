#!/usr/bin/env python3
"""Convert raw job posting text files to normalized markdown files.

Input:  jobPostings/raw/*.txt
Output: jobPostings/YYYY-MM-DD_source_company_role_location.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

FILENAME_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})_(?P<source>[^_]+)_(?P<company>[^_]+)_(?P<role>[^_]+)_(?P<location>[^_]+)$"
)

TECH_KEYWORDS = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "scipy",
    "tensorflow",
    "pytorch",
    "sklearn",
    "machine learning",
    "data science",
    "data engineer",
    "fastapi",
    "docker",
    "aws",
    "gcp",
    "azure",
    "kubernetes",
    "git",
]

SOURCE_CANONICAL = {
    "jobinja": "jobinja.ir",
    "linkedin": "linkedin.com",
    "quera": "quera.org",
    "jabama": "jabama.com",
}

SECTION_KEYS = {
    "responsibilities": ["responsibilities", "responsibility", "duties", "job duties", "وظایف", "مسئولیت"],
    "requirements": ["requirements", "qualifications", "must have", "نیازمندی", "شرایط احراز", "الزامات"],
    "preferred": ["preferred", "nice to have", "plus", "مزیت", "ترجیح", "آشنایی با"],
    "conditions": ["working conditions", "employment", "work type", "hours", "benefits", "شرایط کار", "مزایا"],
    "skills": ["skills", "required skills", "مهارت", "تخصص"],
}


def slugify(value: str, fallback: str = "unknown") -> str:
    value = value.strip().lower().replace(" ", "-")
    value = re.sub(r"[^\w\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


def detect_language(text: str) -> str:
    has_fa = bool(re.search(r"[\u0600-\u06FF]", text))
    has_latin = bool(re.search(r"[A-Za-z]", text))
    if has_fa and has_latin:
        return "mixed"
    if has_fa:
        return "fa"
    return "en"


def parse_frontmatter_like(raw_text: str) -> Tuple[Dict[str, str], str]:
    lines = raw_text.splitlines()
    metadata: Dict[str, str] = {}

    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            for line in lines[1:end]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"')
            return metadata, "\n".join(lines[end + 1 :]).strip()

    return metadata, raw_text.strip()


def parse_filename_metadata(file_path: Path) -> Dict[str, str]:
    stem = file_path.stem
    match = FILENAME_RE.match(stem)
    if match:
        return {
            "saved_at": match.group("date"),
            "source": match.group("source"),
            "company_en": match.group("company").replace("-", " ").title(),
            "role_title": match.group("role").replace("-", " ").title(),
            "location_city": match.group("location").replace("-", " ").title(),
            "location_province": match.group("location").replace("-", " ").title(),
            "company_slug": slugify(match.group("company")),
            "role_slug": slugify(match.group("role")),
            "location_slug": slugify(match.group("location")),
            "source_slug": slugify(match.group("source")),
        }

    today = dt.date.today().isoformat()
    stem_slug = slugify(stem, fallback="job-post")
    return {
        "saved_at": today,
        "source": "unknown",
        "company_en": "Unknown Company",
        "role_title": "Unknown Role",
        "location_city": "Unknown",
        "location_province": "Unknown",
        "company_slug": "unknown-company",
        "role_slug": stem_slug,
        "location_slug": "unknown",
        "source_slug": "unknown",
    }


def collect_bullets(lines: Iterable[str]) -> List[str]:
    bullets: List[str] = []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith(("-", "*", "•")):
            clean = clean[1:].strip()
        bullets.append(clean)
    return bullets


def split_sections(body: str) -> Dict[str, List[str]]:
    lines = [line.rstrip() for line in body.splitlines()]
    normalized = [line.lower().strip() for line in lines]

    section_positions: Dict[str, int] = {}
    for idx, nline in enumerate(normalized):
        for key, markers in SECTION_KEYS.items():
            if any(marker in nline for marker in markers):
                section_positions.setdefault(key, idx)

    boundaries = sorted(section_positions.items(), key=lambda x: x[1])
    extracted: Dict[str, List[str]] = {k: [] for k in SECTION_KEYS}

    for pos, (section_name, start_idx) in enumerate(boundaries):
        end_idx = len(lines)
        if pos + 1 < len(boundaries):
            end_idx = boundaries[pos + 1][1]
        chunk = lines[start_idx + 1 : end_idx]
        extracted[section_name] = collect_bullets(chunk)

    # Fallback heuristics when headings are missing.
    all_bullets = collect_bullets(lines)
    if not extracted["responsibilities"]:
        extracted["responsibilities"] = [
            b
            for b in all_bullets
            if re.search(r"\b(build|develop|design|maintain|analy|lead|implement|respons)\b", b, re.I)
            or re.search(r"(توسعه|طراحی|پیاده|تحلیل|مسئول)", b)
        ][:10]

    if not extracted["requirements"]:
        extracted["requirements"] = [
            b
            for b in all_bullets
            if re.search(r"\b(require|must|experience|degree|proficient|skill|qualification)\b", b, re.I)
            or re.search(r"(نیاز|تسلط|سابقه|مدرک|مهارت|شرایط)", b)
        ][:10]

    if not extracted["preferred"]:
        extracted["preferred"] = [
            b
            for b in all_bullets
            if re.search(r"\b(preferred|plus|nice to have|familiar)\b", b, re.I)
            or re.search(r"(مزیت|ترجیح|آشنایی)", b)
        ][:8]

    if not extracted["conditions"]:
        extracted["conditions"] = [
            b
            for b in all_bullets
            if re.search(r"\b(remote|hybrid|on-site|full[- ]time|part[- ]time|benefit|hour|schedule)\b", b, re.I)
            or re.search(r"(دورکاری|حضوری|ترکیبی|تمام[\s\-]?وقت|پاره[\s\-]?وقت|ساعت|مزایا)", b)
        ][:8]

    if not extracted["skills"]:
        text_lower = body.lower()
        matched = [k for k in TECH_KEYWORDS if k in text_lower]
        extracted["skills"] = matched[:12]

    return extracted


def infer_work_type(text: str) -> str:
    lower = text.lower()
    if "hybrid" in lower or "ترکیبی" in text:
        return "hybrid"
    if "remote" in lower or "دورکار" in text or "دورکاری" in text:
        return "remote"
    if "on-site" in lower or "onsite" in lower or "حضوری" in text:
        return "on-site"
    return "on-site"


def infer_employment_type(text: str) -> str:
    lower = text.lower()
    if "part-time" in lower or "part time" in lower or "پاره وقت" in text:
        return "part-time"
    if "contract" in lower or "پروژه" in text:
        return "contract"
    return "full-time"


def extract_url(text: str) -> str:
    match = re.search(r"https?://\S+", text)
    return match.group(0).strip() if match else ""


def generate_summary(body: str) -> List[str]:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    non_heading_lines = [
        line
        for line in lines
        if not re.match(r"^(#|\*\*|Responsibilities|Requirements|Preferred|Working Conditions|Skills)\b", line, re.I)
    ]
    if non_heading_lines:
        return non_heading_lines[:4]
    return ["Raw posting imported from text file; review and refine this summary."]


def list_to_md(items: List[str], fallback: str = "...") -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in cleaned)


def render_markdown(metadata: Dict[str, str], body: str) -> str:
    sections = split_sections(body)
    summary_lines = generate_summary(body)

    skills = sections["skills"][:10]
    must_have = skills[:6] if skills else ["...", "..."]
    strong = sections["preferred"][:4] if sections["preferred"] else ["..."]

    return f"""---
source: {metadata.get('source', 'unknown')}
url: \"{metadata.get('url', '')}\"
saved_at: {metadata.get('saved_at', dt.date.today().isoformat())}
language: {metadata.get('language', 'mixed')}

company_fa: \"{metadata.get('company_fa', '')}\"
company_en: \"{metadata.get('company_en', '')}\"
company_size: \"{metadata.get('company_size', '')}\"
company_website: \"{metadata.get('company_website', '')}\"
company_intro: \"{metadata.get('company_intro', '')}\"

role_title: \"{metadata.get('role_title', '')}\"
role_category: \"{metadata.get('role_category', '')}\"
location_city: \"{metadata.get('location_city', '')}\"
location_province: \"{metadata.get('location_province', '')}\"
work_type: {metadata.get('work_type', 'on-site')}
employment_type: {metadata.get('employment_type', 'full-time')}
seniority_min_experience: \"{metadata.get('seniority_min_experience', '')}\"
salary: \"{metadata.get('salary', '')}\"

required_gender: \"{metadata.get('required_gender', '')}\"
military_status_requirement: \"{metadata.get('military_status_requirement', '')}\"
minimum_education: \"{metadata.get('minimum_education', '')}\"

status: {metadata.get('status', 'unknown')}
---

## Job Summary
{chr(10).join(summary_lines)}

## Responsibilities
{list_to_md(sections['responsibilities'])}

## Requirements
{list_to_md(sections['requirements'])}

## Preferred Qualifications
{list_to_md(sections['preferred'])}

## Personal & Ethical Qualities
- ...

## Working Conditions
{list_to_md(sections['conditions'])}

## Required Skills (as posted)
{list_to_md(skills)}

## Resume Tailoring Signals
- must_have_keywords:
{chr(10).join(f'  - {item}' for item in must_have)}
- strong_keywords:
{chr(10).join(f'  - {item}' for item in strong)}
- evidence_to_show_from_personal_map:
  - ...

## Notes
- Generated from `jobPostings/raw` text by script; review and refine ambiguous fields.
"""


def build_output_filename(meta: Dict[str, str]) -> str:
    saved_at = meta.get("saved_at", dt.date.today().isoformat())
    source = slugify(meta.get("source_slug") or meta.get("source", "unknown"))
    company = slugify(meta.get("company_slug") or meta.get("company_en", "unknown-company"))
    role = slugify(meta.get("role_slug") or meta.get("role_title", "unknown-role"))
    location = slugify(meta.get("location_slug") or meta.get("location_city", "unknown"))
    return f"{saved_at}_{source}_{company}_{role}_{location}.md"


def merge_metadata(file_meta: Dict[str, str], frontmatter_meta: Dict[str, str], body: str) -> Dict[str, str]:
    merged = {**file_meta, **frontmatter_meta}
    source_value = merged.get("source", "unknown").strip().lower()
    merged["source"] = SOURCE_CANONICAL.get(source_value, source_value)
    merged["url"] = frontmatter_meta.get("url", extract_url(body))
    merged["language"] = frontmatter_meta.get("language", detect_language(body))
    merged["work_type"] = frontmatter_meta.get("work_type", infer_work_type(body))
    merged["employment_type"] = frontmatter_meta.get("employment_type", infer_employment_type(body))
    merged["status"] = frontmatter_meta.get("status", "open")
    return merged


def convert_file(raw_file: Path, out_dir: Path) -> Path:
    raw_text = raw_file.read_text(encoding="utf-8")
    frontmatter_meta, body = parse_frontmatter_like(raw_text)
    file_meta = parse_filename_metadata(raw_file)
    merged_meta = merge_metadata(file_meta, frontmatter_meta, body)

    output_name = build_output_filename(merged_meta)
    output_path = out_dir / output_name

    markdown = render_markdown(merged_meta, body)
    output_path.write_text(markdown.strip() + "\n", encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert raw job posting text files to normalized markdown files.")
    parser.add_argument("--raw-dir", default="jobPostings/raw", help="Directory containing raw .txt job postings.")
    parser.add_argument("--out-dir", default="jobPostings", help="Directory where normalized .md files are written.")
    parser.add_argument("--pattern", default="*.txt", help="Glob pattern for raw files (default: *.txt).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(raw_dir.glob(args.pattern))
    if not raw_files:
        print(f"No files matched {args.pattern} in {raw_dir}")
        return

    generated: List[Path] = []
    for raw_file in raw_files:
        output = convert_file(raw_file, out_dir)
        generated.append(output)
        print(f"Generated: {output}")

    print(f"Done. Generated {len(generated)} file(s).")


if __name__ == "__main__":
    main()
