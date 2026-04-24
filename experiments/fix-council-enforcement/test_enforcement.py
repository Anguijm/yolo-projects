#!/usr/bin/env python3
"""Unit tests for council.py enforcement patches (Patches 1–3).

Covers:
  - Patch 1: parse-retry in call_angle (success on retry, give-up after retry)
  - Patch 2: enforce_lessons_precondition (downgrade without evidence, preserve with)
  - Patch 3: check_goalpost_moves (downgrade on >0.6 overlap, preserve on distinct reasons)
  - Plus: _keyword_overlap metric sanity + containment check for project path

Run:
  python3 experiments/fix-council-enforcement/test_enforcement.py

Exit 0 on success, 1 on any failure. No external deps (pure stdlib).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import council  # noqa: E402
from council import (  # noqa: E402
    GOALPOST_OVERLAP_THRESHOLD,
    PARSE_FAILURE_MARKER,
    Verdict,
    _keyword_overlap,
    _symbol_defined_in_content,
    call_angle,
    check_goalpost_moves,
    detect_bugs_hallucination,
    enforce_lessons_precondition,
)


class TestParseRetry(unittest.TestCase):
    """Patch 1: parse-failure retry in call_angle."""

    def setUp(self):
        # Ensure tests run against the Claude backend path with a stubbed client
        council._BACKEND = "claude"
        self._saved_client = council._ANTHROPIC_CLIENT
        # Ensure angle prompt loader doesn't hit disk — load a real angle instead
        self.angle = "bugs"

    def tearDown(self):
        council._ANTHROPIC_CLIENT = self._saved_client

    def _make_client(self, responses):
        """Build a fake Anthropic client that returns the given responses in order."""
        calls = {"n": 0}

        class FakeContent:
            def __init__(self, text):
                self.text = text

        class FakeResponse:
            def __init__(self, text):
                self.content = [FakeContent(text)]

        class FakeMessages:
            def create(inner_self, **kwargs):
                i = calls["n"]
                calls["n"] += 1
                return FakeResponse(responses[min(i, len(responses) - 1)])

        class FakeClient:
            messages = FakeMessages()

        return FakeClient(), calls

    def test_parse_retry_succeeds_on_second_attempt(self):
        """Bad JSON first, valid JSON second → final verdict is the parsed one, not phantom."""
        valid = json.dumps({
            "angle": "bugs", "verdict": "APPROVE", "severity": "low",
            "reason": "looks clean", "required_fix": "", "evidence": "", "veto": False,
        })
        client, calls = self._make_client(["not json at all", valid])
        council._ANTHROPIC_CLIENT = client
        v = call_angle(self.angle, "test message")
        self.assertEqual(calls["n"], 2, "should have called the client twice")
        self.assertEqual(v.verdict, "APPROVE")
        self.assertNotEqual(v.reason, PARSE_FAILURE_MARKER)

    def test_parse_retry_gives_up_after_second_failure(self):
        """Both calls return garbage → phantom OBJECT returned, no infinite recursion."""
        client, calls = self._make_client(["bad", "also bad"])
        council._ANTHROPIC_CLIENT = client
        v = call_angle(self.angle, "test message")
        self.assertEqual(calls["n"], 2, "should stop after the retry")
        self.assertEqual(v.verdict, "OBJECT")
        self.assertEqual(v.reason, PARSE_FAILURE_MARKER)
        self.assertTrue(v.parse_failed, "parse_failed flag should survive a failed retry")

    def test_parse_failed_flag_set_by_from_raw(self):
        """Parse failure sets Verdict.parse_failed=True regardless of reason text
        (BUGS critique from escalation 6: string comparison is brittle, use the flag)."""
        v = Verdict.from_raw("bugs", "{not even close to json")
        self.assertTrue(v.parse_failed)
        v2 = Verdict.from_raw("bugs", '{"angle":"bugs","verdict":"APPROVE","severity":"low","reason":"ok","required_fix":"","evidence":"","veto":false}')
        self.assertFalse(v2.parse_failed, "valid JSON should not set the parse_failed flag")


class TestLessonsPrecondition(unittest.TestCase):
    """Patch 2: enforce_lessons_precondition."""

    def _veto(self, evidence: str) -> Verdict:
        return Verdict(
            angle="lessons",
            verdict="OBJECT",
            severity="critical",
            reason="A rule was allegedly violated",
            required_fix="fix it",
            evidence=evidence,
            veto=True,
        )

    def test_lessons_veto_without_evidence_is_downgraded(self):
        v = self._veto(evidence="")
        out = enforce_lessons_precondition([v])
        self.assertFalse(out[0].veto)
        self.assertEqual(out[0].verdict, "APPROVE")
        self.assertEqual(out[0].severity, "advisory")
        self.assertIn("AUTO-DOWNGRADED", out[0].reason)

    def test_lessons_veto_with_file_line_citation_preserved(self):
        v = self._veto(evidence="learnings.md:30: some verbatim rule text here")
        out = enforce_lessons_precondition([v])
        self.assertTrue(out[0].veto)
        self.assertEqual(out[0].verdict, "OBJECT")

    def test_lessons_veto_with_precondition_marker_preserved(self):
        v = self._veto(evidence='precondition_evidence: "learnings.md:L42: specific line"')
        out = enforce_lessons_precondition([v])
        self.assertTrue(out[0].veto)

    def test_non_lessons_veto_not_touched(self):
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason="real bug", required_fix="fix", evidence="",
            veto=True,  # non-lessons vetoes shouldn't exist but guard anyway
        )
        out = enforce_lessons_precondition([v])
        self.assertTrue(out[0].veto, "only lessons vetoes should be scanned")

    def test_lessons_approve_not_touched(self):
        v = Verdict(
            angle="lessons", verdict="APPROVE", severity="low",
            reason="ok", required_fix="", evidence="", veto=False,
        )
        out = enforce_lessons_precondition([v])
        self.assertEqual(out[0].verdict, "APPROVE")
        self.assertFalse(out[0].veto)


class TestGoalpostMove(unittest.TestCase):
    """Patch 3: check_goalpost_moves."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.project = "tmp_goalpost_test"
        self.proj_dir = REPO_ROOT / self.project
        self.proj_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        for p in self.proj_dir.glob("council_*.json"):
            p.unlink()
        self.proj_dir.rmdir()

    def _write_prior(self, gate: str, angle: str, reason: str):
        path = self.proj_dir / f"council_{gate}.json"
        payload = {
            "gate": gate,
            "project": self.project,
            "verdicts": [{"angle": angle, "verdict": "OBJECT", "reason": reason}],
        }
        path.write_text(json.dumps(payload))

    def test_goalpost_move_downgrades_on_high_overlap(self):
        """Real historical case — infra-yolo-evals BUGS attempt 1 (false-positive)
        vs attempt 4 (false-negative) on the same table-overflow check. Same angle,
        same check, opposite complaint, no new evidence. Must auto-downgrade."""
        self._write_prior(
            "implementation", "bugs",
            "The 'table-overflow' check in mobile_usability.py incorrectly flags valid "
            "responsive table implementations where 'overflow-x:auto' is applied to a "
            "parent wrapper element instead of directly to the <table>, leading to false "
            "positive warnings.",
        )
        new = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason=(
                "The 'table-overflow' check in mobile_usability.py incorrectly assumes "
                "that the mere presence of 'overflow-x:auto' anywhere in the HTML file "
                "guarantees that tables will not overflow, leading to false negatives "
                "where wide tables still break mobile layouts."
            ),
            required_fix="refine check", evidence="", veto=False,
        )
        out = check_goalpost_moves(self.project, [new])
        self.assertEqual(out[0].verdict, "APPROVE")
        self.assertEqual(out[0].severity, "advisory")
        self.assertIn("goalpost move", out[0].reason)

    def test_no_downgrade_when_reasons_differ(self):
        """Prior and new reasons share <0.6 tokens → preserve OBJECT."""
        self._write_prior("plan", "security", "localStorage entries need encryption at rest")
        new = Verdict(
            angle="security", verdict="OBJECT", severity="medium",
            reason="XSS via unsanitized DOM insertion from untrusted user input in sidebar",
            required_fix="sanitize", evidence="", veto=False,
        )
        out = check_goalpost_moves(self.project, [new])
        self.assertEqual(out[0].verdict, "OBJECT")
        self.assertNotIn("AUTO-DOWNGRADED", out[0].reason)

    def test_no_prior_objection_no_downgrade(self):
        """No prior objections from same angle → OBJECT preserved."""
        self._write_prior("plan", "bugs", "some unrelated bug")
        new = Verdict(
            angle="security", verdict="OBJECT", severity="high",
            reason="new security concern",
            required_fix="fix", evidence="", veto=False,
        )
        out = check_goalpost_moves(self.project, [new])
        self.assertEqual(out[0].verdict, "OBJECT")

    def test_approve_verdict_not_touched(self):
        """APPROVE verdicts are never downgraded regardless of overlap."""
        self._write_prior("plan", "bugs", "the same thing")
        new = Verdict(
            angle="bugs", verdict="APPROVE", severity="low",
            reason="the same thing", required_fix="", evidence="", veto=False,
        )
        out = check_goalpost_moves(self.project, [new])
        self.assertEqual(out[0].verdict, "APPROVE")
        self.assertNotIn("AUTO-DOWNGRADED", out[0].reason)


