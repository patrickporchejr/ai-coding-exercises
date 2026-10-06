# Exercise 8: Parse and Validate LLM Output

**Skills:** structured outputs, validation, failure handling. This is very close to real AI engineering work.

## The interview prompt

> We asked a model to analyze 50 product reviews and return JSON. The responses are in `responses.jsonl`. They *should* all be JSON, but some include markdown fences, trailing commas, wrong types, missing fields, or extra text.
>
> Extract and validate each response against the schema. Route failures to a retry list with the reason, and report the pass rate.

## Input

`responses.jsonl` has one object per line: `{"id": "resp_001", "raw": "<exactly what the model returned>"}`.

## Target schema

```json
{
  "sentiment": "positive" | "negative" | "neutral",
  "rating": 1-5 (integer),
  "topics": ["<string>", ...],
  "summary": "<non-empty string>"
}
```

## Deliverables
1. **`valid.jsonl`**: the responses that passed, parsed into clean objects.
2. **`retry.jsonl`**: the failures, each with its `id`, the original `raw` text, and a specific, machine-readable **reason**. "Invalid JSON" isn't specific enough.
3. **A report**: the overall pass rate, plus a count of failures by reason.
4. **Your repair policy, stated out loud.** Decide which problems you fix automatically (stripping a fence?) and which you send back for retry (a rating of 8?). Be ready to defend where you drew the line.

## Rules
- Don't hand-edit `responses.jsonl`.
- Use a real schema library (Pydantic or `jsonschema`) for validation rather than a pile of `if` statements, and explain why.

## Debrief questions
- Which repairs are safe, and which change the meaning of the output? Where's the line?
- Your pass rate is 70%. How do you get it to 99% upstream so you don't have to repair downstream?
- What would you put in the retry prompt to make the second attempt succeed?
- How do structured outputs (constrained decoding) change this problem? What failures do they *not* prevent?
