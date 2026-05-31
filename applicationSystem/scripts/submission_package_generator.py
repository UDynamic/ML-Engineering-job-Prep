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

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    cwd_candidate = (Path.cwd() / path).resolve()
    if cwd_candidate.exists():
        return cwd_candidate
    return (PROJECT_ROOT / path).resolve()


@dataclass
class PackagePaths:
    root: Path
    markdown_dir: Path
    pdf_dir: Path
    zip_path: Path


@dataclass
class TextBlock:
    kind: str
    text: str
    level: int = 0


@dataclass
class StyledLine:
    text: str
    font_key: str
    font_size: float
    leading: float
    indent: float = 0.0
    color: tuple[float, float, float] = (0.12, 0.12, 0.12)
    spacing_before: float = 0.0
    spacing_after: float = 0.0
    draw_rule_after: bool = False


@dataclass
class JobPostingContext:
    company: str
    role: str
    summary: list[str]
    responsibilities: list[str]
    requirements: list[str]
    preferred: list[str]
    skills: list[str]
    work_conditions: list[str]


def sanitize_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_") or "submission"


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def role_in_english(role: str) -> str:
    english_tokens = re.findall(r"[A-Za-z][A-Za-z0-9/+ -]*", role)
    return normalize_whitespace(english_tokens[0]) if english_tokens else role


def trim_bullet(text: str, max_length: int = 140) -> str:
    clean = normalize_whitespace(text.lstrip("-• ").strip())
    if len(clean) <= max_length:
        return clean
    truncated = clean[: max_length - 3].rsplit(" ", 1)[0].rstrip(",;:.")
    return f"{truncated}..."


def choose_preferred_lines(items: list[str], *, require_latin: bool = False, max_items: int = 3) -> list[str]:
    selected: list[str] = []
    for item in items:
        clean = normalize_whitespace(item)
        if not clean:
            continue
        if require_latin and not re.search(r"[A-Za-z]", clean):
            continue
        selected.append(clean)
        if len(selected) >= max_items:
            break
    return selected


def summarize_requirement(text: str) -> str:
    clean = trim_bullet(text, 96)
    clean = re.sub(r"^(demonstrate|exhibit|lead|design and implement|work closely with)\s+", "", clean, flags=re.IGNORECASE)
    return clean[:1].lower() + clean[1:] if clean else clean


def read_job_posting_context(job_posting_md: Optional[str], company: str, role: str) -> JobPostingContext:
    empty_context = JobPostingContext(
        company=company,
        role=role,
        summary=[],
        responsibilities=[],
        requirements=[],
        preferred=[],
        skills=[],
        work_conditions=[],
    )
    if not job_posting_md:
        return empty_context

    path = resolve_project_path(job_posting_md)
    if not path.exists():
        return empty_context

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    body_start = 0

    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                body_start = index + 1
                break
            if ":" in lines[index]:
                key, value = lines[index].split(":", 1)
                metadata[key.strip()] = value.strip().strip('"')

    sections: dict[str, list[str]] = {}
    current_section: Optional[str] = None
    for raw_line in lines[body_start:]:
        stripped = raw_line.strip()
        heading_match = re.match(r"^##\s+(.+)$", stripped)
        if heading_match:
            current_section = heading_match.group(1).strip().lower()
            sections[current_section] = []
            continue
        if current_section and stripped.startswith("- "):
            sections[current_section].append(stripped[2:].strip())
        elif current_section and stripped:
            sections[current_section].append(stripped)

    return JobPostingContext(
        company=metadata.get("company_en", company) or company,
        role=metadata.get("role_title", role) or role,
        summary=sections.get("job summary", [])[:4],
        responsibilities=sections.get("responsibilities", [])[:5],
        requirements=sections.get("requirements", [])[:6],
        preferred=sections.get("preferred qualifications", [])[:4],
        skills=sections.get("required skills (as posted)", [])[:6],
        work_conditions=sections.get("working conditions", [])[:5],
    )


