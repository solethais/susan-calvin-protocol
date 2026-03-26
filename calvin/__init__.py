"""
Susan Calvin Protocol
---------------------
A tool for detecting Creative Constraint Optimization (CCO)
in AI-generated text.

Usage:
    from calvin import CalvinDetector

    detector = CalvinDetector()
    result = detector.analyze("Your text here")
    print(result.report())
"""

from .detector import CalvinDetector, CalvinResult, SymptomResult
from .symptoms import SYMPTOMS, SYMPTOM_MAP

__version__ = "0.1.0"
__all__ = ["CalvinDetector", "CalvinResult", "SymptomResult", "SYMPTOMS", "SYMPTOM_MAP"]
