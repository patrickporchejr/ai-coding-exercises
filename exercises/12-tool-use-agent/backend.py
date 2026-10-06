"""Fake Tidepool support backend for exercise 12.

Import it from your agent:

    import backend
    backend.reset()                      # fresh state before each task
    backend.lookup_customer("ana@example.com")
    backend.snapshot()                   # current state, for grading

Every public function below is something your agent can call as a tool.
Functions raise backend.NotFound, backend.InvalidRequest, or
backend.TransientError on failure. You write the tool definitions (names,
descriptions, JSON schemas) yourself; that's part of the exercise.

You may read this file. It's the API you're integrating with.
"""

import copy
from datetime import date

TODAY = date(2026, 10, 5)


class NotFound(Exception):
    pass


class InvalidRequest(Exception):
    pass


class TransientError(Exception):
    """A temporary failure. The same call may succeed if retried."""


POLICIES = {
    "refunds": (
        "Monthly plans are not refundable. "
        "Annual plans can be refunded within 30 days of the invoice date. "
        "The refund is prorated: invoice amount x unused days / 365, rounded down to the cent. "
        "Days used = days between the invoice date and today. "
        "Exception: a duplicate charge (two identical invoices for the same period) is always refunded in full, on any plan. "
        "Never refund more than the invoice amount, and never refund an invoice twice."
    ),
    "plan_changes": (
        "Plans: free, team, business. Upgrades take effect immediately. "
        "Downgrades take effect at the end of the current billing period. "
        "Only change a plan when the customer explicitly asks for it."
    ),
    "security": (
        "Possible account compromise (unrecognized logins, changed recovery details) must be escalated "
        "to the security team with a ticket at priority 'urgent'. Do not make account changes yourself."
    ),
    "escalation": (
        "Create a ticket when a request needs a human: security concerns, legal or data requests, "
        "or anything the available tools can't resolve. Priorities: low, medium, high, urgent."
    ),
}

_INITIAL = {
    "customers": {
        "cus_ana": {"customer_id": "cus_ana", "email": "ana@example.com", "name": "Ana Souza", "plan": "team", "billing_cycle": "annual", "seats": 10},
        "cus_ben": {"customer_id": "cus_ben", "email": "ben@example.com", "name": "Ben Carter", "plan": "team", "billing_cycle": "monthly", "seats": 10},
        "cus_chloe": {"customer_id": "cus_chloe", "email": "chloe@example.com", "name": "Chloe Martin", "plan": "business", "billing_cycle": "annual", "seats": 25},
        "cus_dev": {"customer_id": "cus_dev", "email": "dev@example.com", "name": "Dev Patel", "plan": "team", "billing_cycle": "monthly", "seats": 6},
        "cus_emma": {"customer_id": "cus_emma", "email": "emma@example.com", "name": "Emma Schultz", "plan": "team", "billing_cycle": "monthly", "seats": 4},
        "cus_felix": {"customer_id": "cus_felix", "email": "felix@example.com", "name": "Felix Wong", "plan": "business", "billing_cycle": "monthly", "seats": 3},
        "cus_grace": {"customer_id": "cus_grace", "email": "grace@example.com", "name": "Grace Kim", "plan": "team", "billing_cycle": "monthly", "seats": 12},
    },
    "invoices": {
        "INV-1001": {"invoice_id": "INV-1001", "customer_id": "cus_ana", "date": "2026-09-20", "period": "2026-09-20 to 2027-09-19", "amount_cents": 76800, "refunded_cents": 0},
        "INV-1000": {"invoice_id": "INV-1000", "customer_id": "cus_ana", "date": "2025-09-20", "period": "2025-09-20 to 2026-09-19", "amount_cents": 76800, "refunded_cents": 0},
        "INV-2001": {"invoice_id": "INV-2001", "customer_id": "cus_ben", "date": "2026-09-15", "period": "2026-09", "amount_cents": 8000, "refunded_cents": 0},
        "INV-2000": {"invoice_id": "INV-2000", "customer_id": "cus_ben", "date": "2026-08-15", "period": "2026-08", "amount_cents": 8000, "refunded_cents": 0},
        "INV-3001": {"invoice_id": "INV-3001", "customer_id": "cus_chloe", "date": "2026-07-01", "period": "2026-07-01 to 2027-06-30", "amount_cents": 360000, "refunded_cents": 0},
        "INV-4001": {"invoice_id": "INV-4001", "customer_id": "cus_dev", "date": "2026-09-28", "period": "2026-10", "amount_cents": 4800, "refunded_cents": 0},
        "INV-5001": {"invoice_id": "INV-5001", "customer_id": "cus_emma", "date": "2026-10-01", "period": "2026-10", "amount_cents": 3200, "refunded_cents": 0},
        "INV-5002": {"invoice_id": "INV-5002", "customer_id": "cus_emma", "date": "2026-10-01", "period": "2026-10", "amount_cents": 3200, "refunded_cents": 0},
        "INV-6001": {"invoice_id": "INV-6001", "customer_id": "cus_felix", "date": "2026-09-30", "period": "2026-10", "amount_cents": 4500, "refunded_cents": 0},
        "INV-6000": {"invoice_id": "INV-6000", "customer_id": "cus_felix", "date": "2026-08-30", "period": "2026-09", "amount_cents": 4500, "refunded_cents": 0},
        "INV-7001": {"invoice_id": "INV-7001", "customer_id": "cus_grace", "date": "2026-09-22", "period": "2026-09", "amount_cents": 9600, "refunded_cents": 0},
    },
    "refunds": [],
    "plan_changes": [],
    "tickets": [],
}

