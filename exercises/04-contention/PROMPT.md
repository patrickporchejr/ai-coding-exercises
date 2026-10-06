# Exercise 4: Contention (Auction Bids)

**Mode:** hands-on in Postgres. Open **two terminal sessions (A and B)** and interleave them by hand. Doing the interleaving yourself is what makes it stick.

## Setup

```bash
cd exercises/04-contention
docker compose up -d                 # starts Postgres and creates the tables
```

Open two terminals and connect to the database from each one (one is A, the other is B):

```bash
docker exec -it contention-db psql -U postgres -d auction
```

Reset to the starting state between problems (from either session):

```sql
\i /reset.sql
```

To start over completely: `docker compose down -v && docker compose up -d`.

Starting schema (already loaded by `init.sql`):

```sql
CREATE TABLE auctions (id INT PRIMARY KEY, max_bid INT, version INT DEFAULT 0);
CREATE TABLE bids (id SERIAL PRIMARY KEY, auction_id INT, amount INT, status TEXT);
INSERT INTO auctions VALUES (1, 100, 0);
```

## Problems

### 1. Reproduce the race (no protection)
Both sessions `BEGIN`, read `max_bid`, insert a bid (A: 150, B: 120), then update `max_bid` to their own amount. Commit A, then B. What's `max_bid` at the end? Why is that wrong?

### 2. Row locking
Redo #1, but start each transaction with `SELECT max_bid FROM auctions WHERE id = 1 FOR UPDATE;`. Run A's `SELECT ... FOR UPDATE` first, then B's. What does B do? What does B see after A commits?

### 3. Write the row-locking transaction
Write the full transaction for placing a bid: lock, read, insert the bid row, update `max_bid` only if the new bid is higher. Write it from memory, then check it.

### 4. OCC with a conditional update
No `FOR UPDATE` this time. Write the update as:

```sql
UPDATE auctions SET max_bid = 150 WHERE id = 1 AND max_bid = 100;
```

Run it in A and B (B with 120) after both have read 100. Check rows affected. Which session gets 0 rows, and what does your app code do with that?

### 5. OCC with a version column
Same as #4, but use `WHERE id = 1 AND version = 0` and `SET version = version + 1`. Why might you use a version column instead of comparing `max_bid`?

### 6. SERIALIZABLE
Run #1 again, but start both with `BEGIN ISOLATION LEVEL SERIALIZABLE;`. Commit A, then B. What error does B get (look for SQLSTATE `40001`)? Write pseudocode for a retry loop around it.

### 7. Deadlock
Add a second auction row. In A, lock row 1 then row 2. In B, lock row 2 then row 1, interleaved. What happens, and how would you prevent it?

## Interview-style questions to answer out loud
- Which approach do you pick for a hot auction with 1,000 bidders at once, and which for a rarely contested row? Why?
- What's the cost of OCC under high contention?
- What does row locking cost you in throughput?

## Teardown

```bash
docker compose down -v
```
