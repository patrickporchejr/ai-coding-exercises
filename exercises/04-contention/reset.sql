-- Put the tables back to the starting state between problems.
TRUNCATE bids RESTART IDENTITY;
DELETE FROM auctions;
INSERT INTO auctions VALUES (1, 100, 0);