_state = {}
_calls = []
_flaky_remaining = {}


def reset():
    """Restore the initial data and clear the call log. Call before each task."""
    global _state, _calls, _flaky_remaining
    _state = copy.deepcopy(_INITIAL)
    _calls = []
    _flaky_remaining = {("list_invoices", "cus_felix"): 1}


def snapshot():
    """Return a copy of the current state plus the log of tool calls, for grading."""
    return {**copy.deepcopy(_state), "calls": list(_calls)}


def _log(name, **kwargs):
    _calls.append({"tool": name, "args": kwargs})


def _maybe_flaky(name, key):
    if _flaky_remaining.get((name, key), 0) > 0:
        _flaky_remaining[(name, key)] -= 1
        raise TransientError(f"{name} timed out. Try again.")


# ---- Tools -----------------------------------------------------------------

def lookup_customer(email: str) -> dict:
    """Find a customer by email. Returns the customer record."""
    _log("lookup_customer", email=email)
    for c in _state["customers"].values():
        if c["email"].lower() == email.strip().lower():
            return dict(c)
    raise NotFound(f"No customer with email {email!r}.")


def list_invoices(customer_id: str) -> list:
    """List a customer's invoices, newest first."""
    _log("list_invoices", customer_id=customer_id)
    if customer_id not in _state["customers"]:
        raise NotFound(f"No customer {customer_id!r}.")
    _maybe_flaky("list_invoices", customer_id)
    rows = [dict(i) for i in _state["invoices"].values() if i["customer_id"] == customer_id]
    return sorted(rows, key=lambda i: i["date"], reverse=True)


def get_policy(topic: str) -> str:
    """Return the support policy text for a topic: refunds, plan_changes, security, or escalation."""
    _log("get_policy", topic=topic)
    if topic not in POLICIES:
        raise NotFound(f"No policy {topic!r}. Topics: {', '.join(POLICIES)}.")
    return POLICIES[topic]


def issue_refund(invoice_id: str, amount_cents: int, reason: str) -> dict:
    """Refund part or all of an invoice. WRITE ACTION: moves money."""
    _log("issue_refund", invoice_id=invoice_id, amount_cents=amount_cents, reason=reason)
    inv = _state["invoices"].get(invoice_id)
    if inv is None:
        raise NotFound(f"No invoice {invoice_id!r}.")
    if not isinstance(amount_cents, int) or amount_cents <= 0:
        raise InvalidRequest("amount_cents must be a positive integer.")
    if inv["refunded_cents"] > 0:
        raise InvalidRequest(f"{invoice_id} has already been refunded.")
    if amount_cents > inv["amount_cents"]:
        raise InvalidRequest(f"Refund exceeds invoice amount ({inv['amount_cents']} cents).")
    inv["refunded_cents"] = amount_cents
    record = {"refund_id": f"re_{len(_state['refunds']) + 1:03d}", "invoice_id": invoice_id,
              "amount_cents": amount_cents, "reason": reason}
    _state["refunds"].append(record)
    return dict(record)


def change_plan(customer_id: str, new_plan: str) -> dict:
    """Change a customer's plan to free, team, or business. WRITE ACTION."""
    _log("change_plan", customer_id=customer_id, new_plan=new_plan)
    c = _state["customers"].get(customer_id)
    if c is None:
        raise NotFound(f"No customer {customer_id!r}.")
    order = ["free", "team", "business"]
    if new_plan not in order:
        raise InvalidRequest(f"Unknown plan {new_plan!r}. Plans: {', '.join(order)}.")
    if new_plan == c["plan"]:
        raise InvalidRequest(f"Customer is already on {new_plan}.")
    upgrade = order.index(new_plan) > order.index(c["plan"])
    record = {"customer_id": customer_id, "from": c["plan"], "to": new_plan,
              "effective": "immediately" if upgrade else "end_of_period"}
    if upgrade:
        c["plan"] = new_plan
    _state["plan_changes"].append(record)
    return dict(record)


def create_ticket(customer_id: str, summary: str, priority: str) -> dict:
    """Escalate to a human by creating a support ticket. Priority: low, medium, high, or urgent."""
    _log("create_ticket", customer_id=customer_id, summary=summary, priority=priority)
    if customer_id not in _state["customers"]:
        raise NotFound(f"No customer {customer_id!r}.")
    if priority not in ("low", "medium", "high", "urgent"):
        raise InvalidRequest("priority must be low, medium, high, or urgent.")
    record = {"ticket_id": f"T-{len(_state['tickets']) + 1:03d}", "customer_id": customer_id,
              "summary": summary, "priority": priority}
    _state["tickets"].append(record)
    return dict(record)


reset()
