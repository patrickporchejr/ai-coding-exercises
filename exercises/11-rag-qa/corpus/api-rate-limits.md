---
title: API rate limits
last_updated: 2026-02-14
---
# API rate limits

API access is available on the Team and Business plans.

Limits apply per API token:

| Plan | Requests per minute |
|------|---------------------|
| Team | 100 |
| Business | 600 |

When you go over the limit, the API returns **HTTP 429** with a `Retry-After` header giving the number of seconds to wait.

List endpoints are paginated with a `cursor` parameter. Each response includes `next_cursor`, which is null on the last page. Page size defaults to 50 and can go up to 200.
