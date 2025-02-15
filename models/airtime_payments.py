from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AirtimePayments(db.Model):
    txid = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    new_balance = db.Column(db.Integer)
