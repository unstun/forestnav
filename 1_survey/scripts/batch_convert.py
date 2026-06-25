#!/usr/bin/env python3
"""Batch download and convert arXiv papers into a local Markdown corpus."""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import signal
import subprocess
import sys
import sysconfig
import time
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER_LIST = PROJECT_ROOT / "1_survey" / "papers" / "paper_list.csv"
PAPERS_ROOT = PROJECT_ROOT / "1_survey" / "papers"
PDF_DIR = PAPERS_ROOT / "pdf"
MD_DIR = PAPERS_ROOT / "md"
FAILED_CSV = MD_DIR / "failed_conversions.csv"
STATUS_CSV = MD_DIR / "conversion_status.csv"
README_MD = MD_DIR / "README.md"
LITERATURE_INDEX = PROJECT_ROOT / ".pipeline" / "literature" / "index.md"
FETCH_SH = PROJECT_ROOT / ".claude" / "skills" / "fetch-arxiv-md" / "fetch.sh"
USER_AGENT = "ForestNav literature corpus builder (mailto:research@example.com)"
INSTALL_ATTEMPTS: dict[str, bool] = {}
MARKER_TIMEOUT_SECONDS = 300


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "based",
    "by",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "toward",
    "towards",
    "via",
    "with",
}


@dataclass
class Paper:
    arxiv_id: str
    title: str
    year: int
    authors_short: str
    direction_tag: str
    citation_key: str = ""


@dataclass
class Quality:
    size_bytes: int
    lines: int
    sections: int
    formulas: int
    ok: bool
    reason: str = ""


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def collapse_ws(text: str) -> str:
    return " ".join((text or "").split())


def sanitize_token(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "", text)
    return cleaned


def first_author_surname(authors_short: str) -> str:
    first = authors_short.split(" et al.", 1)[0].split(",", 1)[0].strip()
    parts = [sanitize_token(part) for part in first.split() if sanitize_token(part)]
    if not parts:
        return "Unknown"
    return parts[-1]


def title_keyword(title: str) -> str:
    for word in re.findall(r"[A-Za-z][A-Za-z0-9*'-]*", title):
        cleaned = sanitize_token(word)
        if len(cleaned) >= 3 and cleaned.lower() not in STOPWORDS:
            return cleaned
    return "Paper"


def make_citation_key(paper: Paper, used: set[str]) -> str:
    base = f"{first_author_surname(paper.authors_short)}{paper.year}{title_keyword(paper.title)}"
    base = sanitize_token(base) or f"Paper{paper.arxiv_id.replace('.', '')}"
    key = base
    if key in used:
        suffix = paper.arxiv_id.replace(".", "")
        key = f"{base}_{suffix}"
    counter = 2
    while key in used:
        key = f"{base}_{counter}"
        counter += 1
    used.add(key)
    return key


def read_papers(path: Path) -> list[Paper]:
    papers: list[Paper] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                year = int(row["year"])
            except (KeyError, ValueError):
                continue
            papers.append(
                Paper(
                    arxiv_id=row.get("arxiv_id", "").strip(),
                    title=collapse_ws(row.get("title", "")),
                    year=year,
                    authors_short=collapse_ws(row.get("authors_short", "")),
                    direction_tag=collapse_ws(row.get("direction_tag", "")),
                )
            )
    used: set[str] = set()
    for paper in papers:
        paper.citation_key = make_citation_key(paper, used)
    return papers


def ensure_dirs() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)
    LITERATURE_INDEX.parent.mkdir(parents=True, exist_ok=True)


def download_pdf(paper: Paper, force: bool = False) -> Path:
    pdf_path = PDF_DIR / f"{paper.citation_key}.pdf"
    if pdf_path.exists() and pdf_path.stat().st_size > 0 and not force:
        return pdf_path
    url = f"https://arxiv.org/pdf/{paper.arxiv_id}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    tmp_path = pdf_path.with_suffix(".pdf.part")
    with urllib.request.urlopen(request, timeout=120) as response:
        with tmp_path.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    tmp_path.replace(pdf_path)
    return pdf_path


