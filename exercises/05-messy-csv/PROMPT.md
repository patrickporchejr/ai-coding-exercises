# Exercise 5: Clean a Messy CSV

**Skills:** parsing, normalization, edge cases, explaining choices.

## Two phases

1. **Learn** ([`learn/LEARN.md`](learn/LEARN.md)): the Python and pandas you need for this exercise, with drills on a separate practice file. Untimed. Skip it if you already wrangle data in Python.
2. **Mock interview** ([`mock/MOCK.md`](mock/MOCK.md)): this prompt, 60 minutes, no AI, with Claude playing the interviewer.

Don't open `orders_raw.csv` until Phase 2.

## The interview prompt

> `orders_raw.csv` is an export of customer orders. It has mixed date formats, inconsistent casing, stray whitespace, missing values, duplicate rows, and numbers stored as text with currency symbols.
>
> Normalize everything, report what you dropped or fixed and why, and write the cleaned file.

## Deliverables
1. **A Python script** that reads `orders_raw.csv` and writes `orders_clean.csv`.
2. **A report**, printed or written to a file, listing every row you dropped and every value you fixed, each with a reason.
3. **Your choices, stated out loud.** Many rows in this file have more than one defensible answer. Say which one you picked and why.

## Rules
- Don't edit `orders_raw.csv` by hand. All fixes happen in code.
- Don't silently guess. If a value is ambiguous, either flag it in the report or make an explicit rule and apply it consistently.

## Debrief questions
- Which rows were ambiguous rather than simply wrong? How did you decide?
- What counts as a duplicate here? Did you treat exact copies and near-copies the same way?
- What would you do differently if this file had 10 million rows?
- If this ran every night on new exports, how would you know when a new kind of mess showed up?
