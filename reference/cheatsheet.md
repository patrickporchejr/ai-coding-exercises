# Eval Cheatsheet (use during exercises 1 and 3, NOT exercise 2)

## Course recap: the minimal shape

```
dataset.json  ->  run_prompt(case)  ->  output
                                      ├─ code_grader(case, output)  -> 0..10
                                      └─ model_grader(case, output) -> 0..10
                  score = mean(code, model) per case; report avg + worst cases
```

The functions the course builds, in order:

- `generate_dataset()` asks Claude for N test cases as JSON and saves them to `dataset.json`
- `run_prompt(test_case)` is the prompt under test
- `grade_by_model(test_case, output)` is the LLM judge and returns `{strengths, weaknesses, reasoning, score}`
- `grade_syntax(output, test_case)` / code graders are deterministic checks
- `run_test_case(test_case)` runs the prompt, grades it, and returns `{output, test_case, score, reasoning}`
- `run_eval(dataset)` maps over the dataset and prints the average score

## Current API: basic call

```python
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-opus-5-5"            # prompt under test and LLM judges
DATASET_MODEL = "claude-haiku-4-5"   # generating test datasets (cheap; you review the cases anyway)

def chat(prompt: str, system: str | None = None, model: str = MODEL) -> str:
    kwargs = {"system": system} if system else {}
    resp = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    return next(b.text for b in resp.content if b.type == "text")
```

## Changes since the course was recorded

| Course pattern | Current models | Do this instead |
|---|---|---|
| Prefill `{"role": "assistant", "content": "```json"}` + `stop_sequences=["```"]` | **400 error** | Structured outputs, shown below |
| `temperature=0` for a deterministic judge | **400 error** on Opus 5.5 (sampling params removed) | Drop it. Use a tight rubric and structured output, and run each case a few times if you need to measure variance |
| `thinking={"type": "enabled", "budget_tokens": N}` | 400 | `output_config={"effort": "low" \| "medium" \| "high"}`. Opus 5.5 defaults to `medium` |

"Current models" means Opus and Sonnet 4.6 and later, and all Claude 5 models. **Haiku 4.5 follows the older rules**: it still accepts prefill, `temperature`, and `budget_tokens`. Use structured outputs with both models anyway, so the same code works whichever model you call.

## Structured outputs (replaces prefill)

```python
from pydantic import BaseModel, Field

class Grade(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    reasoning: str
    score: int = Field(description="1-10")

resp = client.messages.parse(
    model=MODEL,
    max_tokens=4000,
    messages=[{"role": "user", "content": judge_prompt}],
    output_format=Grade,
)
grade: Grade = resp.parsed_output
```

The same pattern generates the dataset, with `model=DATASET_MODEL`. Define `class TestCase(BaseModel)` and `class Dataset(BaseModel): cases: list[TestCase]`, then parse into `Dataset`.

## Model-grader prompt skeleton

```
You are an expert evaluator. Grade the OUTPUT for the TASK.

<task>{task}</task>
<criteria>{solution_criteria}</criteria>
<output>{output}</output>

Score 1-10. 10 = meets every criterion with no issues. 1 = fails the task.
Be strict: list concrete weaknesses before choosing a score.
```

Tips:
- Give the judge **criteria per test case** (store `solution_criteria` in the dataset), not just a generic "is it good".
- Ask for reasoning *before* the score. The schema field order matters.
- A judge tends to cluster around 7–8. An explicit rubric with anchors (what a 3, 6, or 9 looks like) spreads the scores out.

## Running cases concurrently (optional)

```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(run_test_case, dataset))
```

## Reporting

At minimum, print the average score, a pass rate (for example score >= 7), and the 3 worst cases with the judge's reasoning. Save results to `results/<timestamp>.json` so you can diff v1 against v2.
