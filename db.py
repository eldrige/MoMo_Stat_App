import sqlite3
import json
airtime_data = './airtime_payments.json'

conn = sqlite3.connect('momo_data.db')  # Changed database name for clarity
c = conn.cursor()


def create_table():
    c.execute("""
        CREATE TABLE IF NOT EXISTS airtime_payments (
            date TEXT,
            txid TEXT PRIMARY KEY, 
            payment_amount INTEGER,
            fee INTEGER,
            new_balance INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS incoming_money (
            date TEXT,
            txid TEXT PRIMARY KEY, 
            amount_received INTEGER,
            sender TEXT ,
            new_balance INTEGER
        )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS transfers_to_mobile_numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT,
        amount_transferred INTEGER,
        new_balance INTEGER,
        fee INTEGER,
        recipient TEXT,
        recipient_number TEXT
    )
""")

    conn.commit()


def data_entry(data):

    try:
        c.execute("""
            INSERT INTO airtime_payments (date, txid, payment_amount, fee, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (data['date'], data['txid'], data['payment_amount'], data['fee'], data['new_balance']))
        conn.commit()
        print(f"Data for txid {data['txid']} inserted successfully.")
    except sqlite3.IntegrityError:
        print(f"txid {data['txid']} already exists. Skipping.")


def data_entry_for_incoming_money(data):

    print(data)

    try:
        c.execute("""
            INSERT INTO incoming_money (date, txid, amount_received, sender, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (data['date'], data['txid'], data['amount_received'], data['sender'], data['new_balance']))
        conn.commit()
        print(f"Data for txid {data['txid']} inserted successfully.")
    except sqlite3.IntegrityError:
        print(f"txid {data['txid']} already exists. Skipping.")


def data_entry_for_transfers_to_mobile_numbers(data):
    print(data)

    try:
        c.execute("""
            INSERT INTO transfers_to_mobile_numbers (date, recipient_number, amount_transferred, recipient, new_balance, fee)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data['date'], data['recipient_number'], data['amount_transferred'], data['recipient'], data['new_balance'], data['fee']))

        conn.commit()
        print(
            f"Data for recipient number {data['recipient_number']} inserted successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting data: {e}")


# Main execution
create_table()

# Load JSON data from file (example)
with open('./data/airtime_payments.json', 'r') as f:
    data = json.load(f)
    for record in data:
        data_entry(record)

with open('./data/incoming_money_table.json', 'r') as f:
    data = json.load(f)
    for record in data:
        data_entry_for_incoming_money(record)

with open('./data/transfer_to_mobile_numbers.json', 'r') as f:
    data = json.load(f)
    for record in data:
        data_entry_for_transfers_to_mobile_numbers(record)


c.close()
conn.close()
