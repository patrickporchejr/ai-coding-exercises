# AI Coding Exercises

Hands-on practice for AI engineering interviews. Each exercise is written like a real interview question. You build the solution from scratch, then answer debrief questions the way you would in the room.

**Who it's for:** engineers preparing for interviews that involve LLMs, such as building evals or handling model output, plus the backend and data problems that come up alongside them.

**What's here:**
- **An eval track** (exercises 1–3): build a prompt-evaluation pipeline in Python, first guided and then timed without AI, and finally prove your results can be trusted.
- **Drills** (exercises 4–12): standalone problems on reliability, databases, data cleaning, RAG, tool-use agents, and the metrics and validation work that surround LLM systems.

## Exercises

### Eval track: do these in order

| # | Exercise | Mode | Time box |
|---|----------|------|----------|
| 1 | [Support-ticket triage](exercises/01-eval-ticket-triage/PROMPT.md) | **Guided**: docs, the cheatsheet, and AI help are all allowed. Go slowly and understand each piece. | none (aim for 2–3h) |
| 2 | [Text-to-SQL](exercises/02-eval-text-to-sql/PROMPT.md) | **Timed, no AI**: official docs only. No AI assistants, and no copying from exercise 1. | **60 min** |
| 3 | [Trust your eval: meeting action items](exercises/03-eval-action-items/PROMPT.md) | **Timed, with AI**: the test set and two prompts are provided. Check the LLM judge against your own labels, then decide whether v2 really beats v1. | **60 min** |

Read only the prompt you're working on. Don't look at exercises 2 or 3 until you sit down to do them.

### Drills: any order

| # | Exercise | Skills | Needs |
|---|----------|--------|-------|
| 4 | [Contention: auction bids](exercises/04-contention/PROMPT.md) | Race conditions, row locking, optimistic concurrency, isolation levels, deadlocks | Docker |
| 5 | [Clean a messy CSV](exercises/05-messy-csv/PROMPT.md) | Parsing, normalization, edge cases, explaining your choices | Python |
| 6 | [Paginated API client with retries](exercises/06-paginated-api-client/PROMPT.md) | Reliability, `asyncio`, backoff, error handling | Python (fake API included) |
| 7 | [Join and deduplicate two sources](exercises/07-join-dedupe/PROMPT.md) | Fuzzy matching, conflict rules, flagging uncertainty instead of guessing | Python |
| 8 | [Parse and validate LLM output](exercises/08-validate-llm-output/PROMPT.md) | Structured outputs, schema validation, failure routing | Python |
| 9 | [Triage an error export](exercises/09-error-triage/PROMPT.md) | Grouping, aggregation, streaming large files, prioritization | Python (data generator included) |
| 10 | [Compute eval metrics from labeled data](exercises/10-eval-metrics/PROMPT.md) | Precision, recall, F1 and Cohen's kappa from scratch; label disagreement | Python |
| 11 | [RAG over a help center](exercises/11-rag-qa/PROMPT.md) | Chunking, retrieval, grounded answers with citations, recall@k and faithfulness evals. Best done after the eval track. | API key |
| 12 | [Tool-use agent](exercises/12-tool-use-agent/PROMPT.md) | Tool definitions, a hand-written agent loop, tool errors, guarding write actions, end-state evals | API key (fake backend included) |

Some drills ship with a helper script (a fake server or a data generator). Treat it as a black box: run it, but don't read its source until you're done, because it contains the answer.

## How to use this repo

1. **Get your own copy.** Click **Use this template** to create your own repo. Make it private if you don't want your answers public. You can also just clone it.
2. **Set up** (see below).
3. **Work in the exercise's `answers/` folder.** On `main`, `.gitignore` excludes everything in `answers/`, so your solutions don't end up in a pull request by accident. To keep your work in git, use a separate branch and remove that rule there.
4. **Track your progress** in `LOG.md` and score the eval track with [`reference/rubric.md`](reference/rubric.md).

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

