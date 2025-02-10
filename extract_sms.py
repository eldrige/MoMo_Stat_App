import xml.etree.ElementTree as ET
import json

# Define constants for the transactions we want to extract
TABLE_CONFIG = {
    'internet_voice_bundle': 'Bundles and Packs',
    'cash_power_bill_payments': 'MTN Cash Power'
}

# Define the expected fields for each transaction type
TABLE_SCHEMA = {
    'internet_voice_bundle': ['date', 'time', 'new_balance', 'transaction_id', 'amount'],
    'cash_power_bill_payments': ['date', 'time', 'new_balance', 'transaction_id', 'amount', 'token']
}

SMS_TAG = 'sms'

def parse_xml(file_path: str):
    """Parses the XML file and returns the root element."""
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

def extract_sms_data(root):
    """Extracts SMS data based on predefined keywords."""
    sms_data = {table: [] for table in TABLE_CONFIG.keys()}

    for sms in root.findall(SMS_TAG):
        body = sms.get('body')
        date = sms.get('date')
        if body:
            for table, search_string in TABLE_CONFIG.items():
                if search_string in body:
                    sms_data[table].append({'date': date, 'message': body})

    return sms_data

def save_to_json(data, file_name="transactions.json"):
    """Saves extracted data to a JSON file."""
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"✅ Data saved to {file_name}")

def main():
    xml_file = "sms.xml"  # Ensure this file exists in the same directory
    root = parse_xml(xml_file)

    if root is not None:
        sms_data = extract_sms_data(root)
        save_to_json(sms_data)

if __name__ == "__main__":
    main()
