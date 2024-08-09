# # import chardet

# # with open('anits-assign-kanugvarshi/zomato.csv', 'rb') as f:
# #     rawdata = f.read()
# # result = chardet.detect(rawdata)
# # print(result)

# import pandas as pd

# def clean_column_names(input_csv_file, output_csv_file):
#     # Load the CSV file
#     df = pd.read_csv(input_csv_file)

#     # Replace spaces with underscores in column names
#     df.columns = [col.replace(' ', '_') for col in df.columns]

#     # Write the modified DataFrame to a new CSV file
#     df.to_csv(output_csv_file, index=False)

# if __name__ == "__main__":
#     # Define the paths to the input and output CSV files
#     input_csv = "old_csv_file.csv"
#     output_csv = "new_csv_file.csv"
    
#     # Call the function to clean column names and save to a new CSV
#     clean_column_names(input_csv, output_csv)

import sqlite3
import pandas as pd

def create_database(input_csv_file, input_csv_file1, output_db_file):
    """Creates a SQLite database from two CSV files with a specified schema.

    Args:
        input_csv_file: Path to the first input CSV file (zomato_new.csv).
        input_csv_file1: Path to the second input CSV file (Country-code_new.csv).
        output_db_file: Path to the output SQLite database file.
    """
    # Load the first CSV file with the correct encoding
    df = pd.read_csv(input_csv_file, encoding='latin1')
    
    # Load the second CSV file
    df1 = pd.read_csv(input_csv_file1)

    # Create a connection to the SQLite database
    conn = sqlite3.connect(output_db_file)
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create the tables with the specified schema
    create_country_table = """
    CREATE TABLE IF NOT EXISTS country (
        Country_Code INTEGER PRIMARY KEY,
        Country_Name TEXT
    );
    """
    
    create_restaurants_table = """
    CREATE TABLE IF NOT EXISTS restaurants (
        Restaurant_ID INTEGER PRIMARY KEY,
        Restaurant_Name TEXT,
        Country_Code INTEGER,
        City TEXT,
        Address TEXT,
        Locality TEXT,
        Locality_Verbose TEXT,
        Longitude REAL,
        Latitude REAL,
        Cuisines TEXT,
        Average_Cost_for_two INTEGER,
        Currency TEXT,
        Has_Table_booking TEXT,
        Has_Online_delivery TEXT,
        Is_delivering_now TEXT,
        Switch_to_order_menu TEXT,
        Price_range INTEGER,
        Aggregate_rating REAL,
        Rating_color TEXT,
        Rating_text TEXT,
        Votes INTEGER,
        FOREIGN KEY (Country_Code) REFERENCES country (Country_Code)
    );
    """
    
    cursor.execute(create_country_table)
    cursor.execute(create_restaurants_table)

    # Insert data into the country table
    for _, row in df1.iterrows():
        cursor.execute("""
        INSERT INTO country (Country_Code, Country_Name)
        VALUES (?, ?)
        """, tuple(row))

    # Insert data into the restaurants table
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO restaurants (
            Restaurant_ID, Restaurant_Name, Country_Code, City, Address, Locality,
            Locality_Verbose, Longitude, Latitude, Cuisines, Average_Cost_for_two,
            Currency, Has_Table_booking, Has_Online_delivery, Is_delivering_now,
            Switch_to_order_menu, Price_range, Aggregate_rating, Rating_color,
            Rating_text, Votes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(row))

    # Commit the transactions
    conn.commit()
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Define the paths to the CSV and database files
    csv_file = "zomato_new.csv"
    csv_file1 = "Country-code_new.csv"
    db_file = "zomato.db"
    
    # Call the function to create the database
    create_database(csv_file, csv_file1, db_file)
