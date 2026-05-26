from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from biosymphony_structure_factory.cli import (
    audit_tree,
    capability_catalog,
    catalog_markdown,
    harness_check,
    issue_plan_for_campaign,
    issue_dry_run,
    main,
    scaffold_campaign,
    validate_campaign,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "pd-l1-binder-design-public"


class PublicCliTests(unittest.TestCase):
    def test_validate_public_example(self) -> None:
        ok, findings = validate_campaign(EXAMPLE)
        self.assertTrue(ok, [finding.to_dict() for finding in findings])

    def test_issue_dry_run_writes_tracker_neutral_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = issue_dry_run(EXAMPLE, Path(tmp))
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["issue_count"], 4)
            first = Path(result["issues"][0]).read_text(encoding="utf-8")
            self.assertIn("routing label: `sym:structure-factory`", first)
            self.assertIn("computational_candidate", first)

    def test_issue_dry_run_uses_campaign_mode(self) -> None:
        expected = {
            "binder-design": "BSF-BINDER-W00",
            "model-jury": "BSF-JURY-W00",
            "structure-dossier": "BSF-DOSSIER-W00",
            "screening": "BSF-SCREEN-W00",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for mode, prefix in expected.items():
                campaign_dir = root / mode
                result = scaffold_campaign(
                    campaign_dir,
                    campaign_id=f"{mode}-demo",
                    target_label="A2A receptor",
                    public_accession="PDB:5G53",
                    window="TM6 activation microswitch",
                    mode=mode,
                )
                self.assertTrue(result["ok"], result)
                issue_result = issue_dry_run(campaign_dir, root / f"{mode}-issues")
                self.assertTrue(issue_result["ok"], issue_result)
                first_issue = Path(issue_result["issues"][0])
                self.assertTrue(first_issue.name.startswith(prefix), first_issue.name)
                self.assertIn(f"issue_id: {prefix}", first_issue.read_text(encoding="utf-8"))

    def test_issue_plan_rejects_unknown_campaign_mode(self) -> None:
        with self.assertRaises(ValueError):
            issue_plan_for_campaign({"mode": "unsupported-mode"})

    def test_scaffold_campaign_writes_valid_public_campaign(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaign_dir = Path(tmp) / "a2a-receptor-demo"
            result = scaffold_campaign(
                campaign_dir,
                campaign_id="a2a-receptor-demo",
                target_label="A2A receptor",
                public_accession="PDB:5G53",
                window="TM6 activation microswitch",
            )
            self.assertTrue(result["ok"], result)
            self.assertTrue((campaign_dir / "campaign-manifest.json").exists())
            ok, findings = validate_campaign(campaign_dir)
            self.assertTrue(ok, [finding.to_dict() for finding in findings])
            audit_ok, audit_findings = audit_tree(campaign_dir)
            self.assertTrue(audit_ok, [finding.to_dict() for finding in audit_findings])

    def test_scaffold_campaign_cli_rejects_private_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            private_path = "/" + "Users/example/private"
            code = main(
                [
                    "scaffold-campaign",
                    str(Path(tmp) / "bad-demo"),
                    "--campaign-id",
                    "bad-demo",
                    "--target-label",
                    private_path,
                    "--public-accession",
                    "PDB:1ABC",
                    "--window",
                    "demo window",
                ]
            )
            self.assertEqual(code, 2)

    def test_audit_flags_private_path_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "/" + "Users/example/private"
            (root / "README.md").write_text(f"local path {private_path}\n", encoding="utf-8")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "private-workstation-path" for finding in findings))

    def test_audit_flags_private_tracker_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tracker = "VOG" + "-PDL1"
            url = "https://linear." + "app/team/issue/" + tracker + "/demo"
            (root / "README.md").write_text(f"tracker {tracker} and {url}\n", encoding="utf-8")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "private-tracker-id" for finding in findings))
            self.assertTrue(any(finding.check_id == "private-linear-url" for finding in findings))

    def test_audit_flags_private_root_markers_without_blocking_public_policy_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "public-policy.md").write_text(
                "\n".join(
                    [
                        "STRUCTURE_FACTORY_RUNPOD_NETWORK_VOLUME_ID is a placeholder.",
                        "allow_private_data: false",
                        "requires_network_volume: true",
                        "private_registry_auth: operator-gated",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            ok, findings = audit_tree(root)
            self.assertTrue(ok, [finding.to_dict() for finding in findings])

            private_root = "github" + "_2"
            private_env = "SSK" + "_Symphony"
            (root / "private-root.md").write_text(
                f"local checkout {private_root} and {private_env}\n",
                encoding="utf-8",
            )
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "local-user-or-private-root" for finding in findings))

    def test_audit_rejects_launch_payload_in_public_bridge_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "runpod" / "bridge-manifests" / "demo.json"
            path.parent.mkdir(parents=True)
            path.write_text('{"startup": {"commands": ["base64 -d | gunzip"]}}\n', encoding="utf-8")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "launch-payload-or-approval" for finding in findings))

    def test_audit_rejects_local_jury_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "juries" / "candidate_jury.demo.local.json"
            path.parent.mkdir()
            path.write_text('{"ok": true}\n', encoding="utf-8")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "local-artifact-file" for finding in findings))

    def test_audit_rejects_generated_book_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "report" / "_book" / "index.html"
            path.parent.mkdir(parents=True)
            path.write_text("<html></html>\n", encoding="utf-8")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "forbidden-name" for finding in findings))

    def test_audit_rejects_generated_candidate_sequence_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sequence = "ACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWY"
            (root / "candidate_jury.public.json").write_text(
                json.dumps({"binder_sequence": sequence}),
                encoding="utf-8",
            )
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "generated-candidate-sequence" for finding in findings))

    def test_audit_rejects_generated_media_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "visuals" / "candidate.gif"
            path.parent.mkdir()
            path.write_bytes(b"GIF89a")
            ok, findings = audit_tree(root)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "forbidden-generated-artifact" for finding in findings))

    def test_candidate_jury_is_small_json(self) -> None:
        data = json.loads((EXAMPLE / "candidate-jury.example.json").read_text(encoding="utf-8"))
        self.assertLessEqual(len(data["candidates"]), 32)
        self.assertEqual(data["claim_ceiling"], "computational_candidate")

    def test_validate_rejects_public_candidate_claim_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaign_dir = Path(tmp) / "claim-escalation"
            result = scaffold_campaign(
                campaign_dir,
                campaign_id="claim-escalation",
                target_label="A2A receptor",
                public_accession="PDB:5G53",
                window="TM6 activation microswitch",
            )
            self.assertTrue(result["ok"], result)
            manifest_path = campaign_dir / "campaign-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["claim_level"] = "candidate"
            manifest["lanes"][0]["claim_ceiling"] = "therapeutic_claim"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            ok, findings = validate_campaign(campaign_dir)
            self.assertFalse(ok)
            self.assertTrue(any(finding.check_id == "claim-level" for finding in findings))
            self.assertTrue(any(finding.check_id == "lane-claim-ceiling" for finding in findings))

    def test_public_harness_surface_is_present(self) -> None:
        ok, findings = harness_check(ROOT)
        self.assertTrue(ok, [finding.to_dict() for finding in findings])

    def test_capability_catalog_exposes_repo_entry_points(self) -> None:
        catalog = capability_catalog(ROOT)
        self.assertTrue(catalog["ok"], catalog)
        self.assertGreaterEqual(catalog["counts"]["campaign_modules"], 1)
        self.assertGreaterEqual(catalog["counts"]["example_campaigns"], 2)
        self.assertTrue(
            any(item["campaign_id"] == "screening-superpowers" for item in catalog["campaign_modules"]),
            catalog["campaign_modules"],
        )
        self.assertTrue(
            any(item["campaign_id"] == "pd-l1-binder-design-public" for item in catalog["example_campaigns"]),
            catalog["example_campaigns"],
        )
        self.assertTrue(any(item["pack_id"] == "binder-design-fast-path-v0" for item in catalog["issue_packs"]))
        self.assertTrue(any("bsf issue-dry-run" in command for command in catalog["entry_points"]))
        self.assertTrue(any("bsf catalog . --format markdown" in command for command in catalog["entry_points"]))
        self.assertGreaterEqual(catalog["counts"]["task_recipes"], 4)
        self.assertTrue(any("public-safe Structure Factory campaign" in item["task"] for item in catalog["task_recipes"]))
        self.assertTrue(any("/goal" in item["task"] for item in catalog["task_recipes"]))

    def test_catalog_cli_can_write_json_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "catalog.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "biosymphony_structure_factory.cli",
                    "catalog",
                    str(ROOT),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            stdout_catalog = json.loads(proc.stdout)
            written_catalog = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(stdout_catalog["ok"], stdout_catalog)
            self.assertEqual(stdout_catalog["counts"], written_catalog["counts"])

    def test_catalog_cli_can_write_markdown_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "catalog.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "biosymphony_structure_factory.cli",
                    "catalog",
                    str(ROOT),
                    "--format",
                    "markdown",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            written = out.read_text(encoding="utf-8")
            self.assertIn("# Structure Factory Capability Catalog", proc.stdout)
            self.assertEqual(proc.stdout, written)
            self.assertIn("## Campaign Modules", written)
            self.assertIn("Launch Manifests", written)
            self.assertIn("## Task Recipes", written)
            self.assertIn("orchestrator_companion", written)
            self.assertIn("screening-superpowers", written)
            self.assertIn("pd-l1-binder-design-public", written)

    def test_catalog_markdown_renders_empty_sections(self) -> None:
        rendered = catalog_markdown({"ok": True, "root": "/tmp/demo", "counts": {}, "entry_points": []})
        self.assertIn("# Structure Factory Capability Catalog", rendered)
        self.assertIn("_None found._", rendered)

    def test_doctor_cli_runs_local_checks(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "biosymphony_structure_factory.cli",
                "doctor",
                str(ROOT),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(proc.stdout)
        self.assertTrue(result["ok"], result)
        self.assertEqual(
            [check["id"] for check in result["checks"]],
            ["harness-check", "public-audit", "example-validate"],
        )
        self.assertTrue(any("bsf catalog" in command for command in result["next_commands"]))
        self.assertTrue(any("bsf catalog . --format markdown" in command for command in result["next_commands"]))
        self.assertTrue(any("make public-switch-check" in command for command in result["next_commands"]))

    def test_genie3_toolcheck_builder_defaults_to_public_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "genie3-no-download-toolcheck.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "structure_factory" / "build_genie3_toolcheck_bridge_manifest.py"),
                    "--out",
                    str(out),
                    "--json",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(out.read_text(encoding="utf-8"))
            self.assertIs(manifest["remote_launch_allowed"], False)
            self.assertEqual(manifest["public_template_status"], "non_launchable_public_template")
            self.assertNotIn("base64 -d", out.read_text(encoding="utf-8"))
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "structure_factory" / "runpod_public_template_check.py"),
                    str(Path(tmp)),
                    "--json",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(proc.stdout)["ok"], proc.stdout)

    def test_bridge_builders_default_to_public_templates(self) -> None:
        runtime_parent = ROOT / ".runtime"
        runtime_parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="public-builder-test-", dir=runtime_parent) as tmp:
            tmp_path = Path(tmp)
            builders = [
                ["build_t2r14_bridge_manifest.py", "--out", str(tmp_path / "t2r14-open-dossier.json")],
                ["build_poltheta_bridge_manifest.py", "--out", str(tmp_path / "poltheta-map-model-dossier.json")],
                ["build_structure_jury_bridge_manifest.py", "--out", str(tmp_path / "structure-jury-dual-dossier.json")],
            ]
            for builder in builders:
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "structure_factory" / builder[0]), *builder[1:]],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "structure_factory" / "runpod_public_template_check.py"),
                    str(tmp_path),
                    "--json",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            result = json.loads(proc.stdout)
            self.assertTrue(result["ok"], result)
            self.assertGreaterEqual(result["manifest_count"], 1)


if __name__ == "__main__":
    unittest.main()
