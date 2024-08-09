import sqlite3
def table_creation():
    conn = sqlite3.connect("zomato.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    create_table="""  CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Restaurant_ID INTEGER NOT NULL,
            username TEXT NOT NULL,
            review_text TEXT NOT NULL,
            rating INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        );"""
    cursor.execute(create_table)
    conn.commit()
    conn.close()
if __name__=='main':
    table_creation()

