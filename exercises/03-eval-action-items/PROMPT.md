# Exercise 3: Trust Your Eval (Meeting Action Items)

**Mode:** ⏱ **60 minutes.** Any AI tool is allowed.
**Focus:** this exercise isn't about building a pipeline quickly; AI makes that easy. It's about the questions a senior engineer gets asked once the pipeline exists: *can you trust the judge?* and *is the new prompt actually better, or is that noise?*

## The interview prompt

> Our product extracts action items from meeting transcripts. The current prompt is v1. A teammate wrote v2 and says it's better.
>
> I've given you the test set and both prompts. Tell me whether we should ship v2, and convince me your numbers are trustworthy.

## Provided (you don't build these)
- **`transcripts.jsonl`**: 12 meeting transcripts, each with `gold_action_items` (a list of `owner`, `task`, `due`).
- **`prompts.md`**: the v1 and v2 prompts and the output schema. Use them exactly as written.
- These were checked with Claude Opus 5.5, so run both prompts on Opus 5.5. Other models make different mistakes, and the comparison would change.

## Requirements

### Setup: keep it quick and let AI help
1. Run a prompt on a transcript with structured output, following the schema in `prompts.md`.
2. Build a **judge** that decides, for each extracted item, whether it matches a gold item. Use structured output. Judge each item individually, not whole transcripts at once.
3. From the judge's decisions, compute **precision** (how many extracted items are real) and **recall** (how many gold items were found) for each transcript, then overall.

### Core 1: check the judge
4. **Hand-label at least 20 of the judge's match decisions yourself**, without looking at what the judge said. Mix clear matches, clear non-matches, and borderline cases.
5. Report **how often you and the judge agree** (percent agreement and Cohen's kappa) and **describe the pattern of disagreements**. Is the judge too lenient, too strict, or confused by one kind of case?
6. **Fix the judge once**, then re-measure agreement. Did the change help, or did it just move the errors around?

### Core 2: decide whether v2 beats v1
7. Run **v1 and v2 on all 12 transcripts, 3 times each**.
8. Report precision and recall for both, with the **spread across runs**, not just the average.
9. **Compare them transcript by transcript.** Which transcripts got better and which got worse? Read the outputs and explain *why*, in terms of the v2 rules.
10. **Make the call:** ship v2, ship it with changes, or keep v1. Justify it with your numbers *and* their limits: 12 transcripts and 3 runs isn't much.

## Debrief questions
- Your judge agreed with you 80% of the time. Is that good enough to use? What would you need to see first?
- If you had only run each prompt once, would you have reached the same conclusion?
- v2 improved precision but hurt recall (or the reverse). How do you decide which matters more for this product?
- Which of v2's rules actually changed the output, and which had no effect? What does that tell you about how v2 was written, and about how to write v3?
- Which parts did AI write for you, and what did you have to correct?
- With twice the time, what would you add first: more transcripts, more runs, or a better judge? Why?
