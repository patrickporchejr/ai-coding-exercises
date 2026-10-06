# Eval-from-Scratch Challenge

Build a prompt eval pipeline in Python, three times, the way you'd have to in an interview.

| # | Exercise | Mode | Time box | Folder |
|---|----------|------|----------|--------|
| 1 | Support-ticket triage | **Guided**: docs, course notes, AI help all allowed. Go slowly and understand each piece. | none (aim ~2–3h) | `exercises/01-guided/` |
| 2 | Text-to-SQL | **Timed, no AI**: official docs only. No Claude, no Copilot, no copying from exercise 1. | **60 min** | `exercises/02-timed-no-ai/` |
| 3 | Meeting action items | **Timed, with AI**: use any AI tool you want. The bar is higher. | **60 min** | `exercises/03-timed-with-ai/` |
| 4 | Contention (auction bids) | **Hands-on Postgres**: two sessions, interleaved by hand. Not an eval exercise. Needs Docker. | none | `exercises/04-contention/` |
| 5 | Clean a messy CSV | **Data-cleaning drill**: normalize, report what changed and why. Not an eval exercise. | none | `exercises/05-messy-csv/` |

Each folder has a `PROMPT.md` written like an interview question. Read only the one you're working on. Don't look ahead at 2 or 3 before you sit down to do them.

## The workflow being tested

This is the loop from the Anthropic Academy course *A typical eval workflow*:

1. **Draft a prompt.** Write the prompt under test as a function: `run_prompt(test_case) -> output`.
2. **Build a dataset.** Write it by hand, or have Claude generate it as JSON. Each case is an input plus whatever the grader needs (expected values, criteria).
3. **Run.** Feed every case through the prompt and collect the outputs.
4. **Grade.**
   - *Code graders* are deterministic checks: valid JSON, schema, exact match, "does the SQL execute", and so on.
   - *Model graders* use an LLM judge with a rubric. They return structured output (strengths, weaknesses, reasoning, score).
5. **Score and report.** Compute per-case scores and the average, then look at the failures.
6. **Iterate.** Change the prompt, re-run, and compare v1 with v2.

See `reference/cheatsheet.md` for the course recap and current API notes. Read it before exercise 1. It's off-limits during exercise 2.

## ⚠️ API change since the course

The course gets JSON out of Claude by **prefilling** the assistant turn with `` ```json `` and passing `stop_sequences=["```"]`. **On current models (Opus 4.6+, Sonnet 4.6+, all Claude 5 models), prefill returns a 400 error.** Use structured outputs instead (`client.messages.parse(..., output_format=PydanticModel)`). The cheatsheet shows how. Being able to explain this change is a good interview talking point.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

## Rules of the game

- Put your work in the exercise's `answers/` folder. Git ignores it on `main`.

- Start a timer before exercises 2 and 3. When it goes off, stop and record where you got to in `LOG.md`.
- Keep a short running commentary in comments or notes, the way you'd talk through it in an interview.
- After each exercise, answer the **debrief questions** at the bottom of its `PROMPT.md` without looking anything up.
- Score yourself with `reference/rubric.md` and record it in `LOG.md`.
