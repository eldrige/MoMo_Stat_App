import sqlite3

def insert_data(table: str, data: dict):
    """Inserts a transaction record into the appropriate table."""
    conn = sqlite3.connect('transactions.db')
    cur = conn.cursor()

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cur.execute(sql, tuple(data.values()))

    conn.commit()
    conn.close()

# Example usage
sample_bundle = {'date': '2024-02-09', 'time': '10:30', 'new_balance': '5000', 'transaction_id': '123456', 'amount': 2000}
insert_data('internet_voice_bundle', sample_bundle)

sample_cash_power = {'date': '2024-02-09', 'time': '11:00', 'new_balance': '4500', 'transaction_id': '654321', 'amount': 5000, 'token': '987654'}
insert_data('cash_power_bill_payments', sample_cash_power)
