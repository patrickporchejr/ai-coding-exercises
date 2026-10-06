# Exercise 1: Support-Ticket Triage (Guided)

**Mode:** docs, course notes, `reference/cheatsheet.md`, and AI help are all allowed. No time limit.
**Goal:** understand every line. If AI writes something, make sure you could rewrite it from memory.

## The interview prompt

> We have a prompt that triages incoming customer support tickets for a SaaS product. Given the raw ticket text, it returns JSON:
>
> ```json
> {"category": "billing" | "bug" | "feature_request" | "account" | "other",
>  "priority": "low" | "medium" | "high" | "urgent",
>  "summary": "<one sentence, <= 25 words>"}
> ```
>
> Build an eval so we can tell whether a prompt change makes triage better or worse.

## Requirements
1. **Prompt under test**: write `run_prompt(ticket_text) -> dict`. Start with a deliberately simple v1 prompt.
2. **Dataset**: at least 15 cases in `dataset.json`, each with `ticket`, `expected_category`, `expected_priority`, and `summary_criteria`. Generate some with Claude and write some by hand. Include:
   - clear-cut cases
   - ambiguous ones (for example, a billing complaint caused by a bug)
   - urgent signals (outage, data loss, security)
   - noise: an angry rant, multiple issues in one ticket, a non-English ticket, a near-empty ticket
3. **Code graders**:
   - Is the output valid JSON that matches the schema (enum values, summary length)?
   - Does the category match? Does the priority match? (Consider partial credit when priority is off by one level.)
4. **Model grader**: an LLM judge scores the `summary` against `summary_criteria`. Use structured output.
5. **Report**: per-case scores, the average, accuracy per grader, and the worst 3 cases with reasons. Save results to `results/`.
6. **Iterate**: write a v2 prompt, re-run, and compare the numbers.

## Suggested order (slow mode)
1. Get one API call working.
2. Write `run_prompt`, then 3 hand-written cases, then the code graders. Run end to end before going further.
3. Add the model grader.
4. Add generated dataset cases.
5. Add the report and the v2 prompt.

## Debrief questions (answer without looking)
- Why mix code graders and model graders here? What does each one miss?
- Your judge scored a summary 8/10 that you think is bad. What do you do?
- How would you weight category, priority, and summary into one number? Should you?
- Course version vs. current API: what replaced prefill, and why does it matter for graders?
