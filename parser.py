# import xml.etree.ElementTree as ET

# xml_file = 'sms.xml'
# TABLES = ['incoming_money', "payment_to_code_holders", "transfers_to_mobile_numbers", "bank_transfers", "internet_voice_bundle",
#           "cash_power_bill_payments", "transtxns_initiate_by_third_parties", "withdrawals_from_agents", "airtime"]


# incoming_money_attr = ['amount', 'sender',
#                        'transaction_date', 'new_balance', 'transaction_id']


# def parse_xml(file_path):
#     try:
#         tree = ET.parse(file_path)
#         root = tree.getroot()
#         return root
#     except ET.ParseError as e:
#         print("Error parsing XML:", e)
#         return None


# # Incoming money -> body: "You have received *****", count: 63
# # Payment to code holders -> body: "Your payment of", count: 715
# # Transfers to mobile numbers -> body: "transferred to", count: "585
# # Bank transfers -> body: "You have transferred " , count: 6
# # Internet & voice bundle -> body: "Bundles and Packs", count: 23
# # Cash power bill payments -> body: "MTN Cash Power", count: 11
# # Transtxns initiate by third parties -> body: "Message from debit receiver", count: 36
# # Withdrawals from agents: -> body: "withdrawn", count: 3
# # Airtime: -> body: "to Airtime with token", count: 15


# def extract_sms_data(root):
#     incoming_money = []
#     payment_to_code_holders = []
#     transfers_to_mobile_numbers = []
#     bank_transfers = []
#     internet_voice_bundle = []
#     cash_power_bill_payments = []
#     transtxns_initiate_by_third_parties = []
#     withdrawals_from_agents = []
#     airtime = []

#     for sms in root.findall('sms'):
#         if sms.get('body') and sms.get('body').find('You have received') >= 0:
#             incoming_money.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('Your payment of') >= 0:
#             payment_to_code_holders.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('transferred to') >= 0:
#             transfers_to_mobile_numbers.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('You have transferred') >= 0:
#             bank_transfers.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('Bundles and Packs') >= 0:
#             internet_voice_bundle.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('MTN Cash Power') >= 0:
#             cash_power_bill_payments.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('Message from debit receiver') >= 0:
#             transtxns_initiate_by_third_parties.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('withdrawn') >= 0:
#             withdrawals_from_agents.append(sms.get('body'))
#         elif sms.get('body') and sms.get('body').find('to Airtime with token') >= 0:
#             airtime.append(sms.get('body'))

#     # return incoming_money

#     return {
#         'Incoming money': incoming_money,
#         'Payment to code holders': payment_to_code_holders,
#         'Transfers to mobile numbers': transfers_to_mobile_numbers,
#         'Bank transfers': bank_transfers,
#         'Internet voice bundles': internet_voice_bundle,
#         'Cash power bill payments': cash_power_bill_payments,
#         'Transtnx from third parties': transtxns_initiate_by_third_parties,
#         'Withdrawals': withdrawals_from_agents,
#         'Airtime': airtime
#     }


# root = parse_xml(xml_file)
# if root is not None:
#     sms_data = extract_sms_data(root)
#     for sms in sms_data:
#         print(sms)


# def cash_power_bill_payments


from typing import Dict, List
from datetime import datetime
import xml.etree.ElementTree as ET
from typing import List, Dict
import re
import json

# Constants for table names and their corresponding search strings
TABLE_CONFIG = {
    'incoming_money': 'You have received',
    'payment_to_code_holders': 'Your payment of',
    'transfers_to_mobile_numbers': 'transferred to',
    'bank_transfers': 'You have transferred',
    'internet_voice_bundle': 'Bundles and Packs',
    'cash_power_bill_payments': 'MTN Cash Power',
    'transtxns_initiate_by_third_parties': 'Message from debit receiver',
    'withdrawals_from_agents': 'withdrawn',
    'airtime': 'to Airtime with token',
}

