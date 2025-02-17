def transfer_to_mobile_numbers(sms_data: Dict[str, List[str]]):
    # Get transfer to mobile numbers table
    transfer_to_mobile_numbers_table = sms_data['transfers_to_mobile_numbers']
    # print(transfer_to_mobile_numbers_table)

    categorized_transfers = []
    for transfer_string in transfer_to_mobile_numbers_table:
        # Use regex to extract the relevant information from the string

        pattern = r"\*165\*S\*(\d+) RWF transferred to ([A-Za-z\s]+) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. Fee was: (\d+) RWF\. New balance: (\d+) RWF"

        match = re.search(pattern, transfer_string)
        # match = re.search(
        #     r"\*165\*S\*(\d+) RWF transferred to ([A-Za-z\s]+) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. Fee was: (\d+) RWF\. New balance: (\d+) RWF, TxId: (\d+)", transfer_string)
    
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

    # print(categorized_transfers)
    export_to_json(categorized_transfers, "data/transfer_to_mobile_numbers.json")