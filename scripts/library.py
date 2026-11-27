#!/usr/bin/env python3
"""Inspect, search, batch-get, validate, and atomically patch the art-direction-learning bilingual library."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import math
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
CHANNEL_VALUES = {
    "ad_banner",
    "catalog",
    "exhibition",
    "landing_page",
    "mobile_ui",
    "packaging",
    "pdp",
    "presentation",
    "print_collateral",
    "social_carousel",
    "social_feed",
    "spec_sheet",
    "storefront",
}
CASE_HASH_MODE = "utf8-lf"
CASE_FILES = (("markdown_path", "zh_sha256"), ("markdown_path_en", "en_sha256"))
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
DESCRIPTOR_NAMES = ("descriptor.svg", "descriptor.png")
MAX_HISTORY_REVISIONS = 5
CHINESE_RUN = re.compile(r"[㐀-䶿一-鿿]{2,}")
CHINESE_RUN_LONG = re.compile(r"[㐀-䶿一-鿿]{3,}")
EN_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[:.-][a-z0-9]+)*")
EN_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "of", "in", "on", "at",
    "for", "with", "by", "from", "as", "it", "its", "this", "that", "these", "those",
    "and", "or", "not", "no", "but", "if", "so", "too", "very", "just", "how", "why",
    "what", "when", "where", "who", "can", "do", "does", "did", "my", "our", "your",
    "look", "looks", "looking", "feel", "feels", "make", "makes", "get", "gets",
}
ZH_STOP_BIGRAMS = {
    "没有", "不是", "什么", "为什", "么在", "怎么", "怎样", "如何", "哪里", "哪些",
    "可以", "一个", "一种", "这个", "那个", "这样", "那样", "这么", "那么", "起来",
    "看起", "太多", "没人", "人看", "显得", "感觉", "非常", "有点", "应该", "需要",
    "如果", "就是", "还是", "或者", "以及", "通过", "进行", "使用", "时候", "地方",
    "东西", "问题", "意思", "因为", "所以", "但是", "不过", "而且", "并且", "虽然",
    "可是", "已经", "正在", "根本", "实际", "来很", "多没", "寸没", "有参", "图看",
    "品看", "很廉", "数太", "维尺", "的时", "候用", "来做",
}
SYNONYM_EXPANSIONS: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("看不清", "不清", "模糊", "看不出", "看不懂", "辨认"), ("特写", "引线", "图注", "callout", "crop", "ambiguous")),
    (("尺寸", "大小", "体积", "多大", "长宽高", "三维"), ("比例", "参照", "in-scale", "size", "scale")),
    (("参数", "规格", "配置", "指标", "数据表"), ("参数表", "规格表", "扫描", "分组", "spec", "scannability", "table")),
    (("廉价", "低端", "土气", "地摊", "low", "cheap", "budget"), ("层级", "边框", "降噪", "去促销", "促销", "价签", "hierarchy", "promo", "cluttered", "cramped")),
    (("高价", "太贵", "显得贵", "定价", "套餐", "expensive", "pricing"), ("锚点", "梯度", "价签", "pricing", "tier", "price")),
    (("太乱", "杂乱", "塞满", "堆砌", "拥挤", "clutter", "messy"), ("噪音", "亲密性", "对齐", "留白", "层级", "noise", "crap", "hierarchy")),
    (("没人看", "没人点", "停滑", "划走", "点击率", "ctr"), ("扫视", "孤立", "停滑", "原生", "广告牌", "hook", "billboard", "native")),
    (("遮挡", "裁切", "挡住", "竖屏"), ("安全区", "9:16", "safe", "zones")),
    (("配件", "赠品", "送不送", "清单"), ("标配", "选配", "全家福", "accessories", "included")),
    (("像模板", "模板", "呆板", "平庸"), ("层级", "边框", "非对称", "对比", "hierarchy", "grid")),
)
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
        "channels",
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

ALLOWED_FIELDS = {
    "sources": REQUIRED["sources"]
    | {
        "author",
        "coverage_note",
        "coverage_note_en",
        "isbn",
        "learning_origin",
        "local_path",
        "original_availability",
        "path",
        "pdf_pages",
        "published_at",
        "publisher",
        "secondary_url",
        "sha256",
        "updated_at",
        "url",
        "urls",
    },
    "methods": REQUIRED["methods"]
    | {
        "allowed_genres",
        "evidence_stage",
        "evidence_type",
        "forbidden_genres",
        "learning_origin",
        "scope_layer",
    },
    "cases": REQUIRED["cases"]
    | {
        "evidence_stage",
        "inquiry_chain",
        "learning_origin",
        "method_refs",
        "validation_refs",
    },
    "feedback": REQUIRED["feedback"]
    | {
        "cases_used",
        "date",
        "evidence_stage",
        "learning_origin",
        "methods_used",
        "observation_en",
        "project_status",
        "reusable_lesson",
        "title_en",
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
    methods_by_id: dict[str, dict[str, Any]] = {}
    feedback_by_id: dict[str, dict[str, Any]] = {}

    for group in GROUPS:
        for index, item in enumerate(data.get(group, [])):
            label = f"{group}[{index}]"
            missing = sorted(REQUIRED[group] - set(item.keys()))
            if missing:
                errors.append(f"{label} ({item.get('id', 'unknown')}) missing required fields: {', '.join(missing)}")
            unknown = sorted(set(item.keys()) - ALLOWED_FIELDS[group])
            if unknown:
                errors.append(f"{label} ({item.get('id', 'unknown')}) has unknown fields: {', '.join(unknown)}")
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
            if group == "methods" and isinstance(item_id, str):
                methods_by_id[item_id] = item
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
            channels = item.get("channels")
            if not isinstance(channels, list) or not channels or not all(
                isinstance(ch, str) and ch in CHANNEL_VALUES for ch in channels
            ):
                errors.append(f"{item_id} channels must be a non-empty list of valid channels")
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
                method_refs = item.get("method_refs")
                if method_refs is not None:
                    if not isinstance(method_refs, list) or not all(isinstance(mid, str) for mid in method_refs):
                        errors.append(f"{item_id} method_refs must be a list of method IDs")
                    else:
                        for mid in method_refs:
                            if mid not in methods_by_id:
                                errors.append(f"{item_id} method_ref {mid!r} not found")
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


def collect_catalog_warnings(data: dict[str, Any], root: Path) -> list[str]:
    warnings: list[str] = []
    referenced_methods: set[str] = set()
    for case in data.get("cases", []):
        cid = case.get("id", "<case>")
        mrefs = case.get("method_refs")
        if not isinstance(mrefs, list) or not mrefs:
            warnings.append(f"{cid} has no method_refs (cannot be joined automatically to methods)")
        else:
            referenced_methods.update(mid for mid in mrefs if isinstance(mid, str))

    for method in data.get("methods", []):
        mid = method.get("id")
        if isinstance(mid, str) and mid not in referenced_methods:
            warnings.append(f"{mid} is not referenced by any case method_refs (orphan method)")

    for style in load_styles(root):
        if not style["has_local_anchors"]:
            fallback = "descriptor card available" if style["has_descriptor"] else "text-only fallback"
            warnings.append(
                f"style {style['id']} has 0 local anchor images in {style['local_refs_dir']} ({fallback})"
            )
    return warnings


def _field_text(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, (str, int, float)):
        return str(val).lower()
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False).lower()
    return ""



def _extract_tokens(text: str, include_stopwords: bool = False) -> list[str]:
    tokens: list[str] = []
    lowered = text.lower()
    for tok in EN_TOKEN_RE.findall(lowered):
        if len(tok) < 2:
            continue
        if not include_stopwords and tok in EN_STOPWORDS:
            continue
        tokens.append(tok)
    for run in CHINESE_RUN.findall(lowered):
        if len(run) == 2:
            if include_stopwords or run not in ZH_STOP_BIGRAMS:
                tokens.append(run)
        else:
            for i in range(len(run) - 1):
                bg = run[i : i + 2]
                if include_stopwords or bg not in ZH_STOP_BIGRAMS:
                    tokens.append(bg)
    return tokens


def _expand_query_terms(full_query: str, base_tokens: list[str]) -> list[str]:
    expanded: list[str] = []
    seen = set(base_tokens)
    for triggers, synonyms in SYNONYM_EXPANSIONS:
        if any(trig in full_query or trig in seen for trig in triggers):
            for syn in synonyms:
                if syn not in seen:
                    seen.add(syn)
                    expanded.append(syn)
    return expanded


def _build_idf(items: list[dict[str, Any]]) -> dict[str, float]:
    n_docs = max(len(items), 1)
    df: dict[str, int] = {}
    for item in items:
        blob = " ".join(
            _field_text(item.get(f))
            for f in (*WEIGHT_HIGH_FIELDS, *WEIGHT_MED_FIELDS, *WEIGHT_LOW_FIELDS)
        )
        doc_tokens = set(_extract_tokens(blob, include_stopwords=True))
        for tok in doc_tokens:
            df[tok] = df.get(tok, 0) + 1
    return {tok: math.log((n_docs + 1.0) / (freq + 1.0)) + 1.0 for tok, freq in df.items()}


def chinese_phrase_score(item: dict[str, Any], full_query: str) -> int:
    clauses = CHINESE_RUN_LONG.findall(full_query)
    if not clauses:
        return 0
    symptoms = item.get("when_stuck")
    if isinstance(symptoms, dict):
        symptoms = symptoms.get("zh", [])
    labels = [*item.get("tags", []), *(symptoms if isinstance(symptoms, list) else [symptoms])]
    short_labels = {label for label in labels if isinstance(label, str) and CHINESE_RUN_LONG.fullmatch(label)}
    phrase_text = f"{_field_text(labels)} {_field_text(item.get('title'))}"
    phrases = {part for part in CHINESE_RUN_LONG.findall(phrase_text) if len(part) >= 4 or part in short_labels}

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


def _prepare_query(full_query: str) -> tuple[list[str], list[str], list[str]]:
    terms = [t for t in full_query.split() if t]
    query_tokens = _extract_tokens(full_query, include_stopwords=False)
    if not query_tokens:
        query_tokens = _extract_tokens(full_query, include_stopwords=True)
    unique_tokens = list(dict.fromkeys(query_tokens))
    expanded_tokens = _expand_query_terms(full_query, unique_tokens)
    return terms, unique_tokens, expanded_tokens


def score_item(
    item: dict[str, Any],
    terms: list[str],
    full_query: str,
    idf_map: dict[str, float] | None = None,
    prepared_query: tuple[list[str], list[str], list[str]] | None = None,
) -> float:
    score = 0.0
    high_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_HIGH_FIELDS)
    med_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_MED_FIELDS)
    low_blob = " ".join(_field_text(item.get(f)) for f in WEIGHT_LOW_FIELDS)

    if full_query == str(item.get("id", "")).lower():
        return 100.0

    if prepared_query is not None:
        _, unique_tokens, expanded_tokens = prepared_query
    else:
        _, unique_tokens, expanded_tokens = _prepare_query(full_query)

    def _idf(tok: str) -> float:
        if idf_map is None:
            return 1.5
        return idf_map.get(tok, 1.5)

    # Space-separated raw terms (exact word/phrase hits get strong IDF-weighted score)
    matched_primary = 0
    for term in terms:
        if not term or term in EN_STOPWORDS or term in ZH_STOP_BIGRAMS:
            continue
        hit_h = term in high_blob
        hit_m = term in med_blob
        hit_l = term in low_blob
        if hit_h or hit_m or hit_l:
            matched_primary += 1
            w = _idf(term)
            score += (3.0 if hit_h else 0.0) * w
            score += (2.0 if hit_m else 0.0) * w
            score += (1.0 if hit_l else 0.0) * w

    # Tokenized English words & CJK bi-grams
    matched_tokens = 0
    for tok in unique_tokens:
        hit_h = tok in high_blob
        hit_m = tok in med_blob
        hit_l = tok in low_blob
        if hit_h or hit_m or hit_l:
            matched_tokens += 1
            w = _idf(tok)
            # Avoid double-counting if identical to a space-separated term already scored
            mult = 0.45 if tok in terms else 1.0
            score += mult * w * ((2.6 if hit_h else 0.0) + (1.6 if hit_m else 0.0) + (0.7 if hit_l else 0.0))

    # Mild synonym expansion (only contributes if query triggered a domain synonym)
    for syn in expanded_tokens:
        hit_h = syn in high_blob
        hit_m = syn in med_blob
        if hit_h or hit_m:
            w = _idf(syn)
            score += 0.55 * w * ((2.4 if hit_h else 0.0) + (1.2 if hit_m else 0.0))

    phrase_bonus = chinese_phrase_score(item, full_query)
    score += float(phrase_bonus)

    symptoms = item.get("when_stuck")
    labels = [*item.get("tags", []), *item.get("tags_en", [])]
    if isinstance(symptoms, dict):
        labels.extend([*symptoms.get("en", []), *symptoms.get("zh", [])])
    if full_query and full_query in {_field_text(label).strip() for label in labels}:
        score += 35.0

    if len(terms) > 1 and full_query:
        if full_query in high_blob:
            score += 20.0
        elif full_query in med_blob:
            score += 10.0
        elif full_query in low_blob:
            score += 4.0

    # Suppress stray single-low-weight noise hits on long irrelevant CJK queries
    if phrase_bonus == 0 and matched_primary == 0 and not expanded_tokens:
        if len(unique_tokens) >= 4 and matched_tokens <= 1 and score < 4.5:
            return 0.0

    return round(score, 2)


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


def discover_local_anchors(root: Path, style_id: str) -> tuple[Path, list[str]]:
    local_dir = (root / "style-refs" / style_id / "local").resolve()
    if not local_dir.is_dir():
        return local_dir, []
    images = sorted(
        str(path.resolve())
        for path in local_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    )
    return local_dir, images


def discover_style_descriptor(root: Path, style_id: str) -> str | None:
    ref_dir = (root / "style-refs" / style_id).resolve()
    if not ref_dir.is_dir():
        return None
    for name in DESCRIPTOR_NAMES:
        candidate = ref_dir / name
        if candidate.is_file():
            return str(candidate)
    return None


def _style_anchor_tier(anchors: list[str], descriptor: str | None) -> str:
    if len(anchors) >= 2:
        return "full_local_anchors"
    if len(anchors) == 1:
        return "partial_local_anchors"
    if descriptor:
        return "descriptor_only"
    return "text_only"


def _extract_bullet_value(text: str, label: str) -> str:
    match = re.search(rf"^- \*\*{re.escape(label)}\*\*[：:]\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip().strip("`") if match else ""


def load_styles(root: Path) -> list[dict[str, Any]]:
    styles_dir = root / "styles"
    if not styles_dir.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(styles_dir.glob("*.md")):
        if path.name in {"README.md", "_TEMPLATE.md"}:
            continue
        style_id = path.stem
        content = path.read_text(encoding="utf-8")
        heading = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = heading.group(1).strip() if heading else style_id
        quadrant = _extract_bullet_value(content, "视觉气质象限")
        industry_raw = _extract_bullet_value(content, "可选行业标签")
        tags = [t.strip() for t in re.split(r"[/、,，]", industry_raw) if t.strip()]
        if quadrant:
            tags.insert(0, quadrant)
        evidence_stage = _extract_bullet_value(content, "证据状态") or "source_verified"
        local_dir, anchors = discover_local_anchors(root, style_id)
        descriptor = discover_style_descriptor(root, style_id)
        records.append({
            "id": style_id,
            "title": title,
            "title_en": quadrant or title,
            "quadrant": quadrant,
            "tags": tags,
            "tags_en": [style_id, quadrant] if quadrant else [style_id],
            "status": evidence_stage,
            "evidence_stage": evidence_stage,
            "style_path": f"styles/{path.name}",
            "style_resolved_path": str(path.resolve()),
            "local_refs_dir": str(local_dir),
            "local_anchor_images": anchors,
            "has_local_anchors": bool(anchors),
            "descriptor_image": descriptor,
            "has_descriptor": bool(descriptor),
            "anchor_tier": _style_anchor_tier(anchors, descriptor),
            "observations": content[:1200],
            "rule": _extract_bullet_value(content, "光源设定") or title,
        })
    return records


def cmd_summary(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, catalog_path = load_catalog(root)
    styles = load_styles(root)
    sources_by_id = {s.get("id"): s for s in data.get("sources", []) if isinstance(s, dict) and s.get("id")}
    by_origin: dict[str, dict[str, int]] = {}
    for group in GROUPS:
        group_counts: dict[str, int] = {}
        for item in data.get(group, []):
            origin = infer_learning_origin(item, group, sources_by_id)
            group_counts[origin] = group_counts.get(origin, 0) + 1
        by_origin[group] = group_counts
    counts = {group: len(data.get(group, [])) for group in GROUPS}
    counts["styles"] = len(styles)
    summary = {
        "library_root": str(root),
        "catalog_path": str(catalog_path),
        "schema_version": data.get("schema_version"),
        "revision": data.get("revision"),
        "updated_at": data.get("updated_at"),
        "bilingual_support": True,
        "counts": counts,
        "styles_with_local_anchors": sum(1 for style in styles if style["has_local_anchors"]),
        "styles_with_descriptors": sum(1 for style in styles if style["has_descriptor"]),
        "styles_missing_local_anchors": [style["id"] for style in styles if not style["has_local_anchors"]],
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
    prepared_query = _prepare_query(full_query)
    terms = prepared_query[0]
    search_styles = args.kind in {"all", "styles"}
    groups = [] if args.kind == "styles" else ([args.kind] if args.kind != "all" else list(GROUPS))
    styles = load_styles(root) if search_styles else []
    idf_corpus: list[dict[str, Any]] = [
        item for g in GROUPS for item in data.get(g, []) if isinstance(item, dict)
    ] + styles
    idf_map = _build_idf(idf_corpus)
    min_score = getattr(args, "min_score", 0.0) or 0.0
    brief = bool(getattr(args, "brief", False))
    verbose = bool(getattr(args, "verbose", False))
    evidence_stage_filter = getattr(args, "evidence_stage", None)
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
            profile = build_evidence_profile(item, group, sources_by_id, feedback_by_id)
            ev_stage = infer_evidence_stage(profile)
            if evidence_stage_filter and ev_stage != evidence_stage_filter:
                continue
            score = score_item(item, terms, full_query, idf_map=idf_map, prepared_query=prepared_query)
            if score > 0 and score >= min_score:
                summary_zh = item.get("rule") or item.get("reusable_move") or item.get("observation") or item.get("coverage_note")
                if brief:
                    when_stuck = item.get("when_stuck")
                    when_zh = when_stuck.get("zh", []) if isinstance(when_stuck, dict) else when_stuck
                    when_short = when_zh[:2] if isinstance(when_zh, list) else when_zh
                    short_summary = summary_zh[:180] + ("…" if isinstance(summary_zh, str) and len(summary_zh) > 180 else "") if isinstance(summary_zh, str) else summary_zh
                    entry: dict[str, Any] = {
                        "group": group,
                        "id": item.get("id"),
                        "score": score,
                        "evidence_stage": ev_stage,
                        "title": item.get("title"),
                        "when_stuck": when_short,
                        "summary": short_summary,
                    }
                    if group == "methods":
                        lim = item.get("limits")
                        entry["limits"] = lim[:140] + ("…" if isinstance(lim, str) and len(lim) > 140 else "") if isinstance(lim, str) else lim
                    elif group == "cases":
                        entry["method_refs"] = item.get("method_refs", [])
                        entry["markdown_path"] = item.get("markdown_path")
                else:
                    entry = {
                        "group": group,
                        "id": item.get("id"),
                        "version": item.get("version"),
                        "learning_origin": origin,
                        "evidence_stage": ev_stage,
                        "evidence_type": infer_evidence_type(item, group, origin, feedback_by_id),
                        "evidence_profile": profile,
                        "title": item.get("title"),
                        "status": item.get("status", item.get("reading_status")),
                        "score": score,
                        "when_stuck": item.get("when_stuck"),
                        "summary": summary_zh,
                    }
                    if group == "methods":
                        entry["applies_when"] = item.get("applies_when")
                        entry["limits"] = item.get("limits")
                    if group == "cases":
                        entry["method_refs"] = item.get("method_refs", [])
                        entry["markdown_path"] = item.get("markdown_path")
                        entry["markdown_path_en"] = item.get("markdown_path_en")
                    if verbose:
                        entry["title_en"] = item.get("title_en")
                        entry["tags"] = item.get("tags", [])
                        entry["tags_en"] = item.get("tags_en", [])
                        entry["summary_en"] = item.get("rule_en") or item.get("reusable_move_en") or item.get("observation_en") or item.get("coverage_note_en")
                        if group == "cases":
                            entry["copy_visual_synergy"] = item.get("copy_visual_synergy")
                            entry["asset_prerequisites"] = item.get("asset_prerequisites")
                            entry["transfer_limits"] = item.get("transfer_limits")
                matches.append(entry)

    if search_styles and not args.channel and not getattr(args, "origin", None) and not args.status:
        for style in styles:
            if evidence_stage_filter and style.get("evidence_stage") != evidence_stage_filter:
                continue
            score = score_item(style, terms, full_query, idf_map=idf_map, prepared_query=prepared_query)
            if score > 0 and score >= min_score:
                style_entry: dict[str, Any] = {
                    "group": "styles",
                    "id": style["id"],
                    "title": style["title"],
                    "quadrant": style["quadrant"],
                    "evidence_stage": style["evidence_stage"],
                    "score": score,
                    "summary": style["rule"],
                    "style_path": style["style_path"],
                    "has_local_anchors": style["has_local_anchors"],
                    "has_descriptor": style["has_descriptor"],
                    "anchor_tier": style["anchor_tier"],
                }
                if not brief:
                    style_entry.update({
                        "status": style["status"],
                        "style_resolved_path": style["style_resolved_path"],
                        "local_refs_dir": style["local_refs_dir"],
                        "local_anchor_images": style["local_anchor_images"],
                        "descriptor_image": style["descriptor_image"],
                    })
                if verbose:
                    style_entry["title_en"] = style["title_en"]
                    style_entry["tags"] = style["tags"]
                    style_entry["tags_en"] = style["tags_en"]
                matches.append(style_entry)

    matches.sort(key=lambda row: (-row["score"], row["id"] or ""))
    sliced = matches[: args.limit]
    print(json.dumps(sliced, ensure_ascii=False, indent=2))
    if not sliced:
        print(
            f'No matches for "{args.query}". Fallback: retry with shorter symptom words (e.g. "参数", "尺寸", "层级", "安全区"), add --kind styles, or check references/art-direction.md symptom routing table.',
            file=sys.stderr,
        )
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    root = resolve_library_root(args.library)
    data, _ = load_catalog(root)
    requested_ids: list[str] = args.ids
    found_map: dict[str, dict[str, Any]] = {}
    cases_by_method: dict[str, list[str]] = {}
    for case in data.get("cases", []):
        cid = case.get("id")
        for mid in case.get("method_refs", []) or []:
            cases_by_method.setdefault(mid, []).append(cid)

    for group in GROUPS:
        for item in data.get(group, []):
            item_id = item.get("id")
            if item_id in requested_ids:
                record = {"group": group, "item": copy.deepcopy(item)}
                if group == "methods":
                    record["linked_case_ids"] = cases_by_method.get(item_id, [])
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

    if any(rid not in found_map for rid in requested_ids):
        for style in load_styles(root):
            style_id = style["id"]
            if style_id in requested_ids and style_id not in found_map:
                found_map[style_id] = {
                    "group": "styles",
                    "item": {
                        "id": style["id"],
                        "title": style["title"],
                        "quadrant": style["quadrant"],
                        "tags": style["tags"],
                        "evidence_stage": style["evidence_stage"],
                        "style_path": style["style_path"],
                    },
                    "style_resolved_path": style["style_resolved_path"],
                    "local_refs_dir": style["local_refs_dir"],
                    "has_local_anchors": style["has_local_anchors"],
                    "local_anchor_images": style["local_anchor_images"],
                    "has_descriptor": style["has_descriptor"],
                    "descriptor_image": style["descriptor_image"],
                    "anchor_tier": style["anchor_tier"],
                }

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
    warnings = collect_catalog_warnings(data, root)
    result = {
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
        "warning_count": len(warnings),
        "warnings": warnings,
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


def prune_history(history_dir: Path, keep: int = MAX_HISTORY_REVISIONS) -> None:
    if not history_dir.is_dir():
        return
    pattern = re.compile(r"^(?:catalog|translations)-r(\d+)\.json$")
    revisions: dict[int, list[Path]] = {}
    for path in history_dir.iterdir():
        match = pattern.match(path.name)
        if match:
            revisions.setdefault(int(match.group(1)), []).append(path)
    for rev in sorted(revisions, reverse=True)[keep:]:
        for old_path in revisions[rev]:
            old_path.unlink(missing_ok=True)


def apply_catalog_patch(root: Path, patch: dict[str, Any], check_files: bool = True) -> dict[str, Any]:
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
    prune_history(root / "history")
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


def _next_feedback_id(data: dict[str, Any]) -> str:
    nums = []
    for fb in data.get("feedback", []):
        m = re.fullmatch(r"F-(\d+)", str(fb.get("id", "")))
        if m:
            nums.append(int(m.group(1)))
    return f"F-{(max(nums) if nums else 0) + 1:03d}"


def cmd_feedback(args: argparse.Namespace) -> int:
    if args.feedback_cmd != "add":
        raise ValueError(f"unsupported feedback subcommand: {args.feedback_cmd}")
    root = resolve_library_root(args.library)
    try:
        history = root / "history"
        history.mkdir(exist_ok=True)
        with (history / ".library.lock").open("a+b") as lock:
            lock_writer(lock)
            data, _ = load_catalog(root)
            fb_id = args.id or _next_feedback_id(data)
            entry: dict[str, Any] = {
                "id": fb_id,
                "version": 1,
                "kind": "feedback",
                "learning_origin": "task_feedback",
                "title": args.title,
                "evidence_type": args.evidence_type,
                "source_locator": args.source_locator,
                "observation": args.observation,
                "verified": bool(args.verified),
                "task_id": args.task_id,
                "date": args.date or dt.date.today().isoformat(),
            }
            if args.title_en:
                entry["title_en"] = args.title_en
            if args.observation_en:
                entry["observation_en"] = args.observation_en
            if args.project_status:
                entry["project_status"] = args.project_status
            if args.methods:
                entry["methods_used"] = args.methods
            if args.cases:
                entry["cases_used"] = args.cases
            if args.lesson:
                entry["reusable_lesson"] = args.lesson
            result = apply_catalog_patch(root, {"feedback": [entry]}, check_files=False)
            result["feedback_id"] = fb_id
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

    search = sub.add_parser("search", help="Weighted bilingual & symptom search across methods, cases, sources, feedback, and styles")
    search.add_argument("query", help="Search query (supports bilingual keywords, Chinese colloquial sentences & symptoms)")
    search.add_argument("--kind", choices=["all", *GROUPS, "styles"], default="all")
    search.add_argument("--status", choices=sorted(STATUS_VALUES), help="Filter methods/cases by catalog status (reference, candidate, validated, retired)")
    search.add_argument("--evidence-stage", dest="evidence_stage", choices=sorted(EVIDENCE_STAGES), help="Filter records/styles by evidence stage (source_verified, user_endorsed, field_validated)")
    search.add_argument("--channel", choices=sorted(CHANNEL_VALUES), help="Filter by channel (e.g. pdp, landing_page, ad_banner, spec_sheet)")
    search.add_argument("--origin", choices=sorted(LEARNING_ORIGINS), help="Filter by learning origin (book_canon, benchmark_study, co_dissected_teardown, task_feedback)")
    search.add_argument("--min-score", dest="min_score", type=float, default=0.0, help="Minimum relevance score threshold")
    search.add_argument("--brief", action="store_true", help="Compact output (id, score, title, when_stuck, summary)")
    search.add_argument("--verbose", action="store_true", help="Include full bilingual tags, English summaries, and case metadata")
    search.add_argument("--limit", type=int, default=8)

    get_p = sub.add_parser("get", help="Fetch one or more records or style archetypes by ID in a single batch call")
    get_p.add_argument("ids", nargs="+", help="One or more record or style IDs (e.g. M-001 C-baymard-in-scale-reference apple-dark-pro)")

    val = sub.add_parser("validate", help="Validate catalog schema, references, and bilingual case files")
    val.add_argument("--check-files", action="store_true", help="Verify local source files, bilingual markdown cards, and SHA-256 digests")

    patch = sub.add_parser("apply-patch", help="Atomically merge a JSON patch into catalog.json with backup and validation")
    patch.add_argument("--file", required=True, help="Path to patch JSON file")
    patch.add_argument("--check-files", action="store_true", dest="check_files", default=True, help="Verify referenced files and refresh case digests (default: enabled)")
    patch.add_argument("--skip-file-checks", action="store_false", dest="check_files", help="Skip file existence and case digest checks (use only for metadata-only offline patches)")

    fb_p = sub.add_parser("feedback", help="Record structured project/review feedback into the library")
    fb_sub = fb_p.add_subparsers(dest="feedback_cmd", required=True)
    fb_add = fb_sub.add_parser("add", help="Add a verified or unverified feedback record atomically")
    fb_add.add_argument("--id", help="Optional explicit ID (defaults to next sequential F-###)")
    fb_add.add_argument("--title", required=True, help="Short Chinese or bilingual feedback title")
    fb_add.add_argument("--title-en", dest="title_en", help="Optional English title")
    fb_add.add_argument("--observation", required=True, help="Concrete observation or user decision reason")
    fb_add.add_argument("--observation-en", dest="observation_en", help="Optional English observation")
    fb_add.add_argument("--source-locator", dest="source_locator", required=True, help="Session/project reference where feedback occurred")
    fb_add.add_argument("--task-id", dest="task_id", required=True, help="Task or brief identifier")
    fb_add.add_argument("--evidence-type", dest="evidence_type", choices=sorted(EVIDENCE_TYPES), default="editorial_feedback")
    fb_add.add_argument("--project-status", dest="project_status", choices=sorted(PROJECT_STATUSES))
    fb_add.add_argument("--methods", nargs="*", help="Method IDs used (e.g. M-001 M-019)")
    fb_add.add_argument("--cases", nargs="*", help="Case IDs used")
    fb_add.add_argument("--lesson", help="Reusable lesson extracted from this feedback")
    fb_add.add_argument("--date", help="ISO date YYYY-MM-DD (defaults to today)")
    fb_add.add_argument("--verified", action="store_true", help="Mark feedback as verified")

    args = parser.parse_args()
    commands = {
        "summary": cmd_summary,
        "search": cmd_search,
        "get": cmd_get,
        "validate": cmd_validate,
        "apply-patch": cmd_apply_patch,
        "feedback": cmd_feedback,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
