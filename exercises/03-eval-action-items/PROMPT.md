# Exercise 3: Meeting Action Items (Timed, With AI)

**Mode:** ⏱ **60 minutes.** Any AI tool is allowed (Claude Code, Claude.ai, Copilot).
**The catch:** with AI available, the bar is higher. An interviewer will expect a more complete and more rigorous eval, and will ask you to defend every piece the AI wrote.

## The interview prompt

> Our product extracts action items from meeting transcripts. For each transcript the prompt returns:
>
> ```json
> {"action_items": [{"owner": "<name or null>", "task": "<what>", "due": "<date/phrase or null>"}]}
> ```
>
> Build an eval for it. Use whatever tools you like. At the end I want to know how good the current prompt is, where it fails, and whether your proposed v2 is actually better.

## Requirements (all expected within the hour)
1. **Dataset**: 20+ synthetic transcripts with gold `action_items`. Include no action items at all, implicit commitments ("I'll take a look"), reassigned tasks, an owner who is mentioned but not present, and relative due dates.
2. **Code graders**: schema validity, item **count** match, and **owner** precision/recall against gold (decide how to match names).
3. **Model grader**: does each extracted `task` semantically match a gold item? Judge per item, not per transcript, and use structured output.
4. **Judge validation**: hand-label 10 judge decisions yourself and report the agreement rate. Don't just trust the AI-written judge.
5. **v1 vs v2**: run both prompts on the same dataset and show a side-by-side table with per-metric deltas.
6. **Concurrency and robustness**: parallel calls, retries or error capture, and results saved to disk.

## Stretch
- Run each case 3× and report variance. Is the v1→v2 delta bigger than the noise?
- Rough cost estimate per eval run using `response.usage`.

## Debrief questions
- Which parts did AI get wrong or subtly wrong? How did you catch them?
- Your judge agreed with you 7/10 times. Is that good enough? What would you change?
- Is v2 actually better, or within noise? How do you know?
- Compare with exercise 2: what did AI change about *how* you worked, not just speed?
