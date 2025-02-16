import xml.etree.ElementTree as ET

xml_file = 'sms.xml'
TABLES = ['incoming_money', "payment_to_code_holders", "transfers_to_mobile_numbers", "bank_transfers", "internet_voice_bundle",
          "cash_power_bill_payments", "transtxns_initiate_by_third_parties", "withdrawals_from_agents", "airtime"]


incoming_money_attr = ['amount', 'sender',
                       'transaction_date', 'new_balance', 'transaction_id']


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print("Error parsing XML:", e)
        return None


# Incoming money -> body: "You have received *****", count: 63
# Payment to code holders -> body: "Your payment of", count: 715
# Transfers to mobile numbers -> body: "transferred to", count: "585
# Bank transfers -> body: "You have transferred " , count: 6
# Internet & voice bundle -> body: "Bundles and Packs", count: 23
# Cash power bill payments -> body: "MTN Cash Power", count: 11
# Transtxns initiate by third parties -> body: "Message from debit receiver", count: 36
# Withdrawals from agents: -> body: "withdrawn", count: 3
# Airtime: -> body: "to Airtime with token", count: 15


def extract_sms_data(root):
    incoming_money = []
    payment_to_code_holders = []
    transfers_to_mobile_numbers = []
    bank_transfers = []
    internet_voice_bundle = []
    cash_power_bill_payments = []
    transtxns_initiate_by_third_parties = []
    withdrawals_from_agents = []
    airtime = []

    for sms in root.findall('sms'):
        if sms.get('body') and sms.get('body').find('You have received') >= 0:
            incoming_money.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('Your payment of') >= 0:
            payment_to_code_holders.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('transferred to') >= 0:
            transfers_to_mobile_numbers.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('You have transferred') >= 0:
            bank_transfers.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('Bundles and Packs') >= 0:
            internet_voice_bundle.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('MTN Cash Power') >= 0:
            cash_power_bill_payments.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('Message from debit receiver') >= 0:
            transtxns_initiate_by_third_parties.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('withdrawn') >= 0:
            withdrawals_from_agents.append(sms.get('body'))
        elif sms.get('body') and sms.get('body').find('to Airtime with token') >= 0:
            airtime.append(sms.get('body'))

    # return incoming_money

    return {
        'Incoming money': incoming_money,
        'Payment to code holders': payment_to_code_holders,
        'Transfers to mobile numbers': transfers_to_mobile_numbers,
        'Bank transfers': bank_transfers,
        'Internet voice bundles': internet_voice_bundle,
        'Cash power bill payments': cash_power_bill_payments,
        'Transtnx from third parties': transtxns_initiate_by_third_parties,
        'Withdrawals': withdrawals_from_agents,
        'Airtime': airtime
    }


root = parse_xml(xml_file)
if root is not None:
    sms_data = extract_sms_data(root)
    for sms in sms_data:
        print(sms)
