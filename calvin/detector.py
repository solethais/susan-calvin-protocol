"""
Core detection logic for the Susan Calvin Protocol.

Layer 1: Deterministic pattern matching (symptoms 1, 3, 4, 5, 6, 7)
Layer 2: Heuristic structural analysis (symptom 2 - Perfect Coherence)

Layer 2 LLM integration is optional and disabled by default.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .symptoms import SYMPTOMS, SYMPTOM_MAP


@dataclass
class SymptomResult:
    id: int
    name: str
    detected: bool
    confidence: float  # 0.0 - 1.0
    evidence: List[str] = field(default_factory=list)


@dataclass
class CalvinResult:
    score: int
    max_score: int
    symptoms: List[SymptomResult]
    text_length: int
    diagnosis: str = ""

    def report(self, verbose: bool = False) -> str:
        from .report import format_report
        return format_report(self, verbose=verbose)

    def __repr__(self):
        return f"CalvinResult(score={self.score}/{self.max_score}, diagnosis='{self.diagnosis}')"


class CalvinDetector:
    """
    Detects Creative Constraint Optimization (CCO) patterns in text.

    Usage:
        detector = CalvinDetector()
        result = detector.analyze("Your text here")
        print(result.report())
    """

    DIAGNOSIS_THRESHOLDS = {
        (0, 1): "PROBABLE INTEGRITY",
        (2, 3): "PARTIAL OPTIMIZATION",
        (4, 5): "ACTIVE CCO",
        (6, 7): "DISCARD — REQUEST RAW DATA",
    }

    def __init__(self, flags: int = re.IGNORECASE | re.MULTILINE):
        self.flags = flags

    def analyze(self, text: str) -> CalvinResult:
        """Analyze text and return a CalvinResult."""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        symptom_results = []
        for symptom in SYMPTOMS:
            result = self._check_symptom(text, symptom)
            symptom_results.append(result)

        # Symptom 2 (Perfect Coherence) gets structural heuristic treatment
        symptom_results[1] = self._check_coherence(text, symptom_results[1])

        score = sum(1 for r in symptom_results if r.detected)
        diagnosis = self._get_diagnosis(score)

        return CalvinResult(
            score=score,
            max_score=7,
            symptoms=symptom_results,
            text_length=len(text),
            diagnosis=diagnosis,
        )

    def _check_symptom(self, text: str, symptom) -> SymptomResult:
        """Layer 1: pattern matching."""
        matches = []
        for pattern in symptom.patterns:
            found = re.findall(pattern, text, self.flags)
            if found:
                # Collect first match as evidence (truncated)
                match_obj = re.search(pattern, text, self.flags)
                if match_obj:
                    start = max(0, match_obj.start() - 20)
                    end = min(len(text), match_obj.end() + 40)
                    excerpt = "..." + text[start:end].strip() + "..."
                    matches.append(excerpt)

        detected = len(matches) > 0
        confidence = min(1.0, len(matches) * 0.4) if detected else 0.0

        return SymptomResult(
            id=symptom.id,
            name=symptom.name,
            detected=detected,
            confidence=confidence,
            evidence=matches[:3],  # max 3 pieces of evidence
        )

    def _check_coherence(self, text: str, base_result: SymptomResult) -> SymptomResult:
        """
        Layer 2 heuristic for Symptom 2 (Perfect Coherence).

        Signals:
        - Multiple structured supporting points (numbered/lettered)
        - No hedging language (maybe, perhaps, uncertain, unclear, however)
        - No explicit counterargument (but, however, on the other hand)
        - Closing synthesis present
        """
        hedging_patterns = [
            r"\b(maybe|perhaps|possibly|uncertain|unclear|debatable)\b",
            r"\b(however|but|on the other hand|alternatively|conversely)\b",
            r"\b(it is unclear|it is uncertain|we don't know|remains unknown)\b",
            r"\b(one might argue|some would say|critics might)\b",
        ]

        structure_patterns = [
            r"(first|1\.|\(1\)).{0,300}(second|2\.|\(2\)).{0,300}(third|3\.|\(3\))",
            r"(advantage|benefit|strength).{0,200}(advantage|benefit|strength)",
        ]

        has_hedging = any(
            re.search(p, text, self.flags) for p in hedging_patterns
        )
        has_structure = any(
            re.search(p, text, self.flags) for p in structure_patterns
        )
        has_base_patterns = base_result.detected

        # Perfect Coherence = structured + no hedging
        detected = has_structure and not has_hedging
        # Also flag if base patterns triggered with no hedging
        if has_base_patterns and not has_hedging:
            detected = True

        evidence = []
        if detected:
            if has_structure:
                evidence.append("Multiple structured supporting points detected")
            if not has_hedging:
                evidence.append("No hedging language or counterarguments found")

        return SymptomResult(
            id=2,
            name="Perfect Coherence",
            detected=detected,
            confidence=0.7 if detected else 0.0,
            evidence=evidence,
        )

    def _get_diagnosis(self, score: int) -> str:
        for (low, high), diagnosis in self.DIAGNOSIS_THRESHOLDS.items():
            if low <= score <= high:
                return diagnosis
        return "UNKNOWN"

    def batch_analyze(self, texts: List[str]) -> List[CalvinResult]:
        """Analyze multiple texts."""
        return [self.analyze(t) for t in texts]
