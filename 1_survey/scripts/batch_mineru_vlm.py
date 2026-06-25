#!/usr/bin/env python3
"""Re-convert formula-risk PDFs with MinerU Open API VLM.

This script repairs Markdown files that were previously produced by
``pymupdf4llm`` with zero detected formulas. It stages every MinerU VLM result
under ``1_survey/papers/api_trials/mineru_vlm_batch/`` and only replaces the
main corpus Markdown after a basic quality gate passes.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PAPERS_ROOT = PROJECT_ROOT / "1_survey" / "papers"
PDF_DIR = PAPERS_ROOT / "pdf"
MD_DIR = PAPERS_ROOT / "md"
STATUS_CSV = MD_DIR / "conversion_status.csv"
FAILED_CSV = MD_DIR / "failed_conversions.csv"
STAGE_ROOT = PAPERS_ROOT / "api_trials" / "mineru_vlm_batch"
DEFAULT_CLI = Path("/Users/sun/.local/bin/mineru-open-api")


@dataclass(frozen=True)
class Quality:
    size_bytes: int
    lines: int
    sections: int
    formulas: int
    ok: bool
    reason: str = ""


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_int(value: str | None, default: int = 0) -> int:
    try:
        return int(value or default)
    except ValueError:
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    with tmp_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    tmp_path.replace(path)


def formula_count(text: str) -> int:
    inline = len(re.findall(r"(?<!\$)\$[^$\n]+\$(?!\$)", text))
    display = text.count("$$") // 2
    bracketed = text.count("\\[") + text.count("\\(")
    tagged = len(re.findall(r"\\tag\{[^}]+\}", text))
    return inline + display + bracketed + tagged


def quality_check(path: Path, require_formula: bool = True) -> Quality:
    if not path.exists():
        return Quality(0, 0, 0, 0, False, "missing-md")
    text = path.read_text(encoding="utf-8", errors="replace")
    size_bytes = path.stat().st_size
    lines = text.count("\n") + (1 if text else 0)
    sections = sum(1 for line in text.splitlines() if line.startswith("#"))
    formulas = formula_count(text)
    failures: list[str] = []
    if size_bytes < 5000:
        failures.append("size<5000")
    if lines < 50:
        failures.append("lines<50")
    if sections < 3:
        failures.append("sections<3")
    if require_formula and formulas == 0:
        failures.append("formulas=0")
    return Quality(size_bytes, lines, sections, formulas, not failures, ";".join(failures))


def select_rows(rows: list[dict[str, str]], scope: str) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in rows:
        if row.get("status") != "success":
            continue
        source = row.get("source", "")
        formulas = parse_int(row.get("formulas"))
        if scope == "risk" and source == "pymupdf4llm" and formulas == 0:
            selected.append(row)
        elif scope == "pymupdf" and source == "pymupdf4llm":
            selected.append(row)
        elif scope == "all-success":
            selected.append(row)
    return selected


def shell_quote_list(paths: list[Path]) -> str:
    return "\n".join(str(path) for path in paths) + "\n"


def run_mineru_vlm(row: dict[str, str], cli_path: Path, timeout: int, force: bool) -> tuple[bool, str, Path]:
    key = row["citation_key"]
    pdf_path = Path(row.get("pdf_path") or PDF_DIR / f"{key}.pdf")
    out_dir = STAGE_ROOT / key
    md_path = out_dir / f"{key}.md"
    if md_path.exists() and not force:
        return True, "cached", md_path
    if force:
        shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(cli_path),
        "extract",
        str(pdf_path),
        "--model",
        "vlm",
        "--language",
        "en",
        "--formula=true",
        "--table=true",
        "-f",
        "md,json",
        "-o",
        str(out_dir),
        "--timeout",
        str(timeout),
    ]
    env = os.environ.copy()
    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != 0:
        return False, proc.stdout.strip()[-2000:], md_path
    if not md_path.exists():
        return False, "mineru output md missing", md_path
    return True, proc.stdout.strip()[-2000:], md_path


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        return text.split("\n---\n", 1)[1].lstrip()
    return text


def rewrite_image_refs(markdown: str, figs_dir_name: str) -> str:
    def repl(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        target = match.group(2).strip()
        if re.match(r"^[a-z]+://", target) or target.startswith("/") or target.startswith("#"):
            return match.group(0)
        if target.startswith(f"{figs_dir_name}/"):
            return match.group(0)
        return f"![{alt_text}]({figs_dir_name}/{Path(target).name})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, markdown)


def frontmatter(row: dict[str, str]) -> str:
    title = row.get("title", "").replace('"', "'")
    authors = row.get("authors_short", "").replace('"', "'")
    return (
        "---\n"
        f"citation_key: {row.get('citation_key', '')}\n"
        f"arxiv_id: {row.get('arxiv_id', '')}\n"
        f"arxiv_url: \"https://arxiv.org/abs/{row.get('arxiv_id', '')}\"\n"
        f"title: \"{title}\"\n"
        f"authors_short: \"{authors}\"\n"
        f"year: {row.get('year', '')}\n"
        f"direction_tag: {row.get('direction_tag', '')}\n"
        "source: mineru-vlm\n"
        "converter: mineru-open-api\n"
        "model: vlm\n"
        f"converted_at: {now_utc()}\n"
        "origin: ai+web\n"
        "reviewed: false\n"
        "---\n\n"
    )


def apply_to_corpus(row: dict[str, str], staged_md: Path) -> Quality:
    key = row["citation_key"]
    target_md = MD_DIR / f"{key}.md"
    target_figs = MD_DIR / f"{key}_figs"
    staged_images = staged_md.parent / "images"
    if staged_images.exists():
        shutil.rmtree(target_figs, ignore_errors=True)
        shutil.copytree(staged_images, target_figs)
    body = strip_frontmatter(staged_md.read_text(encoding="utf-8", errors="replace"))
    body = rewrite_image_refs(body, target_figs.name)
    target_md.write_text(frontmatter(row) + body, encoding="utf-8")
    return quality_check(target_md, require_formula=True)


def update_status_row(rows: list[dict[str, str]], row: dict[str, str], quality: Quality) -> None:
    for item in rows:
        if item.get("arxiv_id") == row.get("arxiv_id"):
            item["status"] = "success"
            item["source"] = "mineru-vlm"
            item["reason"] = ""
            item["size_bytes"] = str(quality.size_bytes)
            item["lines"] = str(quality.lines)
            item["sections"] = str(quality.sections)
            item["formulas"] = str(quality.formulas)
            item["md_path"] = str(MD_DIR / f"{row['citation_key']}.md")
            item["pdf_path"] = str(Path(row.get("pdf_path") or PDF_DIR / f"{row['citation_key']}.pdf"))
            return


def append_log(payload: dict[str, object]) -> None:
    STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    log_path = STAGE_ROOT / "batch_status.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=["risk", "pymupdf", "all-success"], default="risk")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--cli", type=Path, default=DEFAULT_CLI)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-zero-formulas", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.cli.exists():
        print(f"mineru-open-api not found: {args.cli}", file=sys.stderr)
        return 2
    if not args.dry_run and not os.environ.get("MINERU_TOKEN"):
        print("MINERU_TOKEN is required for VLM conversion.", file=sys.stderr)
        return 2
    status_rows = read_csv(STATUS_CSV)
    if not status_rows:
        print(f"No status rows found: {STATUS_CSV}", file=sys.stderr)
        return 2
    fieldnames = list(status_rows[0].keys())
    targets = select_rows(status_rows, args.scope)
    if args.start_index:
        targets = targets[args.start_index :]
    if args.limit:
        targets = targets[: args.limit]
    print(f"Targets: {len(targets)} scope={args.scope}")
    if args.dry_run:
        for row in targets:
            print(f"{row['citation_key']}\t{row['arxiv_id']}\t{row['pdf_path']}")
        return 0

    converted = 0
    applied = 0
    failed = 0
    for index, row in enumerate(targets, start=1):
        key = row["citation_key"]
        print(f"[{index}/{len(targets)}] {key}", flush=True)
        ok, message, staged_md = run_mineru_vlm(row, args.cli, args.timeout, args.force)
        log_payload: dict[str, object] = {
            "time": now_utc(),
            "citation_key": key,
            "arxiv_id": row.get("arxiv_id"),
            "stage": "extract",
            "ok": ok,
            "message": message,
        }
        if not ok:
            failed += 1
            append_log(log_payload)
            continue
        converted += 1
        staged_quality = quality_check(staged_md, require_formula=not args.allow_zero_formulas)
        if not staged_quality.ok:
            failed += 1
            log_payload.update(
                {
                    "stage": "quality",
                    "ok": False,
                    "quality_reason": staged_quality.reason,
                    "formulas": staged_quality.formulas,
                }
            )
            append_log(log_payload)
            continue
        final_quality = apply_to_corpus(row, staged_md)
        if not final_quality.ok:
            failed += 1
            log_payload.update(
                {
                    "stage": "apply-quality",
                    "ok": False,
                    "quality_reason": final_quality.reason,
                    "formulas": final_quality.formulas,
                }
            )
            append_log(log_payload)
            continue
        update_status_row(status_rows, row, final_quality)
        write_csv(STATUS_CSV, status_rows, fieldnames)
        applied += 1
        log_payload.update(
            {
                "stage": "applied",
                "ok": True,
                "size_bytes": final_quality.size_bytes,
                "lines": final_quality.lines,
                "sections": final_quality.sections,
                "formulas": final_quality.formulas,
            }
        )
        append_log(log_payload)
        print(f"  applied formulas={final_quality.formulas} lines={final_quality.lines}", flush=True)

    print(f"Summary: converted={converted} applied={applied} failed={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
