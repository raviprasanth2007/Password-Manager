import sqlite3
import os

DB_FILENAME = 'passwords.db'

def get_connection():
    # Connects to the SQLite database
    conn = sqlite3.connect(DB_FILENAME)
    # Allows dict-like access by column name
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Initializes the database and creates the credentials table if it doesn't exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_credential(website, username, encrypted_password):
    """Inserts a new credential into the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO credentials (website, username, encrypted_password)
        VALUES (?, ?, ?)
    ''', (website, username, encrypted_password))
    conn.commit()
    conn.close()

def get_all_credentials():
    """Retrieves all credentials, sorted by the most recently added."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM credentials ORDER BY created_at DESC')
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

def search_credentials(query):
    """Retrieves credentials where the website name matches the search query."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM credentials 
        WHERE website LIKE ? 
        ORDER BY created_at DESC
    ''', ('%' + query + '%',))
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

def delete_credential(cred_id):
    """Deletes a specific credential by ID."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM credentials WHERE id = ?', (cred_id,))
    conn.commit()
    conn.close()

def get_total_count():
    """Returns the total number of saved passwords for the dashboard."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM credentials')
    count = c.fetchone()[0]
    conn.close()
    return count
