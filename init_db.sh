#!/bin/bash

DB_PATH="./data/database.db"

if ! command -v sqlite3 &> /dev/null; then
    echo "Error: sqlite3 is not installed. Please install it first."
    exit 1
fi

# Вставляем три записи
sqlite3 "$DB_PATH" <<EOF
BEGIN TRANSACTION;

INSERT INTO subscriptions (id, name, price, limit_queries)
VALUES
    (1, 'Бесплатная', 0, 20),
    (2, 'Standard', 390, 50),
    (3, 'Premium', 790, -1);

COMMIT;
EOF

if [ $? -eq 0 ]; then
    echo "Successfully inserted 3 records into subscriptions table"
else
    echo "Error occurred while inserting records"
    exit 1
fi