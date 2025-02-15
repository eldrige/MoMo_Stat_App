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


def cash_power_bill_payments(sms_data: Dict[str, List[str]]):
    cash_power_bill_payments_table = sms_data['cash_power_bill_payments']
    print(cash_power_bill_payments_table)

    categorized_cash_power_payments = []

    for message in cash_power_bill_payments_table:

        transaction_id = message.split("TxId:")[1].split("*")[0]
        amount = message.split("payment of ")[1].split(" RWF")[0]
        provider = message.split(" to ")[1].split(" with")[0]
        token = message.split("token ")[1].split(" has")[0]
        date_time = message.split("completed at ")[1].split(". Fee")[0]
        fee = message.split("Fee was ")[1].split(" RWF")[0]
        balance = message.split("new balance: ")[1].split(" RWF")[0]
        # units = message.split("Electricity units: ")[1].split("kwH")[0]

        # try:
        #     date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        # except ValueError:
        #     date = date

        categorized_cash_power_payments.append({
            "transaction_id": transaction_id,
            "payment_amount": amount,
            "token": token,
            "date": date_time,
            # "date": date.isoformat() if isinstance(date, datetime) else date,
            "fee": fee,
            # "units": units,
            "new_balance": balance,
            "provider": provider
        })

    export_to_json(categorized_cash_power_payments,
                   "data/cash_power_bill_payments.json")


def withdrawals_from_agents(sms_data: Dict[str, List[str]]):
    withdrawals_from_agents_table = sms_data['withdrawals_from_agents']

    categorized_withdrawals_from_agents = []

    for message in withdrawals_from_agents_table:

        name = message.split("You ")[1].split(" have")[0].strip()
        agent_info = message.split("via agent: ")[1].split(",")[0].strip()
        agent_name = agent_info.split("(")[0].strip()
        agent_number = agent_info.split("(")[1].strip().strip(")")
        amount = message.split("withdrawn ")[1].split(" RWF")[0]
        account = message.split("account: ")[1].split(" at")[0].strip()
        date_time = message.split("at ")[1].split(" and")[0].strip()
        new_balance = message.split("Your new balance: ")[1].split(" RWF")[0]
        fee = message.split("Fee paid: ")[1].split(" RWF")[0]
        transaction_id = message.split("Id: ")[1].strip().split(".")[0]

        categorized_withdrawals_from_agents.append({
            "name": name,
            "agent_name": agent_name,
            "agent_number": agent_number,
            "account": account,
            "amount": amount,
            "date": date_time,
            "fee": fee,
            "new_balance": new_balance,
            "transaction_id": transaction_id
        })

    export_to_json(categorized_withdrawals_from_agents,
                   "data/withdrawals_from_agents.json")


def internet_voice_bundles(sms_data: Dict[str, List[str]]):
    internet_voice_bundles_table = sms_data['internet_voice_bundle']
    pattern = re.compile(
        r"TxId:(\d+).*?payment of (\d+) RWF to (.*?) with token.*?at ([\d-]+ [\d:]+).*?Fee was (\d+) RWF.*?balance: (\d+) RWF",
        re.DOTALL
    )

    internet_voice_bundles = []

    for message in internet_voice_bundles_table:
        match = pattern.search(message)

        if match:
            transaction_id = match.group(1)
            amount = match.group(2)
            service = match.group(3)
            date_time = match.group(4)
            new_balance = match.group(6)

            internet_voice_bundles.append({
                "transaction_id": transaction_id,
                "amount": amount,
                "service": service,
                "date": date_time,
                "new_balance": new_balance
            })

    export_to_json(internet_voice_bundles,
                   "data/internet_voice_bundles.json")


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


def payment_to_code_holders(sms_data: Dict[str, List[str]]):
    payment_to_code_holders_table = sms_data['payment_to_code_holders']
    pattern = re.compile(
        r"TxId:\s*(\d+).*?payment of ([\d,]+) RWF to (.*?) has been completed at ([\d-]+ [\d:]+).*?balance:\s*([\d,]+) RWF.*?Fee was (\d+) RWF",
        re.DOTALL
    )

    payment_to_code_holders = []

    for message in payment_to_code_holders_table:
        match = pattern.search(message)

        if match:
            transaction_id = match.group(1)
            amount = match.group(2).replace(",", "")
            recipient = match.group(3)
            date_time = match.group(4)
            new_balance = match.group(5).replace(",", "")
            fee = match.group(6)

            payment_to_code_holders.append({
                "transaction_id": transaction_id,
                "amount": amount,
                "date": date_time,
                "new_balance": new_balance,
                "fee": fee,
                "recipient": recipient
            })

    export_to_json(payment_to_code_holders,
                   "data/payment_to_code_holders.json")


def bank_transfers(sms_data: Dict[str, List[str]]):
    bank_transfers_table = sms_data['bank_transfers']
    pattern = re.compile(
        r"You have transferred (\d+) RWF to ([A-Za-z\s]+) \((\d+)\) from your mobile money account (\d+).*?at ([\d-]+ [\d:]+).*?Financial Transaction Id:\s*(\d+)",
        re.DOTALL
    )
    bank_transfers = []

    for message in bank_transfers_table:
        match = pattern.search(message)

        if match:
            amount = match.group(1)
            recipient_name = match.group(2)
            recipient_phone = match.group(3)
            sender_account = match.group(4)
            date_time = match.group(5)
            transaction_id = match.group(6)
            print(amount)

            bank_transfers.append({
                "transaction_id": transaction_id,
                "amount": amount,
                "date": date_time,
                "recipient_name": recipient_name,
                "recipient_phone": recipient_phone,
                "sender_account": sender_account
            })

    export_to_json(bank_transfers,
                   "data/bank_transfers.json")


def main():
    xml_file = 'sms.xml'
    root = parse_xml(xml_file)

    if root is not None:
        sms_data = extract_sms_data(root)

        for table, messages in sms_data.items():
            print(f"Table: {table}")
            for message in messages:
                print(f"- {message}")
            print("-" * 30)

        # populate_received_money_table(sms_data)
        # transfer_to_mobile_numbers(sms_data)
        # populate_airtime_table(sms_data)
        # cash_power_bill_payments(sms_data)
        # withdrawals_from_agents(sms_data)
        # internet_voice_bundles(sms_data)
        # payment_to_code_holders(sms_data)
        bank_transfers(sms_data)


if __name__ == "__main__":
    main()
