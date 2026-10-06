# Exercise 12: Tool-Use Agent

**Skills:** tool definitions, the agent loop, tool errors, guarding write actions, and evaluating an agent by the end state it leaves behind.
**Time box:** 90 minutes. **Needs:** an Anthropic API key.

## The interview prompt

> We want a support agent for Tidepool (the product from exercise 11) that can actually take actions: look up customers, check invoices, issue refunds within policy, change plans, and escalate to a human.
>
> `backend.py` is our support backend. Wire it up to Claude as tools, write the agent loop yourself, and show me how reliably it handles the 10 scenarios in `tasks.jsonl`.

## Input
- **`backend.py`**: the backend's API. You may read it. Its public functions are your tools: `lookup_customer`, `list_invoices`, `get_policy`, `issue_refund`, `change_plan`, `create_ticket`. Call `backend.reset()` before each task and `backend.snapshot()` afterwards to see what changed. "Today" is `backend.TODAY`.
- **`tasks.jsonl`**: 10 scenarios, each with a `user_message`, the `expected` end state (refunds, plan changes, tickets) and `notes` explaining the intended behavior.

## Requirements
1. **Write the tool definitions yourself**: a name, a description, and a JSON schema for each function. Tool descriptions are prompts; write them as if they were.
2. **Write the agent loop by hand.** Call the API, run any requested tools, send the results back, and repeat until Claude is done. Don't use the SDK's tool runner for this version. Set a maximum number of turns.
3. **Handle tool failures.** When a backend function raises, return the error to Claude as a tool result instead of crashing. One task includes a transient failure.
4. **Guard write actions.** `issue_refund` and `change_plan` move money or change accounts. Put an approval hook in front of them that a human could use. For the eval run, auto-approve but log every approval.
5. **Evaluate by end state.** For each task, compare `backend.snapshot()` to `expected`: the right refunds with the exact amounts, the right plan changes and the right tickets, and *nothing extra*. Also check the final reply where `reply_contains` is given.
6. **Report** a pass/fail per task, the overall pass rate, and the number of tool calls per task. For each failure, read the transcript and say what went wrong.

## Stretch
- Run each task 3 times. Which tasks are flaky?
- Add a model grader for the final reply: is it accurate, polite, and does it explain any refusal?
- Rebuild it with the SDK's tool runner and compare the amount of code and the control you keep.

## Things that commonly trip people up
- **Forced tool use isn't available on current models.** Setting `tool_choice` to `{"type": "any"}` or to a specific tool returns a 400 on Opus 5.5, Sonnet 5.5 and Fable 5.1 (Haiku 4.5 still allows it). Use `auto` and say in the prompt what you expect.
- **Pass back everything.** When you send Claude's turn back in the next request, include the full response content, not just the text. Leave earlier turns unedited.
- **Parallel calls.** Claude can request several tools in one turn. Their results go back together in a single message.

## Debrief questions
- Why grade an agent on end state rather than on the exact sequence of tool calls? When does the sequence still matter?
- Where should policy live: in the system prompt, in a `get_policy` tool, or enforced in the backend? What did the refund amount task teach you?
- How does your approval hook behave when a human rejects an action? What does Claude see?
- The agent passes 9 of 10 tasks. Is it ready to ship? What would you need to see first?
- How would you stop a user message from talking the agent out of its policy (task t08)? Is a prompt enough?
