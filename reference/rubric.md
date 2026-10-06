# Self-Scoring Rubric (20 pts)

Score each row 0–4.

| Area | 0 | 2 | 4 |
|---|---|---|---|
| **Dataset design** | A handful of near-identical cases | Reasonable variety | Covers the happy path, edge cases, and adversarial or ambiguous inputs; each case has expected values or criteria the grader can use |
| **Code graders** | None | One basic check (for example "is valid JSON") | Several deterministic checks that catch real failures, each scored and reported separately |
| **Model grader** | None, or "rate 1–10" with no rubric | Rubric plus structured output | Per-case criteria, reasoning before score, anchored scale, and you can say how you'd validate the judge |
| **Pipeline and code quality** | Doesn't run end to end | Runs, but is fragile or hard to change | Clean functions, handles API and parse errors, results saved to disk |
| **Iteration and communication** | No prompt iteration | v2 prompt tried | v1 vs v2 compared with numbers; you can explain *why* the score moved and what you'd do next |

## Interview signals to practice saying out loud
- "Why I chose these test cases: …"
- "What this eval *doesn't* catch: …"
- "How I'd know the LLM judge is trustworthy: hand-label ~20 cases and check agreement."
- "Cost and latency of one eval run: …"
