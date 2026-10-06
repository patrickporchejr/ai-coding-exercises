# Exercise 6: Paginated API Client with Retries

**Skills:** reliability, async, error handling.

## The interview prompt

> We pull records from a partner API. It's paginated, it's flaky (it sometimes returns 429 or 500), and it rate-limits us. Write a client that fetches every record, retries sensibly, stops on errors that will never succeed, and fetches pages concurrently with `asyncio`. Return all records with no duplicates.

## Setup

Start the fake API in its own terminal and leave it running:

```bash
cd exercises/06-paginated-api-client
python fake_api.py
```

Treat `fake_api.py` as a black box, as you would a real partner API. Work from the contract below, not from its source.

## API contract (what the partner's docs tell you)

- `GET http://127.0.0.1:8765/records?page=N`. Pages start at 1.
- Requires the header `Authorization: Bearer test-token`.
- A successful response looks like this:
  ```json
  {"page": 1, "total_pages": 20, "page_size": 25, "records": [{"id": "rec_00001", "name": "...", "email": "...", "score": 42}]}
  ```
- **429** means slow down. It may include a `Retry-After` header (in seconds).
- **500** means a transient server error.
- **4xx other than 429** means a permanent error. Retrying won't help.
- Rate limit: a few requests per second. The docs don't say exactly how many.
- `GET /stats` shows what the server has seen: request counts, 429s and 500s. It isn't rate-limited and needs no auth.

## Requirements
1. **Fetch all pages concurrently** with `asyncio`. You'll need an async HTTP client; `httpx` is a common choice (`pip install httpx`).
2. **Retry 429s and 500s with exponential backoff**, with a cap on both the delay and the number of attempts. Respect `Retry-After` when it's present.
3. **Stop on permanent errors.** Test this by restarting the server with `python fake_api.py --fail-page 7`. Decide what "stop" means: fail the whole run, or skip that page and report it. Be ready to defend the choice.
4. **Return every record exactly once.** Verify it rather than assuming it.
5. **Stay polite.** Limit concurrency so you're not just retrying your way past the rate limit. Check `/stats` before and after a run.

## Debrief questions
- Why add jitter to backoff? What happens with 20 concurrent clients and no jitter?
- How did you decide on the concurrency limit? How would you tune it against a real API?
- Where could duplicates come from besides the overlap you found?
- Your run takes 40 seconds. Where does the time go, and what would you change?
- How would you make the client resumable if the process crashed halfway through?
