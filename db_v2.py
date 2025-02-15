import sqlite3
import json
from typing import Dict, Any


class DatabaseManager:
    def __init__(self, db_name="momo_data.db"):
        self.db_name = db_name

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query that does not return results."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def insert_data(self, table: str, data: Dict[str, Any]):
        """Insert data into a given table dynamically."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.execute_query(query, tuple(data.values()))
            print(f"Data for {table} inserted successfully: {data}")
        except sqlite3.IntegrityError as e:
            print(f"Skipping duplicate entry for {table}: {data}. Error: {e}")


def create_tables(db: DatabaseManager):
    """Creates all necessary tables."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS airtime_payments (
            date TEXT,
            txid TEXT PRIMARY KEY, 
            payment_amount INTEGER,
            fee INTEGER,
            new_balance INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS incoming_money (
            date TEXT,
            txid TEXT PRIMARY KEY, 
            amount_received INTEGER,
            sender TEXT,
            new_balance INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS transfers_to_mobile_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT,
            amount_transferred INTEGER,
            new_balance INTEGER,
            fee INTEGER,
            recipient TEXT,
            recipient_number TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cash_power_bill_payments (
            transaction_id TEXT PRIMARY KEY, 
            date TEXT,
            payment_amount INTEGER,
            new_balance INTEGER,
            fee INTEGER,
            token TEXT,
            provider TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS withdrawals_from_agents (
            transaction_id TEXT PRIMARY KEY, 
            date TEXT,
            name TEXT,
            agent_name TEXT,
            agent_number TEXT,
            account TEXT,
            amount INTEGER,
            new_balance INTEGER,
            fee INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS internet_voice_bundles (
            transaction_id TEXT PRIMARY KEY, 
            date TEXT,
            amount INTEGER,
            new_balance INTEGER,
            service TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS payment_to_code_holders (
            transaction_id TEXT PRIMARY KEY, 
            date TEXT,
            amount INTEGER,
            new_balance INTEGER,
            recipient TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bank_transfers (
            transaction_id TEXT PRIMARY KEY, 
            date TEXT,
            amount INTEGER,
            recipient_name TEXT,
            recipient_phone TEXT,
            sender_account TEXT
        )
        """
    ]

    for query in queries:
        db.execute_query(query)
    print("Tables created successfully.")


def load_and_insert_data(db: DatabaseManager, table: str, file_path: str):
    """Loads JSON data and inserts it into the specified table."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

            for record in data:
                db.insert_data(table, record)

    except FileNotFoundError:
        print(f"File not found: {file_path}. Skipping {table}.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}. Skipping {table}.")


def main():
    db = DatabaseManager()

    # Step 1: Create tables
    create_tables(db)

    # Step 2: Define table-to-file mappings
    table_file_mapping = {
        "airtime_payments": "./data/airtime_payments.json",
        "incoming_money": "./data/incoming_money_table.json",
        "transfers_to_mobile_numbers": "./data/transfer_to_mobile_numbers.json",
        "cash_power_bill_payments": "./data/cash_power_bill_payments.json",
        "withdrawals_from_agents": "./data/withdrawals_from_agents.json",
        "internet_voice_bundles": "./data/internet_voice_bundles.json",
        "payment_to_code_holders": "./data/payment_to_code_holders.json",
        "bank_transfers": "./data/bank_transfers.json",
    }

    # Step 3: Load data for each table
    for table, file_path in table_file_mapping.items():
        load_and_insert_data(db, table, file_path)


if __name__ == "__main__":
    main()
