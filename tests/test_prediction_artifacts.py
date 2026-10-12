from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from biosymphony_structure_factory import binder_executor


ROOT = Path(__file__).resolve().parents[1]
CIF = """data_synthetic
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM CA ALA A 1.0 2.0 3.0
ATOM CA GLY B 4.0 5.0 6.0
#
"""


class PredictionArtifactsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.input = self.root / "case.yaml"
        self.input.write_text("version: 1\nsequences: []\n")
        self.output = self.root / "out"
        self.predictions = self.output / "boltz_results_case" / "predictions" / "case"
        self.predictions.mkdir(parents=True)
        self.structure = self.predictions / "case_model_0.cif"
        self.confidence = self.predictions / "confidence_case_model_0.json"
        self.structure.write_text(CIF)
        self.confidence.write_text(json.dumps({"confidence_score": 0.5, "complex_plddt": 0.6, "ptm": 0.4, "iptm": 0.3}))
        registry = json.loads((ROOT / "references/binder-execution-adapters.json").read_text())
        self.adapter = binder_executor.validate_registry(registry)["adapters"][0]

    def check(self):
        return binder_executor._validate_outputs(self.adapter, self.root, {"input_path": str(self.input), "output_dir": str(self.output)})

    def test_native_bundle_parses_and_records_hashes(self) -> None:
        records, findings = self.check()
        self.assertEqual(findings, [])
        self.assertEqual(records[0]["matched_count"], 1)
        self.assertEqual(len(records[0]["files"][0]["members"]), 2)

    def test_markdown_only_directory_is_rejected(self) -> None:
        self.structure.unlink()
        self.confidence.unlink()
        (self.output / "README.md").write_text("Synthetic placeholder\n")
        self.assertTrue(self.check()[1])

    def test_missing_or_orphaned_confidence_is_rejected(self) -> None:
        self.confidence.rename(self.predictions / "confidence_case_model_1.json")
        self.assertTrue(self.check()[1])

    def test_missing_final_sample_fails_declared_count(self) -> None:
        self.adapter["expected_outputs"][0]["expected_model_count"] = 2
        self.assertTrue(self.check()[1])
        (self.predictions / "case_model_1.cif").write_text(CIF)
        (self.predictions / "confidence_case_model_1.json").write_bytes(self.confidence.read_bytes())
        self.assertEqual(self.check()[1], [])

    def test_extra_samples_fail_declared_count(self) -> None:
        (self.predictions / "case_model_1.cif").write_text(CIF)
        (self.predictions / "confidence_case_model_1.json").write_bytes(self.confidence.read_bytes())
        self.assertTrue(self.check()[1])

    def test_headers_and_invalid_coordinates_are_rejected(self) -> None:
        for content in ("_atom_site.Cartn_x\n", CIF.replace("1.0 2.0 3.0", "nan 2.0 3.0"), CIF.replace("1.0 2.0 3.0", "1.0 2.0")):
            with self.subTest(content=content):
                self.structure.write_text(content)
                self.assertTrue(self.check()[1])

    def test_missing_or_invalid_confidence_values_are_rejected(self) -> None:
        for bad in ({}, [], {"confidence_score": True}, {"confidence_score": float("nan")}, {"confidence_score": 50}):
            with self.subTest(bad=bad):
                self.confidence.write_text(json.dumps(bad))
                self.assertTrue(self.check()[1])

    def test_input_identity_must_match_output_identity(self) -> None:
        self.input = self.input.rename(self.root / "other.yaml")
        self.assertTrue(self.check()[1])

    def test_every_directory_input_needs_a_prediction(self) -> None:
        (self.root / "other.yaml").write_text("version: 1\n")
        self.input = self.root
        self.assertTrue(self.check()[1])

    def test_duplicate_input_stems_are_rejected(self) -> None:
        (self.root / "case.fasta").write_text(">synthetic\nA\n")
        self.input = self.root
        self.assertTrue(self.check()[1])

    def test_native_fas_input_is_covered_in_single_and_mixed_batches(self) -> None:
        self.input = self.input.rename(self.root / "case.fas")
        self.assertEqual(self.check()[1], [])
        (self.root / "other.yaml").write_text("version: 1\n")
        self.input = self.root
        self.assertTrue(self.check()[1])
        (self.root / "other.yaml").unlink()
        (self.root / "other.fas").write_text(">synthetic\nA\n")
        self.assertTrue(self.check()[1])

    def test_symlinked_prediction_is_rejected(self) -> None:
        self.structure.unlink()
        self.structure.symlink_to(self.input)
        self.assertTrue(self.check()[1])

    def test_unknown_validator_and_nonpath_binding_are_rejected(self) -> None:
        for field, value in (("content_validator", "unknown"), ("input_binding", "not_declared")):
            registry = json.loads((ROOT / "references/binder-execution-adapters.json").read_text())
            registry["adapters"][0]["expected_outputs"][0][field] = value
            with self.assertRaises(binder_executor.BinderExecutorError):
                binder_executor.validate_registry(registry)

    def test_zero_exit_does_not_complete_invalid_prediction(self) -> None:
        registry = json.loads((ROOT / "references/binder-execution-adapters.json").read_text())
        adapter = registry["adapters"][0]
        adapter.update(program="true", readiness_argv=["true"], command_argv=["true"])
        runtime = self.root / ".runtime" / "probe"
        runtime.mkdir(parents=True)
        (runtime / "case.yaml").write_text("version: 1\n")
        (runtime / "out").mkdir()
        (runtime / "out" / "README.md").write_text("Synthetic placeholder\n")
        receipt = binder_executor.run_adapter(
            registry, "boltz-local-v1", workspace_root=self.root, runtime_root=runtime,
            bindings={"input_path": "case.yaml", "output_dir": "out"},
            authorization=binder_executor.LOCAL_EXECUTION_AUTHORIZATION,
        )
        self.assertEqual(receipt["returncode"], 0)
        self.assertEqual(receipt["status"], "failed")
        self.assertFalse(receipt["ok"])
