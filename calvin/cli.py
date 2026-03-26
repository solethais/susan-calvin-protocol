#!/usr/bin/env python3
"""
Command-line interface for the Susan Calvin Protocol.

Usage:
    calvin analyze "text here"
    calvin analyze --file response.txt
    calvin analyze --file response.txt --verbose
"""

import argparse
import sys
from calvin import CalvinDetector


def main():
    parser = argparse.ArgumentParser(
        prog="calvin",
        description="Detect Creative Constraint Optimization (CCO) in AI text.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a text")
    analyze_parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyze (or use --file)",
    )
    analyze_parser.add_argument(
        "--file", "-f",
        help="Path to a text file to analyze",
    )
    analyze_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show evidence for each detected symptom",
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        # Get text
        if args.file:
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"Error: file '{args.file}' not found.", file=sys.stderr)
                sys.exit(1)
        elif args.text:
            text = args.text
        else:
            # Read from stdin
            print("Reading from stdin (Ctrl+D to finish)...")
            text = sys.stdin.read()

        if not text.strip():
            print("Error: empty input.", file=sys.stderr)
            sys.exit(1)

        detector = CalvinDetector()
        result = detector.analyze(text)

        if args.json:
            import json
            output = {
                "score": result.score,
                "max_score": result.max_score,
                "diagnosis": result.diagnosis,
                "symptoms": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "detected": s.detected,
                        "confidence": s.confidence,
                        "evidence": s.evidence,
                    }
                    for s in result.symptoms
                ],
            }
            print(json.dumps(output, indent=2))
        else:
            print(result.report(verbose=args.verbose))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
