import sqlite3

def create_tables():
    """Creates SQLite tables based on TABLE_SCHEMA."""
    conn = sqlite3.connect('transactions.db')
    cur = conn.cursor()

    table_queries = {
        'internet_voice_bundle': """CREATE TABLE IF NOT EXISTS internet_voice_bundle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            new_balance TEXT,
            transaction_id TEXT,
            amount INTEGER
        )""",
        'cash_power_bill_payments': """CREATE TABLE IF NOT EXISTS cash_power_bill_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            new_balance TEXT,
            transaction_id TEXT,
            amount INTEGER,
            token TEXT
        )""",
    }

    for query in table_queries.values():
        cur.execute(query)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")