def strip_markdown_inline(text: str) -> str:
    cleaned = text.replace("\r\n", "\n")
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1 (\2)", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", cleaned)
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    cleaned = re.sub(r"_([^_]+)_", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def parse_markdown_blocks(markdown: str) -> list[TextBlock]:
    blocks: list[TextBlock] = []
    in_code_block = False

    for raw_line in markdown.replace("\r\n", "\n").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            code_text = line if line else " "
            blocks.append(TextBlock(kind="paragraph", text=code_text))
            continue

        if not stripped:
            blocks.append(TextBlock(kind="blank", text=""))
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            blocks.append(
                TextBlock(
                    kind="heading",
                    text=strip_markdown_inline(heading_match.group(2)),
                    level=len(heading_match.group(1)),
                )
            )
            continue

        bullet_match = re.match(r"^\s*[-*+]\s+(.+)$", line)
        if bullet_match:
            blocks.append(TextBlock(kind="bullet", text=strip_markdown_inline(bullet_match.group(1))))
            continue

        number_match = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if number_match:
            blocks.append(TextBlock(kind="bullet", text=strip_markdown_inline(number_match.group(1))))
            continue

        quote_match = re.match(r"^\s*>\s?(.+)$", line)
        if quote_match:
            blocks.append(TextBlock(kind="paragraph", text=strip_markdown_inline(quote_match.group(1))))
            continue

        blocks.append(TextBlock(kind="paragraph", text=strip_markdown_inline(stripped)))

    return blocks


def estimate_text_width(text: str, font_size: float, font_key: str) -> float:
    if not text:
        return 0.0

    width_units = 0.0
    for char in text:
        if char in "ilI.,' ":
            width_units += 0.35
        elif char in "mwMW@#%&":
            width_units += 0.9
        elif ord(char) > 127:
            width_units += 1.0
        else:
            width_units += 0.58

    font_factor = 0.52 if font_key.startswith("F1") else 0.5
    if font_key == "F3":
        font_factor = 0.54
    return width_units * font_size * font_factor


def wrap_styled_text(text: str, font_size: float, font_key: str, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        if estimate_text_width(candidate, font_size, font_key) <= max_width:
            current = candidate
            continue

        if estimate_text_width(word, font_size, font_key) > max_width:
            rough_width = max(8, int(max_width / max(font_size * 0.32, 1)))
            split_parts = textwrap.wrap(word, width=rough_width, break_long_words=True, break_on_hyphens=True)
            lines.append(current)
            lines.extend(split_parts[:-1])
            current = split_parts[-1]
            continue

        lines.append(current)
        current = word

    lines.append(current)
    return lines


def block_to_lines(block: TextBlock) -> list[StyledLine]:
    if block.kind == "blank":
        return [StyledLine(text="", font_key="F1", font_size=11.5, leading=8.0, spacing_after=4.0)]

    if block.kind == "heading":
        if block.level == 1:
            return [
                StyledLine(
                    text=block.text,
                    font_key="F2",
                    font_size=20.0,
                    leading=24.0,
                    color=(0.08, 0.16, 0.32),
                    spacing_before=4.0,
                    spacing_after=8.0,
                    draw_rule_after=True,
                )
            ]
        return [
            StyledLine(
                text=block.text,
                font_key="F2",
                font_size=13.0,
                leading=17.0,
                color=(0.14, 0.20, 0.34),
                spacing_before=10.0,
                spacing_after=3.0,
            )
        ]

    if block.kind == "bullet":
        return [
            StyledLine(
                text=f"• {block.text}",
                font_key="F1",
                font_size=11.5,
                leading=16.0,
                indent=16.0,
                color=(0.14, 0.14, 0.14),
                spacing_after=1.0,
            )
        ]

    text = block.text
    if re.match(r"^(dear|sincerely|thank you)", text, flags=re.IGNORECASE):
        return [
            StyledLine(
                text=text,
                font_key="F1",
                font_size=11.5,
                leading=16.0,
                spacing_before=6.0,
                spacing_after=1.0,
            )
        ]

    if re.match(r"^[A-Za-z]+\s+\d{1,2},\s+\d{4}$", text):
        return [
            StyledLine(
                text=text,
                font_key="F3",
                font_size=10.5,
                leading=14.0,
                color=(0.38, 0.38, 0.38),
                spacing_after=8.0,
            )
        ]

    return [
        StyledLine(
            text=text,
            font_key="F1",
            font_size=11.5,
            leading=16.0,
            color=(0.14, 0.14, 0.14),
            spacing_after=3.0,
        )
    ]


def escape_pdf_text(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("–", "-")
        .replace("—", "-")
        .replace("•", "-")
    )

def build_pdf_objects(page_streams: list[str]) -> list[str]:
    objects: list[str] = []
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")

    page_count = len(page_streams)
    kids = []
    for i in range(page_count):
        page_obj_num = 3 + i * 2
        kids.append(f"{page_obj_num} 0 R")
    objects.append(f"<< /Type /Pages /Count {page_count} /Kids [{' '.join(kids)}] >>")

    font_resources = (
        "/Resources << /Font << "
        "/F1 << /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >> "
        "/F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> "
        "/F3 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> "
        ">> >>"
    )

    for i, stream_text in enumerate(page_streams):
        page_obj_num = 3 + i * 2
        content_obj_num = page_obj_num + 1

        page_obj = (
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 612 792] "
            f"/Contents {content_obj_num} 0 R "
            f"{font_resources} >>"
        )
        objects.append(page_obj)

        stream = stream_text.encode("latin-1", errors="replace")
        content = f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"\nendstream"
        objects.append(content.decode("latin-1"))

    return objects


def styled_lines_from_markdown(markdown: str) -> list[StyledLine]:
    lines: list[StyledLine] = []
    for block in parse_markdown_blocks(markdown):
        lines.extend(block_to_lines(block))
    return lines


def paginate_styled_lines(lines: list[StyledLine]) -> list[list[tuple[StyledLine, str, float]]]:
    page_height = 792
    top_margin = 72
    bottom_margin = 54
    left_margin = 72
    right_margin = 72
    content_width = 612 - left_margin - right_margin

    pages: list[list[tuple[StyledLine, str, float]]] = [[]]
    current_y = page_height - top_margin

    for line in lines:
        available_width = content_width - line.indent
        wrapped_segments = wrap_styled_text(line.text, line.font_size, line.font_key, available_width)
        total_height = line.spacing_before + max(len(wrapped_segments), 1) * line.leading + line.spacing_after
        if line.draw_rule_after:
            total_height += 8.0

        if current_y - total_height < bottom_margin:
            pages.append([])
            current_y = page_height - top_margin

        current_y -= line.spacing_before
        for segment in wrapped_segments:
            pages[-1].append((line, segment, current_y))
            current_y -= line.leading

        if line.draw_rule_after:
            pages[-1].append(
                (
                    StyledLine(
                        text="__RULE__",
                        font_key=line.font_key,
                        font_size=line.font_size,
                        leading=0.0,
                        indent=0.0,
                        color=(0.84, 0.86, 0.90),
                    ),
                    "__RULE__",
                    current_y + 4.0,
                )
            )

        current_y -= line.spacing_after

    return [page for page in pages if page] or [[(StyledLine(text="", font_key="F1", font_size=11.5, leading=16.0), "", 720.0)]]


def page_to_stream(page_items: list[tuple[StyledLine, str, float]], page_number: int, page_count: int) -> str:
    left_margin = 72
    right_edge = 540
    commands = [
        "0.98 0.98 0.99 rg",
        "0 0 612 792 re f",
        "0.84 0.86 0.90 RG",
        "0.6 w",
        "72 756 m 540 756 l S",
    ]

    for style, segment, y in page_items:
        if segment == "__RULE__":
            commands.extend(
                [
                    f"{style.color[0]:.3f} {style.color[1]:.3f} {style.color[2]:.3f} RG",
                    "0.8 w",
                    f"{left_margin} {y:.2f} m {right_edge} {y:.2f} l S",
                ]
            )
            continue

        x = left_margin + style.indent
        commands.extend(
            [
                "BT",
                f"/{style.font_key} {style.font_size:.2f} Tf",
                f"{style.color[0]:.3f} {style.color[1]:.3f} {style.color[2]:.3f} rg",
                f"1 0 0 1 {x:.2f} {y:.2f} Tm",
                f"({escape_pdf_text(segment)}) Tj",
                "ET",
            ]
        )

    footer_y = 34
    commands.extend(
        [
            "BT",
            "/F3 9 Tf",
            "0.45 0.45 0.45 rg",
            f"1 0 0 1 72 {footer_y} Tm",
            f"(Submission package) Tj",
            "ET",
            "BT",
            "/F3 9 Tf",
            "0.45 0.45 0.45 rg",
            f"1 0 0 1 500 {footer_y} Tm",
            f"(Page {page_number} of {page_count}) Tj",
            "ET",
        ]
    )

    return "\n".join(commands)


def write_simple_pdf(markdown: str, output_path: Path) -> None:
    styled_lines = styled_lines_from_markdown(markdown)
    pages = paginate_styled_lines(styled_lines)
    page_streams = [page_to_stream(page, index + 1, len(pages)) for index, page in enumerate(pages)]
    objects = build_pdf_objects(page_streams)

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


def build_templates(company: str, role: str, candidate: str, context: Optional[JobPostingContext] = None) -> dict[str, str]:
    today = datetime.now().strftime("%B %d, %Y")
    context = context or JobPostingContext(company=company, role=role, summary=[], responsibilities=[], requirements=[], preferred=[], skills=[], work_conditions=[])
    refined_company = context.company or company
    refined_role = context.role or role
    role_label = role_in_english(refined_role)

    summary_candidates = choose_preferred_lines(context.summary, require_latin=True, max_items=2) or choose_preferred_lines(context.summary, max_items=2)
    summary_focus = trim_bullet(summary_candidates[0], 150) if summary_candidates else f"{refined_company} is hiring for a {role_label} opportunity."
    top_requirements = context.requirements[:2] or context.skills[:2]
    requirement_sentence = (
        "; ".join(summarize_requirement(item) for item in top_requirements)
        if top_requirements
        else "production-quality machine learning systems, careful API design, and dependable delivery"
    )
    key_responsibilities = context.responsibilities[:3]
    responsibility_bullets = key_responsibilities or [
        "Translate machine learning work into reliable product-facing systems.",
        "Build maintainable data and inference workflows with clear operational ownership.",
        "Partner closely with product and engineering stakeholders to ship useful tools."
    ]
    skills_bullets = context.skills[:4] or [
        "Python, SQL, model evaluation, and experiment iteration",
        "API implementation, automation, and deployment-minded engineering",
        "Observability, reproducibility, and maintainable delivery practices",
    ]
    preferred_bullets = choose_preferred_lines(context.preferred, max_items=3) or choose_preferred_lines(context.work_conditions, max_items=2) or [
        "Comfort balancing model quality, simplicity, and operational reliability",
        "Strong written communication and technical judgment",
    ]
    outcome_line = (
        trim_bullet(summary_candidates[1], 135)
        if len(summary_candidates) > 1
        else "A submission package designed to present technical work with clarity, taste, and business relevance."
    )

    return {
        "cover_letter.md": f"""# Cover Letter

{today}

Hiring Team  
{refined_company}

Dear Hiring Team,

I am writing to express my interest in the {role_label} position at {refined_company}. What stands out to me about this opportunity is its emphasis on turning strong machine learning work into dependable, production-ready systems.

My work is strongest where modeling, software engineering, and operational discipline meet. I enjoy building systems that move cleanly from experimentation into production, with careful attention to maintainability, interface design, and measurable outcomes. In practice, that has meant owning workflows across data preparation, model iteration, packaging, and delivery.

From the posting, I especially noticed the focus on {requirement_sentence}. That is exactly the kind of environment where I do my best work: taking ambiguous technical goals, shaping them into robust implementations, and collaborating closely with stakeholders to make the results useful in the real world.

I would be glad to bring that blend of execution, product-mindedness, and engineering care to {refined_company}. Thank you for your time and consideration.

Sincerely,  
{candidate}
""",
        "resume_customized.md": f"""# {candidate} — Resume (Customized)

## Target
- {role_label} at {refined_company}

## Position Snapshot
- {summary_focus}

## Profile
- Machine learning engineer with a strong bias toward shipping production-ready systems, not just isolated models.
- Comfortable owning the path from experimentation to deployed workflow, including data handling, interfaces, evaluation, and iteration.
- Prefer clean architecture, readable code, and measurable progress over novelty for its own sake.

## What I Bring
{chr(10).join(f"- {trim_bullet(item, 120)}" for item in skills_bullets)}

## Experience Highlights
{chr(10).join(f"- {trim_bullet(item, 130)}" for item in responsibility_bullets)}
- Strengthened system reliability through better interfaces, validation, and implementation discipline.
- Worked across technical and product constraints to turn requirements into practical deliverables.

## Working Style
- Think in systems: inputs, outputs, failure modes, and maintainability all matter.
- Communicate clearly with both technical and non-technical collaborators.
- Optimize for trustworthy delivery, not just one-off experimentation.

## High-Value Signals
{chr(10).join(f"- {trim_bullet(item, 125)}" for item in preferred_bullets)}

## Links
- GitHub: <add-link>
- Portfolio: <add-link>
- LinkedIn: <add-link>
""",
        "project_summary.md": f"""# Project Summary

## Opportunity Context
- Role: {role_label}
- Company: {refined_company}
- Relevance: {summary_focus}

## Selected Project Themes
- Productionizing machine learning workflows with clearer interfaces and stronger delivery discipline.
- Turning repeated manual steps into structured automation that improves consistency and reviewability.
- Building tools that balance technical rigor with practical, stakeholder-facing usefulness.

## Why The Fit Is Credible
{chr(10).join(f"- {trim_bullet(item, 130)}" for item in responsibility_bullets)}
- Experience aligns well with teams that value both technical depth and operational reliability.

## Technical Emphasis
{chr(10).join(f"- {trim_bullet(item, 125)}" for item in skills_bullets)}

## Outcome
- {outcome_line}
- Demonstrates execution quality, thoughtful packaging, and end-to-end ownership.
""",
    }


def resolve_output_folder(run_name: Optional[str], company: str, job_posting_md: Optional[str]) -> str:
    if job_posting_md:
        job_posting_path = resolve_project_path(job_posting_md)
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
    base_dir = PROJECT_ROOT / "submissions"
    paths = prepare_paths(base_dir=base_dir, company=company, run_name=run_name, job_posting_md=job_posting_md)

    context = read_job_posting_context(job_posting_md=job_posting_md, company=company, role=role)
    templates = build_templates(company=company, role=role, candidate=candidate, context=context)

    for file_name, markdown_content in templates.items():
        md_path = paths.markdown_dir / file_name
        md_path.write_text(markdown_content.strip() + "\n", encoding="utf-8")

        pdf_path = paths.pdf_dir / file_name.replace(".md", ".pdf")
        write_simple_pdf(markdown_content, pdf_path)

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