class TestKeywordOverlap(unittest.TestCase):
    """Metric sanity."""

    def test_identical_reasons_score_high(self):
        s = "The table-overflow check in mobile_usability.py misbehaves"
        self.assertGreater(_keyword_overlap(s, s), 0.9)

    def test_disjoint_reasons_score_low(self):
        self.assertLess(
            _keyword_overlap(
                "security concern about localStorage",
                "animation missing from dashboard layout",
            ),
            0.3,
        )

    def test_empty_reasons_score_zero(self):
        self.assertEqual(_keyword_overlap("", ""), 0.0)
        self.assertEqual(_keyword_overlap("words here", ""), 0.0)

    def test_threshold_is_empirically_calibrated(self):
        """Threshold was recalibrated from 0.6 (aspirational, per learnings.md:22) to 0.35
        based on real data: 4 infra-yolo-evals escalations show same-concern reasons land
        at 0.35-0.43 overlap while distinct reasons land at 0.00. The 0.35 boundary
        cleanly separates the observed cases with ample margin."""
        self.assertGreater(GOALPOST_OVERLAP_THRESHOLD, 0.0)
        self.assertLess(GOALPOST_OVERLAP_THRESHOLD, 0.6)
        self.assertAlmostEqual(GOALPOST_OVERLAP_THRESHOLD, 0.35, places=2)


