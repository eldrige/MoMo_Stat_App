from flask import Flask, render_template
import json
import re
from datetime import datetime

app = Flask(__name__)

@app.template_filter()
def format_currency(value):
    """Format numbers with commas and RWF symbol."""
    return f"{value:,} RWF"

def parse_transactions():
    """Read transactions from JSON files and categorize them."""
    
    # Load transactions
    with open("transactions.json", "r") as f:
        momo_transactions = json.load(f)["transactions"]

    with open("airtime_payment.json", "r") as f:
        airtime_transactions = json.load(f)["transactions"]

    transactions = []

    # Process MoMo transactions
    for tx in momo_transactions:
        message = tx["message"]
        date = datetime.fromtimestamp(int(tx["date"]) / 1000).strftime("%Y-%m-%d %H:%M:%S")

        # Match Cash Power payments
        match = re.search(r"Your payment of (\d+) RWF to MTN Cash Power.*Your new balance: (\d+) RWF", message)
        if match:
            transactions.append({
                "date": date.split(" ")[0],
                "time": date.split(" ")[1],
                "balance": int(match.group(2)),
                "id": "N/A",
                "amount": int(match.group(1)),
                "type": "Cash Power"
            })
            continue  # Skip further checks for this transaction

        # Match other transactions
        match = re.search(r"Your new balance: (\d+) RWF", message)
        if match:
            transactions.append({
                "date": date.split(" ")[0],
                "time": date.split(" ")[1],
                "balance": int(match.group(1)),
                "id": "N/A",
                "amount": 0,  # Default to 0 if we can't extract an amount
                "type": "Transaction"
            })

    # Process Airtime transactions
    for tx in airtime_transactions:
        message = tx["message"]
        date = datetime.fromtimestamp(int(tx["date"]) / 1000).strftime("%Y-%m-%d %H:%M:%S")

        match = re.search(r"Your payment of (\d+) RWF for Airtime.*Your new balance: (\d+) RWF", message)
        if match:
            transactions.append({
                "date": date.split(" ")[0],
                "time": date.split(" ")[1],
                "balance": int(match.group(2)),
                "id": "N/A",
                "amount": int(match.group(1)),
                "type": "Airtime"
            })

    return transactions

@app.route('/dashboard')
def dashboard():
    transactions = parse_transactions()
    return render_template('dashboard.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
