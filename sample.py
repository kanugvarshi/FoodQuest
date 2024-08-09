import sqlite3

def print_table_description(db_name, table_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Query to get the table description
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print(f"Description of table '{table_name}':")
    for column in columns:
        cid, name, type_, notnull, dflt_value, pk = column
        print(f"Column ID: {cid}, Name: {name}, Type: {type_}, Not Null: {notnull}, Default Value: {dflt_value}, Primary Key: {pk}")
    
    # Query to get the foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()
    
    if foreign_keys:
        print("\nForeign Keys:")
        for fk in foreign_keys:
            id_, seq, table, from_, to, on_update, on_delete, match = fk
            print(f"Foreign Key ID: {id_}, Sequence: {seq}, References Table: {table}, From Column: {from_}, To Column: {to}, On Update: {on_update}, On Delete: {on_delete}, Match: {match}")
    else:
        print("\nNo foreign keys found.")
    
    # Close the connection
    conn.close()

# Define the database name
db_name = 'zomato.db'

# Print descriptions of the tables
print_table_description(db_name, 'country')
print_table_description(db_name, 'restaurants')
