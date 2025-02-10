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

TABLES = list(TABLE_CONFIG.keys())  # creates a list names 'TABLES' that contains the keys of the dictionary 'TABLE_CONFIG'
SMS_TAG = 'sms' # creates a variable 'SMS_TAG' that should not be changed : upper case 'SMS_TAG' is a constant


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
    export_to_json(categorized_payments )

    return categorized_payments


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


def transfer_to_mobile_numbers(sms_data: Dict[str, List[str]]):
    # Get transfer to mobile numbers table
    transfer_to_mobile_numbers_table = sms_data['transfers_to_mobile_numbers']
    print(transfer_to_mobile_numbers_table)

    categorized_transfers = []
    for transfer_string in transfer_to_mobile_numbers_table:
        # Use regex to extract the relevant information from the string

        pattern = r"\*165\*S\*(\d+) RWF transferred to ([A-Za-z\s]+) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. Fee was: (\d+) RWF\. New balance: (\d+) RWF"

        match = re.search(pattern, transfer_string)
        # match = re.search(
        #     r"\*165\*S\*(\d+) RWF transferred to ([A-Za-z\s]+) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. Fee was: (\d+) RWF\. New balance: (\d+) RWF, TxId: (\d+)", transfer_string)
        print(match)
        if match:
            amount_transferred = int(match.group(1))  # Convert to integer
            recipient = match.group(2)
            recipient_number = match.group(3)
            date = match.group(4)
            time = match.group(5)
            fee = int(match.group(6))  # Convert to integer
            new_balance = int(match.group(7))
            # transaction_id = match.group(8)

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

    print(categorized_transfers)
    export_to_json(categorized_transfers, "transfer_to_mobile_numbers.json")

    # return categorized_transfers






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

        # Example usage: Populate the airtime table
        # airtime_table = populate_airtime_table(sms_data)
        transfer_to_mobile_numbers_table = transfer_to_mobile_numbers(sms_data)



if __name__ == "__main__":
    main()