Exercises 1–3, 11 and 12 call the Claude API, so you need an [Anthropic API key](https://platform.claude.com/). Exercise 4 needs Docker. The other drills need only Python.

## Models and cost

Each model job is set in your `.env` (see `.env.example`), so you can choose your own tradeoff between cost and accuracy. The defaults follow the Anthropic Academy course:

| `.env` setting | Job | Default |
|---|---|---|
| `MODEL` | The prompt under test, and the agent in exercise 12 | `claude-opus-5-5` |
| `JUDGE_MODEL` | LLM judges (model graders) | `claude-opus-5-5` |
| `DATASET_MODEL` | Generating test datasets | `claude-haiku-4-5` |

Generating datasets is cheap work that you review by hand anyway. Grading and the prompt under test are where accuracy matters.

### Model options

| Model | ID | Price per million tokens (input / output) | Good for |
|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | $10 / $50 | The most capable model. Usually more than these exercises need. |
| Claude Opus 5.5 | `claude-opus-5-5` | $4 / $20 | The default: accurate judges and a realistic system under test. |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2 / $10 | About half the cost of Opus, and a solid judge. |
| Claude Haiku 4.5 | `claude-haiku-4-5` | $1 / $5 | Dataset generation and cheap practice runs. |

**API rules differ by model.** Fable 5.1, Opus 5.5 and Sonnet 5.5 reject assistant prefill, forced `tool_choice` (`any` or a specific tool), and `budget_tokens` thinking. Opus 5.5 and Fable 5.1 also reject `temperature`, and Sonnet 5.5 only accepts its default value. **Haiku 4.5 follows the older rules and accepts all of these.** Use structured outputs and `tool_choice: auto` so your code works on every model.

Exercise 3's traps were checked with Opus 5.5. Other models make different mistakes, so your v1 vs. v2 comparison will differ if you change `MODEL`.

Rough spend with the default models, assuming the dataset sizes given, and about 10 runs per exercise while you debug:

| Exercise | One full run | While learning |
|---|---|---|
| 1. Ticket triage | ~$0.50 | $3–8 |
| 2. Text-to-SQL | ~$0.20 | $1–3 |
| 3. Trust your eval (both prompts × 3 runs, plus the judge) | ~$1.50 | $4–8 |
| 11. RAG | ~$0.60 | $3–6 |
| 12. Tool-use agent (10 tasks) | ~$1.00 | $5–12 |
| 4–10 | No API calls | $0 |
| **Total** | | **about $15–40** |

With every model set to Sonnet 5.5, expect roughly half that. With Fable 5.1 for `MODEL` and `JUDGE_MODEL`, roughly 2.5 times as much.

To keep it down:
- **Develop on 2–3 cases** and run the full set only when the pipeline works.
- **Save outputs to disk** so you can rerun graders and reports without calling the model again.
- **Set a monthly spend limit** in the Anthropic Console. A bug in a loop is the usual way bills jump.

## The eval workflow (exercises 1–3)

The eval track follows the loop from Anthropic Academy's [*A typical eval workflow*](https://academy.claude.com/courses/building-with-the-claude-api/a-typical-eval-workflow) lesson:

1. **Draft a prompt.** Write the prompt under test as a function: `run_prompt(test_case) -> output`.
2. **Build a dataset.** Write it by hand, or have Claude generate it as JSON. Each case is an input plus whatever the grader needs (expected values, criteria).
3. **Run.** Feed every case through the prompt and collect the outputs.
4. **Grade.**
   - *Code graders* are deterministic checks: valid JSON, schema, exact match, "does the SQL execute", and so on.
   - *Model graders* use an LLM judge with a rubric. They return structured output (strengths, weaknesses, reasoning, score).
5. **Score and report.** Compute per-case scores and the average, then look at the failures.
6. **Iterate.** Change the prompt, re-run, and compare v1 with v2.

[`reference/cheatsheet.md`](reference/cheatsheet.md) recaps the course and shows the current API. Read it before exercise 1. It's off-limits during exercise 2.

### ⚠️ API change since the course

The course gets JSON out of Claude by **prefilling** the assistant turn with `` ```json `` and passing `stop_sequences=["```"]`. **On current models (Opus 4.6+, Sonnet 4.6+, all Claude 5 models), prefill returns a 400 error.** Use structured outputs instead (`client.messages.parse(..., output_format=PydanticModel)`). The cheatsheet shows how. Being able to explain this change is a good interview talking point.

## Rules of the game

- Start a timer before timed exercises. When it goes off, stop and record where you got to in `LOG.md`.
- Keep a short running commentary in comments or notes, the way you'd talk through it in an interview.
- After each exercise, answer the **debrief questions** at the bottom of its `PROMPT.md` without looking anything up.

## Adding an exercise

Each exercise is a folder in `exercises/` named `NN-short-name/` and contains:
- `PROMPT.md`: the interview prompt, requirements or deliverables, and debrief questions. No solutions.
- `answers/.gitkeep`: an empty folder where people put their work.
- Any starter files an interviewer would hand you (schemas, sample data, a fake server, a `docker-compose.yml`). Don't commit an answer key. If data has to be generated, either commit only the generated output or say clearly that the generator shouldn't be read.

Then add a row to the right table above. Pull requests with new exercises are welcome.

## License

[MIT](LICENSE)
