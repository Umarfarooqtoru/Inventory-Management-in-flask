import sqlite3

# Path to the SQLite database
db_path = 'instance/inventory.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the Transaction table
query = "SELECT * FROM transaction"
try:
    cursor.execute(query)
    transactions = cursor.fetchall()

    # Print the transactions
    print("\nTransactions in the Transaction table:")
    for transaction in transactions:
        print(transaction)
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.close()
