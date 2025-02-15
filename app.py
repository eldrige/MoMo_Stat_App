from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# Initialize Flask app and SQLite connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///momo_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the message categories models
class AirtimePayments(db.Model):
    __tablename__ = 'airtime_payments'

    txid = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    new_balance = db.Column(db.Integer)

    def serialize(self):
        return {
            'txid': self.txid,
            'date': self.date,
            'payment_amount': self.payment_amount,
            'fee': self.fee,
            'new_balance': self.new_balance
        }


class IncomingMoney(db.Model):
    txid = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    amount_received = db.Column(db.Integer)
    sender = db.Column(db.String)
    new_balance = db.Column(db.Integer)


class TransfersToMobileNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    amount_transferred = db.Column(db.Integer)
    new_balance = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    recipient = db.Column(db.String)
    recipient_number = db.Column(db.String)


# Create all tables (only once)
with app.app_context():
    airtime_payments = AirtimePayments.query.all()
    db.create_all()


@app.route('/airtime_payments', methods=['GET', 'POST'])
def manage_airtime_payments():
    if request.method == 'GET':
        try:
            airtime_payments = AirtimePayments.query.all()
            if airtime_payments:
                return jsonify([payment.serialize() for payment in airtime_payments]), 200
            else:
                return jsonify({"message": "No data found"}), 404
        except Exception as e:
            return jsonify({"message": f"Error fetching data: {str(e)}"}), 500

    if request.method == 'POST':
        data = request.get_json()
        new_entry = AirtimePayments(
            txid=data['txid'],
            date=data['date'],
            payment_amount=data['payment_amount'],
            fee=data['fee'],
            new_balance=data['new_balance']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Airtime payment added successfully!"}), 201


@app.route('/incoming_money', methods=['GET', 'POST'])
def manage_incoming_money():
    if request.method == 'GET':
        incoming_data = IncomingMoney.query.all()
        return jsonify([{
            'txid': record.txid,
            'date': record.date,
            'amount_received': record.amount_received,
            'sender': record.sender,
            'new_balance': record.new_balance
        } for record in incoming_data])

    if request.method == 'POST':
        data = request.get_json()
        new_entry = IncomingMoney(
            txid=data['txid'],
            date=data['date'],
            amount_received=data['amount_received'],
            sender=data['sender'],
            new_balance=data['new_balance']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Incoming money entry added successfully!"}), 201


@app.route('/transfers_to_mobile_numbers', methods=['GET', 'POST'])
def manage_transfers_to_mobile_numbers():
    if request.method == 'GET':
        transfers_data = TransfersToMobileNumbers.query.all()
        return jsonify([{
            'id': record.id,
            'date': record.date,
            'amount_transferred': record.amount_transferred,
            'new_balance': record.new_balance,
            'fee': record.fee,
            'recipient': record.recipient,
            'recipient_number': record.recipient_number
        } for record in transfers_data])

    if request.method == 'POST':
        data = request.get_json()
        new_entry = TransfersToMobileNumbers(
            date=data['date'],
            amount_transferred=data['amount_transferred'],
            new_balance=data['new_balance'],
            fee=data['fee'],
            recipient=data['recipient'],
            recipient_number=data['recipient_number']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Transfer to mobile number added successfully!"}), 201


@app.route('/check_db', methods=['GET'])
def check_db():
    try:
        # Perform a simple query to check the connection
        db.create_all()  # Create tables if they don't exist
        print(db.session.query(AirtimePayments).first())
        return jsonify({"message": "Database connected successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Database connection failed: {str(e)}"}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
