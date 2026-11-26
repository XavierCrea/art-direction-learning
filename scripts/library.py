#!/usr/bin/env python3
"""Inspect, search, batch-get, validate, and atomically patch the art-direction-learning bilingual library."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

GROUPS = ("sources", "methods", "cases", "feedback")
STATUS_VALUES = {"reference", "candidate", "validated", "retired"}
EVIDENCE_STAGES = {"source_verified", "user_endorsed", "field_validated"}
PROJECT_STATUSES = {"endorsed", "adopted"}
PROJECT_RESULT_TYPES = {"ab_test", "ab_test_result", "market_result"}
AUDIENCE_OUTCOME_TYPES = PROJECT_RESULT_TYPES | {"usability_benchmark", "case_study_metric"}
REPORTED_OUTCOME_STATES = {"source_verified", "source_reported"}
OUTCOME_STATES = REPORTED_OUTCOME_STATES | {"verified", "unverified", "verified_field_observation"}
CASE_HASH_MODE = "utf8-lf"
CASE_FILES = (("markdown_path", "zh_sha256"), ("markdown_path_en", "en_sha256"))
CHINESE_RUN = re.compile(r"[㐀-䶿一-鿿]{3,}")
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
        config = read_json(config_path)
        default_root = config.get("default_library_root", "library")
        candidate = Path(default_root).expanduser()
        return candidate.resolve() if candidate.is_absolute() else (skill_root() / candidate).resolve()
    return (skill_root() / "library").resolve()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def load_catalog(root: Path) -> tuple[dict[str, Any], Path]:
    catalog_path = root / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError(f"catalog.json not found at {catalog_path}")
    return read_json(catalog_path), catalog_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()



def _resolve_md_path(root: Path, md_rel: str) -> Path:
    relative = md_rel.replace("\\", "/")
    if relative.startswith("library/"):
        relative = relative[len("library/"):]
    return (root / relative).resolve()


def normalized_case_bytes(raw: bytes) -> bytes:
    return raw.removeprefix(b"\xef\xbb\xbf").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def case_digest_matches(path: Path, expected: str | None, mode: str | None) -> bool:
    raw = path.read_bytes()
    content = normalized_case_bytes(raw)
    if mode == CASE_HASH_MODE:
        return hashlib.sha256(content).hexdigest() == expected
    # A legacy manifest may have fingerprinted either a Windows or a macOS checkout.
    crlf = content.replace(b"\n", b"\r\n")
    return any(hashlib.sha256(form).hexdigest() == expected for form in (raw, content, crlf))


def read_committed_translations(root: Path, revision: int) -> dict[str, Any] | None:
    path = root / "translations.en.json"
    if not path.is_file():
        return None
    manifest = read_json(path)
    staged_revision = manifest.get("catalog_revision")
    if isinstance(staged_revision, int) and staged_revision > revision:
        previous = root / "history" / f"translations-r{revision}.json"
        return read_json(previous) if previous.is_file() else None
    return manifest


def _valid_when_stuck(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict) and set(value.keys()) == {"zh", "en"}:
        return all(
            isinstance(v, list) and bool(v) and all(isinstance(s, str) and bool(s.strip()) for s in v)
            for v in value.values()
        )
    return False


def validate_catalog(
    data: dict[str, Any],
    root: Path,
    check_files: bool = False,
    translations: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(data.get("revision"), int) or data["revision"] < 1:
        errors.append("revision must be a positive integer")
    for group in GROUPS:
        if not isinstance(data.get(group), list):
            errors.append(f"{group} must be a list")
        elif any(not isinstance(item, dict) for item in data[group]):
            errors.append(f"{group} must contain only objects")
    if errors:
        return errors

    ids: dict[str, str] = {}
    sources_by_id: dict[str, dict[str, Any]] = {}
    feedback_by_id: dict[str, dict[str, Any]] = {}

    for group in GROUPS:
        for index, item in enumerate(data.get(group, [])):
            label = f"{group}[{index}]"
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
            file_path = root / rel_path.replace("\\", "/")
            if not file_path.is_file():
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
            val_refs = item.get("validation_refs", [])
            if not isinstance(val_refs, list) or not all(isinstance(fid, str) for fid in val_refs):
                errors.append(f"{item_id} validation_refs must be a list of feedback IDs")
            else:
                if status == "validated" and not val_refs:
                    errors.append(f"{item_id} is validated but has no validation_refs")
                for feedback_id in val_refs:
                    fb = feedback_by_id.get(feedback_id)
                    if not fb:
                        errors.append(f"{item_id} validation_ref {feedback_id!r} not found")
                    elif status == "validated" and fb.get("verified") is not True:
                        errors.append(f"{item_id} validation_ref {feedback_id!r} is not verified")

            if group == "cases":
                outcome = item.get("outcome_evidence")
                if not isinstance(outcome, dict):
                    errors.append(f"{item_id} outcome_evidence must be an object")
                else:
                    if outcome.get("evidence_type") not in EVIDENCE_TYPES:
                        errors.append(f"{item_id} outcome_evidence has invalid evidence_type")
                    state = outcome.get("verification_status")
                    if state is not None and (not isinstance(state, str) or state not in OUTCOME_STATES):
                        errors.append(f"{item_id} outcome_evidence has invalid verification_status {state!r}")
                    if state == "verified" and not has_text(outcome.get("claim")):
                        errors.append(f"{item_id} verified outcome needs a recorded result")
                for field, _ in CASE_FILES:
                    md_rel = item.get(field)
                    if not isinstance(md_rel, str) or not md_rel.strip():
                        errors.append(f"{item_id} {field} must be a non-empty string")
                    elif check_files:
                        md_path = _resolve_md_path(root, md_rel)
                        if not md_path.is_file():
                            errors.append(f"{item_id} missing {field} file at {md_path}")


    if check_files:
        trans_path = root / "translations.en.json"
        if translations is None:
            translations = read_committed_translations(root, data["revision"])
        if translations is None:
            errors.append(f"missing bilingual translation manifest at {trans_path}")
        else:
            trans_cases = translations.get("cases")
            if not isinstance(trans_cases, dict):
                errors.append("translations.en.json cases must be an object")
                trans_cases = {}
            for item in data["cases"]:
                cid = item.get("id")
                entry = trans_cases.get(cid)
                if not isinstance(entry, dict):
                    errors.append(f"translations.en.json missing entry for case {cid}")
                    continue
                mode = entry.get("hash_mode", translations.get("hash_mode"))
                if mode not in (None, CASE_HASH_MODE):
                    errors.append(f"translations.en.json invalid hash_mode for {cid}")
                    continue
                for path_field, hash_field in CASE_FILES:
                    relative = item.get(path_field)
                    if not has_text(relative):
                        continue
                    card_path = _resolve_md_path(root, relative)
                    if card_path.is_file() and not case_digest_matches(card_path, entry.get(hash_field), mode):
                        errors.append(f"translations.en.json {hash_field} mismatch for {cid}")

    for fb in data["feedback"]:
        fb_id = fb.get("id", "<feedback>")
        if fb.get("evidence_type") not in EVIDENCE_TYPES:
            errors.append(f"{fb_id} has invalid evidence_type")
        if not isinstance(fb.get("verified"), bool):
            errors.append(f"{fb_id} verified must be a boolean")
        state = fb.get("project_status")
        if state is not None and (not isinstance(state, str) or state not in PROJECT_STATUSES):
            errors.append(f"{fb_id} has invalid project_status {state!r}")
        elif state and not confirmed_feedback(fb):
            errors.append(f"{fb_id} project_status needs verified feedback with a locator and observation")

    if errors:
        return errors
    for group in GROUPS:
        for item in data[group]:
            explicit = item.get("evidence_stage")
            if explicit is None:
                continue
            if not isinstance(explicit, str) or explicit not in EVIDENCE_STAGES:
                errors.append(f"{item['id']} has invalid evidence_stage {explicit!r}")
                continue
            profile = build_evidence_profile(item, group, sources_by_id, feedback_by_id)
            supported = {
                "source_verified": profile["source_checked"],
                "user_endorsed": profile["project_status"] in PROJECT_STATUSES,
                "field_validated": profile["audience_result"].startswith("verified"),
            }
            if not supported[explicit]:
                errors.append(f"{item['id']} evidence_stage {explicit!r} lacks supporting evidence")
    return errors


def _field_text(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, (str, int, float)):
        return str(val).lower()
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False).lower()
    return ""



def chinese_phrase_score(item: dict[str, Any], full_query: str) -> int:
    clauses = CHINESE_RUN.findall(full_query)
    if not clauses:
        return 0
    symptoms = item.get("when_stuck")
    if isinstance(symptoms, dict):
        symptoms = symptoms.get("zh", [])
    labels = [*item.get("tags", []), *(symptoms if isinstance(symptoms, list) else [symptoms])]
    short_labels = {label for label in labels if isinstance(label, str) and CHINESE_RUN.fullmatch(label)}
    phrase_text = f"{_field_text(labels)} {_field_text(item.get('title'))}"
    phrases = {part for part in CHINESE_RUN.findall(phrase_text) if len(part) >= 4 or part in short_labels}

    best = 0
    for clause in clauses:
        grams = {clause[i:i + 3] for i in range(len(clause) - 2)}
        for phrase in phrases:
            if clause in phrase or phrase in clause:
                shared = min(len(clause), len(phrase))
                best = max(best, min(20, 5 + shared) if shared >= 4 or clause == phrase else 4)
                continue
            other = {phrase[i:i + 3] for i in range(len(phrase) - 2)}
            common = len(grams & other)
            if common >= 2 and common * 3 >= min(len(grams), len(other)) * 2:
                best = max(best, min(6, common))
    return best


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

    score += chinese_phrase_score(item, full_query)
    symptoms = item.get("when_stuck")
    labels = [*item.get("tags", []), *item.get("tags_en", [])]
    if isinstance(symptoms, dict):
        labels.extend([*symptoms.get("en", []), *symptoms.get("zh", [])])
    if full_query and full_query in {_field_text(label).strip() for label in labels}:
        score += 8

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



def has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def checked_source(source: dict[str, Any]) -> bool:
    return source.get("reading_status") in {"partial_review", "full_review"} and bool(source.get("reviewed_locations"))


def confirmed_feedback(feedback: dict[str, Any]) -> bool:
    return (
        feedback.get("verified") is True
        and has_text(feedback.get("source_locator"))
        and has_text(feedback.get("observation"))
    )


def build_evidence_profile(
    item: dict[str, Any],
    group: str,
    sources_by_id: dict[str, dict[str, Any]],
    feedback_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if group == "sources":
        source_checked = checked_source(item)
    elif group == "feedback":
        source_checked = confirmed_feedback(item)
    else:
        source_checked = any(
            checked_source(sources_by_id[ref["source_id"]])
            for ref in item.get("source_refs", [])
            if isinstance(ref, dict) and ref.get("source_id") in sources_by_id
        )

    feedback = [item] if group == "feedback" else [
        feedback_by_id[fid] for fid in item.get("validation_refs", []) if fid in feedback_by_id
    ]
    adopted, endorsed, results = [], [], []
    for entry in feedback:
        accepted = confirmed_feedback(entry)
        project_status = entry.get("project_status")
        if accepted and project_status == "adopted":
            adopted.append(entry["id"])
        elif accepted and (
            project_status == "endorsed" or (project_status is None and entry.get("evidence_type") == "editorial_feedback")
        ):
            endorsed.append(entry["id"])
        if entry.get("evidence_type") in PROJECT_RESULT_TYPES:
            results.append({
                "status": "verified" if accepted else "unverified",
                "evidence_type": entry["evidence_type"],
                "claim": entry.get("observation"),
                "source": entry["id"],
            })

    outcome = item.get("outcome_evidence")
    if group == "cases" and isinstance(outcome, dict) and outcome.get("evidence_type") in AUDIENCE_OUTCOME_TYPES:
        state = outcome.get("verification_status")
        verified = source_checked and state == "verified" and has_text(outcome.get("claim"))
        reported = source_checked and state in REPORTED_OUTCOME_STATES and has_text(outcome.get("claim"))
        results.append({
            "status": "verified" if verified else "source_reported" if reported else "unverified",
            "evidence_type": outcome["evidence_type"],
            "claim": outcome.get("claim"),
            "source": item["id"],
        })

    best_result = next(
        (result for state in ("verified", "source_reported", "unverified") for result in results if result["status"] == state),
        None,
    )
    return {
        "source_checked": source_checked,
        "project_status": "adopted" if adopted else "endorsed" if endorsed else "none",
        "project_refs": [*adopted, *endorsed],
        "project_adopted": adopted or False,
        "audience_result": f"{best_result['status']}:{best_result['evidence_type']}" if best_result else "none",
        "audience_evidence": results,
    }


def infer_evidence_stage(profile: dict[str, Any]) -> str | None:
    if profile["audience_result"].startswith("verified"):
        return "field_validated"
    if profile["project_status"] in PROJECT_STATUSES:
        return "user_endorsed"
    return "source_verified" if profile["source_checked"] else None


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
                profile = build_evidence_profile(item, group, sources_by_id, feedback_by_id)
                entry: dict[str, Any] = {
                    "group": group,
                    "id": item.get("id"),
                    "version": item.get("version"),
                    "learning_origin": origin,
                    "evidence_stage": infer_evidence_stage(profile),
                    "evidence_type": infer_evidence_type(item, group, origin, feedback_by_id),
                    "evidence_profile": profile,
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


def write_atomic(path: Path, content: bytes) -> None:
    with tempfile.NamedTemporaryFile(prefix=f".{path.name}.", dir=path.parent, delete=False) as handle:
        staged = Path(handle.name)
        try:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            handle.close()
            staged.unlink(missing_ok=True)
            raise
    try:
        if path.exists():
            staged.chmod(stat.S_IMODE(path.stat().st_mode))
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def lock_writer(handle: Any) -> None:
    if os.name == "nt":
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)


def refresh_case_fingerprints(
    root: Path,
    catalog: dict[str, Any],
    case_ids: set[str],
    manifest: dict[str, Any],
) -> list[str]:
    records = manifest.setdefault("cases", {})
    if not isinstance(records, dict):
        return ["translations.en.json cases must be an object"]
    errors = []
    for case in catalog["cases"]:
        cid = case["id"]
        if cid not in case_ids:
            continue
        existing = records.get(cid)
        entry = dict(existing) if isinstance(existing, dict) else {}
        entry.update(title=case.get("title"), title_en=case.get("title_en"), hash_mode=CASE_HASH_MODE)
        for path_field, hash_field in CASE_FILES:
            relative = case.get(path_field)
            if not has_text(relative):
                errors.append(f"{cid} {path_field} must be a non-empty string")
                continue
            card = _resolve_md_path(root, relative)
            if not card.is_file():
                errors.append(f"{cid} missing {path_field} file at {card}")
                continue
            entry[path_field] = relative
            entry[hash_field] = hashlib.sha256(normalized_case_bytes(card.read_bytes())).hexdigest()
        records[cid] = entry
    manifest["catalog_revision"] = catalog["revision"]
    manifest["updated_at"] = catalog["updated_at"]
    return errors


def apply_catalog_patch(root: Path, patch: dict[str, Any], check_files: bool) -> dict[str, Any]:
    data, catalog_path = load_catalog(root)
    old_catalog = catalog_path.read_bytes()
    old_revision = data["revision"]
    manifest_path = root / "translations.en.json"
    if manifest_path.is_file():
        current = read_json(manifest_path)
        staged_revision = current.get("catalog_revision")
        if isinstance(staged_revision, int) and staged_revision > old_revision:
            previous = root / "history" / f"translations-r{old_revision}.json"
            if previous.is_file():
                write_atomic(manifest_path, previous.read_bytes())
            elif not data["cases"]:
                manifest_path.unlink()
            else:
                raise ValueError(f"missing manifest backup for catalog r{old_revision}")
    added_ids, updated_ids = [], []
    changed_cases: set[str] = set()

    for group in GROUPS:
        patch_items = patch.get(group, [])
        if not isinstance(patch_items, list) or any(not isinstance(item, dict) for item in patch_items):
            raise ValueError(f"patch {group} must be a list of objects")
        indexed = {item["id"]: index for index, item in enumerate(data[group])}
        encountered = set()
        for changes in patch_items:
            record_id = changes.get("id")
            if not has_text(record_id) or record_id in encountered:
                raise ValueError(f"missing or duplicate patch ID in {group}: {record_id!r}")
            encountered.add(record_id)
            version = changes.get("version")
            if version is not None and (type(version) is not int or version < 1):
                raise ValueError(f"{record_id} version must be a positive integer")
            if record_id in indexed:
                current = data[group][indexed[record_id]]
                previous_version = current["version"]
                current.update(changes)
                current["version"] = max(previous_version + 1, version or 1)
                updated_ids.append(record_id)
            else:
                data[group].append({**changes, "version": version or 1})
                added_ids.append(record_id)
            if group == "cases":
                changed_cases.add(record_id)

    data["revision"] = old_revision + 1
    data["updated_at"] = patch.get("updated_at") or dt.date.today().isoformat()
    manifest = None
    if check_files and changed_cases:
        manifest = read_json(manifest_path) if manifest_path.is_file() else {"schema_version": 1, "language": "en"}
        errors = refresh_case_fingerprints(root, data, changed_cases, manifest)
        if errors:
            return {"applied": False, "error_count": len(errors), "errors": errors}

    errors = validate_catalog(data, root, check_files, manifest)
    if errors:
        return {"applied": False, "error_count": len(errors), "errors": errors}

    backup = root / "history" / f"catalog-r{old_revision}.json"
    write_atomic(backup, old_catalog)
    if manifest is None:
        write_atomic(catalog_path, json_bytes(data))
    else:
        old_manifest = manifest_path.read_bytes() if manifest_path.is_file() else None
        if old_manifest is not None:
            write_atomic(root / "history" / f"translations-r{old_revision}.json", old_manifest)
        try:
            write_atomic(manifest_path, json_bytes(manifest))
            write_atomic(catalog_path, json_bytes(data))
        except BaseException:
            if catalog_path.read_bytes() == old_catalog:
                if old_manifest is None:
                    manifest_path.unlink(missing_ok=True)
                elif manifest_path.read_bytes() != old_manifest:
                    write_atomic(manifest_path, old_manifest)
            raise
    return {
        "applied": True,
        "previous_revision": old_revision,
        "new_revision": data["revision"],
        "backup_path": str(backup),
        "added_ids": added_ids,
        "updated_ids": updated_ids,
    }


def cmd_apply_patch(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    try:
        patch = read_json(Path(args.file).expanduser().resolve())
        if not isinstance(patch, dict):
            raise ValueError("patch must be an object")
        history = root / "history"
        history.mkdir(exist_ok=True)
        with (history / ".library.lock").open("a+b") as lock:
            lock_writer(lock)
            result = apply_catalog_patch(root, patch, args.check_files)
    except (OSError, ValueError) as exc:
        result = {"applied": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["applied"] else 1


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
