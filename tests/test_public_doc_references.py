from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.structure_factory.public_doc_reference_check import check, sync_skill_references
from scripts.structure_factory.runpod_public_template_check import check_manifest


ROOT = Path(__file__).resolve().parents[1]


class PublicDocReferenceTests(unittest.TestCase):
    def test_public_doc_references_are_current(self) -> None:
        result = check(ROOT)
        self.assertTrue(result["ok"], result)

    def test_doc_reference_check_flags_missing_make_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n", encoding="utf-8")
            (root / "README.md").write_text("Run `make missing-target`.\n", encoding="utf-8")
            result = check(root)
            self.assertFalse(result["ok"])
            self.assertTrue(any(item["check_id"] == "missing-make-target" for item in result["findings"]))

    def test_doc_reference_check_flags_private_package_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                'Homepage = "https://github.com/BioSymphony/biosymphony-structure-factory"\n',
                encoding="utf-8",
            )
            result = check(root)
            self.assertFalse(result["ok"])
            self.assertTrue(any(item["check_id"] == "private-package-url" for item in result["findings"]))

    def test_doc_reference_check_flags_private_repo_urls_in_public_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n", encoding="utf-8")
            (root / "schemas").mkdir()
            (root / "schemas" / "campaign-manifest.schema.json").write_text(
                '{"$id": "https://github.com/BioSymphony/biosymphony-structure-factory/schemas/campaign-manifest.schema.json"}\n',
                encoding="utf-8",
            )
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            (root / ".github" / "ISSUE_TEMPLATE" / "config.yml").write_text(
                "url: https://github.com/BioSymphony/biosymphony-structure-factory/discussions\n",
                encoding="utf-8",
            )
            result = check(root)
            self.assertFalse(result["ok"])
            private_url_findings = [item for item in result["findings"] if item["check_id"] == "private-repo-url"]
            self.assertEqual(len(private_url_findings), 2, result)

    def test_doc_reference_check_flags_stale_skill_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("canonical\n", encoding="utf-8")
            bundled = root / "skills" / "biosymphony-structure-factory" / "references" / "docs"
            bundled.mkdir(parents=True)
            (bundled / "guide.md").write_text("stale\n", encoding="utf-8")
            result = check(root)
            self.assertFalse(result["ok"])
            self.assertTrue(
                any(item["check_id"] == "stale-skill-reference-copy" for item in result["findings"]),
                result,
            )

    def test_doc_reference_check_flags_missing_bundled_skill_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n", encoding="utf-8")
            skill = root / "skills" / "binder-lane-round" / "references" / "docs"
            skill.mkdir(parents=True)
            (skill / "guide.md").write_text("See [missing](missing.md).\n", encoding="utf-8")
            result = check(root)
            self.assertFalse(result["ok"])
            self.assertTrue(
                any(item["check_id"] == "missing-bundled-skill-link" for item in result["findings"]),
                result,
            )

    def test_portable_sync_keeps_local_references_and_links_omitted_targets_publicly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n")
            (root / "docs").mkdir()
            (root / "tools").mkdir()
            (root / "tools" / "method.md").write_text("# Method\n")
            (root / "docs" / "included.md").write_text("# Included\n")
            (root / "docs" / "plot.svg").write_text("<svg/>\n")
            (root / "docs" / "guide.md").write_text(
                "Read [included](included.md#included), [method](../tools/method.md#method), "
                "and [tools](../tools/).\n![plot](plot.svg)\n<img src=\"plot.svg\">\n"
            )
            bundled = root / "skills" / "biosymphony-structure-factory" / "references" / "docs"
            bundled.mkdir(parents=True)
            for name in ("guide.md", "included.md"):
                (bundled / name).write_text("stale\n")
            sync_skill_references(root)
            rendered = (bundled / "guide.md").read_text()
            self.assertIn("[included](included.md#included)", rendered)
            self.assertIn("https://github.com/BioSymphony/structure-factory/blob/main/tools/method.md#method", rendered)
            self.assertIn("https://github.com/BioSymphony/structure-factory/tree/main/tools", rendered)
            self.assertEqual(rendered.count("https://raw.githubusercontent.com/BioSymphony/structure-factory/main/docs/plot.svg"), 2)
            self.assertFalse((bundled.parent / "tools").exists())
            self.assertTrue(check(root)["ok"], check(root))
            sync_skill_references(root)
            self.assertEqual((bundled / "guide.md").read_text(), rendered)
            (root / "docs" / "guide.md").write_text("Updated canonical prose.\n")
            self.assertTrue(any(item["check_id"] == "stale-skill-reference-copy" for item in check(root)["findings"]))

    def test_main_portable_skill_reports_unresolvable_local_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n")
            bundled = root / "skills" / "biosymphony-structure-factory" / "references" / "docs"
            bundled.mkdir(parents=True)
            (bundled / "guide.md").write_text("See [missing](missing.md).\n")
            self.assertTrue(any(item["check_id"] == "missing-bundled-skill-link" for item in check(root)["findings"]))

    def test_other_skill_mirrors_stay_byte_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text("release-check:\n\ttrue\n")
            (root / "docs").mkdir()
            canonical = root / "docs" / "guide.md"
            canonical.write_text("Read [guide](guide.md).\n")
            bundled = root / "skills" / "binder-lane-round" / "references" / "docs"
            bundled.mkdir(parents=True)
            (bundled / "guide.md").write_text("stale\n")
            sync_skill_references(root)
            self.assertEqual((bundled / "guide.md").read_bytes(), canonical.read_bytes())
            self.assertTrue(check(root)["ok"], check(root))

    def test_portable_html_images_require_existing_contained_targets(self) -> None:
        for skill_name in ("biosymphony-structure-factory", "binder-lane-round"):
            with self.subTest(skill=skill_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "Makefile").write_text("release-check:\n\ttrue\n")
                (root / "outside.svg").write_text("<svg/>\n")
                bundled = root / "skills" / skill_name / "references" / "docs"
                bundled.mkdir(parents=True)
                (bundled / "included.svg").write_text("<svg/>\n")
                (bundled / "guide.md").write_text(
                    "<img src='missing.svg'>\n"
                    '<img src="../../../../outside.svg">\n'
                    "<img src='included.svg'>\n"
                )
                findings = check(root)["findings"]
                self.assertEqual(
                    {(item["check_id"], item["message"]) for item in findings},
                    {
                        ("missing-bundled-skill-link", "missing.svg"),
                        ("escaping-bundled-skill-link", "../../../../outside.svg"),
                    },
                )

    def test_runpod_public_template_check_rejects_launchable_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "demo.json"
            path.write_text(
                """{
  "remote_launch_allowed": true,
  "public_template_status": "ready",
  "launch_authorization": {"approved_at": "2026-01-01", "approved_by": "operator"},
  "runpod": {"dataCenterIds": ["US-XX-1"], "networkVolumeId": "abc123"},
  "startup": {"commands": ["echo run"]}
}
""",
                encoding="utf-8",
            )
            findings = check_manifest(path)
            self.assertTrue(findings)


if __name__ == "__main__":
    unittest.main()
