# insert JSON data into the database

import sqlite3
import json
import os

DB_NAME = "momo_analysis.db"
json_file_path = "C:/Users/Hp/Documents/ALU/MoMo_Stat_App/data/transfer_to_mobile_numbers.json"
 

def insert_data_from_json(json_file, table_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    columns = data[0].keys()
    placeholders = ", ".join(["?" for _ in columns])
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    for record in data:
        values = [record.get(col, "") for col in columns]
        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
    print(f"Data inserted into {table_name} from {json_file}")

if __name__ == "__main__":
    insert_data_from_json("../data/transfer_to_mobile_numbers.json", "Transfers_to_mobile_numbers")
    insert_data_from_json("../data/airtime_payments.json", "airtime")
