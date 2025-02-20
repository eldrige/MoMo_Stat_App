import sqlite3
import json
from collections import defaultdict
from datetime import datetime


def analyze_incoming_money_transactions(data):
    total_transactions = len(data)
    total_amount_received = sum(item['amount_received'] for item in data)
    final_balance = data[-1]['new_balance'] if data else None

    # Convert date strings to datetime objects and find the earliest and latest transaction dates
    dates = [datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S")
             for item in data]
    earliest_date = min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None
    latest_date = max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None

    # Identify unique senders and count transactions per sender
    senders = {}
    for item in data:
        sender = item['sender']
        if sender in senders:
            senders[sender] += 1
        else:
            senders[sender] = 1

    # Find the largest transactions
    largest_transactions = sorted(data, key=lambda x: x['amount_received'], reverse=True)[
        :5]  # Top 5 transactions

    # Monthly transaction breakdown
    monthly_transactions = defaultdict(int)
    for item in data:
        date = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S")
        month_year = date.strftime("%Y-%m")
        monthly_transactions[month_year] += item['amount_received']

    # Prepare results
    results = {
        'Total Transactions': total_transactions,
        'Total Amount Received': total_amount_received,
        'Final Balance': final_balance,
        'Earliest Transaction Date': earliest_date,
        'Latest Transaction Date': latest_date,
        'Transactions Per Sender': senders,
        'Largest Transactions': largest_transactions,
        'Monthly Transaction Breakdown': monthly_transactions
    }

    return results


def analyze__airtime_transactions(data):
    total_transactions = len(data)
    total_payment_amounts = sum(item['payment_amount'] for item in data)
    final_balance = data[-1]['new_balance'] if data else None

    # Convert date strings to datetime objects and find the earliest and latest transaction dates
    dates = [datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
             for item in data]
    earliest_date = min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None
    latest_date = max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None

    # Prepare results
    results = {
        'Total Transactions': total_transactions,
        'Total Payment Amounts': total_payment_amounts,
        'Final Balance': final_balance,
        'Earliest Transaction Date': earliest_date,
        'Latest Transaction Date': latest_date
    }

    return results


# Connect to the database

def get_db_connection():
    conn = sqlite3.connect("momo_data.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Function to get transaction summary for a table


def get_table_summary(table_name):
    query = f"""
    SELECT 
        COUNT(*) AS num_transactions, 
        SUM(amount) AS total_amount, 
        MIN(date) AS first_transaction_date, 
        MAX(date) AS last_transaction_date 
    FROM {table_name}
    """
    conn = get_db_connection()
    cursor = conn.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {
        "table": table_name,
        "num_transactions": result["num_transactions"],
        "total_amount": result["total_amount"],
        "first_transaction_date": result["first_transaction_date"],
        "last_transaction_date": result["last_transaction_date"]
    }


# List of tables in your database