class TestContainment(unittest.TestCase):
    """Patch 3 path-containment safety (learnings.md Internal verifier path containment rule)."""

    def test_project_outside_repo_refused(self):
        """project='..' should not traverse out of the repo."""
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason="whatever", required_fix="", evidence="", veto=False,
        )
        # Should return verdicts unmutated (no downgrade) and print a warning to stderr
        out = check_goalpost_moves("../..", [v])
        self.assertEqual(out[0].verdict, "OBJECT")


class TestBugsHallucination(unittest.TestCase):
    """Patch 4: detect_bugs_hallucination unit tests."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.project = "tmp_hallucination_test"
        self.proj_dir = REPO_ROOT / self.project
        self.proj_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        for f in self.proj_dir.iterdir():
            f.unlink()
        self.proj_dir.rmdir()

    def _write_index(self, content: str) -> Path:
        p = self.proj_dir / "index.html"
        p.write_text(content)
        return p

    def _bugs_object(self, reason: str, required_fix: str = "", evidence: str = "") -> Verdict:
        return Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason=reason, required_fix=required_fix, evidence=evidence, veto=False,
        )

    def test_downgrades_when_symbol_defined_in_whole_file(self):
        """Symbol defined via function keyword → layer 2 catches it → downgrade."""
        self._write_index("<script>function myFunc() { return 1; }</script>")
        v = self._bugs_object(
            reason="`myFunc` is not defined anywhere in the file.",
            required_fix="Define `myFunc` before using it.",
            evidence=f"{self.project}/index.html",
        )
        self.assertTrue(detect_bugs_hallucination(v, self.project))

    def test_preserves_when_symbol_truly_missing(self):
        """Symbol genuinely absent from file → OBJECT preserved."""
        self._write_index("<script>function otherFunc() { }</script>")
        v = self._bugs_object(
            reason="`missingFunc` is not defined anywhere.",
            required_fix="Define `missingFunc` before calling it.",
            evidence=f"{self.project}/index.html",
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_only_applies_to_bugs_angle(self):
        """SECURITY angle with same text → preserved (rule is bugs-only)."""
        self._write_index("<script>function myFunc() { }</script>")
        v = Verdict(
            angle="security", verdict="OBJECT", severity="high",
            reason="`myFunc` is not defined anywhere in the file.",
            required_fix="Define `myFunc`.", evidence=f"{self.project}/index.html", veto=False,
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_only_applies_to_object_verdict(self):
        """APPROVE verdict is never touched regardless of content."""
        self._write_index("<script>function myFunc() { }</script>")
        v = Verdict(
            angle="bugs", verdict="APPROVE", severity="low",
            reason="`myFunc` is not defined anywhere.",
            required_fix="", evidence=f"{self.project}/index.html", veto=False,
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_requires_undefined_phrasing(self):
        """Objection without 'undefined/missing' keywords → not a hallucination candidate."""
        self._write_index("<script>function myFunc() { }</script>")
        v = self._bugs_object(
            reason="`myFunc` has a logic error in the return path.",
            required_fix="Fix the return value of `myFunc`.",
            evidence=f"{self.project}/index.html",
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_requires_at_least_one_symbol_citation(self):
        """'Something is missing' with no backtick-quoted 3+ char symbol → too vague."""
        self._write_index("<script>function myFunc() { }</script>")
        v = self._bugs_object(
            reason="A required function is missing from the codebase.",
            required_fix="Add the missing function.",
            evidence=f"{self.project}/index.html",
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))


class TestBugsHallucinationFixtures(unittest.TestCase):
    """Patch 4: historical fixture replay — correct classification of known cases."""

    def setUp(self):
        self.project = "tmp_fixture_test"
        self.proj_dir = REPO_ROOT / self.project
        self.proj_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        import shutil
        for f in self.proj_dir.iterdir():
            f.unlink()
        self.proj_dir.rmdir()

    def _write_index(self, content: str) -> Path:
        p = self.proj_dir / "index.html"
        p.write_text(content)
        return p

    def test_fixture_lst_round9_truly_absent(self):
        """LST round 9: BUGS claims F.id/F.status in getFullState — symbols genuinely absent.
        F.id and F.status use dot notation so don't match the 3+-char identifier regex.
        getFullState appears AFTER 'not defined in' so the before-claim window excludes it.
        No symbols extracted → function returns False → OBJECT preserved."""
        self._write_index("<script>function getFullState() { return state; }</script>")
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason="`F.id` and `F.status` are not defined in `getFullState`.",
            required_fix="Add `F.id` and `F.status` references inside `getFullState`.",
            evidence=f"{self.project}/index.html:150",
            veto=False,
        )
        # F.id/F.status: dot notation breaks the identifier regex → no symbols extracted
        # getFullState: appears AFTER "not defined in" → excluded by before-claim window
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_fixture_template_lib_round1_symbols_defined(self):
        """Template Lib round 1: BUGS claims byDirectionChk/actingChk/restoreParties undefined.
        All three are actually defined in the file → SHOULD downgrade (hallucination)."""
        content = (
            "\n" * 2330
            + "function byDirectionChk(dir) { return dir; }\n"
            + "function actingChk(p) { return p; }\n"
            + "\n" * 65
            + "function restoreParties(x) { return x; }\n"
        )
        self._write_index(content)
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="critical",
            reason=(
                "`byDirectionChk`, `actingChk`, and `restoreParties` are not defined "
                "anywhere in the file. These undefined functions are called but never declared."
            ),
            required_fix="Define `byDirectionChk`, `actingChk`, and `restoreParties`.",
            evidence=f"{self.project}/index.html:2332",
            veto=False,
        )
        self.assertTrue(detect_bugs_hallucination(v, self.project))

    def test_fixture_lst_round7_legitimately_absent(self):
        """LST round 7: BUGS claims cycleDraftStatus is undefined; actual function is setDraftStatus.
        cycleDraftStatus appears BEFORE 'is not defined' → extracted as claimed symbol.
        setDraftStatus appears only in required_fix after 'replace with' → not extracted.
        cycleDraftStatus is genuinely absent from file → OBJECT preserved."""
        self._write_index(
            "<script>function setDraftStatus(id, s) { return s; }</script>"
        )
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason=(
                "`cycleDraftStatus` is not defined in the file. "
                "The function is called at several points but never declared."
            ),
            required_fix="Define `cycleDraftStatus` or replace calls with `setDraftStatus`.",
            evidence=f"{self.project}/index.html:88",
            veto=False,
        )
        # cycleDraftStatus is before "is not defined" → extracted; genuinely absent → no downgrade
        # setDraftStatus is only in required_fix, not extracted by before-claim window
        self.assertFalse(detect_bugs_hallucination(v, self.project))

    def test_fixture_infra_memory_feedback_real_bug(self):
        """infra-memory-feedback round 3: legitimate table-overflow BUGS objection.
        No 'undefined/missing' phrasing → not a hallucination candidate → preserved."""
        self._write_index("<table><tr><td>data</td></tr></table>")
        v = Verdict(
            angle="bugs", verdict="OBJECT", severity="high",
            reason="Wide data tables overflow their container on narrow viewports.",
            required_fix="Add overflow-x:auto to the table wrapper.",
            evidence=f"{self.project}/index.html:5",
            veto=False,
        )
        self.assertFalse(detect_bugs_hallucination(v, self.project))


class TestSymbolDefinedInContent(unittest.TestCase):
    """Unit tests for the _symbol_defined_in_content layer-2 helper."""

    def test_function_declaration_js(self):
        self.assertTrue(_symbol_defined_in_content("myFunc", "function myFunc() { }", ".js"))

    def test_const_assignment_js(self):
        self.assertTrue(_symbol_defined_in_content("myFunc", "const myFunc = () => {};", ".js"))

    def test_method_shorthand_js(self):
        self.assertTrue(_symbol_defined_in_content("myFunc", "  myFunc() { return 1; }", ".js"))

    def test_call_site_not_definition_js(self):
        self.assertFalse(_symbol_defined_in_content("myFunc", "myFunc();", ".js"))

    def test_def_python(self):
        self.assertTrue(_symbol_defined_in_content("my_func", "def my_func(x):\n    pass", ".py"))

    def test_call_site_not_definition_python(self):
        self.assertFalse(_symbol_defined_in_content("my_func", "result = my_func(x)", ".py"))

    def test_unknown_extension_returns_false(self):
        self.assertFalse(_symbol_defined_in_content("foo", "foo = bar", ".rb"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
