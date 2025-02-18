import sqlite3
from flask import Flask, render_template, jsonify, request, render_template
from helpers import analyze_incoming_money_transactions, analyze__airtime_transactions, get_table_summary
from datetime import datetime

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('momo_data.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/get-airtime-payments')
def get_airtime_payments():
    conn = get_db_connection()
    airtime_payments = conn.execute(
        'SELECT * FROM airtime_payments').fetchall()
    conn.close()
    results = [dict(payment) for payment in airtime_payments]

    return jsonify(results)


@app.route('/get-airtime-payments/stats')
def get_airtime_payments_stats():
    conn = get_db_connection()
    airtime_payments = conn.execute(
        'SELECT * FROM airtime_payments').fetchall()
    conn.close()
    results = [dict(payment) for payment in airtime_payments]

    # return jsonify(results)
    stats = analyze__airtime_transactions(results)
    return jsonify(stats)


@app.route('/get-incoming-money')
def get_incoming_money():
    conn = get_db_connection()
    incoming_money = conn.execute(
        'SELECT * FROM incoming_money').fetchall()
    conn.close()
    results = [dict(money) for money in incoming_money]

    return jsonify(results)


@app.route('/get-incoming-money/stats')
def get_incoming_money_stats():
    conn = get_db_connection()
    incoming_money = conn.execute(
        'SELECT * FROM incoming_money').fetchall()
    conn.close()
    results = [dict(money) for money in incoming_money]
    stats = analyze_incoming_money_transactions(results)

    return jsonify(stats)


@app.route('/get-transfers-to-mobile_numbers')
def get_transfers_to_mobile_numbers():
    conn = get_db_connection()
    transfers = conn.execute(
        'SELECT * FROM transfers_to_mobile_numbers').fetchall()
    conn.close()
    results = [dict(money) for money in transfers]

    return jsonify(results)


@app.route('/get-payment-to-code-holders')
def get_payments_to_code_holders():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM payment_to_code_holders').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/get-bank-transfers')
def get_bank_transfers():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM bank_transfers').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/get-internet-voice-bundles')
def get_internet_voice_bundles():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM internet_voice_bundles').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/get-cash-power-bill-payments')
def get_cash_power_bill_payments():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM cash_power_bill_payments').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/get-txns-from-third-parties')
def get_trantnxs_from_third_parties():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM transactions_initiated_by_third_parties').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/get-withdrawals-from-agents')
def get_withdrawals_from_agents():
    conn = get_db_connection()
    withdrawals = conn.execute(
        'SELECT * FROM withdrawals_from_agents').fetchall()
    conn.close()
    results = [dict(payment) for payment in withdrawals]

    return jsonify(results)


@app.route('/get-stats')
def get_momo_stats():
    conn = get_db_connection()
    incoming_money = conn.execute(
        'SELECT * FROM incoming_money').fetchall()
    conn.close()
    results = [dict(money) for money in incoming_money]
    stats = analyze_incoming_money_transactions(results)

    return jsonify(stats)


@app.route('/')
def dashboard():
    conn = get_db_connection()
    tables = [
        "airtime_payments",
        "incoming_money",
        "transfers_to_mobile_numbers",
        "payment_to_code_holders",
        "bank_transfers",
        "internet_voice_bundles",
        "cash_power_bill_payments",
        "transactions_initiated_by_third_parties",
        "withdrawals_from_agents"
    ]


    db_summary =  [get_table_summary(table) for table in tables]
    for table in tables:
        summary = get_table_summary(table)
        print(summary)

    return render_template('index.html', transactions=transactions)


@app.route('/airtime')
def airtime():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM airtime_payments').fetchall()
    return render_template('airtime.html', transactions=transactions)


@app.route('/bank-transfers')
def bankTransfers():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM bank_transfers').fetchall()
    return render_template('bank-transfers.html', transactions=transactions)

@app.route('/cash-power')
def cashPower():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM cash_power_bill_payments').fetchall()
    return render_template('cash-power-bill.html', transactions=transactions)


@app.route('/incoming-money')
def incomingMoney():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM incoming_money').fetchall()
    return render_template('incoming-money.html', transactions=transactions)


@app.route('/internet-voice')
def internetBundles():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM internet_voice_bundles').fetchall()
    return render_template('internet-voice-bundles.html', transactions=transactions)

@app.route('/code-holders')
def codeHolders():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM payment_to_code_holders').fetchall()
    return render_template('code-holders.html', transactions=transactions)


@app.route('/third-parties')
def thirdParties():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM transactions_initiated_by_third_parties').fetchall()
    return render_template('third-party.html', transactions=transactions)

@app.route('/transfers-to-mobile')
def mobileTransfers():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM transfers_to_mobile_numbers').fetchall()
    return render_template('transfers-to-mobile.html', transactions=transactions)

@app.route('/agent-withdrawals')
def agentWithdrawals():
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM withdrawals_from_agents').fetchall()
    return render_template('agent-withdrawal.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
