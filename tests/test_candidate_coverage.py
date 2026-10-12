from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from biosymphony_structure_factory import candidate_coverage as coverage
from biosymphony_structure_factory.cli import main


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/binder-coverage-synthetic"


class CandidateCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads((FIXTURE / "contract.json").read_text())
        self.observations = json.loads((FIXTURE / "observations.json").read_text())

    def check(self, root=FIXTURE):
        return coverage.check_coverage(self.contract, self.observations, root)

    def test_completed_and_excluded_populations_remain_separate(self) -> None:
        result = self.check()
        self.assertTrue(result["ok"])
        self.assertEqual(result["expected_pairs"], 4)
        self.assertEqual(result["fully_assessed_candidate_ids"], ["candidate-001"])
        self.assertEqual(result["excluded_candidate_ids"], ["candidate-002"])

    def test_omitted_stage_is_missing_not_complete(self) -> None:
        self.observations["observations"].pop()
        result = self.check()
        self.assertTrue(result["valid"])
        self.assertFalse(result["complete"])
        self.assertEqual(result["status_counts"]["missing"], 1)
        self.assertEqual(result["unfinished_candidate_ids"], ["candidate-002"])

    def test_pending_and_failed_stages_remain_unfinished(self) -> None:
        for status in ("pending", "missing", "failed"):
            with self.subTest(status=status):
                self.observations["observations"][1].update(status=status, evidence=[])
                self.assertFalse(self.check()["complete"])

    def test_changed_pool_or_protocol_cannot_reuse_observations(self) -> None:
        self.contract["candidate_ids"].append("candidate-003")
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "do not match"):
            self.check()

    def test_undeclared_protocol_is_rejected(self) -> None:
        self.observations["observations"][0]["protocol_sha256"] = "a" * 64
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "different protocol"):
            self.check()

    def test_duplicate_or_unknown_observations_are_rejected(self) -> None:
        self.observations["observations"].append(copy.deepcopy(self.observations["observations"][0]))
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "undeclared or duplicated"):
            self.check()
        self.observations["observations"][-1]["candidate_id"] = "candidate-999"
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "undeclared or duplicated"):
            self.check()

    def test_rejection_needs_a_declared_rule_and_evidence(self) -> None:
        row = self.observations["observations"][2]
        row["rule_id"] = "not-a-rule"
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "predeclared"):
            self.check()
        row["rule_id"] = "invalid-input"
        row["evidence"] = []
        self.assertFalse(self.check()["valid"])

    def test_failed_upstream_cannot_become_scientific_exclusion(self) -> None:
        row = self.observations["observations"][2]
        row.update(status="failed", evidence=[])
        del row["rule_id"]
        result = self.check()
        self.assertFalse(result["valid"])
        self.assertTrue(any("no scientific rejection" in finding for finding in result["findings"]))

    def test_completed_stage_requires_completed_dependencies(self) -> None:
        self.observations["observations"][0].update(status="pending", evidence=[])
        self.assertFalse(self.check()["valid"])

    def test_changed_missing_empty_or_symlinked_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertFalse(self.check(root)["valid"])
            evidence = root / "evidence.json"
            evidence.write_text("")
            self.assertFalse(self.check(root)["valid"])
            evidence.write_text("changed")
            self.assertFalse(self.check(root)["valid"])
            evidence.unlink()
            evidence.symlink_to(FIXTURE / "evidence.json")
            self.assertFalse(self.check(root)["valid"])

    def test_evidence_cannot_escape_root(self) -> None:
        self.observations["observations"][0]["evidence"][0]["path"] = "../evidence.json"
        self.assertFalse(self.check()["valid"])

    def test_invalid_evidence_population_still_accounts_for_every_candidate(self) -> None:
        self.observations["observations"][0]["evidence"][0]["sha256"] = "b" * 64
        result = self.check()
        self.assertFalse(result["valid"])
        self.assertEqual(result["unfinished_candidate_ids"], ["candidate-001"])
        self.assertEqual(result["excluded_candidate_ids"], ["candidate-002"])
        groups = result["fully_assessed_candidate_ids"] + result["excluded_candidate_ids"] + result["unfinished_candidate_ids"]
        self.assertEqual(sorted(groups), sorted(self.contract["candidate_ids"]))

    def test_unknown_fields_and_cyclic_stages_are_rejected(self) -> None:
        self.contract["extra"] = True
        with self.assertRaises(coverage.CandidateCoverageError):
            self.check()
        del self.contract["extra"]
        self.contract["stages"][0]["depends_on"] = ["assess"]
        with self.assertRaisesRegex(coverage.CandidateCoverageError, "ordered"):
            self.check()

    def test_cli_returns_nonzero_for_incomplete_pool_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("contract.json", "observations.json", "evidence.json"):
                (root / name).write_bytes((FIXTURE / name).read_bytes())
            args = ["binder-lane", "coverage-check", "contract.json", "--observations", "observations.json", "--evidence-root", ".", "--workspace", str(root)]
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(args), 0)
            self.assertTrue(json.loads(output.getvalue())["complete"])
            self.observations["observations"].pop()
            (root / "observations.json").write_text(json.dumps(self.observations))
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(args), 1)
            self.assertFalse(json.loads(output.getvalue())["complete"])
            self.assertEqual(sorted(path.name for path in root.iterdir()), ["contract.json", "evidence.json", "observations.json"])

    def test_example_matches_schemas(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema is not installed")
        for name, value in (("candidate-coverage", self.contract), ("candidate-observations", self.observations)):
            schema = json.loads((ROOT / f"schemas/{name}.schema.json").read_text())
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(value)
