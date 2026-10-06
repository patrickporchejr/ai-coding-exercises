-- Small shop database for the text-to-SQL eval.
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    country TEXT NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'shipped', 'delivered', 'refunded'))
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers VALUES
 (1, 'Ana Souza',     'ana@example.com',    'BR', '2025-01-14'),
 (2, 'Ben Carter',    'ben@example.com',    'US', '2025-02-03'),
 (3, 'Chloe Martin',  'chloe@example.com',  'FR', '2025-03-22'),
 (4, 'Dev Patel',     'dev@example.com',    'IN', '2025-04-09'),
 (5, 'Emma Schultz',  'emma@example.com',   'DE', '2025-06-30'),
 (6, 'Felix Wong',    'felix@example.com',  'US', '2025-08-11'),
 (7, 'Grace Kim',     'grace@example.com',  'KR', '2025-11-02'),
 (8, 'Hugo Rossi',    'hugo@example.com',   'IT', '2026-01-19');

INSERT INTO products VALUES
 (1, 'Trail Running Shoes', 'footwear',    12900),
 (2, 'Wool Socks (3-pack)', 'apparel',      2400),
 (3, 'Rain Shell Jacket',   'apparel',     18900),
 (4, 'Hydration Vest',      'gear',         9900),
 (5, 'Headlamp',            'gear',         4500),
 (6, 'Recovery Sandals',    'footwear',     6500),
 (7, 'Energy Gels (12)',    'nutrition',    3000);

INSERT INTO orders VALUES
 (101, 1, '2025-02-01', 'delivered'),
 (102, 2, '2025-02-15', 'delivered'),
 (103, 2, '2025-05-20', 'refunded'),
 (104, 3, '2025-06-01', 'delivered'),
 (105, 4, '2025-07-12', 'shipped'),
 (106, 1, '2025-09-03', 'delivered'),
 (107, 5, '2025-10-10', 'delivered'),
 (108, 6, '2025-12-24', 'delivered'),
 (109, 2, '2026-01-05', 'shipped'),
 (110, 7, '2026-02-14', 'pending'),
 (111, 6, '2026-03-01', 'delivered'),
 (112, 3, '2026-03-18', 'refunded');

INSERT INTO order_items VALUES
 (101, 1, 1), (101, 2, 2),
 (102, 3, 1),
 (103, 4, 1),
 (104, 1, 1), (104, 7, 3),
 (105, 5, 2),
 (106, 6, 1), (106, 2, 1),
 (107, 3, 1), (107, 4, 1),
 (108, 1, 2),
 (109, 7, 5), (109, 5, 1),
 (110, 2, 3),
 (111, 4, 1), (111, 6, 1),
 (112, 3, 1);
