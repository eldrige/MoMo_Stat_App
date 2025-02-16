import sqlite3
from flask import Flask, render_template, jsonify, request
from helpers import process_transactions

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('momo_data.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/airtime-payments')
def get_airtime_payments():
    conn = get_db_connection()
    airtime_payments = conn.execute(
        'SELECT * FROM airtime_payments').fetchall()
    conn.close()
    results = [dict(payment) for payment in airtime_payments]

    return jsonify(results)


@app.route('/incoming-money')
def get_incoming_money():
    conn = get_db_connection()
    incoming_money = conn.execute(
        'SELECT * FROM incoming_money').fetchall()
    conn.close()
    results = [dict(money) for money in incoming_money]

    return jsonify(results)


@app.route('/transfers-to-mobile_numbers')
def get_transfers_to_mobile_numbers():
    conn = get_db_connection()
    transfers = conn.execute(
        'SELECT * FROM transfers_to_mobile_numbers').fetchall()
    conn.close()
    results = [dict(money) for money in transfers]

    return jsonify(results)


@app.route('/payment-to-code-holders')
def get_payments_to_code_holders():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM payment_to_code_holders').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/bank-transfers')
def get_bank_transfers():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM bank_transfers').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/internet-voice-bundles')
def get_internet_voice_bundles():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM internet_voice_bundles').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/cash-power-bill-payments')
def get_cash_power_bill_payments():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM cash_power_bill_payments').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/txns-from-third-parties')
def get_trantnxs_from_third_parties():
    conn = get_db_connection()
    payments = conn.execute(
        'SELECT * FROM transactions_initiated_by_third_parties').fetchall()
    conn.close()
    results = [dict(payment) for payment in payments]

    return jsonify(results)


@app.route('/withdrawals-from-agents')
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
    stats = process_transactions(results)

    return jsonify(stats)

    # conn = get_db_connection()
    # withdrawals = conn.execute(
    #     'SELECT * FROM withdrawals_from_agents').fetchall()
    # conn.close()
    # results = [dict(payment) for payment in withdrawals]

    # return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
