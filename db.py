import sqlite3
import json

DATABASE_NAME = 'momo_data.db'


def create_connection(db_name):
    """Creates and returns a database connection."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def create_table(conn, table_creation_sql):
    """Creates a table in the database.

    Args:
        conn: The database connection object.
        table_creation_sql: SQL query to create the table.
    """
    try:
        c = conn.cursor()
        c.execute(table_creation_sql)
        conn.commit()
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


def insert_data(conn, table_name, data, column_names):
    """Inserts data into the specified table.

    Args:
        conn: The database connection object.
        table_name: The name of the table to insert data into.
        data: A dictionary containing the data to insert.
        column_names: A tuple of column names for the table.
    """
    placeholders = ', '.join(['?'] * len(column_names)
                             )  # dynamically create placeholders
    columns = ', '.join(column_names)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        c = conn.cursor()
        # Use data.get() for safer access
        c.execute(sql, [data.get(col) for col in column_names])
        conn.commit()
        # flexible id
        print(
            f"Data inserted successfully into {table_name} with id {data.get('txid') or data.get('transaction_id')}")
    except sqlite3.IntegrityError:
        print(
            f"Record with  id {data.get('txid') or data.get('transaction_id')} already exists in {table_name}. Skipping.")
    except sqlite3.Error as e:
        print(f"Error inserting data into {table_name}: {e}")


def load_and_insert_data(conn, table_name, json_file_path, column_names):
    """Loads data from a JSON file and inserts it into the database.

    Args:
        conn: The database connection object.
        table_name: The name of the table to insert data into.
        json_file_path: The path to the JSON file containing the data.
        column_names: A tuple of column names for the table.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            for record in data:
                insert_data(conn, table_name, record, column_names)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {json_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """Main function to create tables and load data."""

    table_schemas = {
        'airtime_payments': {
            'sql': """
                CREATE TABLE IF NOT EXISTS airtime_payments (
                    date TEXT,
                    txid TEXT PRIMARY KEY, 
                    payment_amount INTEGER,
                    fee INTEGER,
                    new_balance INTEGER
                )
            """,
            'columns': ('date', 'txid', 'payment_amount', 'fee', 'new_balance')
        },
        'incoming_money': {
            'sql': """
                CREATE TABLE IF NOT EXISTS incoming_money (
                    date TEXT,
                    txid TEXT PRIMARY KEY, 
                    amount_received INTEGER,
                    sender TEXT ,
                    new_balance INTEGER
                )
            """,
            'columns': ('date', 'txid', 'amount_received', 'sender', 'new_balance')
        },
        'transfers_to_mobile_numbers': {
            'sql': """
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
            'columns': ('date', 'recipient_number', 'amount_transferred', 'recipient', 'new_balance', 'fee')
        },
        'cash_power_bill_payments': {
            'sql': """
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
            'columns': ('transaction_id', 'date', 'payment_amount', 'new_balance', 'fee', 'token', 'provider')
        },
        'withdrawals_from_agents': {
            'sql': """
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
            'columns': ('transaction_id', 'date', 'name', 'agent_name', 'agent_number', 'account', 'amount', 'new_balance', 'fee')
        },
        'internet_voice_bundles': {
            'sql': """
                CREATE TABLE IF NOT EXISTS internet_voice_bundles (
                    transaction_id TEXT PRIMARY KEY, 
                    date TEXT,
                    amount INTEGER,
                    new_balance INTEGER,
                    service TEXT
                )
            """,
            'columns': ('transaction_id', 'date', 'amount', 'new_balance', 'service')
        },
        'payment_to_code_holders': {
            'sql': """
                CREATE TABLE IF NOT EXISTS payment_to_code_holders (
                    transaction_id TEXT PRIMARY KEY, 
                    date TEXT,
                    amount INTEGER,
                    new_balance INTEGER,
                    recipient TEXT
                )
            """,
            'columns': ('transaction_id', 'date', 'amount', 'new_balance', 'recipient')
        },
        'bank_transfers': {
            'sql': """
                CREATE TABLE IF NOT EXISTS bank_transfers (
                    transaction_id TEXT PRIMARY KEY, 
                    date TEXT,
                    amount INTEGER,
                    recipient_name TEXT,
                    recipient_phone TEXT,
                    sender_account TEXT
                )
            """,
            'columns': ('transaction_id', 'date', 'amount', 'recipient_name', 'recipient_phone', 'sender_account')
        },
        'transactions_initiated_by_third_parties': {
            'sql': """
                CREATE TABLE IF NOT EXISTS transactions_initiated_by_third_parties (
                    transaction_id TEXT PRIMARY KEY, 
                    external_transaction_id TEXT,
                    date TEXT,
                    amount INTEGER,
                    sender TEXT,
                    fee INTEGER,
                    new_balance INTEGER
                )
            """,
            'columns': ('transaction_id', 'external_transaction_id', 'date', 'amount', 'sender', 'fee', 'new_balance')
        },
    }

    data_files = {
        'airtime_payments': './data/airtime_payments.json',
        'incoming_money': './data/incoming_money_table.json',
        'transfers_to_mobile_numbers': './data/transfer_to_mobile_numbers.json',
        'cash_power_bill_payments': './data/cash_power_bill_payments.json',
        'withdrawals_from_agents': './data/withdrawals_from_agents.json',
        'internet_voice_bundles': './data/internet_voice_bundles.json',
        'payment_to_code_holders': './data/payment_to_code_holders.json',
        'bank_transfers': './data/bank_transfers.json',
        'transactions_initiated_by_third_parties': './data/transactions_initiated_by_third_parties.json',
    }

    with create_connection(DATABASE_NAME) as conn:
        for table_name, schema in table_schemas.items():
            create_table(conn, schema['sql'])
            load_and_insert_data(
                conn, table_name, data_files[table_name], schema['columns'])

    print("Data loading complete.")


if __name__ == "__main__":
    main()
