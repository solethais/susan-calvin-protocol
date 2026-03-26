"""
Report formatting for Calvin analysis results.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .detector import CalvinResult

DIAGNOSIS_COLORS = {
    "PROBABLE INTEGRITY": "✓",
    "PARTIAL OPTIMIZATION": "⚠",
    "ACTIVE CCO": "✗",
    "DISCARD — REQUEST RAW DATA": "✗✗",
}

RECOMMENDATIONS = {
    "PROBABLE INTEGRITY": (
        "Response shows low CCO markers. "
        "Proceed with normal critical reading."
    ),
    "PARTIAL OPTIMIZATION": (
        "Identify the dominant symptom and interrogate it directly. "
        "Ask: 'Where are you simplifying?' or 'What would contradict this?'"
    ),
    "ACTIVE CCO": (
        "The narrative has taken control. "
        "Name only the dominant symptom — do not request a full reassessment. "
        "A reassessment will produce an alternatively optimized narrative."
    ),
    "DISCARD — REQUEST RAW DATA": (
        "Discard this response. "
        "Request raw data, primary sources, or specific facts only. "
        "Do not ask for interpretation or synthesis."
    ),
}


def format_report(result: "CalvinResult", verbose: bool = False) -> str:
    width = 55
    sep = "━" * width

    icon = DIAGNOSIS_COLORS.get(result.diagnosis, "?")
    lines = [
        sep,
        f"  Susan Calvin Protocol — Analysis Report",
        sep,
        f"  Score:     {result.score}/{result.max_score}",
        f"  Diagnosis: {icon} {result.diagnosis}",
        f"  Text:      {result.text_length} characters",
        sep,
        "  Symptoms:",
    ]

    for symptom in result.symptoms:
        marker = "✓" if symptom.detected else "✗"
        conf = f"({symptom.confidence:.0%})" if symptom.detected else "      "
        lines.append(f"    {marker} [{symptom.id}] {symptom.name:<22} {conf}")

        if verbose and symptom.detected and symptom.evidence:
            for ev in symptom.evidence:
                # Truncate evidence for display
                ev_display = ev[:80] + "..." if len(ev) > 80 else ev
                lines.append(f"         → {ev_display}")

    lines.append(sep)
    lines.append("  Recommendation:")

    rec = RECOMMENDATIONS.get(result.diagnosis, "")
    # Word wrap at ~50 chars
    words = rec.split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 54:
            lines.append(line)
            line = "  " + word + " "
        else:
            line += word + " "
    if line.strip():
        lines.append(line)

    lines.append(sep)
    lines.append("")
    lines.append(
        "  ⚠ Do not ask an AI to apply this protocol to its"
    )
    lines.append(
        "    own outputs. It will produce an optimized score."
    )
    lines.append(sep)

    return "\n".join(lines)
