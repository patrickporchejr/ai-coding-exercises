# Phase 2: Mock interview

**Goal:** do [the real exercise](../PROMPT.md) the way you'd do it in the room: timed, thinking out loud, with an interviewer who asks questions and pushes back.

**Mode:** **60 minutes, no AI help on the code.** Official docs only: the [Python docs](https://docs.python.org/3/) and the [pandas docs](https://pandas.pydata.org/docs/). Claude plays the interviewer, not your pair programmer.

**Do Phase 1 first** ([`../learn/LEARN.md`](../learn/LEARN.md)) unless you already know pandas.

> ⚠️ **Don't open `interviewer.md`.** It's the interviewer's script and lists every trap in the data.

## How to run it

1. Start a fresh Claude Code session in this repo (so it has no memory of your practice).
2. Say: **"Run the messy-csv mock interview. Read `exercises/05-messy-csv/mock/interviewer.md` and be my interviewer."**
3. Work in `../answers/mock/`. Keep that terminal or editor separate from the Claude session. Paste code or output into the chat only when you want to show the interviewer something, like you'd share your screen.
4. Talk as you go. Type your thinking into the chat in short lines: what you see, what you're about to do, what you decided and why. That's what is being scored, as much as the code.

## How the hour runs

| Time | What happens |
|---|---|
| 0–5 min | The interviewer gives you the prompt. Look at the data and **ask clarifying questions**. |
| 5–40 min | Build. The interviewer stays quiet unless you ask something, and checks in around 20 and 35 min. |
| 40–50 min | Walk through your output and report. Expect pushback on specific rows. |
| 50–60 min | Follow-up questions: scale, running it nightly, what you'd do with more time. |

If time runs out, stop. Leaving the code unfinished is normal. Being able to explain what you have and what's left counts.

## After the mock

The interviewer gives you a scored debrief using the rubric in `interviewer.md`. Then:
- Now you may open `interviewer.md` and compare its trap list with what you caught.
- Answer the debrief questions at the bottom of [`../PROMPT.md`](../PROMPT.md) in `LOG.md`.
- Wait a few days and redo the mock with a stricter time box (45 min) if you want a second rep.