TABLE_SCHEMA = {
    'incoming_money': ['amount_received', 'sender', 'date', 'time', 'new_balance', 'transaction_id'],
    'payment_to_code_holders': ['amount_paid', 'recipient', 'date', 'time', 'new_balance', 'transaction_id', 'payment_code'],
    'transfers_to_mobile_numbers': ['amount_transferred', 'recipient', 'recipient_number', 'date', 'time', 'fee', 'new_balance', 'transaction_id'],
    'bank_transfers': ['amount_transferred', 'recipient', 'date', 'time', 'fee', 'new_balance', 'transaction_id', 'bank_name'],
    'internet_voice_bundle': ['date', 'time', 'new_balance', 'transaction_id', 'amount'],
    'cash_power_bill_payments': ['date', 'time', 'new_balance', 'transaction_id', 'amount', 'token'],
    'transtxns_initiate_by_third_parties': ['date', 'time', 'new_balance', 'transaction_amount', 'transaction_initiator', 'financial_transaction_id', 'external_transaction_id'],
    'withdrawals_from_agents': ['date', 'time', 'new_balance', 'transaction_id', 'amount', 'agent_name', 'agent_number', 'fee'],
    'airtime': ['date', 'time', 'new_balance', 'transaction_id', 'amount'],
}

TABLES = list(TABLE_CONFIG.keys())  # Dynamically generate TABLES
SMS_TAG = 'sms'


def parse_xml(file_path: str) -> ET.Element | None:
    """
    Parses an XML file and returns the root element.

    Args:
        file_path (str): The path to the XML file.

    Returns:
        ET.Element | None: The root element of the XML tree, or None if parsing fails.
    """
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None


def extract_sms_data(root: ET.Element) -> Dict[str, List[str]]:
    """
    Extracts SMS data from the XML root element based on predefined search strings.

    Args:
        root (ET.Element): The root element of the XML tree.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are table names and values are lists of SMS bodies.
    """
    sms_data = {table: []
                for table in TABLES}  # Initialize dictionary for SMS data

    for sms in root.findall(SMS_TAG):
        body = sms.get('body')
        if body:
            for table, search_string in TABLE_CONFIG.items():
                if search_string in body:
                    sms_data[table].append(body)

    return sms_data


def populate_airtime_table(sms_data: Dict[str, List[str]]):
    # Get airtime table
    airtime_table = sms_data['airtime']

    categorized_payments = []
    for payment_string in airtime_table:
        # Use regex to extract the relevant information from the string
        match = re.search(
            r"TxId:(\d+).*?Your payment of (\d+) RWF.*?at ([\d-]+ [\d:]+).*?Fee was (\d+) RWF.*?Your new balance: (\d+) RWF", payment_string)

        if match:
            txid = match.group(1)
            payment_amount = int(match.group(2))  # Convert to integer
            date = match.group(3)
            fee = int(match.group(4))  # Convert to integer
            new_balance = int(match.group(5))  # Convert to integer

            payment_data = {
                "date": date,
                "txid": txid,
                "payment_amount": payment_amount,
                "fee": fee,
                "new_balance": new_balance
            }
            categorized_payments.append(payment_data)

    print(categorized_payments)
    export_to_json(categorized_payments, "data/airtime_payments.json")

    return categorized_payments


def populate_received_money_table(sms_data: Dict[str, List[str]]):
    received_money_table = sms_data.get('incoming_money', [])
    categorized_received_money = []

    for message in received_money_table:
        match = re.search(
            r"You have received (\d+) RWF from ([\w\s]+) \(\*{9}\d{3}\).*?at ([\d-]+ [\d:]+).*?Your new balance:(\d+) RWF.*?Financial Transaction Id: (\d+)",
            message
        )

        if match:
            amount_received = int(match.group(1))
            sender = match.group(2)
            date_str = match.group(3)
            new_balance = int(match.group(4))
            txid = match.group(5)

            # Convert date string to datetime
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = date_str  # Keep it as a string if parsing fails

            received_money_data = {
                "txid": txid,
                "amount_received": amount_received,
                "sender": sender,
                "date": date.isoformat() if isinstance(date, datetime) else date,
                "new_balance": new_balance,
            }

            categorized_received_money.append(received_money_data)

    print(categorized_received_money)
    # Ensure this function exists
    export_to_json(categorized_received_money,
                   'data/incoming_money_table.json')
    return categorized_received_money


