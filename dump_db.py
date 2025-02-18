import sqlite3

db_path = "momo_data.db"
dump_file = "backup.sql"

with sqlite3.connect(db_path) as conn, open(dump_file, "w") as f:
    for line in conn.iterdump():
        f.write(f"{line}\n")

print("Database dump completed!")
