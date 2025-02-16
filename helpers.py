from collections import defaultdict
from datetime import datetime


def process_transactions(transactions):
    stats = {
        "total_transactions": len(transactions),
        "total_amount_received": 0,
        "first_transaction_date": None,
        "last_transaction_date": None,
        "sender_breakdown": defaultdict(int),
        "largest_transaction": {"amount": 0, "sender": None, "date": None},
        "smallest_transaction": {"amount": float("inf"), "sender": None, "date": None},
        "monthly_breakdown": defaultdict(int)
    }

    for txn in transactions:
        date_obj = datetime.strptime(txn["date"], "%Y-%m-%d")
        amount = txn["amount"]
        sender = txn["sender"]

        # Update totals
        stats["total_amount_received"] += amount
        stats["sender_breakdown"][sender] += amount
        stats["monthly_breakdown"][date_obj.strftime("%Y-%m")] += amount

        # Update first and last transaction dates
        if not stats["first_transaction_date"] or date_obj < stats["first_transaction_date"]:
            stats["first_transaction_date"] = date_obj
        if not stats["last_transaction_date"] or date_obj > stats["last_transaction_date"]:
            stats["last_transaction_date"] = date_obj

        # Update largest transaction
        if amount > stats["largest_transaction"]["amount"]:
            stats["largest_transaction"] = {
                "amount": amount, "sender": sender, "date": date_obj}

        # Update smallest transaction
        if amount < stats["smallest_transaction"]["amount"]:
            stats["smallest_transaction"] = {
                "amount": amount, "sender": sender, "date": date_obj}

    # Convert date objects to strings for output
    stats["first_transaction_date"] = stats["first_transaction_date"].strftime(
        "%Y-%m-%d")
    stats["last_transaction_date"] = stats["last_transaction_date"].strftime(
        "%Y-%m-%d")
    stats["largest_transaction"]["date"] = stats["largest_transaction"]["date"].strftime(
        "%Y-%m-%d")
    stats["smallest_transaction"]["date"] = stats["smallest_transaction"]["date"].strftime(
        "%Y-%m-%d")

    return stats