def run_fetch_arxiv(paper: Paper, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PROJECT_ROOT"] = str(PROJECT_ROOT)
    args = ["bash", str(FETCH_SH), paper.arxiv_id, paper.citation_key]
    proc = subprocess.Popen(
        args,
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
    except KeyboardInterrupt:
        os.killpg(proc.pid, signal.SIGTERM)
        raise
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            stdout, stderr = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        stderr = (stderr or "") + f"\nfetch-arxiv-md timed out after {timeout_seconds}s"
        return subprocess.CompletedProcess(args, 124, stdout, stderr)
    return subprocess.CompletedProcess(args, proc.returncode, stdout, stderr)


def ensure_python_package(import_name: str, package_name: str) -> bool:
    probe = subprocess.run(
        [sys.executable, "-c", f"import {import_name}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if probe.returncode == 0:
        return True
    if INSTALL_ATTEMPTS.get(package_name):
        return False
    INSTALL_ATTEMPTS[package_name] = True
    install_cmd = [sys.executable, "-m", "pip", "install", package_name]
    if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
        install_cmd.insert(4, "--user")
    install = subprocess.run(
        install_cmd,
        text=True,
        check=False,
    )
    return install.returncode == 0


def find_console_script(name: str) -> Path | None:
    candidates: list[Path] = []
    if path := shutil.which(name):
        candidates.append(Path(path))
    scripts_dir = sysconfig.get_path("scripts")
    if scripts_dir:
        candidates.append(Path(scripts_dir) / name)
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    return None


def marker_single_path() -> Path | None:
    if not ensure_python_package("marker.converters.pdf", "marker-pdf"):
        return None
    return find_console_script("marker_single")


def rewrite_marker_image_refs(markdown: str, figs_dir_name: str) -> str:
    def repl(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        target = match.group(2).strip()
        if re.match(r"^[a-z]+://", target) or target.startswith("/") or target.startswith("#"):
            return match.group(0)
        return f"![{alt_text}]({figs_dir_name}/{Path(target).name})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, markdown)


def try_marker_pdf(pdf_path: Path, md_path: Path, figs_dir: Path) -> bool:
    marker_single = marker_single_path()
    if marker_single is None:
        return False
    out_dir = md_path.parent / f".marker_{md_path.stem}"
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [
                str(marker_single),
                str(pdf_path),
                "--output_dir",
                str(out_dir),
                "--output_format",
                "markdown",
                "--disable_multiprocessing",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=MARKER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        shutil.rmtree(out_dir, ignore_errors=True)
        return False
    if result.returncode != 0:
        shutil.rmtree(out_dir, ignore_errors=True)
        return False
    candidates = sorted(out_dir.rglob("*.md"))
    if not candidates:
        shutil.rmtree(out_dir, ignore_errors=True)
        return False
    markdown = candidates[0].read_text(encoding="utf-8", errors="replace")
    images = [p for p in out_dir.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}]
    if images:
        figs_dir.mkdir(parents=True, exist_ok=True)
        for image in images:
            target = figs_dir / image.name
            if image.resolve() != target.resolve():
                shutil.copy2(image, target)
        markdown = rewrite_marker_image_refs(markdown, figs_dir.name)
    md_path.write_text(markdown, encoding="utf-8")
    shutil.rmtree(out_dir, ignore_errors=True)
    return True


def write_pymupdf_script(pdf_path: Path, md_path: Path, figs_dir: Path) -> str:
    return f"""
from pathlib import Path
import pymupdf4llm

pdf_path = Path({str(pdf_path)!r})
md_path = Path({str(md_path)!r})
figs_dir = Path({str(figs_dir)!r})
figs_dir.mkdir(parents=True, exist_ok=True)
try:
    markdown = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(figs_dir),
        image_format="png",
    )
except TypeError:
    markdown = pymupdf4llm.to_markdown(str(pdf_path))
md_path.write_text(markdown, encoding="utf-8")
"""


def try_pymupdf4llm(pdf_path: Path, md_path: Path, figs_dir: Path) -> bool:
    if not ensure_python_package("pymupdf4llm", "pymupdf4llm"):
        return False
    result = subprocess.run(
        [sys.executable, "-c", write_pymupdf_script(pdf_path, md_path, figs_dir)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode == 0 and md_path.exists() and md_path.stat().st_size > 0


def add_frontmatter(md_path: Path, paper: Paper, source: str) -> None:
    body = md_path.read_text(encoding="utf-8", errors="replace")
    if body.startswith("---\n") and "\n---\n" in body[4:]:
        body = body.split("\n---\n", 1)[1]
    frontmatter = (
        "---\n"
        f"citation_key: {paper.citation_key}\n"
        f"arxiv_id: {paper.arxiv_id}\n"
        f'arxiv_url: "https://arxiv.org/abs/{paper.arxiv_id}"\n'
        f'title: "{paper.title.replace(chr(34), chr(39))}"\n'
        f'authors_short: "{paper.authors_short.replace(chr(34), chr(39))}"\n'
        f"year: {paper.year}\n"
        f"direction_tag: {paper.direction_tag}\n"
        f"source: {source}\n"
        f"converted_at: {now_utc()}\n"
        "origin: ai+web\n"
        "reviewed: false\n"
        "---\n\n"
    )
    md_path.write_text(frontmatter + body, encoding="utf-8")


def fallback_pdf_to_md(paper: Paper, pdf_path: Path) -> tuple[bool, str]:
    md_path = MD_DIR / f"{paper.citation_key}.md"
    figs_dir = MD_DIR / f"{paper.citation_key}_figs"
    if try_marker_pdf(pdf_path, md_path, figs_dir):
        add_frontmatter(md_path, paper, "marker-pdf")
        return True, "marker-pdf"
    if try_pymupdf4llm(pdf_path, md_path, figs_dir):
        add_frontmatter(md_path, paper, "pymupdf4llm")
        return True, "pymupdf4llm"
    return False, "pdf-fallback-failed"


def quality_check(md_path: Path) -> Quality:
    if not md_path.exists():
        return Quality(0, 0, 0, 0, False, "missing-md")
    text = md_path.read_text(encoding="utf-8", errors="replace")
    size_bytes = md_path.stat().st_size
    lines = text.count("\n") + (1 if text else 0)
    sections = sum(1 for line in text.splitlines() if line.startswith("#"))
    formulas = len(re.findall(r"\$[^$\n]+\$", text)) + text.count("$$") // 2
    failures: list[str] = []
    if size_bytes < 5000:
        failures.append(f"size<{5000}")
    if lines < 50:
        failures.append("lines<50")
    if sections < 3:
        failures.append("sections<3")
    return Quality(size_bytes, lines, sections, formulas, not failures, ";".join(failures))


def has_complete_frontmatter(md_path: Path, citation_key: str) -> bool:
    if not md_path.exists():
        return False
    head = md_path.read_text(encoding="utf-8", errors="replace")[:1200]
    return (
        head.startswith("---\n")
        and f"citation_key: {citation_key}" in head
        and "origin: ai+web" in head
        and "reviewed: false" in head
    )


def frontmatter_value(md_path: Path, key: str, default: str = "existing") -> str:
    if not md_path.exists():
        return default
    text = md_path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return default
    frontmatter = text.split("\n---\n", 1)[0]
    prefix = f"{key}:"
    for line in frontmatter.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip('"')
    return default


def read_status_rows() -> dict[str, dict[str, str]]:
    if not STATUS_CSV.exists():
        return {}
    with STATUS_CSV.open(newline="", encoding="utf-8") as handle:
        return {row["arxiv_id"]: row for row in csv.DictReader(handle) if row.get("arxiv_id")}


def read_failed_rows() -> dict[str, dict[str, str]]:
    if not FAILED_CSV.exists():
        return {}
    with FAILED_CSV.open(newline="", encoding="utf-8") as handle:
        return {row["arxiv_id"]: row for row in csv.DictReader(handle) if row.get("arxiv_id")}


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    with tmp_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    tmp_path.replace(path)


def write_conversion_state(
    status_rows_by_id: dict[str, dict[str, object]],
    failed_rows_by_id: dict[str, dict[str, object]],
) -> None:
    write_rows(STATUS_CSV, list(status_rows_by_id.values()), status_fieldnames())
    write_rows(FAILED_CSV, list(failed_rows_by_id.values()), failed_fieldnames())


def status_fieldnames() -> list[str]:
    return [
        "arxiv_id",
        "citation_key",
        "title",
        "authors_short",
        "year",
        "direction_tag",
        "status",
        "source",
        "reason",
        "size_bytes",
        "lines",
        "sections",
        "formulas",
        "pdf_path",
        "md_path",
    ]


def failed_fieldnames() -> list[str]:
    return [
        "arxiv_id",
        "citation_key",
        "title",
        "direction_tag",
        "stage",
        "reason",
        "exit_code",
        "pdf_path",
        "md_path",
    ]


def row_for_status(paper: Paper, status: str, source: str, quality: Quality, reason: str) -> dict[str, object]:
    return {
        "arxiv_id": paper.arxiv_id,
        "citation_key": paper.citation_key,
        "title": paper.title,
        "authors_short": paper.authors_short,
        "year": paper.year,
        "direction_tag": paper.direction_tag,
        "status": status,
        "source": source,
        "reason": reason,
        "size_bytes": quality.size_bytes,
        "lines": quality.lines,
        "sections": quality.sections,
        "formulas": quality.formulas,
        "pdf_path": str(PDF_DIR / f"{paper.citation_key}.pdf"),
        "md_path": str(MD_DIR / f"{paper.citation_key}.md"),
    }


def row_for_failure(paper: Paper, stage: str, reason: str, exit_code: int | str = "") -> dict[str, object]:
    return {
        "arxiv_id": paper.arxiv_id,
        "citation_key": paper.citation_key,
        "title": paper.title,
        "direction_tag": paper.direction_tag,
        "stage": stage,
        "reason": reason,
        "exit_code": exit_code,
        "pdf_path": str(PDF_DIR / f"{paper.citation_key}.pdf"),
        "md_path": str(MD_DIR / f"{paper.citation_key}.md"),
    }


def load_success_rows() -> list[dict[str, str]]:
    if not STATUS_CSV.exists():
        return []
    with STATUS_CSV.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "success"]


def parse_int(value: str | None, default: int = 0) -> int:
    try:
        return int(value or default)
    except ValueError:
        return default


def should_retry_pymupdf_zero_formulas(previous: dict[str, str] | None) -> bool:
    if not previous:
        return False
    return previous.get("source") == "pymupdf4llm" and parse_int(previous.get("formulas")) == 0


def should_process_paper(
    paper: Paper,
    previous: dict[str, str] | None,
    retry_pymupdf_zero_formulas: bool,
    retry_failed: bool,
) -> bool:
    md_path = MD_DIR / f"{paper.citation_key}.md"
    if retry_pymupdf_zero_formulas and should_retry_pymupdf_zero_formulas(previous):
        return True
    if previous and previous.get("status") == "failed" and not retry_failed:
        return False
    if previous is None or previous.get("status") != "success":
        return True
    return not has_complete_frontmatter(md_path, paper.citation_key)


def write_readme(
    success_rows: list[dict[str, str]],
    failed_rows: list[dict[str, object]],
    candidate_count: int,
) -> None:
    direction_counts: Counter[str] = Counter()
    for row in success_rows:
        for tag in row["direction_tag"].split(";"):
            direction_counts[tag] += 1
    total_size = sum(int(row.get("size_bytes") or 0) for row in success_rows)
    total_sections = sum(int(row.get("sections") or 0) for row in success_rows)
    total_formulas = sum(int(row.get("formulas") or 0) for row in success_rows)
    count = len(success_rows)
    avg_size = round(total_size / count, 1) if count else 0
    avg_sections = round(total_sections / count, 1) if count else 0
    avg_formulas = round(total_formulas / count, 1) if count else 0

    lines = [
        "---",
        "origin: ai+web",
        "reviewed: false",
        f"updated: {now_utc()}",
        "---",
        "",
        "# Path Quality Motion Planning Markdown Corpus",
        "",
        f"- 候选池：{candidate_count} 篇",
        f"- 已处理：{len(success_rows) + len(failed_rows)} 篇",
        f"- 总计：成功 {len(success_rows)} 篇 / 失败 {len(failed_rows)} 篇",
        f"- 平均 section 数：{avg_sections}",
        f"- 平均公式数：{avg_formulas}",
        f"- 平均文件大小：{avg_size} bytes",
        f"- 候选清单：`{DEFAULT_PAPER_LIST.relative_to(PROJECT_ROOT)}`",
        f"- 转换状态：`{STATUS_CSV.relative_to(PROJECT_ROOT)}`",
        f"- 失败记录：`{FAILED_CSV.relative_to(PROJECT_ROOT)}`",
        "",
        "## 各方向论文数量",
        "",
        "| 方向 | 成功篇数 |",
        "|------|---------:|",
    ]
    for direction, n_papers in sorted(direction_counts.items()):
        lines.append(f"| {direction} | {n_papers} |")
    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "本库用于后续 AI 精读和人工筛选。`reviewed: false` 表示尚未人工核验，不能直接作为论文 claim 或实验决策依据。",
            "",
        ]
    )
    README_MD.write_text("\n".join(lines), encoding="utf-8")


def write_literature_index(success_rows: list[dict[str, str]]) -> None:
    lines = [
        "# ForestNav 文献索引",
        "",
        "## 2026-06-23 path-quality motion-planning Markdown corpus",
        "",
        "> 状态：自动检索、下载和转换完成；`reviewed: false`，后续引用前必须回到原文核验。",
        "",
        "| CitationKey | 标题 | 作者 | 年份 | 来源 | arXiv/DOI | 方向 | MD路径 |",
        "|-------------|------|------|------|------|-----------|------|--------|",
    ]
    for row in sorted(success_rows, key=lambda item: (item["direction_tag"], item["citation_key"])):
        arxiv = row["arxiv_id"]
        md_rel = Path(row["md_path"]).relative_to(PROJECT_ROOT)
        title = row["title"].replace("|", "\\|")
        authors = row["authors_short"].replace("|", "\\|")
        direction = row["direction_tag"].replace("|", "\\|")
        lines.append(
            f"| {row['citation_key']} | {title} | {authors} | {row['year']} | {row['source']} | arXiv:{arxiv} | {direction} | `{md_rel}` |"
        )
    lines.append("")
    LITERATURE_INDEX.write_text("\n".join(lines), encoding="utf-8")


def process_paper(
    paper: Paper,
    force: bool,
    fetch_timeout: int,
    prefer_pdf_fallback: bool = False,
) -> tuple[dict[str, object], dict[str, object] | None]:
    pdf_path = PDF_DIR / f"{paper.citation_key}.pdf"
    md_path = MD_DIR / f"{paper.citation_key}.md"
    try:
        pdf_path = download_pdf(paper, force=force)
    except Exception as exc:  # noqa: BLE001 - keep batch moving.
        failure = row_for_failure(paper, "download-pdf", str(exc))
        return row_for_status(paper, "failed", "none", Quality(0, 0, 0, 0, False, "pdf-download"), str(exc)), failure

    source = "arxiv-e-print"
    complete_frontmatter = has_complete_frontmatter(md_path, paper.citation_key)
    existing_quality = quality_check(md_path) if complete_frontmatter else None
    if prefer_pdf_fallback:
        previous_source = frontmatter_value(md_path, "source", "existing") if complete_frontmatter else "none"
        ok, source = fallback_pdf_to_md(paper, pdf_path)
        quality = quality_check(md_path)
        if ok and quality.ok:
            return row_for_status(paper, "success", source, quality, ""), None
        if existing_quality and existing_quality.ok:
            return (
                row_for_status(
                    paper,
                    "success",
                    previous_source,
                    existing_quality,
                    "retry-pdf-fallback-failed-kept-existing",
                ),
                None,
            )
        failure = row_for_failure(paper, "pdf-fallback", source)
        return row_for_status(paper, "failed", source, quality, source), failure

    needs_conversion = force or not complete_frontmatter or not (existing_quality and existing_quality.ok)
    if needs_conversion:
        fetch_result = run_fetch_arxiv(paper, timeout_seconds=fetch_timeout)
        if fetch_result.returncode == 2:
            ok, source = fallback_pdf_to_md(paper, pdf_path)
            if not ok:
                failure = row_for_failure(paper, "pdf-fallback", source, fetch_result.returncode)
                return row_for_status(paper, "failed", source, Quality(0, 0, 0, 0, False, source), source), failure
        elif fetch_result.returncode != 0:
            ok, source = fallback_pdf_to_md(paper, pdf_path)
            if not ok:
                reason = (fetch_result.stderr or fetch_result.stdout or "fetch-arxiv failed").strip().splitlines()[-1]
                failure = row_for_failure(paper, "fetch-arxiv-md", reason, fetch_result.returncode)
                return row_for_status(paper, "failed", "arxiv-e-print", Quality(0, 0, 0, 0, False, reason), reason), failure
    else:
        source = frontmatter_value(md_path, "source")

    quality = quality_check(md_path)
    if not quality.ok and source == "arxiv-e-print":
        ok, fallback_source = fallback_pdf_to_md(paper, pdf_path)
        if ok:
            source = fallback_source
            quality = quality_check(md_path)
    if quality.ok:
        return row_for_status(paper, "success", source, quality, ""), None
    failure = row_for_failure(paper, "quality-gate", quality.reason)
    return row_for_status(paper, "failed", source, quality, quality.reason), failure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-list", type=Path, default=DEFAULT_PAPER_LIST)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0, help="Zero-based offset into paper_list.csv.")
    parser.add_argument("--sleep", type=float, default=3.0)
    parser.add_argument("--fetch-timeout", type=int, default=240)
    parser.add_argument("--marker-timeout", type=int, default=MARKER_TIMEOUT_SECONDS)
    parser.add_argument(
        "--stop-after-success",
        type=int,
        default=None,
        help="Stop once at least N successful Markdown files have been registered.",
    )
    parser.add_argument("--force", action="store_true", help="Re-download PDFs and re-run conversion.")
    parser.add_argument("--dry-run", type=int, default=0, help="Process only the first N papers.")
    parser.add_argument(
        "--only-pending",
        action="store_true",
        help="Process only papers without a successful durable status row or complete Markdown.",
    )
    parser.add_argument(
        "--retry-pymupdf-zero-formulas",
        action="store_true",
        help="Retry successful pymupdf4llm rows whose formula count is zero using the marker PDF path.",
    )
    parser.add_argument("--retry-failed", action="store_true", help="Retry rows already recorded as failed.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    global MARKER_TIMEOUT_SECONDS
    MARKER_TIMEOUT_SECONDS = args.marker_timeout
    ensure_dirs()
    all_papers = read_papers(args.paper_list)
    candidate_count = len(all_papers)
    candidate_ids = {paper.arxiv_id for paper in all_papers}
    status_by_id = read_status_rows()
    failed_by_id = read_failed_rows()
    status_rows_by_id: dict[str, dict[str, object]] = {
        arxiv_id: row for arxiv_id, row in status_by_id.items() if arxiv_id in candidate_ids
    }
    failed_rows_by_id: dict[str, dict[str, object]] = {
        arxiv_id: row for arxiv_id, row in failed_by_id.items() if arxiv_id in candidate_ids
    }

    papers = all_papers
    if args.only_pending:
        papers = [
            paper
            for paper in papers
            if should_process_paper(
                paper,
                status_by_id.get(paper.arxiv_id),
                args.retry_pymupdf_zero_formulas,
                args.retry_failed,
            )
        ]
    if args.start_index:
        papers = papers[args.start_index :]
    limit = args.dry_run or args.limit
    if limit:
        papers = papers[:limit]
    if not papers:
        print("No papers to process.")
        return 1

    completed = 0
    successes = 0
    failures = 0

    for index, paper in enumerate(papers, start=1):
        previous = status_by_id.get(paper.arxiv_id)
        md_path = MD_DIR / f"{paper.citation_key}.md"
        prefer_pdf_fallback = args.retry_pymupdf_zero_formulas and should_retry_pymupdf_zero_formulas(previous)
        if (
            has_complete_frontmatter(md_path, paper.citation_key)
            and not args.force
            and not prefer_pdf_fallback
            and (previous is None or previous.get("status") == "success")
        ):
            quality = quality_check(md_path)
            if quality.ok:
                source = frontmatter_value(md_path, "source", previous.get("source", "existing") if previous else "existing")
                status_row = row_for_status(paper, "success", source, quality, "")
                failure_row = None
            else:
                print(f"[{index}/{len(papers)}] {paper.citation_key} arXiv:{paper.arxiv_id} (quality retry)", flush=True)
                status_row, failure_row = process_paper(paper, force=args.force, fetch_timeout=args.fetch_timeout)
                if index < len(papers):
                    time.sleep(args.sleep)
        else:
            print(f"[{index}/{len(papers)}] {paper.citation_key} arXiv:{paper.arxiv_id}", flush=True)
            status_row, failure_row = process_paper(
                paper,
                force=args.force,
                fetch_timeout=args.fetch_timeout,
                prefer_pdf_fallback=prefer_pdf_fallback,
            )
            if index < len(papers):
                time.sleep(args.sleep)

        status_rows_by_id[paper.arxiv_id] = status_row
        completed += 1
        if status_row["status"] == "success":
            successes += 1
        else:
            failures += 1
        if failure_row:
            failed_rows_by_id[paper.arxiv_id] = failure_row
        else:
            failed_rows_by_id.pop(paper.arxiv_id, None)
        write_conversion_state(status_rows_by_id, failed_rows_by_id)
        if completed % 10 == 0 or completed == len(papers):
            print(
                f"[{completed}/{len(papers)}] 已完成 {completed} 篇, 成功 {successes}, 失败 {failures}",
                flush=True,
            )
        if args.stop_after_success and successes >= args.stop_after_success:
            print(
                f"Reached stop-after-success={args.stop_after_success}; writing corpus indexes.",
                flush=True,
            )
            break

    write_conversion_state(status_rows_by_id, failed_rows_by_id)
    success_rows = [
        row
        for row in status_rows_by_id.values()
        if row.get("status") == "success" and row.get("arxiv_id") in candidate_ids
    ]
    failed_rows = list(failed_rows_by_id.values())
    write_readme(success_rows, failed_rows, candidate_count)
    write_literature_index(success_rows)
    print(f"Summary: success={len(success_rows)} failed={len(failed_rows)}")
    if args.dry_run:
        print(f"Dry-run processed {args.dry_run} papers.")
    if args.dry_run or args.limit or args.start_index or args.only_pending:
        return 0
    return 0 if len(success_rows) >= 200 else 2


if __name__ == "__main__":
    raise SystemExit(main())
