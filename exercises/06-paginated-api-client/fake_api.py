"""Fake paginated API for exercise 6. Uses only the standard library.

Run it in its own terminal:
    python fake_api.py                  # normal mode
    python fake_api.py --fail-page 7    # page 7 always returns 403 (a permanent error)

See PROMPT.md for the API contract. Don't read the rest of this file before
you've finished: treat the server as a black box, as you would in an interview.
"""

import argparse
import json
import random
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TOKEN = "test-token"
PAGE_SIZE = 25
TOTAL_RECORDS = 487
OVERLAP = 2
RATE_LIMIT = 5  # requests per rolling second
P_429 = 0.10
P_500 = 0.12


def build_records(seed):
    rng = random.Random(seed)
    first = ["Ana", "Ben", "Chloe", "Dev", "Emma", "Felix", "Grace", "Hugo", "Iris", "Jon"]
    last = ["Souza", "Carter", "Martin", "Patel", "Schultz", "Wong", "Kim", "Rossi", "Okafor", "Lund"]
    records = []
    for i in range(1, TOTAL_RECORDS + 1):
        name = f"{rng.choice(first)} {rng.choice(last)}"
        records.append({
            "id": f"rec_{i:05d}",
            "name": name,
            "email": f"{name.lower().replace(' ', '.')}{i}@example.com",
            "score": rng.randint(0, 100),
        })
    return records


class State:
    def __init__(self, seed, fail_page):
        self.records = build_records(seed)
        self.fail_page = fail_page
        self.rng = random.Random(seed + 1)
        self.lock = threading.Lock()
        self.recent = deque()
        self.stats = {"requests": 0, "200": 0, "401": 0, "403": 0, "404": 0,
                      "400": 0, "429_random": 0, "429_rate_limit": 0, "500": 0}

    @property
    def total_pages(self):
        return -(-TOTAL_RECORDS // PAGE_SIZE)

    def page(self, n):
        # Each page after the first repeats the last OVERLAP records of the
        # previous page, the way a live dataset shifts under pagination.
        start = max(0, (n - 1) * PAGE_SIZE - (OVERLAP if n > 1 else 0))
        end = min(TOTAL_RECORDS, n * PAGE_SIZE)
        return self.records[start:end]


def make_handler(state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def send_json(self, status, body, headers=None):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/stats":
                with state.lock:
                    return self.send_json(200, dict(state.stats))

            with state.lock:
                state.stats["requests"] += 1

            if url.path != "/records":
                return self.send_json(404, {"error": "not_found"})

            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                with state.lock:
                    state.stats["401"] += 1
                return self.send_json(401, {"error": "unauthorized"})

            try:
                n = int(parse_qs(url.query).get("page", ["1"])[0])
                if n < 1:
                    raise ValueError
            except ValueError:
                with state.lock:
                    state.stats["400"] += 1
                return self.send_json(400, {"error": "invalid_page"})

            now = time.monotonic()
            with state.lock:
                while state.recent and now - state.recent[0] > 1.0:
                    state.recent.popleft()
                state.recent.append(now)
                over_limit = len(state.recent) > RATE_LIMIT
                roll = state.rng.random()
                latency = state.rng.uniform(0.05, 0.3)
                if over_limit:
                    state.stats["429_rate_limit"] += 1
                elif n == state.fail_page:
                    state.stats["403"] += 1
                elif n > state.total_pages:
                    state.stats["404"] += 1
                elif roll < P_429:
                    state.stats["429_random"] += 1
                elif roll < P_429 + P_500:
                    state.stats["500"] += 1
                else:
                    state.stats["200"] += 1

            time.sleep(latency)

            if over_limit:
                return self.send_json(429, {"error": "rate_limited"}, {"Retry-After": "1"})
            if n == state.fail_page:
                return self.send_json(403, {"error": "forbidden"})
            if n > state.total_pages:
                return self.send_json(404, {"error": "page_out_of_range"})
            if roll < P_429:
                # Some 429s carry Retry-After and some don't.
                headers = {"Retry-After": "2"} if roll < P_429 / 2 else {}
                return self.send_json(429, {"error": "too_many_requests"}, headers)
            if roll < P_429 + P_500:
                return self.send_json(500, {"error": "internal_error"})

            return self.send_json(200, {
                "page": n,
                "total_pages": state.total_pages,
                "page_size": PAGE_SIZE,
                "records": state.page(n),
            })

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--fail-page", type=int, default=None)
    args = parser.parse_args()

    state = State(args.seed, args.fail_page)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(state))
    print(f"Fake API on http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
