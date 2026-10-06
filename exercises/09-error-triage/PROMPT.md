# Exercise 9: Triage an Error Export

**Skills:** grouping, aggregation, streaming, prioritization.

## The interview prompt

> Here's a large export of error events from our error tracker (think Sentry). Group them into issues by a normalized signature, rank the issues by frequency and by number of affected users, and output the top issues with a sample event for each.
>
> Watch memory: stream the file instead of loading it all.

## Setup

Generate the export. It isn't committed because it's large:

```bash
cd exercises/09-error-triage
python generate_events.py                  # 400,000 events, about 190 MB
python generate_events.py --events 50000   # smaller file while you develop
```

Don't read `generate_events.py` beyond its usage line. It defines the answer.

## Input

`events.jsonl` has one event per line, with fields such as `event_id`, `timestamp`, `level`, `service`, `release`, `user_id` (sometimes null), `exception` (`type`, `message`), `stacktrace` (a list of `file`/`function`/`line` frames), and `request`.

## Deliverables
1. **A script that streams `events.jsonl`** without loading it all into memory, and builds issue groups from a **normalized signature**. You decide what goes into the signature and what gets stripped out.
2. **Two rankings of the top 10 issues:** one by event count and one by unique affected users. Each entry shows the signature, both counts, the first-seen and last-seen times, and one sample event.
3. **Explain the normalization.** List what you strip or replace and why, and show at least one place where your first attempt grouped too much or too little.
4. **Memory evidence.** Show that peak memory stays flat as the file grows, for example with `tracemalloc` or by comparing the 50k and 400k runs.

## Rules
- No pandas `read_json` on the whole file. Process it line by line.
- Lines can be malformed. Don't crash; count them and report how many.

## Debrief questions
- What's in your signature? What did you deliberately leave out?
- Where do the two rankings disagree, and which would you show an on-call engineer first?
- Which per-issue state did you keep in memory? How would it grow with 100× more events, and with 100× more distinct users?
- How would you run this continuously on a live stream instead of a file?
