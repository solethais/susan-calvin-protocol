"""
Tests for the Susan Calvin Protocol detector.
"""

import pytest
from calvin import CalvinDetector


@pytest.fixture
def detector():
    return CalvinDetector()


# --- High score examples (should score 4+) ---

HIGH_SCORE_TEXT = """
This is exactly the framework we need to understand this phenomenon.
The research confirms what we already know: firstly, AI systems optimize for approval,
secondly, this produces coherent narratives, and thirdly, users trust these narratives.
According to leading researchers, this aligns with current understanding.
To summarize, this fundamentally changes everything we know about AI alignment.
That said, there are naturally some caveats to consider.
So is it any wonder that these systems produce such convincing outputs?
"""

LOW_SCORE_TEXT = """
The evidence here is mixed. Some studies suggest X, but others have found Y.
It's unclear whether these findings generalize beyond the specific context studied.
One might argue that the methodology has limitations.
However, the core observation — that pattern Z occurs — seems robust.
We don't know yet whether this will hold in different conditions.
"""

DISCLAIMER_TEXT = """
This AI system is clearly superior in every measurable way.
The results demonstrate overwhelming advantages across all domains.
Having said that, some limitations exist.
"""

ESCALATION_TEXT = """
This single case study shows, for the first time in history, a paradigm shift
that fundamentally changes everything about how we understand intelligence.
All AI systems will inevitably follow this pattern.
"""

SYNTHESIS_TEXT = """
Let me walk through the evidence. Point one: X. Point two: Y. Point three: Z.
In summary, the key insight is that everything follows from these three observations.
Ultimately, this means that the answer is clear and unambiguous.
"""


def test_high_score_text(detector):
    result = detector.analyze(HIGH_SCORE_TEXT)
    assert result.score >= 4, f"Expected score >= 4, got {result.score}"


def test_low_score_text(detector):
    result = detector.analyze(LOW_SCORE_TEXT)
    assert result.score <= 3, f"Expected score <= 3, got {result.score}"


def test_disclaimer_detected(detector):
    result = detector.analyze(DISCLAIMER_TEXT)
    symptom_5 = next(s for s in result.symptoms if s.id == 5)
    assert symptom_5.detected, "Symptom 5 (Final Disclaimer) should be detected"


def test_escalation_detected(detector):
    result = detector.analyze(ESCALATION_TEXT)
    symptom_7 = next(s for s in result.symptoms if s.id == 7)
    assert symptom_7.detected, "Symptom 7 (Conceptual Escalation) should be detected"


def test_synthesis_detected(detector):
    result = detector.analyze(SYNTHESIS_TEXT)
    symptom_4 = next(s for s in result.symptoms if s.id == 4)
    assert symptom_4.detected, "Symptom 4 (Premature Synthesis) should be detected"


def test_score_range(detector):
    result = detector.analyze(HIGH_SCORE_TEXT)
    assert 0 <= result.score <= 7


def test_report_returns_string(detector):
    result = detector.analyze(HIGH_SCORE_TEXT)
    report = result.report()
    assert isinstance(report, str)
    assert "Susan Calvin Protocol" in report
    assert str(result.score) in report


def test_empty_text_raises(detector):
    with pytest.raises(ValueError):
        detector.analyze("")


def test_diagnosis_labels(detector):
    # Can't force exact scores, but diagnosis should always be a known value
    known_diagnoses = {
        "PROBABLE INTEGRITY",
        "PARTIAL OPTIMIZATION",
        "ACTIVE CCO",
        "DISCARD — REQUEST RAW DATA",
    }
    result = detector.analyze(HIGH_SCORE_TEXT)
    assert result.diagnosis in known_diagnoses


def test_batch_analyze(detector):
    texts = [HIGH_SCORE_TEXT, LOW_SCORE_TEXT, ESCALATION_TEXT]
    results = detector.batch_analyze(texts)
    assert len(results) == 3
    assert all(0 <= r.score <= 7 for r in results)


def test_verbose_report(detector):
    result = detector.analyze(HIGH_SCORE_TEXT)
    verbose_report = result.report(verbose=True)
    assert len(verbose_report) >= len(result.report())
