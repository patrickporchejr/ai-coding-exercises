# Exercise 7: Join and Deduplicate Two Sources

**Skills:** fuzzy matching, conflict rules, flagging uncertainty instead of guessing.

## The interview prompt

> We have two lists of healthcare providers. `credentialing.csv` comes from our credentialing team. `claims_directory.csv` comes from a claims system. They describe many of the same people, but with different spellings, missing IDs, and conflicting fields.
>
> Produce one merged provider list. Match records across the two files, pick a winner for each conflicting field using a rule you state, and list the matches you're unsure about.

## What you're working with
- **`credentialing.csv`**: one name column (`full_name`), sometimes with titles. Address split into parts. `last_verified` date.
- **`claims_directory.csv`**: separate first and last names. One combined address string. `updated_at` date.
- **Both** have `npi` (a 10-digit national provider ID), but it's sometimes missing, and it may not always be right.

## Deliverables
1. **A Python script** that writes `merged_providers.csv`, with one row per real-world provider and a column recording which source records it came from.
2. **Field-level conflict rules**, written down. For example: which phone wins, which specialty wins, and whether "newer" always beats "verified".
3. **An uncertain-matches report** listing each pair you're not confident about, why, and what evidence would settle it. Don't silently merge or silently split these.
4. **Unmatched records** from each side, listed separately.

## Rules
- Don't hard-code matches by row. Your matching logic should work on a new file with different people.
- A wrong merge (two different people combined) is worse than a missed merge. Design for that.

## Debrief questions
- What signals did you match on, and how did you weigh them? Which signal did you trust least?
- Find a case where NPIs match but you'd still be suspicious, or where they differ but you think it's the same person.
- How would your approach change for 2 million records per side?
- How would you turn your "unsure" list into something a human reviewer could clear quickly?