def transfer_to_mobile_numbers(sms_data: Dict[str, List[str]]):
    transfer_to_mobile_numbers_table = sms_data['transfers_to_mobile_numbers']

    categorized_transfers = []
    for transfer_string in transfer_to_mobile_numbers_table:

        pattern = r"\*165\*S\*(\d+) RWF transferred to ([A-Za-z\s]+) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. Fee was: (\d+) RWF\. New balance: (\d+) RWF"

        match = re.search(pattern, transfer_string)

        if match:
            amount_transferred = int(match.group(1))  # Convert to integer
            recipient = match.group(2)
            recipient_number = match.group(3)
            date = match.group(4)
            time = match.group(5)
            fee = int(match.group(6))  # Convert to integer
            new_balance = int(match.group(7))

            transfer_data = {
                "amount_transferred": amount_transferred,
                "recipient": recipient,
                "recipient_number": recipient_number,
                "date": date,
                "time": time,
                "fee": fee,
                "new_balance": new_balance
            }

            categorized_transfers.append(transfer_data)

    export_to_json(categorized_transfers,
                   "data/transfer_to_mobile_numbers.json")


def payment_to_code_holders(sms_data: Dict[str, List[str]]):
    payment_to_code_holders_table = sms_data['payment_to_code_holders']

    categorized_transfers = []
    for transfer_string in payment_to_code_holders_table:

        pattern = r"TxId: (\d+).*?Your payment of(\d+) RWF to([\w\s] + \d+).*?at([\d-] + [\d:]+).*?Your new balance: (\d+) RWF.*?Fee was(\d+) RWF"

        match = re.search(pattern, transfer_string)
        print(match)

        if match:
            txid = match.group(1)
            payment_amount = int(match.group(2))
            date_str = match.group(3)
            fee = int(match.group(4))
            new_balance = int(match.group(5))

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = date_str

            categorized_transfers.append({
                "txid": txid,
                "payment_amount": payment_amount,
                "date": date.isoformat() if isinstance(date, datetime) else date,
                "fee": fee,
                "new_balance": new_balance,
                "transaction_type": "airtime_payment"
            })

    export_to_json(categorized_transfers,
                   "data/payment_to_code_holders.json")


def export_to_json(data, filename="airtime_payments.json"):
    """
    Exports a list of dictionaries to a JSON file.

    Args:
        data: A list of dictionaries to be exported.
        filename: The name of the JSON file to create (default: "airtime_payments.json").
    """

    with open(filename, "w") as f:  # "w" for write mode
        json.dump(data, f, indent=4)  # indent for pretty formatting
    print(f"Data exported to {filename}")


def cash_power_bill_payments(sms_data: Dict[str, List[str]]):
    cash_power_bill_payments_table = sms_data['cash_power_bill_payments']

    categorized_cash_power_payments = []

    for power_payment_string in cash_power_bill_payments_table:
        pattern = r"\*162\*TxId:(\d+)\*S\*Your payment of (\d+) RWF to MTN Cash Power with token ([\d\-]+) has been completed at ([\d\-]+) ([\d:]+)\. Fee was (\d+) RWF\. Your new balance: (\d+) RWF \. Message: - -.\*EN#"

        match = re.search(pattern, power_payment_string)
        print(match)

        if match:
            transaction_id = match.group(1)
            payment_amount = int(match.group(2))
            token = match.group(3)
            date = match.group(4)
            time = match.group(5)
            new_balance = int(match.group(7))

            try:
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = date

            categorized_cash_power_payments.append({
                "transaction_id": transaction_id,
                "payment_amount": payment_amount,
                "token": token,
                "date": date.isoformat() if isinstance(date, datetime) else date,
                "time": time,
                "new_balance": new_balance
            })


def main():
    xml_file = 'sms.xml'
    root = parse_xml(xml_file)

    if root is not None:
        sms_data = extract_sms_data(root)

        # for table, messages in sms_data.items():
        #     print(f"Table: {table}")
        #     for message in messages:
        #         print(f"- {message}")
        #     print("-" * 30)

        # populate_received_money_table(sms_data)
        # transfer_to_mobile_numbers(sms_data)
        payment_to_code_holders(sms_data)
        # populate_airtime_table(sms_data)


if __name__ == "__main__":
    main()
