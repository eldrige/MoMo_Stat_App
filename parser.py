import xml.etree.ElementTree as ET

xml_file = 'sms.xml'


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print("Error parsing XML:", e)
        return None


def extract_sms_data(root):
    sms_list = []
    for sms in root.findall('sms'):
        sms_data = {
            'address': sms.get('address'),
            'date': sms.get('date'),
            'body': sms.get('body'),
            'service_center': sms.get('service_center'),
            'read': sms.get('read'),
            'status': sms.get('status'),
            'date_sent': sms.get('date_sent'),
            'readable_date': sms.get('readable_date'),
            'contact_name': sms.get('contact_name'),
        }
        sms_list.append(sms_data)

    return sms_list


root = parse_xml(xml_file)
if root is not None:
    sms_data = extract_sms_data(root)
    for sms in sms_data:
        print(sms)


# Incoming money -> body: "You have received *****", count: 63
# Payment to code holders -> body: "Your payment of", count: 715
# Transfers to mobile numbers -> body: "transferred to", count: "585
# Bank transfers -> body: "You have transferred " , count: 6
# Internet & voice bundle -> body: "Bundles and Packs", count: 23
# Cash power bill payments -> body: "MTN Cash Power", count: 11
# Transtxns initiate by third parties -> body: "Message from debit receiver", count: 36
# Withdrawals from agents: -> body: "withdrawn", count: 3
# Airtime: -> body: "to Airtime with token", count: 15
