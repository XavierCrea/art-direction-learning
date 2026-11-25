#!/usr/bin/env python3
"""Inspect, search, batch-get, validate, and atomically patch the art-direction-learning bilingual library."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

GROUPS = ("sources", "methods", "cases", "feedback")
STATUS_VALUES = {"reference", "candidate", "validated", "retired"}
EVIDENCE_STAGES = {"source_verified", "user_endorsed", "field_validated"}
READING_STATUS_VALUES = {"registered", "metadata_only", "partial_review", "full_review"}
LEARNING_ORIGINS = {"book_canon", "benchmark_study", "co_dissected_teardown", "task_feedback"}
EVIDENCE_TYPES = {
    "ab_test",
    "usability_benchmark",
    "author_reported",
    "editorial_analysis",
    "case_study_metric",
    "counterfactual_exercise",
    "delivery_check",
    "editorial_feedback",
    "ab_test_result",
    "market_result",
    "comparative_field_teardown",
}

REQUIRED = {
    "sources": {
        "id",
        "kind",
        "title",
        "version",
        "reading_status",
        "reviewed_locations",
        "retrieved_at",
    },
    "methods": {
        "id",
        "version",
        "title",
        "title_en",
        "tags",
        "tags_en",
        "when_stuck",
        "channels",
        "status",
        "source_refs",
        "rule",
        "rule_en",
        "applies_when",
        "limits",
        "steps",
        "checks",
        "validation_refs",
    },
    "cases": {
        "id",
        "version",
        "title",
        "title_en",
        "tags",
        "tags_en",
        "when_stuck",
        "status",
        "source_refs",
        "case_type",
        "markdown_path",
        "markdown_path_en",
        "observations",
        "copy_visual_synergy",
        "analysis",
        "reusable_move",
        "reusable_move_en",
        "asset_prerequisites",
        "outcome_evidence",
        "transfer_limits",
    },
    "feedback": {
        "id",
        "version",
        "title",
        "kind",
        "evidence_type",
        "source_locator",
        "observation",
        "verified",
        "task_id",
    },
}

WEIGHT_HIGH_FIELDS = ("id", "title", "title_en", "tags", "tags_en", "when_stuck")
WEIGHT_MED_FIELDS = ("rule", "rule_en", "reusable_move", "reusable_move_en", "applies_when", "channels", "case_type")
WEIGHT_LOW_FIELDS = (
    "analysis",
    "observations",
    "copy_visual_synergy",
    "limits",
    "transfer_limits",
    "asset_prerequisites",
    "steps",
    "checks",
    "observation",
    "observation_en",
    "coverage_note",
    "coverage_note_en",
)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_library_root(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).expanduser().resolve()
    env_value = os.environ.get("ART_DIRECTION_LIBRARY_ROOT") or os.environ.get("VISUAL_PLANNING_LIBRARY_ROOT")
    if env_value:
        return Path(env_value).expanduser().resolve()
    config_path = skill_root() / "references" / "library-location.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        default_root = config.get("default_library_root", "library")
        candidate = Path(default_root).expanduser()
        return candidate.resolve() if candidate.is_absolute() else (skill_root() / candidate).resolve()
    return (skill_root() / "library").resolve()


def load_catalog(root: Path) -> tuple[dict[str, Any], Path]:
    catalog_path = root / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError(f"catalog.json not found at {catalog_path}")
    return json.loads(catalog_path.read_text(encoding="utf-8")), catalog_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_md_path(root: Path, md_rel: str) -> Path:
    return (skill_root() / md_rel).resolve() if md_rel.startswith("library/") else (root / md_rel).resolve()


def _valid_when_stuck(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict) and set(value.keys()) == {"zh", "en"}:
        return all(
            isinstance(v, list) and bool(v) and all(isinstance(s, str) and bool(s.strip()) for s in v)
            for v in value.values()
        )
    return False


def validate_catalog(data: dict[str, Any], root: Path, check_files: bool = False) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(data.get("revision"), int) or data["revision"] < 1:
        errors.append("revision must be a positive integer")
    for group in GROUPS:
        if not isinstance(data.get(group), list):
            errors.append(f"{group} must be a list")

    ids: dict[str, str] = {}
    sources_by_id: dict[str, dict[str, Any]] = {}
    feedback_by_id: dict[str, dict[str, Any]] = {}

    for group in GROUPS:
        for index, item in enumerate(data.get(group, [])):
            label = f"{group}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            missing = sorted(REQUIRED[group] - set(item.keys()))
            if missing:
                errors.append(f"{label} ({item.get('id', 'unknown')}) missing required fields: {', '.join(missing)}")
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                errors.append(f"{label} id must be a non-empty string")
            elif item_id in ids:
                errors.append(f"duplicate id {item_id} in {group} and {ids[item_id]}")
            else:
                ids[item_id] = group
            version = item.get("version")
            if not isinstance(version, int) or version < 1:
                errors.append(f"{item_id or label} version must be a positive integer")
            if group == "sources" and isinstance(item_id, str):
                sources_by_id[item_id] = item
            if group == "feedback" and isinstance(item_id, str):
                feedback_by_id[item_id] = item

    for source in data.get("sources", []):
        source_id = source.get("id", "<source>")
        if source.get("reading_status") not in READING_STATUS_VALUES:
            errors.append(f"{source_id} has invalid reading_status")
        if not isinstance(source.get("reviewed_locations"), list):
            errors.append(f"{source_id} reviewed_locations must be a list")
        if source.get("kind") == "book":
            pages = source.get("pdf_pages")
            if not isinstance(pages, int) or pages < 1:
                errors.append(f"{source_id} book source must include positive integer pdf_pages")
        rel_path = source.get("path")
        availability = source.get("original_availability", "archived" if rel_path else "citation_only")
        if availability not in {"archived", "external", "citation_only"}:
            errors.append(f"{source_id} has invalid original_availability")
        if availability == "citation_only" and ("path" in source or "local_path" in source):
            errors.append(f"{source_id} citation_only source must omit local machine paths")
        if check_files and rel_path:
            file_path = root / rel_path
            if not file_path.exists():
                errors.append(f"{source_id} missing file at {file_path}")
            elif source.get("sha256"):
                actual = sha256_file(file_path)
                if actual != source["sha256"]:
                    errors.append(f"{source_id} sha256 mismatch for {file_path}")

    for group in ("methods", "cases"):
        for item in data.get(group, []):
            item_id = item.get("id", f"<{group}>")
            status = item.get("status")
            if status not in STATUS_VALUES:
                errors.append(f"{item_id} has invalid status {status!r}")
            ev_stage = item.get("evidence_stage")
            if ev_stage is not None and ev_stage not in EVIDENCE_STAGES:
                errors.append(f"{item_id} has invalid evidence_stage {ev_stage!r}")
            if not _valid_when_stuck(item.get("when_stuck")):
                errors.append(f"{item_id} has invalid when_stuck (expected bilingual dict {{'zh': [...], 'en': [...]}})")
            refs = item.get("source_refs")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{item_id} must have non-empty source_refs")
            else:
                for ref in refs:
                    source_id = ref.get("source_id") if isinstance(ref, dict) else None
                    if source_id not in sources_by_id:
                        errors.append(f"{item_id} references unknown source_id {source_id!r}")
                    else:
                        source = sources_by_id[source_id]
                        max_pages = source.get("pdf_pages")
                        for page in ref.get("pdf_pages", []):
                            if not isinstance(page, int) or page < 1 or (isinstance(max_pages, int) and page > max_pages):
                                errors.append(f"{item_id} has out-of-range pdf_page {page} for {source_id}")
            if status == "validated":
                val_refs = item.get("validation_refs", [])
                if not isinstance(val_refs, list) or not val_refs:
                    errors.append(f"{item_id} is validated but has no validation_refs")
                for feedback_id in val_refs:
                    fb = feedback_by_id.get(feedback_id)
                    if not fb:
                        errors.append(f"{item_id} validation_ref {feedback_id!r} not found")
                    elif fb.get("verified") is not True:
                        errors.append(f"{item_id} validation_ref {feedback_id!r} is not verified")

            if group == "cases":
                outcome = item.get("outcome_evidence")
                if not isinstance(outcome, dict):
                    errors.append(f"{item_id} outcome_evidence must be an object")
                elif outcome.get("evidence_type") not in EVIDENCE_TYPES:
                    errors.append(f"{item_id} outcome_evidence has invalid evidence_type {outcome.get('evidence_type')!r}")
                for field in ("markdown_path", "markdown_path_en"):
                    md_rel = item.get(field)
                    if not isinstance(md_rel, str) or not md_rel.strip():
                        errors.append(f"{item_id} {field} must be a non-empty string")
                    elif check_files:
                        md_path = _resolve_md_path(root, md_rel)
                        if not md_path.exists():
                            errors.append(f"{item_id} missing {field} file at {md_path}")

    if check_files:
        trans_path = root / "translations.en.json"
        if not trans_path.exists():
            errors.append(f"missing bilingual translation manifest at {trans_path}")
        else:
            trans = json.loads(trans_path.read_text(encoding="utf-8"))
            trans_cases = trans.get("cases", {})
            for item in data.get("cases", []):
                cid = item.get("id")
                t_entry = trans_cases.get(cid)
                if not isinstance(t_entry, dict):
                    errors.append(f"translations.en.json missing entry for case {cid}")
                    continue
                zh_p = _resolve_md_path(root, item["markdown_path"])
                en_p = _resolve_md_path(root, item["markdown_path_en"])
                if zh_p.exists() and t_entry.get("zh_sha256") != sha256_file(zh_p):
                    errors.append(f"translations.en.json zh_sha256 mismatch for {cid}")
                if en_p.exists() and t_entry.get("en_sha256") != sha256_file(en_p):
                    errors.append(f"translations.en.json en_sha256 mismatch for {cid}")

    for fb in data.get("feedback", []):
        fb_id = fb.get("id", "<feedback>")
        if fb.get("evidence_type") not in EVIDENCE_TYPES:
            errors.append(f"{fb_id} has invalid evidence_type")
        if not isinstance(fb.get("verified"), bool):
            errors.append(f"{fb_id} verified must be a boolean")

    return errors


def _field_text(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, (str, int, float)):
        return str(val).lower()
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False).lower()
    return ""


def score_item(item: dict[str, Any], terms: list[str], full_query: str) -> int:
    score = 0
    high_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_HIGH_FIELDS)
    med_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_MED_FIELDS)
    low_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_LOW_FIELDS)

    for term in terms:
        if not term:
            continue
        score += (1 if term in high_blob else 0) * 3
        score += (1 if term in med_blob else 0) * 2
        score += (1 if term in low_blob else 0) * 1

    if len(terms) > 1 and full_query:
        if full_query in high_blob:
            score += 6
        elif full_query in med_blob:
            score += 4
        elif full_query in low_blob:
            score += 2

    if full_query == str(item.get("id", "")).lower():
        score += 100

    return score


def infer_learning_origin(item: dict[str, Any], group: str, sources_by_id: dict[str, dict[str, Any]]) -> str:
    explicit = item.get("learning_origin")
    if isinstance(explicit, str) and explicit in LEARNING_ORIGINS:
        return explicit
    if group == "feedback":
        return "task_feedback"
    if group == "sources":
        kind = item.get("kind")
        if kind == "book":
            return "book_canon"
        if kind == "field_teardown":
            return "co_dissected_teardown"
        return "benchmark_study"
    for ref in item.get("source_refs", []):
        sid = ref.get("source_id") if isinstance(ref, dict) else None
        src = sources_by_id.get(sid) if isinstance(sid, str) else None
        if src:
            s_origin = infer_learning_origin(src, "sources", sources_by_id)
            if s_origin in ("co_dissected_teardown", "book_canon"):
                return s_origin
    return "benchmark_study"


def cmd_summary(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, catalog_path = load_catalog(root)
    sources_by_id = {s.get("id"): s for s in data.get("sources", []) if isinstance(s, dict) and s.get("id")}
    by_origin: dict[str, dict[str, int]] = {}
    for group in GROUPS:
        group_counts: dict[str, int] = {}
        for item in data.get(group, []):
            origin = infer_learning_origin(item, group, sources_by_id)
            group_counts[origin] = group_counts.get(origin, 0) + 1
        by_origin[group] = group_counts
    summary = {
        "library_root": str(root),
        "catalog_path": str(catalog_path),
        "schema_version": data.get("schema_version"),
        "revision": data.get("revision"),
        "updated_at": data.get("updated_at"),
        "bilingual_support": True,
        "counts": {group: len(data.get(group, [])) for group in GROUPS},
        "by_learning_origin": by_origin,
        "sources": [
            {
                "id": s.get("id"),
                "title": s.get("title"),
                "kind": s.get("kind"),
                "learning_origin": infer_learning_origin(s, "sources", sources_by_id),
                "reading_status": s.get("reading_status"),
                "version": s.get("version"),
            }
            for s in data.get("sources", [])
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def infer_evidence_stage(
    item: dict[str, Any],
    group: str,
    feedback_by_id: dict[str, dict[str, Any]],
) -> str:
    explicit = item.get("evidence_stage")
    if isinstance(explicit, str) and explicit in EVIDENCE_STAGES:
        return explicit
    if group == "feedback":
        ev_type = item.get("evidence_type")
        if ev_type in {"ab_test_result", "market_result"} and item.get("verified") is True:
            return "field_validated"
        return "user_endorsed" if item.get("verified") is True else "source_verified"
    if group == "methods":
        val_refs = item.get("validation_refs", [])
        if isinstance(val_refs, list) and val_refs:
            for fid in val_refs:
                fb = feedback_by_id.get(fid)
                if fb and fb.get("verified") is True and fb.get("evidence_type") in {"ab_test_result", "market_result"}:
                    return "field_validated"
            for fid in val_refs:
                fb = feedback_by_id.get(fid)
                if fb and fb.get("verified") is True:
                    return "user_endorsed"
        return "source_verified"
    if group == "cases":
        outcome = item.get("outcome_evidence")
        if isinstance(outcome, dict) and outcome.get("evidence_type") in {"ab_test_result", "market_result"}:
            return "field_validated"
        return "source_verified"
    return "source_verified"


def infer_evidence_type(
    item: dict[str, Any],
    group: str,
    origin: str,
    feedback_by_id: dict[str, dict[str, Any]],
) -> str:
    if group == "cases":
        outcome = item.get("outcome_evidence")
        if isinstance(outcome, dict) and outcome.get("evidence_type"):
            return str(outcome["evidence_type"])
    if group == "feedback" and item.get("evidence_type"):
        return str(item["evidence_type"])
    if group == "methods":
        if item.get("evidence_type"):
            return str(item["evidence_type"])
        for fid in item.get("validation_refs", []):
            fb = feedback_by_id.get(fid)
            if fb and fb.get("evidence_type"):
                return str(fb["evidence_type"])
    return origin


def cmd_search(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, _ = load_catalog(root)
    sources_by_id = {s.get("id"): s for s in data.get("sources", []) if isinstance(s, dict) and s.get("id")}
    feedback_by_id = {f.get("id"): f for f in data.get("feedback", []) if isinstance(f, dict) and f.get("id")}
    full_query = args.query.strip().lower()
    terms = [t for t in full_query.split() if t]
    groups = [args.kind] if args.kind != "all" else list(GROUPS)
    matches = []

    for group in groups:
        for item in data.get(group, []):
            origin = infer_learning_origin(item, group, sources_by_id)
            if args.status and item.get("status") != args.status:
                continue
            if args.channel and args.channel not in item.get("channels", []):
                continue
            if getattr(args, "origin", None) and origin != args.origin:
                continue
            score = score_item(item, terms, full_query)
            if score > 0:
                entry: dict[str, Any] = {
                    "group": group,
                    "id": item.get("id"),
                    "version": item.get("version"),
                    "learning_origin": origin,
                    "evidence_stage": infer_evidence_stage(item, group, feedback_by_id),
                    "evidence_type": infer_evidence_type(item, group, origin, feedback_by_id),
                    "title": item.get("title"),
                    "title_en": item.get("title_en"),
                    "status": item.get("status", item.get("reading_status")),
                    "score": score,
                    "when_stuck": item.get("when_stuck"),
                    "tags": item.get("tags", []),
                    "tags_en": item.get("tags_en", []),
                    "summary": item.get("rule") or item.get("reusable_move") or item.get("observation") or item.get("coverage_note"),
                    "summary_en": item.get("rule_en") or item.get("reusable_move_en") or item.get("observation_en") or item.get("coverage_note_en"),
                }
                if group == "methods":
                    entry["applies_when"] = item.get("applies_when")
                    entry["limits"] = item.get("limits")
                if group == "cases":
                    entry["markdown_path"] = item.get("markdown_path")
                    entry["markdown_path_en"] = item.get("markdown_path_en")
                    entry["copy_visual_synergy"] = item.get("copy_visual_synergy")
                    entry["asset_prerequisites"] = item.get("asset_prerequisites")
                    entry["transfer_limits"] = item.get("transfer_limits")
                matches.append(entry)

    matches.sort(key=lambda row: (-row["score"], row["id"] or ""))
    print(json.dumps(matches[: args.limit], ensure_ascii=False, indent=2))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, _ = load_catalog(root)
    requested_ids: list[str] = args.ids
    found_map: dict[str, dict[str, Any]] = {}

    for group in GROUPS:
        for item in data.get(group, []):
            item_id = item.get("id")
            if item_id in requested_ids:
                record = {"group": group, "item": copy.deepcopy(item)}
                if group == "cases":
                    if item.get("markdown_path"):
                        md_path = _resolve_md_path(root, item["markdown_path"])
                        record["markdown_resolved_path"] = str(md_path)
                        record["markdown_exists"] = md_path.exists()
                    if item.get("markdown_path_en"):
                        md_en_path = _resolve_md_path(root, item["markdown_path_en"])
                        record["markdown_en_resolved_path"] = str(md_en_path)
                        record["markdown_en_exists"] = md_en_path.exists()
                found_map[item_id] = record

    missing = [rid for rid in requested_ids if rid not in found_map]
    results = [found_map[rid] for rid in requested_ids if rid in found_map]

    if len(requested_ids) == 1 and results and not missing:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
        return 0

    output = {
        "requested_count": len(requested_ids),
        "found_count": len(results),
        "missing_ids": missing,
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if missing else 0


def cmd_validate(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, _ = load_catalog(root)
    errors = validate_catalog(data, root, check_files=args.check_files)
    result = {
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
        "catalog_revision": data.get("revision"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def cmd_apply_patch(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, catalog_path = load_catalog(root)
    patch_path = Path(args.file).expanduser().resolve()
    if not patch_path.exists():
        print(json.dumps({"applied": False, "error": f"Patch file not found: {patch_path}"}, ensure_ascii=False, indent=2))
        return 1

    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    new_data = copy.deepcopy(data)
    old_revision = new_data.get("revision", 1)
    added_ids: list[str] = []
    updated_ids: list[str] = []

    for group in GROUPS:
        patch_items = patch.get(group, [])
        if not isinstance(patch_items, list):
            continue
        existing_list = new_data.setdefault(group, [])
        index_by_id = {item.get("id"): idx for idx, item in enumerate(existing_list) if isinstance(item, dict)}
        for p_item in patch_items:
            p_id = p_item.get("id")
            if p_id in index_by_id:
                idx = index_by_id[p_id]
                old_ver = existing_list[idx].get("version", 1)
                merged = copy.deepcopy(existing_list[idx])
                merged.update(p_item)
                if "version" not in p_item or p_item["version"] <= old_ver:
                    merged["version"] = old_ver + 1
                existing_list[idx] = merged
                updated_ids.append(p_id)
            else:
                if "version" not in p_item:
                    p_item["version"] = 1
                existing_list.append(p_item)
                added_ids.append(p_id)

    new_data["revision"] = old_revision + 1
    new_data["updated_at"] = patch.get("updated_at") or dt.date.today().isoformat()

    errors = validate_catalog(new_data, root, check_files=args.check_files)
    if errors:
        print(
            json.dumps(
                {
                    "applied": False,
                    "rolled_back": True,
                    "error_count": len(errors),
                    "errors": errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    history_dir = root / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    backup_path = history_dir / f"catalog-r{old_revision}.json"
    shutil.copy2(catalog_path, backup_path)

    catalog_path.write_text(json.dumps(new_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "applied": True,
                "previous_revision": old_revision,
                "new_revision": new_data["revision"],
                "backup_path": str(backup_path),
                "added_ids": added_ids,
                "updated_ids": updated_ids,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", help="Path to the art direction library root")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("summary", help="Show library counts and source status")

    search = sub.add_parser("search", help="Weighted bilingual & symptom search across methods, cases, sources, feedback")
    search.add_argument("query", help="Search query (supports space-separated bilingual keywords & symptoms)")
    search.add_argument("--kind", choices=["all", *GROUPS], default="all")
    search.add_argument("--status", choices=sorted(STATUS_VALUES))
    search.add_argument("--channel", help="Filter by channel (e.g. pdp, landing_page, ad_banner, spec_sheet)")
    search.add_argument("--origin", choices=sorted(LEARNING_ORIGINS), help="Filter by learning origin (book_canon, benchmark_study, co_dissected_teardown, task_feedback)")
    search.add_argument("--limit", type=int, default=8)

    get_p = sub.add_parser("get", help="Fetch one or more records by ID in a single batch call")
    get_p.add_argument("ids", nargs="+", help="One or more record IDs (e.g. M-001 M-004 C-baymard-in-scale-reference)")

    val = sub.add_parser("validate", help="Validate catalog schema, references, and bilingual case files")
    val.add_argument("--check-files", action="store_true", help="Verify local source files, bilingual markdown cards, and SHA-256 digests")

    patch = sub.add_parser("apply-patch", help="Atomically merge a JSON patch into catalog.json with backup and validation")
    patch.add_argument("--file", required=True, help="Path to patch JSON file")
    patch.add_argument("--check-files", action="store_true", help="Also verify referenced files exist before committing")

    args = parser.parse_args()
    commands = {
        "summary": cmd_summary,
        "search": cmd_search,
        "get": cmd_get,
        "validate": cmd_validate,
        "apply-patch": cmd_apply_patch,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
