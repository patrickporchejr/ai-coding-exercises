CREATE TABLE auctions (id INT PRIMARY KEY, max_bid INT, version INT DEFAULT 0);
CREATE TABLE bids (id SERIAL PRIMARY KEY, auction_id INT, amount INT, status TEXT);
INSERT INTO auctions VALUES (1, 100, 0);
