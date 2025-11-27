import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_channel BOOLEAN DEFAULT FALSE,
                joined_group BOOLEAN DEFAULT FALSE,
                is_vip BOOLEAN DEFAULT FALSE,
                balance INTEGER DEFAULT 0,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def register_user(self, user_id, username, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()
    
    def check_registration(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone() is not None
    
    def update_channel_status(self, user_id, status):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET joined_channel = ? WHERE user_id = ?', (status, user_id))
        self.conn.commit()
    
    def update_group_status(self, user_id, status):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET joined_group = ? WHERE user_id = ?', (status, user_id))
        self.conn.commit()
    
    def check_membership(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT joined_channel, joined_group FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result and result[0] and result[1]
    
    def set_vip(self, user_id, status):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET is_vip = ? WHERE user_id = ?', (status, user_id))
        self.conn.commit()
    
    def is_vip(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT is_vip FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result and result[0]
    
    def update_balance(self, user_id, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        self.conn.commit()
    
    def get_balance(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

db = Database()