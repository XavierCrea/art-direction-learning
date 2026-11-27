"""Regressions for evidence, natural search and portable case-library updates."""

import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "library.py"
LIBRARY = runpy.run_path(str(SCRIPT))
CASE_ID = "C-coca-cola-recycle-me-deformation"


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "library"
        shutil.copytree(ROOT / "library", self.root, ignore=shutil.ignore_patterns("history"))
        (self.root / "history").mkdir()
        self.catalog_path = self.root / "catalog.json"
        self.manifest_path = self.root / "translations.en.json"

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--library", str(self.root), *args],
            capture_output=True,
            encoding="utf-8",
        )

    def listing(self, term):
        process = self.cli("search", term)
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads(process.stdout)

    def search(self, term):
        return self.listing(term)[0]

    def new_case_patch(self):
        data = LIBRARY["read_json"](self.catalog_path)
        case = dict(data["cases"][-1], id="C-test-case",
                    markdown_path="cases/C-test-case.md", markdown_path_en="cases/en/C-test-case.md")
        (self.root / case["markdown_path"]).write_bytes(b"# A test case\r\n")
        (self.root / case["markdown_path_en"]).write_bytes(b"# A test case\n")
        return {"cases": [case]}

    def write_patch(self, payload, name="patch.json"):
        path = Path(self.temp.name) / name
        path.write_bytes(LIBRARY["json_bytes"](payload))
        return path

    def test_search_prioritizes_relevant_colloquial_queries(self):
        for term, ids in {
            "看不出这是什么": {"M-002", "C-baymard-descriptive-callouts"},
            "说是电芯，实际根本看不出来是什么": {"M-002", "C-baymard-descriptive-callouts"},
            "画面做完一眼看不出是什么部件": {"M-002", "C-baymard-descriptive-callouts"},
            "图看不清": {"M-002", "C-baymard-descriptive-callouts"},
            "三维尺寸没有参照": {"M-001", "C-baymard-in-scale-reference"},
            "参数太多没人看": {"M-005", "C-baymard-spec-sheet-scannability", "C-refactoring-ui-data-labels-and-tables"},
            "产品看起来很廉价": {"M-007", "M-042", "C-ikea-price-relief-and-empty-product-narrative", "C-refactoring-ui-hierarchy-tactics"},
            "looks cheap": {"M-042", "C-ikea-price-relief-and-empty-product-narrative", "C-muller-brockmann-color-fields-and-posters", "M-007"},
            "像模板": {"M-007", "C-refactoring-ui-hierarchy-tactics"},
            "想让人再看一眼": {"M-036", "C-aotw-fnac-visual-subversion-light-cone"},
            "9:16 safe zones": {"M-033", "C-tiktok-9x16-safe-zones-and-2s-hook"},
        }.items():
            with self.subTest(term=term):
                self.assertIn(self.search(term)["id"], ids)
        for term in ("黑洞和宇宙为什么在膨胀", "晚饭想给猫做点什么好吃的"):
            with self.subTest(term=term):
                proc = self.cli("search", term)
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(json.loads(proc.stdout), [])
                self.assertIn("Fallback:", proc.stderr)

    def test_endorsement_is_distinct_from_adoption_and_audience_results(self):
        for term in ("F-002", "M-028", "C-xiaomi-su7-2026-mall-billboard-teardown"):
            with self.subTest(term=term):
                record = self.search(term)
                evidence = record["evidence_profile"]
                self.assertEqual(record["evidence_stage"], "user_endorsed")
                self.assertEqual(evidence["project_status"], "endorsed")
                self.assertFalse(evidence["project_adopted"])
                self.assertEqual(evidence["audience_result"], "none")
        reported = self.search("C-me-rows-live-product-hero")
        self.assertTrue(reported["evidence_profile"]["audience_result"].startswith("source_reported:"))
        self.assertNotEqual(reported["evidence_stage"], "field_validated")

    def test_rejects_unsupported_explicit_evidence_stage(self):
        doc = LIBRARY["read_json"](self.catalog_path)
        case = next(item for item in doc["cases"] if item["id"] == CASE_ID)
        case["evidence_stage"] = "field_validated"
        case["outcome_evidence"] = {
            "evidence_type": "ab_test_result", "claim": "Test only", "verification_status": "unverified"
        }
        self.catalog_path.write_bytes(LIBRARY["json_bytes"](doc))
        found = self.search(CASE_ID)
        self.assertNotEqual(found["evidence_stage"], "field_validated")
        self.assertEqual(found["evidence_profile"]["audience_result"], "unverified:ab_test_result")
        checked = self.cli("validate", "--check-files")
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("lacks supporting evidence", checked.stdout)

    def test_verified_audience_result_without_adoption(self):
        doc = LIBRARY["read_json"](self.catalog_path)
        doc["feedback"].append({
            "id": "F-test-outcome", "version": 1, "title": "Audience test",
            "kind": "feedback", "evidence_type": "ab_test_result", "source_locator": "Test report, page 1",
            "observation": "No difference was detected in the paired comparison.",
            "verified": True, "task_id": "test",
        })
        self.catalog_path.write_bytes(LIBRARY["json_bytes"](doc))
        found = self.search("F-test-outcome")["evidence_profile"]
        self.assertEqual(found["audience_result"], "verified:ab_test_result")
        self.assertEqual(found["project_status"], "none")
        self.assertIn("No difference", found["audience_evidence"][0]["claim"])

    def test_active_library_is_used_and_newlines_are_portable(self):
        doc = LIBRARY["read_json"](self.catalog_path)
        record = next(row for row in doc["cases"] if row["id"] == CASE_ID)
        record["markdown_path"] = record["markdown_path"].replace("/", "\\")
        self.catalog_path.write_bytes(LIBRARY["json_bytes"](doc))

        got = json.loads(self.cli("get", CASE_ID).stdout)
        card = Path(got["markdown_resolved_path"])
        self.assertTrue(card.is_relative_to(self.root))
        original = LIBRARY["normalized_case_bytes"](card.read_bytes())
        card.write_bytes(b"\xef\xbb\xbf" + original.replace(b"\n", b"\r\n"))
        self.assertEqual(self.cli("validate", "--check-files").returncode, 0)

        card.write_bytes(original + b"\nChanged content.\n")
        checked = self.cli("validate", "--check-files")
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("zh_sha256 mismatch", checked.stdout)

        card.unlink()
        checked = self.cli("validate", "--check-files")
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn("missing markdown_path file", checked.stdout)

    def test_windows_legacy_manifest_is_readable_after_lf_checkout(self):
        card = self.root / "cases" / f"{CASE_ID}.md"
        content = LIBRARY["normalized_case_bytes"](card.read_bytes())
        windows_content = content.replace(b"\n", b"\r\n")
        manifest = LIBRARY["read_json"](self.manifest_path)
        entry = manifest["cases"][card.stem]
        manifest.pop("hash_mode", None)
        entry.pop("hash_mode", None)
        entry["zh_sha256"] = hashlib.sha256(windows_content).hexdigest()
        self.manifest_path.write_bytes(LIBRARY["json_bytes"](manifest))
        card.write_bytes(content)
        self.assertEqual(self.cli("validate", "--check-files").returncode, 0)

    def test_new_case_generates_fingerprints_and_preserves_unmodified_backup(self):
        prior = self.catalog_path.read_bytes()
        delta = self.write_patch(self.new_case_patch())
        result = self.cli("apply-patch", "--file", str(delta), "--check-files")
        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(Path(payload["backup_path"]).read_bytes(), prior)
        entry = LIBRARY["read_json"](self.manifest_path)["cases"]["C-test-case"]
        self.assertEqual(entry["zh_sha256"], entry["en_sha256"])
        self.assertEqual(self.cli("validate", "--check-files").returncode, 0)

    def test_catalog_replace_failure_keeps_previous_catalog_and_manifest(self):
        old_catalog, old_manifest = self.catalog_path.read_bytes(), self.manifest_path.read_bytes()
        replacement = os.replace

        def fail_catalog_replace(source, target):
            if target == self.catalog_path:
                raise OSError("simulated failure before catalog replace")
            replacement(source, target)

        with patch.object(os, "replace", side_effect=fail_catalog_replace):
            with self.assertRaises(OSError):
                LIBRARY["apply_catalog_patch"](self.root, self.new_case_patch(), True)
        self.assertEqual(self.catalog_path.read_bytes(), old_catalog)
        self.assertEqual(self.manifest_path.read_bytes(), old_manifest)
        self.assertEqual(self.cli("validate", "--check-files").returncode, 0)

    def test_interrupted_manifest_is_recovered_on_next_patch(self):
        data = LIBRARY["read_json"](self.catalog_path)
        revision = data["revision"]
        prior = LIBRARY["read_json"](self.manifest_path)
        (self.root / "history" / f"translations-r{revision}.json").write_bytes(LIBRARY["json_bytes"](prior))
        interrupted = dict(prior, catalog_revision=revision + 1, cases={})
        self.manifest_path.write_bytes(LIBRARY["json_bytes"](interrupted))

        self.assertEqual(self.cli("validate", "--check-files").returncode, 0)
        delta = self.write_patch({"methods": [{"id": "M-001", "applies_when": "Test retry"}]})
        patched = self.cli("apply-patch", "--check-files", "--file", str(delta))
        self.assertEqual(patched.returncode, 0, patched.stdout)
        self.assertEqual(LIBRARY["read_json"](self.manifest_path), prior)

    def test_simultaneous_writers_do_not_lose_updates(self):
        old_revision = LIBRARY["read_json"](self.catalog_path)["revision"]
        args = [sys.executable, "-B", str(SCRIPT), "--library", str(self.root), "apply-patch", "--check-files"]
        todo = {"M-001": "Test first writer", "M-002": "Test second writer"}
        processes = []
        for index, (record_id, value) in enumerate(todo.items()):
            delta = self.write_patch({"methods": [{"id": record_id, "applies_when": value}]}, f"patch-{index}.json")
            processes.append(subprocess.Popen([*args, "--file", str(delta)], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, (stdout, stderr))
        doc = LIBRARY["read_json"](self.catalog_path)
        self.assertEqual(doc["revision"], old_revision + 2)
        by_id = {m["id"]: m for m in doc["methods"]}
        for record_id, value in todo.items():
            self.assertEqual(by_id[record_id]["applies_when"], value)

    def test_english_case_index_paths_resolve(self):
        for card in (self.root / "cases" / "en").glob("*.md"):
            index = (card.parent / "../../README.en.md").resolve()
            self.assertIn("](../../README.en.md)", card.read_text(encoding="utf-8"))
            self.assertTrue(index.is_file())

    def test_channel_filter_includes_cases_and_rejects_invalid_channel(self):
        hits = self.listing("9:16 safe zones")
        self.assertTrue(any(item["group"] == "cases" for item in hits))
        filtered = json.loads(self.cli("search", "9:16 safe zones", "--channel", "ad_banner").stdout)
        ids = {item["id"] for item in filtered}
        self.assertIn("M-033", ids)
        self.assertIn("C-tiktok-9x16-safe-zones-and-2s-hook", ids)
        bad = self.cli("search", "safe zones", "--channel", "nonexistent_channel")
        self.assertNotEqual(bad.returncode, 0)

    def test_apply_patch_defaults_to_check_files_rejects_unknown_fields_and_prunes_history(self):
        bad_patch = self.write_patch({"methods": [{"id": "M-001", "apply_when": "typo field"}]})
        rejected = self.cli("apply-patch", "--file", str(bad_patch))
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("unknown fields", rejected.stdout)

        for idx in range(7):
            delta = self.write_patch({"methods": [{"id": "M-001", "applies_when": f"Iteration {idx}"}]})
            ok = self.cli("apply-patch", "--file", str(delta))
            self.assertEqual(ok.returncode, 0, ok.stdout)
        backups = list((self.root / "history").glob("catalog-r*.json"))
        self.assertLessEqual(len(backups), LIBRARY["MAX_HISTORY_REVISIONS"])

    def test_style_search_get_and_local_anchor_detection(self):
        local_dir = self.root / "style-refs" / "apple-dark-pro" / "local"
        if local_dir.is_dir():
            for img in local_dir.iterdir():
                if img.name != ".gitkeep":
                    img.unlink()

        empty_get = json.loads(self.cli("get", "apple-dark-pro").stdout)
        self.assertEqual(empty_get["group"], "styles")
        self.assertFalse(empty_get["has_local_anchors"])
        self.assertEqual(empty_get["local_anchor_images"], [])

        val = json.loads(self.cli("validate", "--check-files").stdout)
        self.assertTrue(val["valid"])
        self.assertTrue(any("apple-dark-pro" in w and "0 local anchor images" in w for w in val["warnings"]))

        anchor = local_dir / "01-test-anchor.jpg"
        anchor.parent.mkdir(parents=True, exist_ok=True)
        anchor.write_bytes(b"fake-jpg")

        populated_get = json.loads(self.cli("get", "apple-dark-pro").stdout)
        self.assertTrue(populated_get["has_local_anchors"])
        self.assertEqual(populated_get["local_anchor_images"], [str(anchor.resolve())])
        self.assertEqual(populated_get["anchor_tier"], "partial_local_anchors")

        found = json.loads(self.cli("search", "apple dark pro", "--kind", "styles").stdout)
        self.assertEqual(found[0]["id"], "apple-dark-pro")
        self.assertTrue(found[0]["has_local_anchors"])

    def test_status_and_evidence_stage_filters_and_brief_output(self):
        brief_out = self.cli("search", "参数", "--kind", "methods", "--brief").stdout
        verbose_out = self.cli("search", "参数", "--kind", "methods", "--verbose").stdout
        self.assertLess(len(brief_out), len(verbose_out))
        self.assertNotIn("evidence_profile", json.loads(brief_out)[0])

        by_stage = json.loads(self.cli("search", "小米", "--evidence-stage", "user_endorsed").stdout)
        self.assertTrue(any(row["id"] == "M-028" for row in by_stage))
        bad_status = self.cli("search", "小米", "--status", "user_endorsed")
        self.assertNotEqual(bad_status.returncode, 0)

    def test_method_refs_validation_linkage_and_feedback_add(self):
        got_m1 = json.loads(self.cli("get", "M-001").stdout)
        self.assertIn("C-baymard-in-scale-reference", got_m1["linked_case_ids"])

        bad_patch = self.write_patch({"cases": [{"id": CASE_ID, "method_refs": ["M-999"]}]})
        rejected = self.cli("apply-patch", "--file", str(bad_patch))
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("method_ref 'M-999' not found", rejected.stdout)

        fb = self.cli(
            "feedback", "add",
            "--title", "测试反馈",
            "--observation", "结构化反馈写入验证",
            "--source-locator", "unit-test",
            "--task-id", "ut-feedback",
            "--project-status", "endorsed",
            "--methods", "M-001",
            "--verified",
        )
        self.assertEqual(fb.returncode, 0, fb.stdout)
        fb_payload = json.loads(fb.stdout)
        self.assertTrue(fb_payload["applied"])
        self.assertTrue(fb_payload["feedback_id"].startswith("F-"))

    def test_qa_check_dimensions_overlay_and_qr_behavior(self):
        qa_script = ROOT / "scripts" / "qa_check.py"
        # Minimal valid 1080x1920 PNG header (IHDR chunk)
        import struct
        import zlib

        def make_png(w: int, h: int) -> bytes:
            sig = b"\x89PNG\r\n\x1a\n"
            ihdr_data = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
            ihdr = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF)
            iend = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", zlib.crc32(b"IEND") & 0xFFFFFFFF)
            return sig + ihdr + iend

        img_path = Path(self.temp.name) / "sample_9x16.png"
        img_path.write_bytes(make_png(1080, 1920))
        overlay_path = Path(self.temp.name) / "overlay.svg"
        proc = subprocess.run(
            [
                sys.executable, "-B", str(qa_script), str(img_path),
                "--expected-ratio", "9:16",
                "--min-width", "1080",
                "--safe-zone-overlay", str(overlay_path),
            ],
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["overall_status"], "pass")
        self.assertEqual(report["checks"]["dimensions"]["width"], 1080)
        self.assertTrue(overlay_path.is_file())
        self.assertIn("SAFE AREA:", overlay_path.read_text(encoding="utf-8"))

        bad_ratio = subprocess.run(
            [sys.executable, "-B", str(qa_script), str(img_path), "--expected-ratio", "16:9"],
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(bad_ratio.returncode, 1)
        self.assertEqual(json.loads(bad_ratio.stdout)["overall_status"], "fail")


if __name__ == "__main__":
    unittest.main()
