import xml.etree.ElementTree as ET
from typing import List, Dict

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

def main():
    xml_file = 'sms.xml'
    root = parse_xml(xml_file)

    if root is not None:
        sms_data = extract_sms_data(root)

        # Example usage: Print the extracted data for each table
        for table, messages in sms_data.items():
            print(f"Table: {table}")
            for message in messages:
                print(f"- {message}")
            print("-" * 30)


if __name__ == "__main__":
    main()
