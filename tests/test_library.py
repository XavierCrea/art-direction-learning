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
            "像模板": {"M-007", "C-refactoring-ui-hierarchy-tactics"},
            "想让人再看一眼": {"M-036", "C-aotw-fnac-visual-subversion-light-cone"},
            "9:16 safe zones": {"M-033", "C-tiktok-9x16-safe-zones-and-2s-hook"},
        }.items():
            with self.subTest(term=term):
                self.assertIn(self.search(term)["id"], ids)
        for term in ("黑洞和宇宙为什么在膨胀", "晚饭想给猫做点什么好吃的"):
            with self.subTest(term=term):
                self.assertEqual(self.listing(term), [])

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


if __name__ == "__main__":
    unittest.main()
