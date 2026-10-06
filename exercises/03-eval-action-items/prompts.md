# Prompts under test

Both prompts get the same output schema:

```json
{"action_items": [{"owner": "<name or null>", "task": "<what>", "due": "<date/phrase or null>"}]}
```

Replace `{transcript}` with the meeting transcript. Use the prompt text exactly as written so your results are comparable with other people's.

## v1 (current production prompt)

```
Extract the action items from this meeting transcript.

For each action item, give the owner (the person responsible, or null if
nobody is), the task, and the due date or deadline phrase if one was
mentioned (otherwise null).

<transcript>
{transcript}
</transcript>
```

## v2 (proposed replacement)

```
Extract the action items from this meeting transcript.

Rules:
- Only include explicit commitments with a concrete deliverable. Skip vague
  intentions such as "I'll take a look" or "we should think about".
- Every action item needs a clear owner who is in the meeting. Skip anything
  without one.
- If a task is handed to someone else, list it under the final owner only.
- Don't include decisions, cancelled tasks, or work that's already done.
- For "due", copy the deadline phrase exactly as said (for example "Friday"
  or "end of week"), or null if none was given.

<transcript>
{transcript}
</transcript>
```
