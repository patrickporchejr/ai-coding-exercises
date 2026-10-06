"""Generate events.jsonl, a large error-event export for exercise 9.

    python generate_events.py                  # 400,000 events (about 190 MB)
    python generate_events.py --events 50000   # smaller file while you develop

Don't read the rest of this file before you've finished the exercise: it
defines the underlying issues, which is what you're supposed to discover.
"""

import argparse
import json
import random
import uuid
from datetime import datetime, timedelta, timezone

RELEASES = ["web@1.4.2", "web@1.4.3", "web@1.5.0"]


def rid(rng):
    return rng.randint(1000, 999999)


ISSUES = [
    # (weight, service, exc_type, message_fn, frames, user_mode)
    (30, "api", "TimeoutError", lambda r: f"Request to payments-svc timed out after {r.randint(3000, 30000)}ms",
     [("app/clients/payments.py", "charge", 88), ("app/routes/checkout.py", "submit_order", 142)], "many"),
    (22, "api", "KeyError", lambda r: "'user_id'",
     [("app/auth/session.py", "current_user", 57), ("app/routes/profile.py", "get_profile", 23)], "many"),
    (6, "api", "KeyError", lambda r: "'user_id'",
     [("app/jobs/digest.py", "build_digest", 111), ("app/jobs/runner.py", "run", 40)], "anon"),
    (40, "worker", "ConnectionResetError", lambda r: f"[Errno 104] Connection reset by peer (conn id 0x{r.getrandbits(48):012x})",
     [("site-packages/redis/connection.py", "read_response", 812), ("app/cache/store.py", "get", 31)], "bot"),
    (18, "api", "ValueError", lambda r: f"invalid literal for int() with base 10: '{r.choice(['abc', 'null', '12a', ' ', 'NaN'])}'",
     [("app/routes/orders.py", "list_orders", 64)], "many"),
    (15, "web", "TypeError", lambda r: "Cannot read properties of undefined (reading 'price')",
     [("static/js/cart.js", "renderLineItem", 210), ("static/js/cart.js", "renderCart", 180)], "many"),
    (12, "api", "IntegrityError", lambda r: f"duplicate key value violates unique constraint \"orders_pkey\" DETAIL: Key (id)=({rid(r)}) already exists.",
     [("site-packages/sqlalchemy/engine/base.py", "_execute_context", 1910), ("app/models/order.py", "save", 77)], "many"),
    (9, "api", "PermissionError", lambda r: f"User {uuid.UUID(int=r.getrandbits(128))} is not allowed to access workspace {rid(r)}",
     [("app/auth/permissions.py", "require", 45), ("app/routes/workspace.py", "open_workspace", 88)], "many"),
    (8, "worker", "FileNotFoundError", lambda r: f"[Errno 2] No such file or directory: '/tmp/exports/{uuid.UUID(int=r.getrandbits(128))}.csv'",
     [("app/jobs/export.py", "upload_export", 133)], "many"),
    (7, "api", "ValidationError", lambda r: f"email: value is not a valid email address: '{r.choice(['bob@', 'x@y', 'anna.example.com'])}{rid(r)}'",
     [("app/schemas/user.py", "validate_email", 19), ("app/routes/signup.py", "signup", 51)], "many"),
    (5, "web", "ChunkLoadError", lambda r: f"Loading chunk {r.randint(100, 999)} failed. (timeout: https://cdn.example.com/static/js/{r.randint(100, 999)}.{r.getrandbits(32):08x}.chunk.js)",
     [("static/js/runtime.js", "requireEnsure", 72)], "many"),
    (4, "worker", "MemoryError", lambda r: "",
     [("app/jobs/report.py", "build_report", 205), ("app/jobs/runner.py", "run", 40)], "few"),
    (3, "api", "ZeroDivisionError", lambda r: "division by zero",
     [("app/analytics/metrics.py", "conversion_rate", 28)], "many"),
    (2, "api", "RecursionError", lambda r: "maximum recursion depth exceeded while calling a Python object",
     [("app/utils/tree.py", "walk", 14)], "few"),
    (2, "web", "TypeError", lambda r: "Cannot read properties of null (reading 'addEventListener')",
     [("static/js/nav.js", "initMenu", 33)], "many"),
    (1, "api", "SSLError", lambda r: f"HTTPSConnectionPool(host='hooks.partner{r.randint(1, 9)}.com', port=443): certificate verify failed",
     [("site-packages/requests/adapters.py", "send", 517), ("app/webhooks/deliver.py", "deliver", 66)], "many"),
]

LINE_SHIFT = {"web@1.4.2": 0, "web@1.4.3": 3, "web@1.5.0": 11}


def make_users(rng):
    many = [f"u_{rng.randint(100000, 999999)}" for _ in range(8000)]
    few = many[:5]
    bot = "u_000042"
    return many, few, bot


def pick_user(rng, mode, users):
    many, few, bot = users
    if mode == "bot":
        return bot if rng.random() < 0.97 else rng.choice(many)
    if mode == "anon":
        return None
    if mode == "few":
        return rng.choice(few)
    return rng.choice(many) if rng.random() > 0.08 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=int, default=400_000)
    parser.add_argument("--seed", type=int, default=9)
    parser.add_argument("--out", default="events.jsonl")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    users = make_users(rng)
    weights = [w for w, *_ in ISSUES]
    start = datetime(2026, 9, 1, tzinfo=timezone.utc)

    with open(args.out, "w") as f:
        for i in range(args.events):
            _, service, exc_type, msg_fn, frames, user_mode = rng.choices(ISSUES, weights)[0]
            release = rng.choice(RELEASES)
            shift = LINE_SHIFT[release]
            stack = [
                {"file": fname, "function": fn, "line": line + (0 if fname.startswith("site-packages") else shift)}
                for fname, fn, line in frames
            ]
            event = {
                "event_id": uuid.UUID(int=rng.getrandbits(128)).hex,
                "timestamp": (start + timedelta(seconds=rng.randint(0, 30 * 86400))).isoformat(),
                "level": "error" if rng.random() > 0.05 else "fatal",
                "service": service,
                "release": release,
                "user_id": pick_user(rng, user_mode, users),
                "exception": {"type": exc_type, "message": msg_fn(rng)},
                "stacktrace": stack,
                "request": {"method": rng.choice(["GET", "POST"]), "path": f"/api/{rng.choice(['orders', 'users', 'carts'])}/{rid(rng)}"},
            }
            line = json.dumps(event)
            if rng.random() < 0.00005:
                line = line[: rng.randint(10, len(line) - 10)]
            f.write(line + "\n")

    print(f"Wrote {args.events:,} events to {args.out}")


if __name__ == "__main__":
    main()
